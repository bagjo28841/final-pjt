from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.http import HttpResponse, JsonResponse
import datetime
from pytz import timezone, utc
from .models import Stamp
from .forms import CustomUserCreationForm


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # 스탬프 생성
            Stamp.objects.create(user=request.user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            
            # 스탬프 - 가입 후 경과 날짜 확인
            time1 = request.user.date_joined # not naive
            time2 = datetime.datetime.now(tz=datetime.timezone.utc)
            if (time2-time1).days > 7:
                stamp = get_object_or_404(Stamp, user=request.user)
                stamp.joined_stamp = True
                stamp.counter += 1
                stamp.save()
                if stamp.counter == 15 and request.user.user_rank == 2:
                    request.user.user_rank = 3
                    request.user.save()
                elif stamp.counter == 24:
                    stamp.all_stamp = True
                    stamp.counter += 1
                    stamp.save()
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    return redirect('movies:index')


@login_required
def profile(request, username):
    person = get_object_or_404(get_user_model(), username=username)
    stamp = get_object_or_404(Stamp, user=person)
    # follower 스탬프 확인
    if len(person.followers.all()) >= 1:
        stamp.follower_stamp = True
        stamp.counter += 1
        stamp.save()
        if stamp.counter == 15 and request.user.user_rank == 2:
            request.user.user_rank = 3
            request.user.save()
        elif stamp.counter == 24:
            stamp.all_stamp = True
            stamp.counter += 1
            stamp.save()

    context = {
        'person': person,
        'stamp': stamp,
    }
    return render(request, 'accounts/profile.html', context)


@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        person = get_object_or_404(get_user_model(), pk=user_pk)
        user = request.user
        if person != user:
            if person.followers.filter(pk=user.pk).exists():
                person.followers.remove(user)
                followed = False
            else:
                person.followers.add(user)
                followed = True
            context = {
                'followed': followed,
                'followers': person.followers.count(),
                'followings': person.followings.count(),
            }
            return JsonResponse(context)
    return redirect('accounts:profile', person.username)
