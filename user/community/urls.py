from django.urls import path
from .views import *


app_name = 'community'
urlpatterns = [
    path('', list, name='list'),
    path('create/', create, name = "create"),
    path('detail/<int:id>/', detail, name="detail"),
    path('create-answer/<int:post_id>/', create_answer, name="create-answer"),
    path('add-like/<int:post_id>/', add_like, name = "add-like"),
    path('remove-like/<int:post_id>', remove_like, name="remove-like"),
    path('add-scrap/<int:post_id>/', add_scrap, name="add-scrap"),
    path('remove-scrap/<int:post_id>/', remove_scrap, name="remove-scrap"),
]
