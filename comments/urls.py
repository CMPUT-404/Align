from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from comments import views

urlpatterns = [
    path('posts/<str:post_id>/comments', views.post_comments),
    path('posts/deleteComment/<str:comment_id>', views.delete_comment),
    #path('snippets/<int:pk>', views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
