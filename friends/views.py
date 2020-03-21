from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from friends.models import Following
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from friends.serializers import FollowingSerializer
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer

User = get_user_model()


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    # all apis in following need perms
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def create(self, request, *args, **kwargs):
        response = {"query": "friendrequest", 
                    "success": False,
                    "message": "Friend request not sent"}

        try:
            # get data necessary
            requestInfo = request.data
            senderUrl, receiverUrl = normalize(requestInfo["author"]["id"], requestInfo["friend"]["id"])
    
            senderUser = get_user_by_url(senderUrl)
            receiverUser = get_user_by_url(receiverUrl)
            
            if ((senderUser == None) and (receiverUser == None)):
                # none of the users are from our server ignore
                response["error"] = "None of the users are from our server"
                return Response(response)
            
            # else, prepare data for serializer
            data = {"receiver": receiverUrl, "sender": senderUrl}
            
        except:
            response["error"] = "Unable to parse message as expected"
            return Response(response, status=400)
        
        # check: can't follow self
        if (senderUrl == receiverUrl):
            response["error"] = "You cannot follow yourself!"
            return Response(response, status=400)
    
        # serialize and check for errors
        serializer = FollowingSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            response["success"] = True
            response["message"] = "Friend request sent"
            return Response(serializer.data, status=200)
        else:
            response["error"] = serializer.errors
            return Response(response, status=400)

#    # shows only the requests of you
#    def list(self, request, *args, **kwargs):
#        you = UserSerializer(request.user, context={'request': request})
#
#        query1 = Following.objects.filter(receiver=request.user)
#        query2 = Following.objects.filter(sender=request.user)
#        requests_to_you = FollowingSerializer(instance=query1, many=True, context={'request': request})
#        requests_from_you = FollowingSerializer(instance=query2, many=True, context={'request': request})
#
#        for r in requests_to_you.data:
#            # get users json object
#            r['sender'] = UserSerializer(get_user_by_url(r['sender']), context={'request': request}).data
#            r['receiver'] = you.data  # do you really need your own user data?
#        for r in requests_from_you.data:
#            # get users json object
#            r['sender'] = you.data
#            r['receiver'] = UserSerializer(get_user_by_url(r['receiver']), context={'request': request}).data
#
#        return Response([*requests_to_you.data, *requests_from_you.data])

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










    @action(methods=['post'], detail=False, url_path='deletefollower', url_name='deleteFollower')
    def delete_follower(self, request):

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
                
            
                
            
                
        
                
            


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint for friend questions
    """

    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    # all apis in following need perms
    permission_classes = [
        permissions.IsAuthenticated
    ]

    @action(methods=['post', 'get'], detail=True, url_path='friends', url_name='friendInList')
    def friendInList(self, request, pk=None):

        if request.method == 'GET':
            # get friend list of author
            # URL: /author/{author_id}/friends
            responseDictionary = {"query": "friends", "authors": []}

            try:
                user = User.objects.get(id=pk)
                query1 = Following.objects.filter(receiver=user, status=True)
                query2 = Following.objects.filter(sender=user, status=True)
                friends1 = FollowingSerializer(instance=query1, many=True, context={'request': request})
                friends2 = FollowingSerializer(instance=query2, many=True, context={'request': request})

                friendList = []

                # add to friend list
                for friend in friends1.data:
                    data = UserSerializer(get_user_by_url(friend['sender']), context={'request': request}).data
                    friendList.append(data["url"])

                for friend in friends2.data:
                    data = UserSerializer(get_user_by_url(friend['receiver']), context={'request': request}).data
                    friendList.append(data["url"]) 

                responseDictionary["authors"] = friendList
                response = Response(responseDictionary)
            except:
                response = Response(responseDictionary)
            return response



        elif request.method == 'POST':
            # ask if anyone in the list is a friend
            # URL: ​/author​/{author_id}​/friends
            responseDictionary = {"query": "friends", "author": pk, "authors": []}
            try:
                toCheck = request.data["authors"]
                pkUser = User.objects.get(id=pk)
                friendList = []
                # check if friend is a pkUser's friend
                for friend in toCheck:
                    friendUser = get_user_by_url(friend)
                    query1 = Following.objects.filter(receiver=pkUser, sender=friendUser, status=True).first()
                    query2 = Following.objects.filter(receiver=friendUser, sender=pkUser, status=True).first()
                    if query1 != None or query2 != None:
                        friendList.append(friend)

                responseDictionary["authors"] = friendList
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

        responseDictionary = {"query": "friends", "friends": True, "authors": []}
        try:
            # check if they are friends
            pkUser = User.objects.get(id=pk)
            skUser = User.objects.get(id=sk)
            friends1 = UserSerializer(instance=pkUser, context={'request': request})
            friends2 = UserSerializer(instance=skUser, context={'request': request})
            responseDictionary["authors"] = [friends1.data, friends2.data]
            query1 = Following.objects.filter(receiver=pkUser, sender=skUser, status=True).first()
            query2 = Following.objects.filter(receiver=skUser, sender=pkUser, status=True).first()
            responseDictionary["friends"] = query1 != None or query2 != None
            response = Response(responseDictionary)
        except:
            raise
            responseDictionary["friends"] = False  # WARNING code unreachable
            response = Response(responseDictionary)

        return response




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
    
    