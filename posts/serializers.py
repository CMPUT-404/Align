from posts.models import Posts
from rest_framework import serializers
from django.contrib.auth import get_user_model
import datetime
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
    @classmethod
    def create(self, validated_data):
        author_id = validated_data.get("author",Posts.author)
        author_obj = User.objects.get(id = author_id)
        '''
        if validated_data.get('visible_to', Posts.visible_to) == "":
            vis = author_id
        else:
            vis = validated_data.get('visible_to', Posts.visible_to) + "," + author_id
            '''

        #print(author_obj)
        #validated_data['author'] = author_obj
        #print("__________________________________")
        #print(author_obj.id)
        post = Posts(
            title=validated_data.get('title', Posts.title),
            author = author_obj,
            #author=validated_data.get('author', Posts.author),
            description=validated_data.get('description', Posts.description),
            content=validated_data.get('content', Posts.content),
            visibilities=validated_data.get('visibilities', Posts.visibilities),
            #visible_to = vis,
            visible_to = validated_data.get('visible_to', Posts.visible_to),
            publish = str(datetime.datetime.now())
        )
        post.save()
        return True

    class Meta:
        model = Posts
        fields = ['title','author', 'description','content','visibilities','visible_to','publish']
