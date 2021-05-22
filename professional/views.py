from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse, HttpResponse
from .models import ProReview
from movies.models import Movie
from .forms import ProReviewForm

# Create your views here.
@require_GET
def index(request):
    if request.user.is_authenticated:
        if request.user.user_rank >= 3:
            proreviews = ProReview.objects.order_by('-pk')
            context = {
                'proreviews': proreviews,
            }
            return render(request, 'professional/index.html', context)
        return redirect('community:index')
    return redirect('accounts:login')

@login_required
@require_http_methods(['GET', 'POST'])
def create(request, movie_id):
    if request.user.user_rank == 4:
        if request.method == 'POST':
            form = ProReviewForm(request.POST) 
            movie = get_object_or_404(Movie, movie_id=movie_id)
            if form.is_valid():
                proreview = form.save(commit=False)
                proreview.user = request.user
                proreview.movie_id = movie_id
                proreview.movie_title = movie.title
                proreview.save()
                return redirect('professional:detail', proreview.pk)
        else:
            form = ProReviewForm()
        context = {
            'form': form,
        }
        return render(request, 'professional/create.html', context)
    else:
        return redirect('movies:detail', movie_id)

@require_POST
def delete(request, proreview_pk):
    proreview = get_object_or_404(ProReview, pk=proreview_pk)
    if request.user.is_authenticated:
        if request.user == proreview.user:
            proreview.delete()
            return redirect('professional:index')
    return redirect('accounts:login')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, proreview_pk):
    proreview = get_object_or_404(ProReview, pk=proreview_pk)
    if request.user == proreview.user:
        if request.method == 'POST':
            form = ProReviewForm(request.POST, instance=proreview)
            if form.is_valid():
                form.save()
                return redirect('professional:detail', proreview.pk)
        else:
            form = ProReviewForm(instance=proreview)
    else:
        return redirect('movies:index')
        # return HttpResponseForbidden()
    context = {
        'form': form,
        'proreview': proreview,
    }
    return render(request, 'professional/update.html', context)


@require_GET
def detail(request, proreview_pk):
    proreview = get_object_or_404(ProReview, pk=proreview_pk)
    context = {
        'proreview': proreview,
    }
    return render(request, 'professional/detail.html', context)


@require_POST
def like(request, proreview_pk):
    if request.user.is_authenticated:
        proreview = get_object_or_404(ProReview, pk=proreview_pk)
        user = request.user

        if proreview.like_users.filter(pk=user.pk).exists():
            proreview.like_users.remove(user)
            # flag
            liked = False
        else:
            proreview.like_users.add(user)
            liked = True
        context = {
            'liked': liked,
            'count': proreview.like_users.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:login')