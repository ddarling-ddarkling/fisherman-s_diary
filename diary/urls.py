from django.urls import path
from . import views

urlpatterns = [
    path('', views.diary_page, name='diary_page'),
    path('diary/<int:pk>/', views.diary_detail, name='diary_detail'),
]