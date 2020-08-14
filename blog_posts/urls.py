from django.urls import path
from .views import (
    create_blog_post_view,
    get_all_posts,
    get_post_detail_view,
    update_post_detail_view,
    BlogListView
)
app_name = 'blog_posts'

urlpatterns = [
    path('create_post/',create_blog_post_view,name='create_post'),
    path('get_all_posts/',BlogListView.as_view(),name='get_all_posts'),
    path('get_post_detail/<slug>/',get_post_detail_view,name='post_details'),
    path('update_blog_post/<slug>/',update_post_detail_view,name='update_post'),
    path('delete_blog_post/<slug>/',update_post_detail_view,name='delete_post')
]