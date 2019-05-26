from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from diary.models import Diary, Comment
from users.forms import ProfileForm
from users.models import Profile, Relationship


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
    follower_relationships = Relationship.objects.filter(following=profile_user)
    following_relationships = Relationship.objects.filter(follower=profile_user)
    if profile_user:
        user_profile, created = Profile.objects.get_or_create(user=profile_user)
    else:
        return HttpResponse("Авторизуйтесь")

    print(user_profile)
    follow_sign = False
    if request.user.is_authenticated:
        relationship = Relationship.objects.filter(following=profile_user, follower=request.user)
        if relationship:
            follow_sign = True
        else:
            follow_sign = False

    if profile_user == request.user or request.user.is_staff:
        diary_list = Diary.objects.filter(author=profile_user).order_by('-published_date')
    else:
        diary_list = Diary.objects.filter(author=profile_user, deleted=False).order_by('-published_date')

    if profile_user == request.user:
        header = "Мои посты:"
        places_header = "Мои места"
    else:
        header = "Посты пользователя:"
        places_header = "Места пользователя"

    return render(request, 'registration/profile.html', {'profile': user_profile,
                                                         'profile_user': profile_user,
                                                         'follower_relationships': follower_relationships,
                                                         'following_relationships': following_relationships,
                                                         'follow_sign': follow_sign,
                                                         'diary_list': diary_list,
                                                         'header': header,
                                                         'places_header': places_header})


def profile_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_profile = get_object_or_404(Profile, user=user)
    if user != request.user:
        return redirect('profile', pk=user.pk)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.save()
            return redirect('profile', pk=user.pk)
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'registration/profile_edit.html', {'form': form})


def subscribe(request, pk):
    following_user = get_object_or_404(User, pk=pk)
    if request.user:
        relationship, created = Relationship.objects.get_or_create(following=following_user, follower=request.user)

    return redirect('profile', pk=following_user.pk)


def unsubscribe(request, pk):
    following_user = get_object_or_404(User, pk=pk)
    relationship = get_object_or_404(Relationship, following=following_user, follower=request.user)
    if request.user:
        relationship.delete()

    return redirect('profile', pk=following_user.pk)
