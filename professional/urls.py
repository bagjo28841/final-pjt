from django.urls import path
from . import views

app_name = 'professional'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/create/', views.create, name='create'),
    path('<int:proreview_pk>/', views.detail, name='detail'),
    path('<int:proreview_pk>/delete/', views.delete, name='delete'),
    path('<int:proreview_pk>/update/', views.update, name='update'),
    path('<int:proreview_pk>/like/', views.like, name='like'),
]