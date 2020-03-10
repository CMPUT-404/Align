from django.shortcuts import render
import json
from django.http import HttpResponse, Http404

# Create your views here.
from django.contrib.auth import get_user_model
from friends.models import FriendRequests
from friends.models import Friends
from friends.models import Followers
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from friends.serializers import FriendRequestSerializer
from friends.serializers import FriendsSerializer
from friends.serializers import FollowersSerializer
from rest_framework.authtoken.models import Token

User = get_user_model()

class FriendRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that makes a friend request.
    """

    queryset = FriendRequests.objects.all()
    serializer_class = FriendRequestSerializer

    def create(self, request):
        # make friend request
        responseDictionary = {"query":"friendrequest", "success": True, "message":"Friend request sent"}

        try:

            try:
                # swagger format
                body = request.body
                requestJson = json.loads(body)
                authorID = requestJson["author"]["id"].split('/')[-1]
                friendID = requestJson["friend"]["id"].split('/')[-1]
                if (authorID == ''):
                    requestJson["author"]["id"].split('/')[-2]
                if (friendID == ''):
                    requestJson["friend"]["id"].split('/')[-2]
            except:
                # html form format
                requestJson = request.data
                authorID = requestJson["authorID"].split("/")[-2]
                friendID = requestJson["friendID"].split("/")[-2]

            if (not (friendID and authorID)):
                raise ValueError("No friendID or authorID was given")
            validated_data = {"author": authorID, "friend": friendID}
            FriendRequestViewSet.serializer_class.create(validated_data)        # create request
            FollowersViewSet.serializer_class.create(validated_data)                          # create follower
            response = Response(responseDictionary)

        except:
            responseDictionary["success"] = False
            responseDictionary["message"] = "Friend request not sent"
            response = Response(responseDictionary)

        return response
    
    def retrieve(self, request, pk=None):
        # retrieve a list of friend requests that the user has
        responseDictionary = {"query":"friend request list", "author": [], "requests": []}
        
        try:
            pkUser = User.objects.get(id=pk)
            pkhost = pkUser.host + '/author/' + str(pk)
            if ('http' not in pkhost):
                pkhost = 'https://' + pkhost   
            name = pkUser.displayName
            responseDictionary["author"] = [pkhost, name]
            responseDictionary["requests"] = FriendRequestViewSet.serializer_class.requests(pk)
            response = Response(responseDictionary)
        except:
            response = Response(responseDictionary)
                
        return response

    @action(methods=['get'], detail=False, url_path='user/(?P<sk>[^/.]+)', url_name='friendrequestList')
    def friendRequestList(self, request, pk=None, sk=None):
        
        responseDictionary = {"query":"friend request list", "author": [], "requests": []}
        
        try:
            pkUser = User.objects.get(id=sk)
            pkhost = pkUser.host + '/author/' + str(sk)
            if ('http' not in pkhost):
                pkhost = 'https://' + pkhost   
            name = pkUser.displayName
            responseDictionary["author"] = [pkhost, name]
            responseDictionary["requests"] = FriendRequestViewSet.serializer_class.requests(sk)
            responseDictionary["author"] = {"id":responseDictionary["author"][0], "displayName":responseDictionary["author"][1]}
            responseDictionary["requests"] = {"id": responseDictionary["requests"][0][0], "displayName": responseDictionary["requests"][0][1]}
            response = Response(responseDictionary)
        except:
            raise
            response = Response(responseDictionary)
                
        return response




    def list(self, request):
        # list friend requests with user data

       return Response(FriendRequestViewSet.serializer_class.list())


class FriendViewSet(viewsets.ModelViewSet):
    """
    API endpoint that processes accepting/declining friends requests
    """

    queryset = Friends.objects.all()
    serializer_class = FriendsSerializer

    @action(methods=['post'], detail=False, url_path='requestprocess', url_name='friendRequestProcess')
    def friendRequestProcess(self, request):
        # accept/decline friend request

        # POST /friend/requestprocess
        responseDictionary = {"query":"friendrequestprocess", "success": True}

        try:
            try:
                # swagger
                body = request.body
                requestJson = json.loads(body)
                authorID = requestJson["author"].split('/')[-2]             # person accepting/declining
                friendID = requestJson["friend"].split('/')[-2]             # person who sent request
                friendStatus = requestJson["friendstatus"]
                if (authorID == ''):
                    requestJson["author"].split('/')[-2]
                if (friendID == ''):
                    requestJson["friend"].split('/')[-2]
            except Exception as e:
                # html form
                print(e.args)
                requestJson = request.data
                authorID = requestJson["author"].split("/")[-2]
                friendID = requestJson["friend"].split("/")[-2]
                try:
                    friendStatus = requestJson["friendstatus"]
                except:
                    raise RuntimeError("couldn't get status")

            if (not (friendID and authorID)):
                raise ValueError("No friendID or authorID was given")
            validated_data = {"author": authorID, "friend": friendID}
            FriendRequestViewSet.serializer_class.delete(validated_data)    # delete friends request
            if (friendStatus == "accept"):
                # create friend
                FollowersViewSet.serializer_class.delete(validated_data)        # delete following relation
                validated_data = {"author": friendID, "friend": authorID}
                FriendRequestViewSet.serializer_class.delete(validated_data, supress=True)   # delete reverse friend request
                validated_data = {"author": friendID, "friend": authorID}
                FollowersViewSet.serializer_class.delete(validated_data, supress=True)       # delete reverse follower
                FriendViewSet.serializer_class.create(validated_data)           # create friend
            response = Response(responseDictionary)

        except:
            responseDictionary["success"] = False
            response = Response(responseDictionary)

        return response

    @action(methods=['post'], detail=False, url_path='delete', url_name='friendDelete')
    def friendDelete(self, request):

        # POST /friend/delete
        responseDictionary = {"query":"frienddelete", "success": True}

        try:
            try:
                # swagger
                body = request.body
                requestJson = json.loads(body)
                authorID = requestJson["author"].split('/')[-2]             # person requesting deletion
                friendID = requestJson["friend"].split('/')[-2]            # friend getting deleted
                if (authorID == ''):
                    requestJson["author"].split('/')[-2]
                if (friendID == ''):
                    requestJson["friend"].split('/')[-2]
            except:
                # html form
                requestJson = request.data
                authorID = requestJson["author"].split("/")[-2]
                friendID = requestJson["friend"].split("/")[-2]

            if (not (friendID and authorID)):
                raise ValueError("No friendID or authorID was given")
            validated_data = {"author": authorID, "friend": friendID}
            FriendViewSet.serializer_class.delete(validated_data)       # delete friend relation
            validated_data = {"author": friendID, "friend": authorID}
            FollowersViewSet.serializer_class.create(validated_data)    # create one way follower
            response = Response(responseDictionary)

        except:
            responseDictionary["success"] = False
            response = Response(responseDictionary)

        return response
    
    @action(methods=['get'], detail=False, url_path='user/(?P<sk>[^/.]+)', url_name='friendList')
    def friendList(self, request, pk=None, sk=None): 
        responseDictionary = {"query":"friends", "author": {}, "authors": []}
        try:
            pkUser = User.objects.get(id=sk)
            pkhost = pkUser.host + '/author/' + str(sk)
            if ('http' not in pkhost):
                pkhost = 'https://' + pkhost   
            name = pkUser.displayName
            responseDictionary["author"] = {"id": pkhost, "displayName" :name}
            alist = FriendsSerializer.friendsList(sk)
            authors = []
            for friend in alist:
                authors.append({"id": friend[0], "displayName": friend[1]})
            responseDictionary["authors"] = authors    
            response = Response(responseDictionary)
        except:
            response = Response(responseDictionary)
        return response
    
    def list(self, request):
        # list friends with user data

       return Response(FriendViewSet.serializer_class.list())


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that asks a service if anyone in the list is a friend.
    """

    queryset = Friends.objects.all()
    serializer_class = FriendsSerializer

    @action(methods=['post', 'get'], detail=True, url_path='friends', url_name='friendInList')
    def friendInList(self, request, pk=None):

        if (request.method == 'GET'):
            # get friend list of author
            # URL: /author/{author_id}/friends
            responseDictionary = {"query":"friends", "authors": []}
            try:
                responseDictionary["authors"] = FriendsSerializer.friendsList(pk)
                response = Response(responseDictionary)
            except:
                response = Response(responseDictionary)
            return response

        elif (request.method == 'POST'):
            # ask if anyone in the list is a friend
            # URL: ​/author​/{author_id}​/friends
            responseDictionary = {"query":"friends", "author": str(pk), "authors": []}
            try:
                # swagger
                body = request.body
                requestJson = json.loads(body)
                pk = requestJson["author"]
                listOfFriends = requestJson["authors"]
                responseDictionary["authors"] = FriendsSerializer.areFriendsMany(pk, listOfFriends)
                response = Response(responseDictionary)
            except:
                response = Response(responseDictionary)
            return response

        else:
            responseDictionary = {"Error":"Page does not exist"}
            return Response(responseDictionary)

    @action(methods=['get'], detail=True, url_path='friends/(?P<sk>[^/.]+)', url_name='areFriends')
    def areFriends(self, request, pk=None, sk=None):
        # ask if 2 authors are friends
        # URL: /author/{author1_id}/friends/{author2_id}

        responseDictionary = {"query":"friends", "friends": False, "authors": [str(pk),str(sk)]}
        try:
            pkUser = User.objects.get(id=pk)
            skUser = User.objects.get(id=sk)
            pkhost = pkUser.host + '/author/' + str(pk)
            skhost = skUser.host +'/author/' + str(sk)
            if ('http' not in pkhost):
                pkhost = 'https://' + pkhost
            if ('http' not in skhost):
                skhost = 'https://' + skhost
            responseDictionary["authors"] = [pkhost, skhost]
            response = Response(responseDictionary)
            responseDictionary["friends"] = FriendsSerializer.areFriendsSingle(pk,sk)
        except:
            response = Response(responseDictionary)

        return response

class FollowersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that handles followers
    """

    queryset = Followers.objects.all()
    serializer_class = FollowersSerializer

    def create(self, request):
        # accept/decline friend request
        responseDictionary = {"query":"following", "author": '', "followers": [], "message": "not implemented yet"}
        response = Response(responseDictionary)
        return response

    def retrieve(self, request, pk=None):
        # GET /following/authorID

        responseDictionary = {"query":"following", "author": pk, "followers": []}

        try:
            pkUser = User.objects.get(id=pk)
            pkhost = pkUser.host + '/author/' + str(pk)
            if ('http' not in pkhost):
                pkhost = 'https://' + pkhost
            responseDictionary["author"] = pkhost
            responseDictionary["followers"] = FollowersViewSet.serializer_class.following(pk)
            response = Response(responseDictionary)
        except:
            response = Response(responseDictionary)
        return response

    @action(methods=['post'], detail=False, url_path='delete', url_name='deleteFollowing')
    def deleteFollowing(self, request):

        responseDictionary = {"query": "delete following", "success": True}

        try:
            try:
                # swagger
                body = request.body
                requestJson = json.loads(body)
                authorID = requestJson["author"].split('/')[-2]               # person requesting deletion
                friendID = requestJson["following"].split('/')[-2]            # friend getting deleted
                if (authorID == ''):
                    requestJson["author"].split('/')[-2]
                if (friendID == ''):
                    requestJson["following"].split('/')[-2]
            except:
                # html form
                requestJson = request.data
                authorID = requestJson["author"].split("/")[-2]
                friendID = requestJson["following"].split("/")[-2]

            validated_data = {"author": friendID, "friend": authorID}
            FollowersViewSet.serializer_class.delete(validated_data)
            response = Response(responseDictionary)

        except:
            responseDictionary["success"] = False
            response = Response(responseDictionary)

        return response
    
    @action(methods=['get'], detail=False, url_path='user/(?P<sk>[^/.]+)', url_name='followList')
    def followList(self, request, pk=None, sk=None): 
        
        responseDictionary = {"query":"following", "author": sk, "followers": []}

        try:
            pkUser = User.objects.get(id=sk)
            pkhost = pkUser.host + '/author/' + str(sk)
            if ('http' not in pkhost):
                pkhost = 'https://' + pkhost
            responseDictionary["author"] = {"id":pkhost, "displayName": pkUser.displayName}
            followersList = FollowersViewSet.serializer_class.following(sk)
            followers = []
            for follow in followersList:
                followers.append({"id": follow[0], "displayName": follow[1]})    
            responseDictionary["followers"] = followers    
            response = Response(responseDictionary)
        except:
            raise
            response = Response(responseDictionary)
        return response
    
    
    
    def list(self, request):
        # list of follower with user data

       return Response(FollowersViewSet.serializer_class.list())