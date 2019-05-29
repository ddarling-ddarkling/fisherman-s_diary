from django.urls import path
from . import views

urlpatterns = [
    path('', views.diary_page, name='diary_page'),
    path('diary/<int:pk>/', views.diary_detail, name='diary_detail'),
    path('diary/new/', views.diary_new, name='diary_new'),
    path('diary/<int:pk>/edit/', views.diary_edit, name='diary_edit'),
    path('diary/<int:pk>/remove/', views.diary_remove, name='diary_remove'),
    path('diary/<int:pk>/restore/', views.restore, name='restore'),
    path('diary/comment_remove/<int:pk>/', views.comment_remove, name='comment_remove'),
    path('diary/<int:pk>/liked_it/', views.liked_it, name='liked_it'),
    path('diary/<int:pk>/disliked_it/', views.disliked_it, name='disliked_it'),
]