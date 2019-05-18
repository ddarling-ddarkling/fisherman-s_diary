from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/<int:pk>', views.profile, name='profile'),
    path('accounts/<int:pk>/edit/', views.profile_edit, name='profile_edit'),
]
