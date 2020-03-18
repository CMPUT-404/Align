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
    publish = serializers.SerializerMethodField()

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
    def get_publish(self,obj):
        return (obj.publish)

    def get_author_data(self,obj):
        user = User.objects.get(id = obj.auth)
        return {"id": user.id, "username": user.username, "email": user.email, "bio": user.bio, "host": user.host, "firstName": user.firstName,"lastName": user.lastName, "displayName": user.displayName,"github":user.github}
    def get_contentType(self,obj):
        return ("text/plain")

class CommentsCreateSerializer(serializers.Serializer):
    @classmethod
    def create(self, a,b,post_id):
        post = Posts.objects.get(id = post_id)
        comment = Comments(
            auth = a,
            root = post,
            comment = b,
            publish = str(datetime.datetime.now()),
            )
        comment.save()
        return True

    @classmethod
    def delete(self, validated_data):
        try:
            comment = Comments.objects.get(id = validated_data)
            comment.delete()
        except:
            return false
    class Meta:
        model = Comments
        fields = ['auth','root','comment','publish']
