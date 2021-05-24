import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.conf import settings
from .models import Movie


# Create your views here.
def movie_update(request):
    if settings.IS_FIRST:
        Movie.objects.all().delete()
        for i in range(1, 4):
            # data 받아오기
            my_url = f'https://api.themoviedb.org/3/movie/popular?api_key=fae9dc8695dc36b190fa7f4146fc979f&page={i}'
            response = requests.get(my_url)
            movie_dict = response.json()

            # 필요한 정보 골라내기
            movie_list = movie_dict.get('results')
            for movie in movie_list:
                title = movie.get('original_title')
                movie_id = movie.get('id')
                overview = movie.get('overview')
                if movie.get('release_date'):
                    release_date = movie.get('release_date')
                else:
                    release_date = '2999-01-01'
                poster_path = movie.get('poster_path')
                popularity = movie.get('popularity')
                vote_count = movie.get('vote_count')
                vote_average = movie.get('vote_average')
                genre_ids = movie.get('genre_ids')

                # Movie DB에 저장하기, 중복제거
                Movie.objects.create(title=title, overview=overview, release_date=release_date, poster_path=poster_path, popularity=popularity, vote_count=vote_count, vote_average=vote_average, genres=genre_ids, movie_id=movie_id)
                settings.IS_FIRST = False
    return redirect('movies:index')

@require_GET
def index(request):
    if settings.IS_FIRST:
        return redirect('movies:movie_update')
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


@require_GET
def detail(request, movie_id):
    movie = get_object_or_404(Movie, movie_id=movie_id)

    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)


@require_GET
def recommended(request):

    return render(request, 'movies/recommended.html')