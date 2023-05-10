from django.urls import path
from . import views

urlpatterns = [
    
    path('post/', views.post, name='post'),
    path('', views.all_posts, name='all_posts'),
    path('page/', views.page , name='page')
]