import requests
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
from friends.models import Following
from users.serializers import UserSerializer
import base64
from django.contrib.auth import authenticate
from requests.auth import HTTPBasicAuth
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
        postId = kwargs['pk']
        host = request.query_params.get('host', None)
        post = None

        if host:
            find = False
            servers = Server.objects.all()
            server_serializer = ServerSerializer(instance=servers, context={'request': request}, many=True)
            for server in server_serializer.data:
                if host == server["domain"]:
                    find = True
                    break
            if find:
                try:
                    # url = "{}posts/{}".format(host, postId)  #FIXME
                    url = '{}posts'.format(host)  # XXX workaround
                    response = requests.get(url=url)
                    data = response.json()
                    posts = data['posts']
                    for i in posts:
                        if str(i["id"]) == str(postId):
                            post = i
                            break
                    if not post:
                        raise Exception("Cannot get the post with id = {}".format(postId))
                except Exception as e:
                    return Response(e.args, status=500)
            else:
                return Response("The host {} is not in the server list, the access is denied".format(host), status=400)
        else:
            queryset = Posts.objects.get(id=postId)
            serializer_class = PostsSerializer(instance=queryset, context={'request': request})
            post = serializer_class.data

        response = {
            "query": "getPost",
            "count": 1,
            "size": None,
            "next": None,
            "previous": None,
            "post": post
        }
        return Response(response)

@api_view(['GET'])
def get_public_posts(request):
    list = ["https://cloud-align-server.herokuapp.com/","https://cloud-align-server2.herokuapp.com/","https://shrouded-anchorage-92529.herokuapp.com/service/","http://127.0.0.1:8000/"]
    #queryset = Posts.objects.filter(visibility = True).order_by("-published")
    try:
        auth_header = request.META['HTTP_AUTHORIZATION']
        print(auth_header)
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        password = decoded_credentials[1]
        if (username == "remote@host.com") and (password == "yipu666"):
            queryset = Posts.objects.filter(visibility="PUBLIC").order_by("-published")
            serializer_class = PostsSerializer(instance=queryset, context={'request': request}, many=True)
            all_posts = serializer_class.data
            response = {
                    "query": "posts",
                    "count": len(all_posts),
                    "size": None,
                    "next": None,
                    "previous": None,
                    "posts": all_posts
                }
            return Response(response)
        else:
            queryset = Posts.objects.filter(visibility="PUBLIC").order_by("-published")
            serializer_class = PostsSerializer(instance=queryset, context={'request': request}, many=True)
            all_posts = serializer_class.data
            servers = Server.objects.all()
            server_serializer = ServerSerializer(instance=servers, context={'request': request}, many=True)
            for server in server_serializer.data:
                try:
                    domain = server["domain"]
                    url = "{}posts".format(domain)
                    if domain in list:
                        response = requests.get(url=url,auth=HTTPBasicAuth('remote@host.com', 'yipu666'))
                    else:
                        response = requests.get(url=url)
                    print(response.status_code)
                    if 200 <= response.status_code <= 299:
                        data = response.json()
                        posts = data['posts']
                        all_posts += posts
                    if posts is None:
                        raise Exception(data)
                    
                except Exception as e:
                    # return Response(e.args, status=500)
                    print("[ERROR] NETWORK ERROR WHEN GET POSTS FROM", url, e.args)
                    pass

            response = {
        "query": "posts",
        "count": len(all_posts),
        "size": None,
        "next": None,
        "previous": None,
        "posts": all_posts
            }
            return Response(response)
        
    except:
        
        queryset = Posts.objects.filter(visibility="PUBLIC").order_by("-published")
        serializer_class = PostsSerializer(instance=queryset, context={'request': request}, many=True)
        all_posts = serializer_class.data
        servers = Server.objects.all()
        server_serializer = ServerSerializer(instance=servers, context={'request': request}, many=True)
        for server in server_serializer.data:
            try:
                domain = server["domain"]
                url = "{}posts".format(domain)
                if domain in list:
                    response = requests.get(url=url,auth=HTTPBasicAuth('remote@host.com', 'yipu666'))
                else:
                    response = requests.get(url=url)
                print(response.status_code)
                if 200 <= response.status_code <= 299:
                    data = response.json()
                    posts = data['posts']
                    all_posts += posts
                if posts is None:
                    raise Exception(data)
                
            except Exception as e:
                # return Response(e.args, status=500)
                print("[ERROR] NETWORK ERROR WHEN GET POSTS FROM", url, e.args)
                pass

        response = {
        "query": "posts",
        "count": len(all_posts),
        "size": None,
        "next": None,
        "previous": None,
        "posts": all_posts
        }
        return Response(response)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts_author(request,author_id):
    if request.method == 'GET':
        author_obj = User.objects.get(id = author_id)
        queryset = Posts.objects.all().filter(author_obj = author_obj).order_by("-published")
        serializer_class = PostsSerializer(instance=queryset, context={'request': request}, many=True)
        dict = {"query":"posts","count":len(serializer_class.data),"size": None,"next":None,"previous":None,"posts":serializer_class.data}
        return Response(dict)
