from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views

urlpatterns = [
    path('author/posts', views.get_posts),
    #path('author/<string:author_id>/posts', views.get_posts_by_id),
    #path('snippets/<int:pk>', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
