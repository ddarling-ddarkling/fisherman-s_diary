from django.urls import path
from . import views

urlpatterns = [
    path('', views.diary_page, name='diary_page'),
    path('diary/<int:pk>/', views.diary_detail, name='diary_detail'),
    path('diary/new/', views.diary_new, name='diary_new'),
    path('diary/<int:pk>/edit/', views.diary_edit, name='diary_edit'),
    path('diary/<pk>/remove/', views.diary_remove, name='diary_remove'),
]