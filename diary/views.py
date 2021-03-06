from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.utils import timezone
from django.forms import modelformset_factory

from places.models import Place
from .models import Diary, Comment, Mark, Image
from django.shortcuts import render, get_object_or_404
from .forms import DiaryForm, CommentForm, ImageForm


def diary_page(request):
    diary_list = Diary.objects.filter(deleted=False).filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(diary_list, 8)
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
    image_list = Image.objects.filter(diary_id=diary)
    comment_list = Comment.objects.filter(diary_id=diary).order_by('-published_date')

    if request.user.is_authenticated:
        try:
            user_mark = Mark.objects.get(user_id=request.user, diary_id_id=diary.pk)
        except ObjectDoesNotExist:
            user_mark = None
    else:
        user_mark = None

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

    return render(request, 'diary/diary_detail.html', {'diary': diary, 'comments': comments,
                                                       'form': form, 'user_mark': user_mark,
                                                       'image_list': image_list})


def diary_new(request):
    header = "Новая запись"

    if request.user.is_authenticated:
        # place_choices = Place.objects.filter(visibility="me", deleted=False, author=request.user)
        # free_place_choices = Place.objects.filter(visibility="all", deleted=False)

        ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)

        if request.method == "POST":
            diary_form = DiaryForm(request.POST)
            formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
            if diary_form.is_valid() and formset.is_valid():
                diary = diary_form.save(commit=False)
                diary.published_date = timezone.now()
                diary.author = request.user
                diary.save()
                for form in formset:
                    if 'image' in form.cleaned_data and form.cleaned_data['image']:
                        image = form.save(commit=False)
                        image.diary_id = diary
                        image.save()
                    elif 'image' in form.cleaned_data and not form.cleaned_data['image']:
                        form.cleaned_data['id'].delete()

                return redirect('diary_detail', pk=diary.pk)
        else:
            diary_form = DiaryForm()
            formset = ImageFormSet(queryset=Image.objects.none())
    else:
        return HttpResponseForbidden()

    return render(request, 'diary/diary_edit.html', {'diary_form': diary_form,
                                                     'formset': formset,
                                                     'header': header})


def diary_edit(request, pk):
    header = "Редактировать запись"
    diary = get_object_or_404(Diary, pk=pk)
    try:
        images = Image.objects.filter(diary_id=diary)
    except ObjectDoesNotExist:
        images = Image.objects.none()

    if diary.author != request.user:
        return HttpResponseForbidden()

    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3-len(images))
    if request.method == "POST":
        diary_form = DiaryForm(request.POST, instance=diary, prefix="diary_form")
        formset = ImageFormSet(request.POST, request.FILES, queryset=images)
        if diary_form.is_valid() and formset.is_valid():
            diary = diary_form.save(commit=False)
            diary.published_date = timezone.now()
            diary.save()
            for form in formset:
                if 'image' in form.cleaned_data and form.cleaned_data['image']:
                    image = form.save(commit=False)
                    image.diary_id = diary
                    image.save()
                elif 'image' in form.cleaned_data and not form.cleaned_data['image']:
                    form.cleaned_data['id'].delete()

            return redirect('diary_detail', pk=diary.pk)
    else:
        diary_form = DiaryForm(instance=diary, prefix="diary_form")
        formset = ImageFormSet(queryset=images)

    return render(request, 'diary/diary_edit.html', {'diary_form': diary_form,
                                                     'formset': formset,
                                                     'header': header})


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
    like = Mark.objects.filter(user_id=request.user, diary_id_id=diary.pk, mark="like")

    if request.user.is_authenticated:
        if like:
            like.delete()
        else:
            like, created = Mark.objects.get_or_create(user_id=request.user, diary_id_id=diary.pk)
            like.mark = "like"
            like.save()
    else:
        return HttpResponseForbidden()
    return redirect('diary_detail', pk=diary.pk)


def disliked_it(request, pk):
    diary = get_object_or_404(Diary, pk=pk)
    dislike = Mark.objects.filter(user_id=request.user, diary_id_id=diary.pk, mark="dislike")

    if request.user.is_authenticated:
        if dislike:
            dislike.delete()
        else:
            dislike, created = Mark.objects.get_or_create(user_id=request.user, diary_id_id=diary.pk)
            dislike.mark = "dislike"
            dislike.save()
    else:
        return HttpResponseForbidden()
    return redirect('diary_detail', pk=diary.pk)


def image_view(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return render(request, 'diary/image.html', {'image': image})






