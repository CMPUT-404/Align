from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
# Create your views here.
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from posts.models import Posts, Server
from posts.serializers import PostsSerializer, PostsCreateSerializer, ServerSerializer
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.shortcuts import render
import json
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
#from rest_framework.authtoken.models import Token
User = get_user_model()


class PostsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    permission_classes = (IsAuthenticated,)  
    queryset = Posts.objects.all().filter().order_by("-published")
    serializer_class = PostsSerializer

    def retrieve(self, request, *args, **kwargs):
        a = kwargs['pk']
        queryset = Posts.objects.all().filter(id = a).order_by("-published")
        serializer_class = PostsSerializer(instance=queryset, context={'request': request}, many=True)
        dict = {"query":"posts","count":len(serializer_class.data),"size": None,"next":None,"previous":None,"posts":serializer_class.data}
        return Response(dict)
    
@api_view(['GET'])
def get_public_posts(request):
    #queryset = Posts.objects.filter(visibility = True).order_by("-published")
    queryset = Posts.objects.filter(visibility = "PUBLIC").order_by("-published")
    serializer_class = PostsSerializer(instance=queryset, context={'request': request}, many=True)
    dict = {"query":"posts","count":len(serializer_class.data),"size": None,"next":None,"previous":None,"posts":serializer_class.data}
    return Response(dict)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts_author(request,author_id):
    factory = APIRequestFactory()
    requests = factory.get('/')
    if request.method == 'GET':
        serializer_context = {
            'request': Request(requests),
        }
        author_obj = User.objects.get(id = author_id)
        queryset = Posts.objects.all().filter(author_obj = author_obj).order_by("-published")
        serializer_class = PostsSerializer(instance=queryset, context= serializer_context, many=True)
        dict = {"query":"posts","count":len(serializer_class.data),"size": None,"next":None,"previous":None,"posts":serializer_class.data}
        return Response(dict)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts_by_auth(request):
    factory = APIRequestFactory()
    requests = factory.get('/')
    if request.method == 'GET':
        serializer_context = {
            'request': Request(requests),
        }
        user = request.user
        current_obj = user
        #queryset = Posts.objects.all().filter(Q(visibility = True)|Q(visibleTo__icontains = current_obj.id)|Q(author_obj = current_obj)).order_by("-published")
        queryset = Posts.objects.all().filter(Q(visibility = "PUBLIC")|Q(author_obj = current_obj)).order_by("-published")
        serializer_class = PostsSerializer(instance=queryset, context= serializer_context, many=True)
        dict = {"query":"posts","count":len(serializer_class.data),"size": None,"next":None,"previous":None,"posts":serializer_class.data}
        return Response(dict)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request,author_id):
    permission_classes = (IsAuthenticated,)
     
    factory = APIRequestFactory()
    requests = factory.get('/')
    if request.method == 'GET':
        serializer_context = {
            'request': Request(requests),
        }
        current_obj = request.user
        author_obj = User.objects.get(id = author_id)
        #queryset = Posts.objects.all().filter(author_obj = author_obj).filter(Q(visibility = True)|Q(visibleTo__icontains = current_obj.id)|Q(author_obj = current_obj)).order_by("-published")
        queryset = Posts.objects.all().filter(author_obj = author_obj).filter(Q(visibility = "PUBLIC")|Q(author_obj = current_obj)).order_by("-published")
        serializer_class = PostsSerializer(instance=queryset, context= serializer_context, many=True)
        dict = {"query":"posts","count":len(serializer_class.data),"size": None,"next":None,"previous":None,"posts":serializer_class.data}
        return Response(dict)
    else:
        HttpResponse.status_code = 403
        return HttpResponse("All the method other than get is not allowed")
#
# @api_view(['GET', 'POST'])
# def get_posts(request):
#     factory = APIRequestFactory()
#     requests = factory.get('/')
#     if request.method == 'GET':
#         serializer_context = {
#             'request': Request(requests),
#         }
#         id = request.data.get('id')
#         #print(id)
#         queryset = Posts.objects.all().filter(Q(visibilities = True)|Q(visible_to = id)).order_by("-publish")
#         serializer_class = PostsSerializer(instance=queryset, context= serializer_context, many=True)
#         #data = serializers.serialize('json', self.get_queryset())
#         return Response(serializer_class.data)
#     if request.method == 'POST':
#         #serializer_context = {
#         #    'request': Request(requests)
#         #}
#         #print(request.data)
#         try:
#             PostsCreateSerializer.create(request.data)
#             return HttpResponse("the post has been successfully added")
#         except:
#             # 406
#             HttpResponse.status_code = 406
#             return HttpResponse("the post has not been added")
#
# @api_view(['DELETE'])
# def delete_posts_author(request,post_id):
#     factory = APIRequestFactory()
#     requests = factory.get('/')
#     if request.method == 'DELETE':
#         serializer_context = {
#             'request': Request(requests),
#         }
#         #id = request.data.get('id')
#         #print(id)
#         try:
#             PostsCreateSerializer.delete(post_id)
#             return HttpResponse("the post has been successfully deleted")
#         except:
#             HttpResponse.status_code = 406
#             return HttpResponse("the post has not been deleted")
#
#
# @api_view(['GET', 'POST'])
# def get_posts_by_id(request,author_id):
#     #print("_____________________________")
#     #print(author_id)
#     factory = APIRequestFactory()
#     requests = factory.get('/')
#     if request.method == 'GET':
#         serializer_context = {
#             'request': Request(requests),
#         }
#         your_id = request.data.get('id')
#         if your_id == None:
#             return HttpResponse("id is invalid")
#         #author_id = request.data.get('author_id')
#         if author_id == None:
#             return HttpResponse("author_id is invalid")
#         #print("_____________________________")
#         #print(your_id)
#         #print(author_id)
#         queryset = Posts.objects.all().filter(Q(author = author_id)).filter(Q(visibilities = True)|Q(visible_to = your_id)).order_by("-publish")
#         serializer_class = PostsSerializer(instance=queryset, context= serializer_context, many=True)
#         #data = serializers.serialize('json', self.get_queryset())
#         return Response(serializer_class.data)
#     else:
#         return HttpResponse("the should be a Get request")


class ListOrAdminOnly(permissions.BasePermission):
    """
    Custom permission to only allow access to lists for admins
    """

    def has_permission(self, request, view):
        return view.action == 'list' or request.user and request.user.is_staff


class ServerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [
        ListOrAdminOnly
    ]
    queryset = Server.objects.all().filter()
    serializer_class = ServerSerializer
