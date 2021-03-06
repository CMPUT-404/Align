"""align URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from users import views as user_views
from posts import views as posts_views
#from posts import views as AuthorPosts
from comments import views as comments_views
from friends import views as friends_views

router = routers.DefaultRouter()
#router.register(r'users', user_views.UserViewSet)
router.register(r'groups', user_views.GroupViewSet)

router.register(r'posts', posts_views.PostsViewSet,basename='Post-list')
router.register(r'server', posts_views.ServerViewSet)
#router.register(r'comments', comments_views.CommentsViewSet)

router.register(r'friendrequest', friends_views.FollowingViewSet)
router.register(r'author', friends_views.AuthorViewSet)


urlpatterns = [
    path('', include('posts.urls')),
    path('', include('comments.urls')),
    path('admin/', admin.site.urls),
    #path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^posts$', posts_views.get_public_posts),
    url(r'^author/login$', user_views.LoginView.as_view()),
    url(r'^author/register$', user_views.RegisterView.as_view()),
    url(r'^author/validate$', user_views.ValidateView.as_view()),
    url(r'^author/search/(?P<pk>[a-zA-Z0-9._@+-]+)/$', user_views.SearchUserView.as_view())
]