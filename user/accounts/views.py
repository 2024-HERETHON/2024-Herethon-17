from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings
from .models import Profile
from .forms import ProfileForm  # 프로필 폼 추가
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from community.models import Post, Scrap  # 추가: Post 모델 가져오기
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            request.session['username'] = request.POST['username']
            request.session['password1'] = request.POST['password1']
            request.session['nickname'] = request.POST['nickname']  # 닉네임 추가
            return redirect('accounts:signup_child')
        else:
            return render(request, 'accounts/signup.html', {'error': '비밀번호가 일치하지 않습니다.'})
    return render(request, 'accounts/signup.html')

def signup_child(request):
    if request.method == "POST":
        username = request.session['username']
        password = request.session['password1']
        nickname = request.session['nickname']  # 닉네임 가져오기
        gender = request.POST['gender']
        birth_date_str = request.POST['birth_date']
        
        # 출생일 문자열을 datetime.date 객체로 변환
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()

        # 사용자 생성
        user = User.objects.create_user(username, password=password)

        # 프로필 생성 및 연결
        profile = Profile(user=user, gender=gender, birth_date=birth_date, nickname=nickname)
        profile.save()

        auth.login(request, user)
        return redirect('accounts:home')
    return render(request, 'accounts/signup_child.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Django의 로그인 함수를 사용
            return redirect('accounts:home')  # 로그인 후 리다이렉트할 페이지
        else:
            # 로그인 실패 시 에러 메시지와 함께 로그인 페이지를 다시 렌더링
            return render(request, 'accounts/login.html', {'error': 'Username or password is incorrect'})
    else:
        # GET 요청 처리, 로그인 폼을 보여줌
        return render(request, 'accounts/login.html')

def logout(request):
    # 로그아웃 처리
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return redirect('accounts:login')

def home(request):  
    return render(request, 'accounts/home.html')

@login_required
def mypage(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                form.save()
                return redirect('accounts:mypage')
        else:
            form = ProfileForm(instance=request.user.profile)
        
        try:
            profile = Profile.objects.get(user=request.user)
            birth_date = profile.birth_date
            gender = profile.gender
            nickname = profile.nickname

            # 작성한 게시글과 스크랩한 게시글 가져오기
            user_posts = Post.objects.filter(author=request.user)
            user_scraps = Scrap.objects.filter(user=request.user).values_list('post', flat=True)
            scraped_posts = Post.objects.filter(id__in=user_scraps)

            # 출생일로부터 현재까지 몇 개월인지 계산
            current_age_months = calculate_age_in_months(birth_date)

            return render(request, 'accounts/mypage.html', {
                'nickname': nickname,
                'gender': gender,
                'current_age_months': current_age_months,
                'profile_pic_url': profile.profile_pic.url if profile.profile_pic else None,
                'form': form,
                'user_posts': user_posts,
                'scraped_posts': scraped_posts,
            })
        except Profile.DoesNotExist:
            return render(request, 'accounts/mypage.html', {
                'nickname': 'Unknown',
                'gender': '미정',
                'current_age_months': '알 수 없음',
                'profile_pic_url': None,
                'form': form,
                'user_posts': [],
                'scraped_posts': [],
            })
    else:
        return redirect('accounts:login')

def calculate_age_in_months(birth_date):
    today = date.today()
    delta = relativedelta(today, birth_date)
    
    years = delta.years
    months = delta.months
    
    if years == 0:
        if months == 1:
            return '1개월'
        else:
            return f'{months}개월'
    elif years == 1:
        if months == 0:
            return '1년'
        elif months == 1:
            return '1년 1개월'
        else:
            return f'1년 {months}개월'
    else:
        if months == 0:
            return f'{years}년'
        elif months == 1:
            return f'{years}년 1개월'
        else:
            return f'{years}년 {months}개월'

@login_required
def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                form.save()
                return redirect('accounts:mypage')
        else:
            form = ProfileForm(instance=request.user.profile)
        
        return render(request, 'accounts/edit_profile.html', {
            'form': form,
            'profile_pic_url': request.user.profile.profile_pic.url if request.user.profile.profile_pic else None
        })
    else:
        return redirect('accounts:login')
