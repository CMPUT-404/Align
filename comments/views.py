from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from comments.models import Comments
from comments.serializers import CommentsSerializer,CommentsCreateSerializer
from rest_framework.views import APIView
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

@api_view(['GET', 'POST'])
def post_comments(request,post_id):
    factory = APIRequestFactory()
    requests = factory.get('/')
    if request.method == 'GET':
        serializer_context = {
            'request': Request(requests),
        }
        #id = request.data.get('post_id')
        #print(id)
        queryset = Comments.objects.all().filter(root = post_id).order_by("-publish")
        serializer_class = CommentsSerializer(instance=queryset, context= serializer_context, many=True)
        #data = serializers.serialize('json', self.get_queryset())
        return Response(serializer_class.data)
    if request.method == 'POST':
        #serializer_context = {
        #    'request': Request(requests)
        #}
        #print(request.data)
        #print("____________")
        #print(request.data)
        #print("____________")
        #print(post_id)
        try:
            CommentsCreateSerializer.create(request.data,post_id)
            return HttpResponse("the post has been successfully added")
        except:
            return HttpResponse("the post has not been added")
            '''
        serializer = CommentsCreateSerializer(data = request.data)
        serializer.is_valid()
        print
        if serializer.is_valid():
            serializer.save()
            return HttpResponse("the post has been successfully added")
        else:
            return HttpResponse("the post has not been added")
            '''
