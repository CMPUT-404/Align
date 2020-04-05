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
from posts.models import Posts, Server
from posts.serializers import PostsSerializer, PostsCreateSerializer, ServerSerializer
from django.http import HttpResponse, JsonResponse
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
from requests.auth import HTTPBasicAuth
import requests
User = get_user_model()

@api_view(['GET', 'POST'])
def post_comments(request,post_id):
    factory = APIRequestFactory()
    request_s = factory.get('/')
    if request.method == 'GET':
        serializer_context = {
            'request': Request(request_s),
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
            'request': Request(request_s)
        }
        try:
            host = request.query_params.get('host', None)
            if host:
                find = False
                servers = Server.objects.all()
                server_serializer = ServerSerializer(instance=servers, context={'request': request}, many=True)
                connect = host + "service/"
                for server in server_serializer.data:
                    if host == server["domain"] or connect == server["domain"]:
                        find = True
                        break
                if find:
                    try:
                        # url = "{}posts/{}".format(host, postId)  #FIXME
                        url_format = '{}posts/' + post_id + '/comments'
                        url = url_format.format(host)  # XXX workaround
                        #print(request.data['comment'])
                        body = request.data
                        a = body['comment']
                        print(body['comment'])
                        print(a['author'])
                        print(post_id)
                        response = requests.post(url=url,data = body,auth=HTTPBasicAuth('remote@host.com', 'yipu666'))
                        print(response.status_code)
                        if 200 <= response.status_code <= 299:
                            response = {
	                                "query": "addComment",
                                    "success":True,
                                    "message":"Comment Added"
                            }
                            return Response(response)
                        else:
                            raise Exception("fail to create a foreign comment")
                    except Exception as e:
                        return Response(e.args, status=500)
                else:
                    return Response("The host {} is not in the server list, the access is denied".format(host), status=400)
        except:
            try:
                a = request.data['comment']
            except:
                HttpResponse.status_code = 400
                return HttpResponse("the body u provided does not contain a 'comment' tag or the data with 'comment' is invalid")
            try:
                a = request.data['comment']
                b = a['author']
            except:
                HttpResponse.status_code = 400
                return HttpResponse("the body u provided its comment tag does not contain a 'auth' tag")
            try:
                post = Posts.objects.get(id = post_id)
            except:
                HttpResponse.status_code = 400
                return HttpResponse("the post_id u provided is invalid or there is no such posts with this id")
            a = request.data['comment']
            try:
                a = request.data['comment']
        
                b = a['author']
                CommentsCreateSerializer.create(b,a,post_id)
                response = {
	                "query": "addComment",
                    "success":True,
                    "message":"Comment Added"
                }
                return Response(response, status=200)
            except:
                response = {
	                "query": "addComment",
                    "success":False,
                    "message":"Comment Added"
                }
                return Response(response, status=406)

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
