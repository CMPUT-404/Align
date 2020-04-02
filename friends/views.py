import requests
from django.contrib.auth.models import AnonymousUser

# Create your views here.
from django.contrib.auth import get_user_model

from friends.models import Following
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from friends.serializers import FollowingSerializer

from posts.models import Server
from posts.serializers import ServerSerializer
from users.serializers import UserSerializer

User = get_user_model()

class FollowingPermissionSet(permissions.BasePermission):

    def has_permission(self, request, view):
        # everyone can create 
        return (view.action == 'create')


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    # all apis in following need perms
    permission_classes = [FollowingPermissionSet | permissions.IsAuthenticated]



    def create(self, request, *args, **kwargs):
        response = {"query": "friendrequest", 
                    "success": False,
                    "message": "Friend request not sent"}

        try:
            # get data necessary
            requestInfo = request.data
            senderUrl, receiverUrl = normalize(requestInfo["author"]["id"], requestInfo["friend"]["id"])
            senderHost, receiverHost = normalize(requestInfo["author"]["host"], requestInfo["friend"]["host"])
            
            senderUser = get_user_by_url(senderUrl)
            receiverUser = get_user_by_url(receiverUrl)
            
            if ((senderUser == None) and (receiverUser == None)):
                # none of the users are from our server ignore
                response["error"] = "None of the users are from our server"
                return Response(response, status=400)
            
            # else, prepare data for serializer
            data = {"receiver": receiverUrl, "sender": senderUrl}
            
        except:
            response["error"] = "Unable to parse message as expected"
            return Response(response, status=400)
        
        # check: can't follow self
        if (senderUrl == receiverUrl):
            response["error"] = "You cannot follow yourself!"
            return Response(response, status=400)
    
        # checkhost
        
        # sent from someone we don't trust
        if ((senderHost != getHost()) or (Server.objects.filter(domain=senderHost, status=True).exists())):
            response["error"] = "Sender host is not trusted: {}".format(senderHost)
            return Response(response, status=400)
        
        
        # receiver host is not ours, send to other server
        if (receiverHost != getHost()):
            if (Server.objects.filter(domain=receiverHost, status=True).exists()):
                # send to other server
                url = "{}friendrequest/".format(receiverHost)                    
                serverResponse = requests.post(url=url, json=requestInfo)
                try:
                    jsonResponse = serverResponse.json()
                    if (not jsonResponse["success"]):
                        response["error"] = "The foreign server responded: {}".format(jsonResponse)
                        return Response(response, status=400)
                except:
                    response["error"] = "The foreign server responded: {}".format(serverResponse.text)
                    return Response(response, status=400)
                
            else:
                response["error"] = "Receiver host is not a trusted server: {}".format(receiverHost)
                return Response(response, status=400)
            
        # other servers response went well if necessary
        # serialize and check for errors        
        serializer = FollowingSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response["success"] = True
            response["message"] = "Friend request sent"
            return Response(response, status=200)
        else:
            response["error"] = serializer.errors
            return Response(response, status=400)


    def update(self, request, pk=None, **kwargs):
        pass

    def partial_update(self, request, pk=None, **kwargs):
        pass

    '''TO DELETE A REQUEST, USE DELETE /newfollowing/<following:id> (DEBUG ONLY)'''
    # def destroy(self, request, pk=None):
    #     pass
    
    
    
    
    
    
    
    @action(methods=['post'], detail=False, url_path='accept', url_name='acceptFriend')
    def accept_friend_request(self, request, pk=None):
        
        response = {"query": "friendaccept", 
                    "success": False,
                    "message": "Friend request not accepted"}
        
        try:
            # get data necessary
            requestInfo = request.data
            receiverUrl, senderUrl = normalize(requestInfo["author"]["id"], requestInfo["friend"]["id"])
            
        except:
            # parsing error
            response["error"] = "Unable to parse message as expected"
            return Response(response, status=400)
        
        result = Following.objects.filter(sender=senderUrl, receiver=receiverUrl).first()
        if (result == None):
            # no friend request was sent
            response["error"] = "No friend request matches the given details"
            return Response(response, status=400)
        
        if (result.status == True):
            # already friends, an error but not a serious one
            response["success"] = True
            response["message"] = "Friend request accepted"
            response["error"] = "The users are already friends"
            return Response(response, status=200)
        
        if (result.status == False):
            # already rejected
            response["error"] = "The user has already rejected this request"
            return Response(response, status=400)
        
        if (result.status == None):
            # good
            result.status = True
            result.save()
            response["success"] = True
            response["message"] = "Friend request accepted"
            try:
                # accept reverse relation on our server
                result = Following.objects.filter(sender=receiverUrl, receiver=senderUrl).first()
                if (result != None):
                    result.status = True
                    result.save()
            except:
                # no reverse relation
                pass
            return Response(response, status=200)
        
        return Response(response)
    









    @action(methods=['post'], detail=False, url_path='reject', url_name='rejectFriend')
    def reject_friend_request(self, request, pk=None):
        
        response = {"query": "friendreject", 
                    "success": False,
                    "message": "Friend request not rejected"}
        
        try:
            # get data necessary
            requestInfo = request.data
            receiverUrl, senderUrl = normalize(requestInfo["author"]["id"], requestInfo["friend"]["id"])
            
        except:
            # parsing error
            response["error"] = "Unable to parse message as expected"
            return Response(response, status=400)
        
        result = Following.objects.filter(sender=senderUrl, receiver=receiverUrl).first()
        if (result == None):
            # no friend request was sent
            response["error"] = "No friend request matches the given details"
            return Response(response, status=400)
        
        if (result.status == True):
            # already friends, can't reject
            response["error"] = "The users are already friends"
            return Response(response, status=400)
        
        if (result.status == False):
            # already rejected, an error but not a serious one
            response["success"] = True
            response["message"] = "Friend request rejected"
            response["error"] = "The user has already rejected this request"
            return Response(response, status=200)
        
        if (result.status == None):
            # good
            result.status = False
            result.save()
            response["success"] = True
            response["message"] = "Friend request rejected"
            return Response(response, status=200)
        
        return Response(response)










    @action(methods=['post'], detail=False, url_path='deletefollowing', url_name='deleteFollowing')
    def delete_following(self, request):

        response = {"query": "deletefollow", 
                    "success": False,
                    "message": "Following not deleted"}
        
        try:
            # get data necessary
            requestInfo = request.data
            deleterUrl, gettingDeletedUrl = normalize(requestInfo["author"]["id"], requestInfo["friend"]["id"])
            
        except:
            # parsing error
            response["error"] = "Unable to parse message as expected"
            return Response(response, status=400)
        
        result = Following.objects.filter(sender=deleterUrl, receiver=gettingDeletedUrl).first()
        if (result == None):
            # was not following user
            response["error"] = "No follower was found matching the given details"
            return Response(response, status=400)
            
        if (result.status == True):
            # they are friends, use other api
            response["error"] = "Users are friends, use the deletefriend API"
            return Response(response, status=400)
        
        # delete request
        result.delete()
        response["success"] = True
        response["message"] = "Following deleted"
        return Response(response, status=200)
        
    
    
    
    
    
    
    
    
    
    
    
    @action(methods=['post'], detail=False, url_path='deletefriend', url_name='deleteFriend')
    def delete_friend(self, request):

        response = {"query": "deletefriend", 
                    "success": False,
                    "message": "Friend not deleted"}
        
        try:
            # get data necessary
            requestInfo = request.data
            deleterUrl, gettingDeletedUrl = normalize(requestInfo["author"]["id"], requestInfo["friend"]["id"])
            
        except:
            # parsing error
            response["error"] = "Unable to parse message as expected"
            return Response(response, status=400)
        
        result1 = Following.objects.filter(sender=deleterUrl, receiver=gettingDeletedUrl).first()
        result2 = Following.objects.filter(sender=gettingDeletedUrl, receiver=deleterUrl).first()
        
        if ((result1 == None) and (result2 == None)):
            # not in db
            response["error"] = "No friend was found matching the given details"
            return Response(response, status=400)
        
        if (result1 != None):
            # deleter was the sender
            
            if (result1.status != True):
                # they are not friends
                response["error"] = "Users are not currently friends"
                return Response(response, status=400)
            
            if (result2 != None):
                # change reverse relation
                result2.status = False
                result2.save()
                result1.delete()
                
            else:
                # reverse relation doesn't exist
                result1.status = False
                result1.save()
                
            response["success"] = True
            response["message"] = "Friend deleted"
            return Response(response, status=200)
        
        else:
            # deleter was the receiver
            
            if (result2.status != True):
                # they are not friends
                response["error"] = "Users are not currently friends"
                return Response(response, status=400)
            
            if (result1 != None):
                # change reverse relation
                result1.status = False
                result1.save()
                result2.delete()
                
            else:
                # reverse relation doesn't exist
                result2.status = False
                result2.save()
                
            response["success"] = True
            response["message"] = "Friend deleted"
            return Response(response, status=200)
                
            
                
            
                
