from posts.models import Posts
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

#class UserSerializer(serializers.HyperlinkedModelSerializer):
    #class Meta:
        #model = obj.author
        #fields = ['username', 'email', 'bio', 'host', 'firstName', 'lastName', 'displayName', 'url', 'github', 'groups']

class PostsSerializer(serializers.HyperlinkedModelSerializer):
    author_data = serializers.SerializerMethodField()
    contentType = serializers.SerializerMethodField()
    class Meta:
        model = Posts
        fields = ['id','title','author','author_data', 'description','contentType','content','categories','visibilities','visible_to','publish']

    def get_author_data(self,obj):
        return {"id": obj.author.id, "username": obj.author.username, "email": obj.author.email, "bio": obj.author.bio, "host": obj.author.bio, "firstName": obj.author.firstName,"lastName": obj.author.lastName, "displayName": obj.author.displayName,"github":obj.author.github}
        #print(real_id)
        #return User.objects.get(id = real_id)

    def get_contentType(self,obj):
        return ("text/plain")

class PostsCreateSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        post = Posts.objects.create(
            title=validated_data.get('title', Posts.title),
            author=validated_data.get('author', Posts.author),
            description=validated_data.get('description', Posts.description),
            content=validated_data.get('content', Posts.content),
            visibilities=validated_data.get('visibilities', Posts.visibilities),
            visible_to =validated_data.get('visible_to', Posts.visible_to),
            publish = validated_data.get('publish', Posts.publish),
        )
        return post
    class Meta:
        model = Posts
        fields = ['title','author', 'description','content','visibilities','visible_to','publish']
