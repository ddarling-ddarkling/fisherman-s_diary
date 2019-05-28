from django.urls import path
from . import views


urlpatterns = [
    path('places/user/<int:pk>', views.places, name='user_places'),
    path('places/detail/<int:pk>/', views.place_detail, name='place_detail'),
    path('places/new/', views.new_place, name='new_place'),
    path('places/<int:pk>/edit/', views.place_edit, name='place_edit'),
    path('places/remove/<int:pk>/', views.place_remove, name='place_remove'),
    path('places/<int:pk>/restore/', views.place_restore, name='place_restore'),
    path('places/map/', views.main_map, name='main_map'),
]