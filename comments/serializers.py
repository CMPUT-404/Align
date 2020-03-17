from comments.models import Comments
from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import Posts
import datetime
User = get_user_model()

class CommentsSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    auth = serializers.SerializerMethodField()
    root = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    author_data = serializers.SerializerMethodField()
    contentType = serializers.SerializerMethodField()


    class Meta:
        model = Comments
        fields = ['id','auth','root', 'comment','publish']

    def get_id(self,obj):
        return (obj.id)
    def get_auth(self,obj):
        return (obj.auth)
    def get_root(self,obj):
        return (obj.root.id)
    def get_comment(self,obj):
        return (obj.comment)

    def get_author_data(self,obj):
        user = User.objects.get(id = obj.auth)
        #post = obj.root.author
        return {"id": user.id, "username": user.username, "email": user.email, "bio": user.bio, "host": user.host, "firstName": user.firstName,"lastName": user.lastName, "displayName": user.displayName,"github":user.github}
        #print(real_id)
        #return User.objects.get(id = real_id)

    def get_contentType(self,obj):
        return ("text/plain")

class CommentsCreateSerializer(serializers.HyperlinkedModelSerializer):
    @classmethod
    def create(self, validated_data,post_id):
        #p_id = validated_data.get("root",Comments.root)
        post = Posts.objects.get(id = post_id)
        #user_id = validated_data.get("user_id",Comments.author)
        #author_obj = User.objects.get(id = user_id)
        comment = Comments(
            #id=validated_data.get('id', Posts.title),
            #author=validated_data.get('author', Posts.author),
            #auth = validated_data.get("auth",Comments.auth),
            auth = "f9d62b2d-da10-4f7f-9124-9233d49d1701",
            root = post,
            #comment = validated_data.get('comment', Comments.comment),
            comment = "good day",
            #publish = validated_data.get('publish', Comments.publish),
            publish = str(datetime.datetime.now()),
            )
        comment.save()
        return True

    @classmethod
    def delete(self, validated_data):
        # delete friend request

        try:
            comment = Comments.objects.get(id = validated_data)
            #request = FriendRequests.objects.get(authorID=friend, friendID=author)
            comment.delete()
        except:
            return false
            #if (supress):
                #return
            #raise RuntimeError("Unable to delete friend request")
    class Meta:
        model = Comments
        fields = ['auth','root','comment','publish']
