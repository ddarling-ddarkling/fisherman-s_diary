from django.shortcuts import redirect
from django.utils import timezone
from .models import Diary
from django.shortcuts import render, get_object_or_404
from .forms import DiaryForm


def diary_page(request):
    diaries = Diary.objects.filter(deleted__lte=False).filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'diary/diary_page.html', {'diaries': diaries})


def diary_detail(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    return render(request, 'diary/diary_detail.html', {'diary': diary})


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
    if request.method == "POST" and diary.author == request.user:
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
    if diary.author == request.user:
        diary.deleted = True
        diary.save()
    return redirect('diary_page')