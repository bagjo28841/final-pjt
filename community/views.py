from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.http import JsonResponse, HttpResponse
from .models import Review, Comment
from movies.models import Movie
from accounts.models import Stamp
from .forms import ReviewForm, CommentForm


@require_GET
def index(request):
    if request.user.is_authenticated:
        reviews = Review.objects.order_by('-pk')
        context = {
            'reviews': reviews,
        }
        return render(request, 'community/index.html', context)
    return redirect('accounts:login')


@login_required
@require_http_methods(['GET', 'POST'])
def create(request, movie_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        movie = get_object_or_404(Movie, movie_id=movie_id)
        my_stamp = get_object_or_404(Stamp, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie_id = movie_id
            review.movie_title = movie.title
            review.save()
            
            # 등업 확인하기
            if request.user.user_rank == 1:
                if len(request.user.review_set.all()) >= 10 and len(request.user.comment_set.all()) >= 10:
                    request.user.user_rank = 2
                    request.user.save()
                    my_stamp.bonus = True
                return redirect('community:detail', review.pk)

            # 스탬프 확인하기
            else:
                genre_ids = list(map(int, movie.genres[1:-1].split(', ')))
                for genre in genre_ids:
                    if genre == 28:
                        my_stamp.action = True
                        continue
                    elif genre == 12:
                        my_stamp.adventure = True
                        continue
                    elif genre == 16:
                        my_stamp.animation = True
                        continue
                    elif genre == 35:
                        my_stamp.comedy = True
                        continue
                    elif genre == 80:
                        my_stamp.crime = True
                        continue
                    elif genre == 99:
                        my_stamp.documentary = True
                        continue
                    elif genre == 18:
                        my_stamp.drama = True
                        continue
                    elif genre == 10751:
                        my_stamp.family = True
                        continue
                    elif genre == 14:
                        my_stamp.fantasy = True
                        continue
                    elif genre == 36:
                        my_stamp.history = True
                        continue
                    elif genre == 27:
                        my_stamp.horror = True
                        continue
                    elif genre == 10402:
                        my_stamp.music = True
                        continue
                    elif genre == 9648:
                        my_stamp.mystery = True
                        continue
                    elif genre == 10749:
                        my_stamp.romance = True
                        continue
                    elif genre == 878:
                        my_stamp.science_fiction = True
                        continue
                    elif genre == 10770:
                        my_stamp.tv_movie = True
                        continue
                    elif genre == 53:
                        my_stamp.thriller = True
                        continue
                    elif genre == 10752:
                        my_stamp.war = True
                        continue
                    elif genre == 37:
                        my_stamp.western = True
                        continue
            my_stamp.save()
            print(my_stamp)
            return redirect('community:detail', review.pk)

    else:
        form = ReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'community/create.html', context)


@require_POST
def delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user.is_authenticated:
        if request.user == review.user:
            review.delete()
            return redirect('community:index')
    return redirect('accounts:login')


@login_required
@require_http_methods(['GET', 'POST'])
def update(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                return redirect('community:detail', review.pk)
        else:
            form = ReviewForm(instance=review)
    else:
        return redirect('movies:index')
        # return HttpResponseForbidden()
    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'community/update.html', context)


@require_GET
def detail(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        comments = review.comment_set.all()
        comment_form = CommentForm()
        context = {
            'review': review,
            'comment_form': comment_form,
            'comments': comments,
        }
        return render(request, 'community/detail.html', context)
    return redirect('accounts:login')


@require_POST
def create_comment(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.review = review
        comment.user = request.user
        comment.save()
        # 등업 확인하기
        if request.user.user_rank == 1:
            if len(request.user.review_set.all()) >= 10 and len(request.user.comment_set.all()) >= 10:
                request.user.user_rank = 2
                request.user.save()
        return redirect('community:detail', review.pk)
    context = {
        'comment_form': comment_form,
        'review': review,
        'comments': review.comment_set.all(),
    }
    return render(request, 'community/detail.html', context)


@require_POST
def delete_comment(request, review_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
        # return HttpResponseForbidden()
    return redirect('community:detail', review_pk)
    # return HttpResponse(status=401)


@login_required
@require_http_methods(['GET', 'POST'])
def update_comment(request, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        if request.user == comment.user:
            # 새로운 값을 받아오기
            print(request.POST)
            # 그걸 form 형식으로 넣어줘서
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
    context = {
        'comment_content': comment.content
    }
    return JsonResponse(context)


@require_POST
def like(request, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user

        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            # flag
            liked = False
        else:
            review.like_users.add(user)
            liked = True
        context = {
            'liked': liked,
            'count': review.like_users.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:login')