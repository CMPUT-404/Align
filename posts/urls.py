from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views

urlpatterns = [
    path('posts/author/<str:author_id>', views.get_posts_author),
    path('author/<str:author_id>/posts', views.get_posts),
    path('author/posts',views.get_posts_by_auth),
    #path('snippets/<int:pk>', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
