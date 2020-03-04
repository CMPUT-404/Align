from django.shortcuts import render
from rest_framework.decorators import api_view
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from posts.models import Posts
from posts.serializers import PostsSerializer,PostsCreateSerializer
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

#@api_view(['GET', 'POST'])
class PostsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #test = Posts.objects.get(title = "dsfsf")
    #print(test.title)
    queryset = Posts.objects.all().filter(visibilities = True).order_by("-publish")
    serializer_class = PostsSerializer

    def create(self, request):
        # make friend request
        if request.method == 'GET':
            #responseDictionary = {"query":"friendrequest", "success": True, "message":"Friend request sent"}
            if request.data == None:
                return response
            else:
                queryset = Posts.objects.all().filter(id = request.data).order_by("-publish")
                serializer_class = PostsSerializer
                return response


@api_view(['GET', 'POST'])
def get_posts(request):
    factory = APIRequestFactory()
    requests = factory.get('/')
    if request.method == 'GET':
        serializer_context = {
            'request': Request(requests),
        }
        id = request.data.get('id')
        #print(id)
        queryset = Posts.objects.all().filter(Q(visibilities = True)|Q(visible_to = id)).order_by("-publish")
        serializer_class = PostsSerializer(instance=queryset, context= serializer_context, many=True)
        #data = serializers.serialize('json', self.get_queryset())
        return Response(serializer_class.data)
    if request.method == 'POST':
        #serializer_context = {
        #    'request': Request(requests)
        #}
        print(request.data)
        try:
            PostsCreateSerializer.create(request.data)
            return HttpResponse("the post has been successfully added")
        except:
            return HttpResponse("the post has not been added")


@api_view(['GET', 'POST'])
def get_posts_by_id(request,author_id):
    #print("_____________________________")
    #print(author_id)
    factory = APIRequestFactory()
    requests = factory.get('/')
    if request.method == 'GET':
        serializer_context = {
            'request': Request(requests),
        }
        your_id = request.data.get('id')
        if your_id == None:
            return HttpResponse("id is invalid")
        #author_id = request.data.get('author_id')
        if author_id == None:
            return HttpResponse("author_id is invalid")
        #print("_____________________________")
        #print(your_id)
        #print(author_id)
        queryset = Posts.objects.all().filter(Q(author = author_id)).filter(Q(visibilities = True)|Q(visible_to = your_id)).order_by("-publish")
        serializer_class = PostsSerializer(instance=queryset, context= serializer_context, many=True)
        #data = serializers.serialize('json', self.get_queryset())
        return Response(serializer_class.data)
    else:
        return HttpResponse("the should be a Get request")
