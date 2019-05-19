from django.shortcuts import redirect
from django.utils import timezone
from .models import Diary, Comment
from django.shortcuts import render, get_object_or_404
from .forms import DiaryForm, CommentForm


def diary_page(request):
    diaries = Diary.objects.filter(deleted__lte=False).filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'diary/diary_page.html', {'diaries': diaries})


def diary_detail(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    comments = Comment.objects.filter(diary_id=diary.pk)
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
    return render(request, 'diary/diary_detail.html', {'diary': diary, 'comments': comments, 'form': form})


def diary_new(request):
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
    return render(request, 'diary/diary_edit.html', {'form': form})


def diary_edit(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    if diary.author != request.user:
        return redirect('diary_detail', pk=diary.pk)

    if request.method == "POST":
        form = DiaryForm(request.POST, instance=diary)
        if form.is_valid():
            diary = form.save(commit=False)
            diary.published_date = timezone.now()
            diary.save()
            return redirect('diary_detail', pk=diary.pk)
    else:
        form = DiaryForm(instance=diary)
    return render(request, 'diary/diary_edit.html', {'form': form})


def diary_remove(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    if diary.author == request.user or request.user.is_staff:
        diary.deleted = True
        diary.save()
    return redirect('diary_page')