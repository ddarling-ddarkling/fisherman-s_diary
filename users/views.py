from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from users.forms import ProfileForm
from users.models import Profile


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def profile(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    if profile_user:
        user_profile, created = Profile.objects.get_or_create(user=profile_user)
    else:
        return HttpResponse("Авторизуйтесь")
    print(user_profile)
    return render(request, 'registration/profile.html', {'profile': user_profile, 'profile_user': profile_user})


def profile_edit(request, pk):
    user_profile = get_object_or_404(Profile, pk=pk)
    if request.method == "POST" and user_profile.user == request.user:
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            profile_user = form.save(commit=False)
            profile_user.save()
            return redirect('profile', pk=profile_user.pk)
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'registration/profile_edit.html', {'form': form})
