from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from comments.models import Comments
from comments.serializers import CommentsSerializer,CommentsCreateSerializer
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.decorators import api_view
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
User = get_user_model()

@api_view(['GET', 'POST'])
def post_comments(request,post_id):
    factory = APIRequestFactory()
    requests = factory.get('/')
    if request.method == 'GET':
        serializer_context = {
            'request': Request(requests),
        }
        try:
            post = Posts.objects.get(id = post_id)
        except:
            HttpResponse.status_code = 400
            return HttpResponse("the post_id u provided is invalid or there is no such posts with this id")
        post = Posts.objects.get(id = post_id)
        queryset = Comments.objects.all().filter(root = post).order_by("-published")
        serializer_class = CommentsSerializer(instance=queryset, context= serializer_context, many=True)
        dict = {"query":"comments","count":len(serializer_class.data),"size": None,"next":None,"previous":None,"comments":serializer_class.data}
        return Response(dict)
    elif request.method == 'POST':
        serializer_context = {
            'request': Request(requests)
        }
        try:
            a = request.data['auth']
        except:
            HttpResponse.status_code = 400
            return HttpResponse("the body u provided does not contain a 'auth' tag or the data with 'auth' is empty")
        try:
            b = request.data['comment']
        except:
            HttpResponse.status_code = 400
            return HttpResponse("the body u provided does not contain a 'comment' tag or the data with 'comment' is empty")
        try:
            post = Posts.objects.get(id = post_id)
        except:
            HttpResponse.status_code = 400
            return HttpResponse("the post_id u provided is invalid or there is no such posts with this id")
        try:
            author_obj = User.objects.get(id = request.data['auth'])
        except:
            HttpResponse.status_code = 400
            return HttpResponse("the auth u provided is invalid or there is no such user with this id")
        try:
            CommentsCreateSerializer.create(request.data['auth'],request.data['comment'],post_id)
            return HttpResponse("the comment has been successfully added")
        except:
            HttpResponse.status_code = 406
            return HttpResponse("the comment has not been added")
    else:
        HttpResponse.status_code = 400
        return HttpResponse("this specific http is not allowed for this api")

@api_view(['DELETE'])
# delete
def delete_comment(request,comment_id):
    factory = APIRequestFactory()
    requests = factory.get('/')
    if request.method == 'DELETE':
        serializer_context = {
            'request': Request(requests),
        }
       
        try:
            CommentsCreateSerializer.delete(comment_id)
            return HttpResponse("the comment has been successfully deleted")
        except:
            # 406
            HttpResponse.status_code = 400
            return HttpResponse("the comment has not been deleted or there is no such comment")
    else:
        HttpResponse.status_code = 400
        return HttpResponse("this specific http is not allowed for this api")
