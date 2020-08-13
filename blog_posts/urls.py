from django.urls import path
from .views import (
    create_blog_post_view,
    get_all_posts
)
app_name = 'blog_posts'

urlpatterns = [
    path('create_post/',create_blog_post_view,name='create_post'),
    path('get_all_posts/',get_all_posts,name='get_all_posts')
]