# author/posts
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts_by_auth(request):
    try:
        auth_header = request.META['HTTP_AUTHORIZATION']
        print(request.META['HTTP_X_USER_ID'])
        print(request.META['HTTP_HOST'])
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        print(username)
        password = decoded_credentials[1]
        if username == "remote@host.com":
            if password == "yipu666":
                servers = Server.objects.all()
                server_serializer = ServerSerializer(instance=servers, context={'request': request}, many=True)
                for server in server_serializer.data:
                    domain = server["domain"]
                    if host in domain:
                        url_string = "{}author/"+str(user_id)+"/friends/"
                        url = url_string.format(domain)
                        response = requests.get(url=url,auth=HTTPBasicAuth('remote@host.com', 'yipu666'))
                        friendList = response.data["author"]
                        final_list = []
                        for i in friendList:
                            a = i[-37:-1]
                            final_list = final_list + a

                queryset = Posts.objects.all().filter(Q(visibility = "PUBLIC")|Q(visibility = "FRIENDS",author_obj__in = final_list)|Q(visibility = "PRIVATE",visibleTo__icontains = user_id)).order_by("-published")
                serializer_class = PostsSerializer(instance=queryset, context={'request': request}, many=True)
                dict = {"query":"posts","count":0,"size": None,"next":None,"previous":None,"posts":serializer_class.data}
                return Response(dict,status = 200)
            else:
                return Response("wrong password",status = 403)
        else:
            return Response("wrong username",status = 403)
    #feed_bot = authenticate(username=username, password=password
    except:
        user = request.user
        current_obj = user
        userUrl, _ = normalize(UserSerializer(user, context={'request': request}).data["url"], '/')
        query1 = Following.objects.filter(receiver=userUrl, status=True)
        query2 = Following.objects.filter(sender=userUrl, status=True)
        friendList = []
        large_friendList = []
        for friend in query1:
            a = friend.sender
            friendList.append(a[-37:-1])

        for friend in query2:
            a = friend.receiver
            friendList.append(a[-37:-1])
    
        for friend_id in friendList:
            aList = []
            friend_user = User.objects.filter(id = friend_id)

            #print(friend_user)
            userUrl, _ = normalize(UserSerializer(friend_user[0], context={'request': request}).data["url"], '/')
            query1 = Following.objects.filter(receiver=userUrl, status=True)
            query2 = Following.objects.filter(sender=userUrl, status=True)
            for friend in query1:
                a = friend.sender
                aList.append(a[-37:-1])

            for friend in query2:
                a = friend.receiver
                aList.append(a[-37:-1])
            
            large_friendList = large_friendList + aList
        queryset = Posts.objects.all().filter(Q(visibility = "SERVERONLY")|Q(author_obj = current_obj)|Q(visibility = "FOAF",author_obj__in = large_friendList)|Q(visibility = "PUBLIC")|Q(visibility = "FRIENDS",author_obj__in = friendList)|Q(visibility = "PRIVATE",visibleTo__icontains = current_obj.id)).order_by("-published")
        serializer_class = PostsSerializer(instance=queryset, context={'request': request}, many=True)
        all_posts = serializer_class.data
        servers = Server.objects.all()
        server_serializer = ServerSerializer(instance=servers, context={'request': request}, many=True)
        for server in server_serializer.data:
            try:
                domain = server["domain"]
                url = "{}author/posts".format(domain)
                headers = {'X-USER-ID': str(user.id)}
                response = requests.get(url=url,auth=HTTPBasicAuth('remote@host.com', 'yipu666'),headers=headers)
            #print(response.status_code)
                if 200 <= response.status_code <= 299:
                    data = response.json()
                    posts = data['posts']
                    if posts is None:
                        raise Exception(data)
                    all_posts += posts
            except Exception as e:
                # return Response(e.args, status=500)
                print("[ERROR] NETWORK ERROR WHEN GET POSTS FROM", url, e.args)
                pass

        response = {
            "query": "posts",
            "count": len(all_posts),
            "size": None,
            "next": None,
            "previous": None,
            "posts": all_posts
        }
        return Response(response)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts(request,author_id):
    permission_classes = (IsAuthenticated,)
    factory = APIRequestFactory()
    requests = factory.get('/')
    try:
        auth_header = request.META['HTTP_AUTHORIZATION']
        print(request.META['HTTP_X_USER_ID'])
        print(request.META['HTTP_HOST'])
        encoded_credentials = auth_header.split(' ')[1]  # Removes "Basic " to isolate credentials
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
        username = decoded_credentials[0]
        print(username)
        author_obj = User.objects.get(id = author_id)
        password = decoded_credentials[1]
        if username == "remote@host.com":
            if password == "yipu666":
                #print("__________________")
                #print(type(username))
                #print(type(password))
                #print("___________________")
                queryset = Posts.objects.all().filter(author_obj = author_obj).filter(Q(visibility = "PUBLIC")).order_by("-published")
                serializer_class = PostsSerializer(instance=queryset, context={'request': request}, many=True)
                dict = {"query":"posts","count":0,"size": None,"next":None,"previous":None,"posts":serializer_class.data}
                return Response(dict,status = 200)
            else:
                return Response("wrong password",status = 403)
        else:
            return Response("wrong username",status = 403)
    except:
        serializer_context = {
            'request': Request(requests),
        }
        # serializer_context = {
        #     'request': Request(requests),
        # }
        # find all the user who has the friends of the current user
        user = request.user
        current_obj = user
        userUrl, _ = normalize(UserSerializer(user, context={'request': request}).data["url"], '/')
        query1 = Following.objects.filter(receiver=userUrl, status=True)
        query2 = Following.objects.filter(sender=userUrl, status=True)
        #print("_________________")
        friendList = []
        large_friendList = []
        # add to friend list
        for friend in query1:
            a = friend.sender
            #print("__________________")
            #print(a)
            #print(a[-37:-1])
            #print("__________________")
            friendList.append(a[-37:-1])

        for friend in query2:
            a = friend.receiver
            #print("__________________")
            #print(a)
            #print(a[-37:-1])
            #print("__________________")
            friendList.append(a[-37:-1])
        #print(friendList)
    
        for friend_id in friendList:
            aList = []
            friend_user = User.objects.filter(id = friend_id)

            print(friend_user)
            userUrl, _ = normalize(UserSerializer(friend_user[0], context={'request': request}).data["url"], '/')
        #    print("____________________")
        #    print(userUrl)
        #    print("____________________")
            query1 = Following.objects.filter(receiver=userUrl, status=True)
            query2 = Following.objects.filter(sender=userUrl, status=True)
            for friend in query1:
                a = friend.sender
                aList.append(a[-37:-1])

            for friend in query2:
                a = friend.receiver
                aList.append(a[-37:-1])
            
            large_friendList = large_friendList + aList
        #print("__________________")
        #print(a)
            #print(a[-37:-1])
            #print("__________________")
        #print("_____________________")
        #print(large_friendList)
        #print("_____________________")
        # |Q(visibility = "SERVERONLY",author_obj = current_obj)|Q(visibility = "FOAF",author_obj__in = large_friendList)|Q(visibility = "PRIVATE",author_obj = current_obj)|Q(visibility = "PRIVATE",visibility__contains = current_obj)
        #queryset = Posts.objects.all().filter(Q(visibility = True)|Q(visibleTo__icontains = current_obj.id)|Q(author_obj = current_obj)).order_by("-published")
        author_obj = User.objects.get(id = author_id)
        queryset = Posts.objects.all().filter(author_obj = author_obj).filter(Q(visibility = "SERVERONLY")|Q(author_obj = current_obj)|Q(visibility = "FOAF",author_obj__in = large_friendList)|Q(visibility = "PUBLIC")|Q(visibility = "FRIENDS",author_obj__in = friendList)|Q(visibility = "PRIVATE",visibleTo__icontains = current_obj.id)).order_by("-published")
        
        #queryset = Posts.objects.all().filter(author_obj = author_obj).filter(Q(visibility = True)|Q(visibleTo__icontains = current_obj.id)|Q(author_obj = current_obj)).order_by("-published")
        #queryset = Posts.objects.all().filter(author_obj = author_obj).filter(Q(visibility = "PUBLIC")|Q(author_obj = current_obj)).order_by("-published")
        serializer_class = PostsSerializer(instance=queryset, context= serializer_context, many=True)
        all_posts = serializer_class.data
        servers = Server.objects.all()
        server_serializer = ServerSerializer(instance=servers, context={'request': request}, many=True)
        for server in server_serializer.data:
            try:
                domain = server["domain"]
                url = "{}author/"+str(author_id)+"posts".format(domain)
                headers = {'X-USER-ID': str(user.id)}
                response = requests.get(url=url,auth=HTTPBasicAuth('remote@host.com', 'yipu666'),headers=headers)
            #print(response.status_code)
                if 200 <= response.status_code <= 299:
                    data = response.json()
                    posts = data['posts']
                    if posts is None:
                        raise Exception(data)
                    all_posts += posts
            except Exception as e:
                # return Response(e.args, status=500)
                print("[ERROR] NETWORK ERROR WHEN GET POSTS FROM", url, e.args)
                pass

        response = {
            "query": "posts",
            "count": len(all_posts),
            "size": None,
            "next": None,
            "previous": None,
            "posts": all_posts
        }
        return Response(response)
#.filter(author_obj = author_obj)
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

def normalize(str1, str2):
    # normalize urls
    if (str1[-1] != '/'):
        str1 += '/'
    if (str2[-1] != '/'):
        str2 += '/'    
    
    return str1, str2