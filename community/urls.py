from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/create/', views.create, name='create'),
    path('<int:review_pk>/', views.detail, name='detail'),
    path('<int:review_pk>/delete/', views.delete, name='delete'),
    path('<int:review_pk>/update/', views.update, name='update'),
    path('<int:review_pk>/create_comment/', views.create_comment, name='create_comment'),
    path('<int:review_pk>/delete_comment/<int:comment_pk>/', views.delete_comment, name='delete_comment'),
    path('<int:review_pk>/update_comment/<int:comment_pk>/', views.update_comment, name='update_comment'),
    path('<int:review_pk>/like/', views.like, name='like'),
]
