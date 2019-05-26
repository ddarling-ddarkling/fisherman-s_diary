from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from diary.models import Diary
from places.forms import PlaceForm
from places.models import Place


def places(request, pk):
    profile_user = get_object_or_404(User, pk=pk)
    if request.user == profile_user:
        place_list = Place.objects.filter(author=profile_user)
        header = "Мои места:"
    else:
        place_list = Place.objects.filter(author=profile_user).filter(visibility="all", deleted=False)
        header = "Места пользователя " + profile_user.username + " :"
    return render(request, 'places.html', {'place_list': place_list, 'header': header, 'profile_user': profile_user})


def place_detail(request, pk):
    place = get_object_or_404(Place, pk=pk)
    profile_user = get_object_or_404(User, pk=place.author.pk)
    if request.user != profile_user and place.visibility == "me":
        return HttpResponseForbidden()

    if request.user == profile_user or request.user.is_staff:
        diary_list = Diary.objects.filter(place=place.pk).order_by('-published_date')
    else:
        diary_list = Diary.objects.filter(place=place.pk, deleted=False).order_by('-published_date')

    if request.user == profile_user:
        places_header = "Мои места"
    else:
        places_header = "Места пользователя " + profile_user.username

    return render(request, 'detail.html', {'place': place, 'diary_list': diary_list, 'profile_user': profile_user,
                                           'places_header': places_header})


def new_place(request):
    header = "Новое место"
    if request.method == "POST":
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.author = request.user
            place.save()
            return redirect('user_places', pk=place.author.pk)
    else:
        form = PlaceForm()
    return render(request, 'edit.html', {'form': form, 'header': header})


def place_edit(request, pk):
    header = "Редактировать место"
    place = get_object_or_404(Place, pk=pk)
    if place.author != request.user:
        return redirect('user_places', pk=place.author.pk)

    if request.method == "POST":
        form = PlaceForm(request.POST, instance=place)
        if form.is_valid():
            place = form.save(commit=False)
            place.save()
            return redirect('user_places', pk=place.author.pk)
    else:
        form = PlaceForm(instance=place)
    return render(request, 'edit.html', {'form': form, 'header': header})


def place_remove(request, pk):
    place = get_object_or_404(Place, pk=pk)
    if place.author == request.user or request.user.is_staff:
        place.deleted = True
        place.save()
    return redirect('place_detail', pk=place.pk)


def place_restore(request, pk):
    place = get_object_or_404(Place, pk=pk)
    if place.author == request.user or request.user.is_staff:
        place.deleted = False
        place.save()
    return redirect('place_detail', pk=place.pk)



