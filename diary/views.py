from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone

from places.models import Place
from .models import Diary, Comment, Mark
from django.shortcuts import render, get_object_or_404
from .forms import DiaryForm, CommentForm


def diary_page(request):
    diary_list = Diary.objects.filter(deleted__lte=False).filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(diary_list, 4)
    page = request.GET.get('page')
    try:
        diaries = paginator.page(page)
    except PageNotAnInteger:
        diaries = paginator.page(1)
    except EmptyPage:
        diaries = paginator.page(paginator.num_pages)
    return render(request, 'diary/diary_page.html', {'diaries': diaries})


def diary_detail(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    comment_list = Comment.objects.filter(diary_id=diary.pk).order_by('-published_date')

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.diary_id = diary
            comment.author = request.user
            comment.published_date = timezone.now()
            comment.save()
            return redirect('diary_detail', pk=diary.pk)
    else:
        form = CommentForm()

    paginator = Paginator(comment_list, 4)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request, 'diary/diary_detail.html', {'diary': diary, 'comments': comments, 'form': form})


def diary_new(request):
    header = "Новая запись"

    if request.user.is_authenticated:
        place_choices = Place.objects.filter(visibility="me", deleted=False, author=request.user)
        free_place_choices = Place.objects.filter(visibility="all", deleted=False)

        if request.method == "POST":
            form = DiaryForm(request.POST)
            if form.is_valid():
                diary = form.save(commit=False)
                diary.published_date = timezone.now()
                diary.author = request.user
                diary.save()
                return redirect('diary_detail', pk=diary.pk)
        else:
            form = DiaryForm()
    else:
        return HttpResponseForbidden()

    return render(request, 'diary/diary_edit.html', {'form': form, 'header': header, 'place_choices': place_choices,
                                                     'free_place_choices': free_place_choices})


def diary_edit(request, pk):
    header = "Редактировать запись"
    diary = get_object_or_404(Diary, pk=pk)

    if diary.author != request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.published_date = timezone.now()
            diary.save()
            return redirect('diary_detail', pk=diary.pk)
    else:
        form = DiaryForm(instance=diary)
    return render(request, 'diary/diary_edit.html', {'form': form, 'header': header})


def diary_remove(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    if diary.author == request.user or request.user.is_staff:
        diary.deleted = True
        diary.save()
    return redirect('diary_detail', pk=diary.pk)


def restore(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    if diary.author == request.user or request.user.is_staff:
        diary.deleted = False
        diary.save()
    return redirect('diary_detail', pk=diary.pk)


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    diary = get_object_or_404(Diary, pk=comment.diary_id.pk)
    if comment.author == request.user or request.user.is_staff:
        comment.delete()
    return redirect('diary_detail', pk=diary.pk)


def liked_it(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    like = Mark.objects.filter(user_id=request.user, diary_id_id=diary.pk, type="like")

    if request.user.is_authenticated:
        if like:
            like.delete()
        else:
            like, created = Mark.objects.get_or_create(user_id=request.user, diary_id_id=diary.pk)
            like.type = "like"
            like.save()
    else:
        return HttpResponseForbidden()
    return redirect('diary_detail', pk=diary.pk)


def disliked_it(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    dislike = Mark.objects.filter(user_id=request.user, diary_id_id=diary.pk, type="dislike")

    if request.user.is_authenticated:
        if dislike:
            dislike.delete()
        else:
            dislike, created = Mark.objects.get_or_create(user_id=request.user, diary_id_id=diary.pk)
            dislike.type = "dislike"
            dislike.save()
    else:
        return HttpResponseForbidden()
    return redirect('diary_detail', pk=diary.pk)







