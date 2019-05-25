from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/<int:pk>', views.profile, name='profile'),
    path('accounts/<int:pk>/edit/', views.profile_edit, name='profile_edit'),
    path('accounts/profile/subscribe/<int:pk>', views.subscribe, name='subscribe'),
    path('accounts/profile/unsubscribe/<int:pk>', views.unsubscribe, name='unsubscribe'),
    path('accounts/profile/user_place/<int:pk>', views.user_place, name='user_place'),
]
