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
    author = serializers.SerializerMethodField()
    contentType = serializers.SerializerMethodField()
    published = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id','auth','root', 'comment','published','author']

    def get_id(self,obj):
        return (obj.id)
    def get_auth(self,obj):
        return (obj.auth)
    def get_root(self,obj):
        return (obj.root.id)
    def get_comment(self,obj):
        return (obj.comment)
    def get_published(self,obj):
        return (obj.published)

    def get_author(self,obj):
        user = User.objects.get(id = obj.auth)
        return {"id": user.id, "host": user.host, "displayName": user.displayName}
    def get_contentType(self,obj):
        return ("text/plain")

class CommentsPostSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    contentType = serializers.SerializerMethodField()
    published = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['id','contentType', 'comment','published','author']

    def get_id(self,obj):
        return (obj.id)
    def get_comment(self,obj):
        return (obj.comment)
    def get_published(self,obj):
        return (obj.published)
    def get_author(self,obj):
        user = User.objects.get(id = obj.auth)
        user_id = str(user.id)
        return {"id": user.id, "url":"https://cloud-align-server.herokuapp.com/author/" + user_id +"/","host": user.host, "displayName": user.displayName,"github":user.github}
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
            published = str(datetime.datetime.now()),
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
        fields = ['auth','root','comment','published']
