from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views

urlpatterns = [
    path('posts/author/<str:author_id>', views.get_posts),
    path('posts/user/<str:author_id>', views.get_posts_author),
    #path('snippets/<int:pk>', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