class AuthorPermissionSet(permissions.BasePermission):
    """
    Custom permission to only allow access to lists for admins
    """

    def has_permission(self, request, view):
        # free for all
        if view.action == 'retrieve':
            return True

        # user ok
        elif view.action == 'update':
            return request.user and type(request.user) != AnonymousUser

        elif view.action == 'list':
            return request.user and type(request.user) != AnonymousUser

        elif view.action == 'partial_update':
            return request.user and type(request.user) != AnonymousUser

        # admin only
        elif view.action == 'destroy':
            return request.user and request.user.is_staff

        elif view.action == 'create':
            return request.user and request.user.is_staff

        # i dont handle
        else:
            return True


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for friend questions
    """

    permission_classes = [
        AuthorPermissionSet
    ]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        a = kwargs['pk']
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
                    url = '{}author/{}'.format(host, a)
                    response = requests.get(url=url)
                    data = response.json()
                    if not data:
                        raise Exception("Cannot get the user with id = {}".format(a))
                except Exception as e:
                    return Response(e.args, status=500)
            else:
                return Response("The host {} is not in the server list, the access is denied".format(host), status=400)
        else:
            queryset = User.objects.get(id=a)
            serializer = UserSerializer(instance=queryset, context={'request': request})

            # get friends from following model
            userUrl, _ = normalize(UserSerializer(queryset, context={'request': request}).data["url"], '/')
            query1 = Following.objects.filter(receiver=userUrl, status=True)
            query2 = Following.objects.filter(sender=userUrl, status=True)

            friendList = []

            # add to friend list
            for friend in query1:
                friendList.append(friend.sender)

            for friend in query2:
                friendList.append(friend.receiver)

            data = dict(serializer.data)

            data["friends"] = friendList

        return Response(data)


    @action(methods=['post', 'get'], detail=True, url_path='friends', url_name='friendList')
    def friend_List(self, request, pk=None):

        if request.method == 'GET':
            # get friend list of author
            # URL: /author/{author_id}/friends
            response = {"query": "friends", "authors": []}

            try:
                # get user object
                user = User.objects.get(id=pk)
            except:
                response["error"] = "Author is not from this server"
                return Response(response, status=400)
                
            # get friends from following model
            userUrl, _ = normalize(UserSerializer(user, context={'request': request}).data["url"], '/')
            response["authors"] = friendList(userUrl)
            return Response(response, status=200)


        elif request.method == 'POST':
            # ask if anyone in the list is a friend
            # URL: ​/author​/{author_id}​/friends
            response = {"query": "friends", "author": pk, "authors": []}
            try:
                # get user object
                user = User.objects.get(id=pk)
            except:
                response["error"] = "Author is not from this server"
                return Response(response, status=400)
            
            try:
                toCheck = request.data["authors"]
                userUrl, _ = normalize(UserSerializer(user, context={'request': request}).data["url"], '/')
                ListofFriends = friendList(userUrl)
                isFriend = []
                # check if friend is a user's friend
                for friend in toCheck:
                    friendUrl, _ = normalize(friend, '/')
                    if (friendUrl in ListofFriends):
                        isFriend.append(friend)
                response["authors"] = isFriend
                return Response(response, status=200)
            
            except:
                response["error"] = "Unable to parse message as expected"
                return Response(response,status=400)

        else:
            response = {"error": "Page does not exist"}
            return Response(response, status=405)








    @action(methods=['get'], detail=True, url_path='followers', url_name='followerList')
    def follower_List(self, request, pk=None):

        # get follower list of author
        # URL: /author/{author_id}/followers
        response = {"query": "followers", "authors": []}
        
        try:
            # get user object
            user = User.objects.get(id=pk)
        except:
            response["error"] = "Author is not from this server"
            return Response(response, status=400)
                
        # get friends from following model
        userUrl, _ = normalize(UserSerializer(user, context={'request': request}).data["url"], '/')
        query = Following.objects.filter(sender=userUrl)
        
        followerList = []

        # add to friend list
        for follower in query:
            followerList.append(follower.receiver)

        query = Following.objects.filter(receiver=userUrl)
        for follower in query:
            if (follower.status == True):
                followerList.append(follower.sender)	

        response["authors"] = followerList
        return Response(response, status=200)








    @action(methods=['get'], detail=True, url_path='friends/(?P<sk>[^/.]+)', url_name='areFriends')
    def are_friends(self, request, pk=None, sk=None):
        # ask if 2 authors are friends
        # URL: /author/{author1_id}/friends/{author2_id}

        response = {"query": "friends", "friends": False, "authors": []}

        # check if they are friends
        try:
            user1 = User.objects.get(id=pk)
        except:
            user1 = None
        try:
            user2 = User.objects.get(id=sk)
        except:
            user2 = None
        user = user1 if (user1!= None) else user2
        friendID = sk if (user1 != None) else pk
        
        # users aren't from server
        if (user == None):
            response["error"] = "Neither of the authors are from this server"
            return Response(response, status=400)
        
        
        userUrl, _ = normalize(UserSerializer(user, context={'request': request}).data["url"], '/')            
        query1 = Following.objects.filter(receiver=userUrl, status=True)
        query2 = Following.objects.filter(sender=userUrl, status=True)
            
        # check locally first
        for friend in query1:
            if (get_id(friend.sender) == str(friendID)):
                response["friends"] = True
                response["authors"] = [userUrl, friend.sender]
                return Response(response, status=200)
            
        for friend in query2:
            if (get_id(friend.receiver) == str(friendID)):
                response["friends"] = True
                response["authors"] = [userUrl, friend.receiver]
                return Response(response, status=200)

        # check other servers
        query = Following.objects.filter(sender=userUrl)
        
        for friend in query:
            if ((friend.status != True) and (get_id(friend.receiver) == str(friendID))):
                hostUrl, _ = normalize(get_host(friend.receiver), '/')
                if ((hostUrl == getHost()) or (hostUrl == '') or (not Server.objects.filter(domain=hostUrl, status=True).exists())):
                    break
                url = "{}author/{}/friends/{}/".format(hostUrl, str(friendID), get_id(userUrl))
                serverResponse = requests.get(url)
                try:
                    jsonResponse = serverResponse.json()
                    if (jsonResponse["friends"]):
                        response["friends"] = True
                        response["authors"] = [userUrl, friend.receiver]
                        return Response(response, status=200)
                    else:
                        break
                except:
                    break
        
        return Response(response, status=200)





    @action(methods=['get'], detail=True, url_path='friendrequests', url_name='requestList')
    def request_List(self, request, pk=None):

        # get request list of author
        # URL: /author/{author_id}/friendrequests
        response = {"query": "requests", "requests": []}
        
        try:
            # get user object
            user = User.objects.get(id=pk)
        except:
            response["error"] = "Author is not from this server"
            return Response(response, status=400)
                
        # get friends from following model
        userUrl, _ = normalize(UserSerializer(user, context={'request': request}).data["url"], '/')
        query = Following.objects.filter(receiver=userUrl)
        
        requestList = []

        # add to friend list
        for request in query:
            if ((request.status != True) and (request.status != False)):
                requestList.append(request.sender)

        response["requests"] = requestList
        return Response(response, status=200)






def getHost():
    return "https://cloud-align-server.herokuapp.com/"


def normalize(str1, str2):
    # normalize urls
    if (str1[-1] != '/'):
        str1 += '/'
    if (str2[-1] != '/'):
        str2 += '/'    
    
    return str1, str2


def get_user_by_url(url):
    try:
        user_id = str(url).split("/")[-2]
        return User.objects.get(id=user_id)
    except:
        return None
    
def get_id(string):
    try:
        return str(string).split('/')[-2]
    except:
        return ''
    
def get_host(string):
    try:
        return '/'.join(string.split('/')[:-3])
    except:
        ''
def friendList(userUrl):  
    
    query1 = Following.objects.filter(receiver=userUrl, status=True)
    query2 = Following.objects.filter(sender=userUrl, status=True)

    friendList = []

    # add to friend list
    
    # check locally
    for friend in query1:
        friendList.append(friend.sender)

    for friend in query2:
        friendList.append(friend.receiver)
        
    # check other servers    
    query = Following.objects.filter(sender=userUrl)
    for item in query:
        if (item.status != True):
            hostUrl, _ = normalize(get_host(item.receiver), '/')
            if ((hostUrl == getHost()) or (hostUrl == '') or (not Server.objects.filter(domain=hostUrl, status=True).exists())):
                continue
            url = "{}author/{}/friends/{}/".format(hostUrl, get_id(item.receiver), get_id(userUrl))
            serverResponse = requests.get(url)
            try:
                jsonResponse = serverResponse.json()
                if (jsonResponse["friends"]):
                    friendList.append(item.receiver)
            except:
                continue
        
        
    return friendList    






