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
    path('diary/new_place/', views.new_place, name='new_place'),
    path('diary/<int:pk>/place_edit/', views.place_edit, name='place_edit'),
    path('diary/place_remove/<int:pk>/', views.place_remove, name='place_remove'),
]