from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views

urlpatterns = [
    path('author/posts', views.get_posts),
    path('author/<str:author_id>/posts', views.get_posts_by_id),
    #path('snippets/<int:pk>', views.snippet_detail),
    path('author/allPosts/<str:author_id>', views.get_posts_author),
    #path('author/deletePosts/<str:post_id>', views.delete_posts_author),
]

urlpatterns = format_suffix_patterns(urlpatterns)
