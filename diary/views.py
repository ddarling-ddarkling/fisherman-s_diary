from django.shortcuts import render
from django.utils import timezone
from .models import Diary
from django.shortcuts import render, get_object_or_404


def diary_page(request):
    diaries = Diary.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'diary/diary_page.html', {'diaries': diaries})


def diary_detail(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    return render(request, 'diary/diary_detail.html', {'diary': diary})