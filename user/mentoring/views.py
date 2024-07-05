from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required

def home(request):
    mentos = Mento.objects.all()
    sort = request.GET.get('sort', 'latest')
    
    if sort == 'popular':
        mentos = Mento.objects.all().annotate(popularity= Count('questions')).order_by('-popularity', '-id')
    else:
        mentos = Mento.objects.all().order_by('-id')
    return render(request, 'mentoring/home.html', {'mentos': mentos})

@login_required
def detail(request, id):
    mento = get_object_or_404(Mento, id=id)
    return render(request, 'mentoring/detail.html', {'mento': mento})

@login_required
def question(request, mento_id):
    mento = get_object_or_404(Mento, id=mento_id)
    if request.method == "POST":
        content = request.POST.get('content')
        question = Question.objects.create(content=content, mento=mento, user=request.user)
        question.save()
        return redirect('mentoring:question', mento_id)
    questions = Question.objects.filter(mento=mento)
    return render(request, 'mentoring/question.html', {'mento': mento, 'questions': questions})

@login_required
def search(request):
    sort = request.GET.get('sort', 'latest')
    search = request.GET.get('search', '')
    
    if search:
        search_list = Mento.objects.filter(
            Q(name__icontains=search) | 
            Q(nickname__icontains=search) | 
            Q(tag__icontains=search) |
            Q(intro__icontains=search) |
            Q(content_1__icontains=search) |
            Q(content_2__icontains=search) |
            Q(content_3__icontains=search) |
            Q(content_4__icontains=search)
        )
    else:
        search_list = Mento.objects.all()

    return render(request, 'mentoring/search.html', {'search_list': search_list, 'sort': sort})

@login_required
def record_sheet(request):
    if request.method == "POST":
        plan = request.POST.get('plan')
        advice = request.POST.get('advice')
        pledge = request.POST.get('pledge')
        record = Record.objects.create(plan=plan, advice=advice, pledge=pledge, user=request.user)
        return redirect('mentoring:home')
    return render(request, 'mentoring/record_sheet.html')

@login_required
def create_comment(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == "POST":
        content = request.POST.get('content')
        Comment.objects.create(content=content, question=question)
        return redirect('mentoring:question', question_id)
    return render(request, 'mentoring/question.html')
