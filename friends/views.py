import copy
from django.shortcuts import render
import json
from django.http import HttpResponse, Http404

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from friends.models import FriendRequests, Following
from friends.models import Friends
from friends.models import Followers
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from friends.serializers import FriendRequestSerializer, FollowingSerializer
from friends.serializers import FriendsSerializer
from friends.serializers import FollowersSerializer
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer

User = get_user_model()


class FriendRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint that makes a friend request.
    """

    queryset = FriendRequests.objects.all()
    serializer_class = FriendRequestSerializer

    def create(self, request):
        # make friend request
        responseDictionary = {"query": "friendrequest", "success": True, "message": "Friend request sent"}

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
            FriendRequestViewSet.serializer_class.create(validated_data)  # create request
            FollowersViewSet.serializer_class.create(validated_data)  # create follower
            response = Response(responseDictionary)

        except:
            responseDictionary["success"] = False
            responseDictionary["message"] = "Friend request not sent"
            response = Response(responseDictionary)

        return response

    def retrieve(self, request, pk=None):
        # retrieve a list of friend requests that the user has
        responseDictionary = {"query": "friend request list", "author": [], "requests": []}

        try:
            pkUser = User.objects.get(id=pk)
            name = pkUser.displayName
            responseDictionary["author"] = {"id": pkUser.id, "displayName": name}
            requests = FriendRequestViewSet.serializer_class.requests(pk)
            requestList = []
            for aRequest in requests:
                requestList.append({"id": aRequest[0], "displayName": aRequest[1]})
            responseDictionary["requests"] = requestList
            response = Response(responseDictionary)
        except:
            response = Response(responseDictionary)

        return response

    @action(methods=['get'], detail=False, url_path='user/(?P<sk>[^/.]+)', url_name='friendrequestList')
    def friendRequestList(self, request, pk=None, sk=None):

        responseDictionary = {"query": "friend request list", "author": [], "requests": []}

        try:
            pkUser = User.objects.get(id=sk)
            name = pkUser.displayName
            responseDictionary["author"] = {"id": sk, "displayName": name}
            requests = FriendRequestViewSet.serializer_class.requests(sk)
            requestList = []
            for aRequest in requests:
                requestList.append({"id": aRequest[0], "displayName": aRequest[1]})
            responseDictionary["requests"] = requestList
            response = Response(responseDictionary)
        except:
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
        responseDictionary = {"query": "friendrequestprocess", "success": True}

        try:
            try:
                # swagger
                body = request.body
                requestJson = json.loads(body)
                authorID = requestJson["author"]  # person accepting/declining
                friendID = requestJson["friend"]  # person who sent request
                friendStatus = requestJson["friendstatus"]
            except Exception as e:
                # html form
                requestJson = request.data
                authorID = requestJson["author"]
                friendID = requestJson["friend"]
                friendStatus = requestJson["friendstatus"]

            if (not (friendID and authorID)):
                raise ValueError("No friendID or authorID was given")
            validated_data = {"author": authorID, "friend": friendID}
            FriendRequestViewSet.serializer_class.delete(validated_data)  # delete friends request
            if (friendStatus == "accept"):
                # create friend
                FollowersViewSet.serializer_class.delete(validated_data)  # delete following relation
                validated_data = {"author": friendID, "friend": authorID}
                FriendRequestViewSet.serializer_class.delete(validated_data,
                                                             supress=True)  # delete reverse friend request
                validated_data = {"author": friendID, "friend": authorID}
                FollowersViewSet.serializer_class.delete(validated_data, supress=True)  # delete reverse follower
                FriendViewSet.serializer_class.create(validated_data)  # create friend
            response = Response(responseDictionary)

        except:
            responseDictionary["success"] = False
            response = Response(responseDictionary)

        return response

    @action(methods=['post'], detail=False, url_path='delete', url_name='friendDelete')
    def friendDelete(self, request):

        # POST /friend/delete
        responseDictionary = {"query": "frienddelete", "success": True}

        try:
            try:
                # swagger
                body = request.body
                requestJson = json.loads(body)
                authorID = requestJson["author"]  # person requesting deletion
                friendID = requestJson["friend"]  # friend getting deleted
            except:
                # html form
                requestJson = request.data
                authorID = requestJson["author"]
                friendID = requestJson["friend"]

            if (not (friendID and authorID)):
                raise ValueError("No friendID or authorID was given")
            validated_data = {"author": authorID, "friend": friendID}
            FriendViewSet.serializer_class.delete(validated_data)  # delete friend relation
            validated_data = {"author": friendID, "friend": authorID}
            FollowersViewSet.serializer_class.create(validated_data)  # create one way follower
            response = Response(responseDictionary)

        except:
            responseDictionary["success"] = False
            response = Response(responseDictionary)

        return response

    @action(methods=['get'], detail=False, url_path='user/(?P<sk>[^/.]+)', url_name='friendList')
    def friendList(self, request, pk=None, sk=None):
        responseDictionary = {"query": "friends", "author": {}, "authors": []}
        try:
            pkUser = User.objects.get(id=sk)
            name = pkUser.displayName
            responseDictionary["author"] = {"id": sk, "displayName": name}
            alist = FriendsSerializer.friendsList(sk)
            authors = []
            for friend in alist:
                idNum = friend[0] if (friend[0][-1] == '/') else (friend[0] + '/')
                idNum = idNum.split('/')[-2]
                authors.append({"id": idNum, "displayName": friend[1]})
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
            responseDictionary = {"query": "friends", "authors": []}
            try:
                responseDictionary["authors"] = FriendsSerializer.friendsList(pk)
                response = Response(responseDictionary)
            except:
                response = Response(responseDictionary)
            return response

        elif (request.method == 'POST'):
            # ask if anyone in the list is a friend
            # URL: ​/author​/{author_id}​/friends
            responseDictionary = {"query": "friends", "author": str(pk), "authors": []}
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
            responseDictionary = {"Error": "Page does not exist"}
            return Response(responseDictionary)

    @action(methods=['get'], detail=True, url_path='friends/(?P<sk>[^/.]+)', url_name='areFriends')
    def areFriends(self, request, pk=None, sk=None):
        # ask if 2 authors are friends
        # URL: /author/{author1_id}/friends/{author2_id}

        responseDictionary = {"query": "friends", "friends": False, "authors": [str(pk), str(sk)]}
        try:
            pkUser = User.objects.get(id=pk)
            skUser = User.objects.get(id=sk)
            pkhost = pkUser.host + '/author/' + str(pk)
            skhost = skUser.host + '/author/' + str(sk)
            if ('http' not in pkhost):
                pkhost = 'https://' + pkhost
            if ('http' not in skhost):
                skhost = 'https://' + skhost
            responseDictionary["authors"] = [pkhost, skhost]
            response = Response(responseDictionary)
            responseDictionary["friends"] = FriendsSerializer.areFriendsSingle(pk, sk)
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
        responseDictionary = {"query": "following", "author": '', "followers": [], "message": "not implemented yet"}
        response = Response(responseDictionary)
        return response

    def retrieve(self, request, pk=None):
        # GET /following/authorID

        responseDictionary = {"query": "following", "author": pk, "followers": []}

        try:
            responseDictionary["author"] = pk
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
                authorID = requestJson["author"]  # person requesting deletion
                friendID = requestJson["following"]  # friend getting deleted
            except:
                # html form
                requestJson = request.data
                authorID = requestJson["author"]
                friendID = requestJson["following"]

            validated_data = {"author": friendID, "friend": authorID}
            FollowersViewSet.serializer_class.delete(validated_data)
            response = Response(responseDictionary)

        except:
            responseDictionary["success"] = False
            response = Response(responseDictionary)

        return response

    @action(methods=['get'], detail=False, url_path='user/(?P<sk>[^/.]+)', url_name='followList')
    def followList(self, request, pk=None, sk=None):

        responseDictionary = {"query": "following", "author": sk, "followers": []}

        try:
            pkUser = User.objects.get(id=sk)
            responseDictionary["author"] = {"id": sk, "displayName": pkUser.displayName}
            responseDictionary["followers"] = FollowersViewSet.serializer_class.following(sk)
            response = Response(responseDictionary)
        except:
            response = Response(responseDictionary)
        return response

    def list(self, request):
        # list of follower with user data

        return Response(FollowersViewSet.serializer_class.list())


# new following
class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    # all apis in following need perms
    permission_classes = [
        permissions.IsAuthenticated
    ]

    # TODO special: Accept request if receiver has already sent sender an request, set status to true
    def create(self, request, *args, **kwargs):
        sender_serializer = UserSerializer(request.user, context={'request': request})

        # FIXME check TODO
        query = Following.objects.filter(receiver=request.user)
        requests = FollowingSerializer(instance=query, many=True, context={'request': request})
        receiver_url = request.data["receiver"]
        for r in requests.data:
            if receiver_url == r["sender"]:
                return Response("please use alternative api to accept an request", status=501)
        #####################################################################################

        data = {"receiver": request.data["receiver"], "sender": sender_serializer.data['url']}

        if request.data["receiver"] == sender_serializer.data['url']:
            return Response("you cannot follow yourself!", status=400)

        serializer = FollowingSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    # shows only the requests of you
    def list(self, request, *args, **kwargs):
        you = UserSerializer(request.user, context={'request': request})

        query1 = Following.objects.filter(receiver=request.user)
        query2 = Following.objects.filter(sender=request.user)
        requests_to_you = FollowingSerializer(instance=query1, many=True, context={'request': request})
        requests_from_you = FollowingSerializer(instance=query2, many=True, context={'request': request})

        for r in requests_to_you.data:
            # get users json object
            r['sender'] = UserSerializer(get_user_by_url(r['sender']), context={'request': request}).data
            r['receiver'] = you.data  # do you really need your own user data?
        for r in requests_from_you.data:
            # get users json object
            r['sender'] = you.data
            r['receiver'] = UserSerializer(get_user_by_url(r['sender']), context={'request': request}).data

        return Response([*requests_to_you.data, *requests_from_you.data])

    def update(self, request, pk=None, **kwargs):
        pass

    def partial_update(self, request, pk=None, **kwargs):
        pass

    '''TO DELETE A REQUEST, USE DELETE /newfollowing/<following:id> (DEBUG ONLY)'''
    # def destroy(self, request, pk=None):
    #     pass


# TODO NEED TO ACCORDING TO USER AND STATUS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request):
    receiver = request.user
    sender_id = request.data["sender"]
    #request_id = request.data["id"]
    try:
        r = Following.objects.filter(sender=sender_id, receiver=receiver).first()
        if (r == None):
            raise RuntimeException()
        if (r.receiver != receiver):
            return Response("The request cannot be accepted, because the current user is not the receiver of the friend request",status=400)
        if r.status != None:
            return Response("The request cannot be accepted, because its status is {}".format(r.status), status=400)    
        r.status = True
        r.save()

        # make other friend relation true
        reverseFollowing = Following.objects.filter(receiver=r.sender, sender=r.receiver).first()
        if (reverseFollowing != None):
            reverseFollowing.status = True
            reverseFollowing.save()

        return Response("Friend request accepted", status=200)
    except:
        return Response("The request with id {} not found".format(request_id), status=400)


# TODO NEED TO ACCORDING TO USER AND STATUS
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request):
    receiver = request.user
    sender_id = request.data["sender"]
    #request_id = request.data["id"]
    try:
        r = Following.objects.filter(sender=sender_id, receiver=receiver).first()
        if (r == None):
            raise RuntimeException()
        if (r.receiver != receiver):
            return Response("The request cannot be accepted, because the current user is not the receiver of the friend request",status=400)
        if r.status == False:
            return Response("The request cannot be rejected, because its status is {}".format(r.status), status=400)
        r.status = False    
        r.save()
        return Response("Friend request rejected", status=200)
    except:
        return Response("The request with id {} not found".format(sender_id), status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_friend(request):
    deleting = request.user
    to_delete = request.data["friend"]
    try:
        to_delete = User.objects.get(id=to_delete)
        friendRelation1 = Following.objects.filter(sender=deleting, receiver=to_delete, status=True).first()         # this relation needs to be deleted
        friendRelation2 = Following.objects.filter(sender=to_delete, receiver=deleting, status=True).first()         # this one needs to be modified
        if (friendRelation1 != None):
            friendRelation1.delete()
        if (friendRelation2 != None):
            friendRelation2.status = False
            friendRelation2.save()
        if ((friendRelation1 == None) and (friendRelation2 == None)):
            return Response("The current user {} is not friends with {}".format(request.user.displayName, to_delete.displayName), status=400)
        return Response("Friend deleted", status=200)
    except:
        return Response("The request with id % not found".format(request.data["following"]), status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_following(request):
    deleting = request.user
    to_delete = request.data["following"]
    try:
        to_delete = User.objects.get(id=to_delete)
        followingRelation1 = Following.objects.filter(sender=deleting, receiver=to_delete, status=False).first()         # delete rejected request if present
        followingRelation2 = Following.objects.filter(sender=deleting, receiver=to_delete, status=None).first()          # delete unreplied request if present
        if (followingRelation1 != None):
            followingRelation1.delete()
        if (followingRelation2 != None):
            followingRelation2.delete()
        if ((followingRelation1 == None) and (followingRelation2 == None)):
            return Response("The current user {} is not following {}".format(request.user.displayName, to_delete.displayName), status=400)
        return Response("Following deleted", status=200)
    except:
        return Response("The request with id % not found".format(request.data["following"]), status=400)

def get_user_by_url(url):
    user_id = url.split("/")[-2]
    return User.objects.get(id=user_id)
