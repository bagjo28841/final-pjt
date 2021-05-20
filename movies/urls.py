from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('movie-update', views.movie_update, name="movie_update"),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('recommended', views.recommended, name='recommended'),
]
