from comments.models import Comments
from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import Posts
import datetime
from users.serializers import UserSerializer
User = get_user_model()

class CommentsSerializer(serializers.Serializer):
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
    def get_contentType(self,obj):
        return (obj.content)
    def get_author(self,obj):
        return {"id": obj.auth_id, "host": obj.host, "displayName": obj.name}
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
    def get_contentType(self,obj):
        return (obj.content)
    def get_author(self,obj):
        return {"id": obj.auth_id, "url":obj.url,"github":obj.github,"host": obj.host, "displayName": obj.name}

class CommentsCreateSerializer(serializers.Serializer):
    @classmethod
    def create(self,b, a,post_id):
        post = Posts.objects.get(id = post_id)
        comment = Comments(
            auth_id = b.get('id', ""),
	        url = b.get('url', ""),
	        host = b.get('host', ""),
	        name = b.get('displayName', ""),
	        github = b.get('github', ""),
            content = a.get('contentType',""),
            root = post,
            comment = a.get('comment',""),
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
        fields = ['auth_id','url','host','name','github','root','comment','published']
