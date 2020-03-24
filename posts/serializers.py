from posts.models import Posts, Server
from comments.models import Comments
from rest_framework import serializers
from django.contrib.auth import get_user_model
import datetime
from comments.serializers import CommentsPostSerializer
User = get_user_model()

#class UserSerializer(serializers.HyperlinkedModelSerializer):
    #class Meta:
        #model = obj.author
        #fields = ['username', 'email', 'bio', 'host', 'firstName', 'lastName', 'displayName', 'url', 'github', 'groups']

class PostsSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.SerializerMethodField()
    contentType = serializers.SerializerMethodField()
    unlisted = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    #visible = serializers.SerializerMethodField()
    class Meta:
        model = Posts
        fields = ['id','title','author_obj','author', 'description','contentType','content','categories','visibility','visibleTo','comments','published','image','unlisted']

    def get_author(self,obj):
        user_id = str(obj.author_obj.id)
        return {"id": obj.author_obj.id, "host": obj.author_obj.host, "displayName": obj.author_obj.displayName,"url": "https://cloud-align-server.herokuapp.com/author/" + user_id +"/" ,"github":obj.author_obj.github}

    def get_contentType(self,obj):
        return ("text/plain")
    
    def get_unlisted(self,obj):
        return (False)

    def get_comments(self,obj):
        queryset = Comments.objects.all().filter(root = obj).order_by("-published")
        serializer_class = CommentsPostSerializer(instance=queryset, many=True)
        return(serializer_class.data)
        '''
    
    def create(self, obj):
        if obj["visible_to"] == "":
            visible_list = obj["author"].id
        else:
            visible_list = str(obj["author"].id) + "," + obj["visible_to"]

        post = Posts(
            title=obj["title"],
            author = obj["author"],
            #author=validated_data.get('author', Posts.author),
            description=obj["description"],
            content=obj["content"],
            visibilities=obj["visibilities"],
            visible_to = visible_list,
            #visible_to = validated_data.get('visible_to', Posts.visible_to),
            publish = str(datetime.datetime.now())
        )
        post.save()
        return post

    def get_visible(self,obj):
        if obj.visible_to == "":
            visible_list = obj.author.id
        else:
            visible_list = str(obj.author.id) + "," + obj.visible_to
        return visible_list
'''

class PostsCreateSerializer(serializers.HyperlinkedModelSerializer):
    @classmethod
    def create(self, validated_data):
        author_id = validated_data.get("author",Posts.author)
        author = User.objects.get(id = author_id)
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
            author_obj = author,
            #author=validated_data.get('author', Posts.author),
            description=validated_data.get('description', Posts.description),
            content=validated_data.get('content', Posts.content),
            visibility=validated_data.get('visibilities', Posts.visibilities),
            #visible_to = vis,
            image = validated_data.get('image', Posts.image),
            visibleTo = validated_data.get('visibleTo', Posts.visibleTo),
            published = str(datetime.datetime.now())
        )
        post.save()
        return True

    @classmethod
    def delete(self, validated_data):
        # delete friend request

        try:
            post = Posts.objects.get(id = validated_data)
            #request = FriendRequests.objects.get(authorID=friend, friendID=author)
            post.delete()
        except:
            return false
            #if (supress):
                #return
            #raise RuntimeError("Unable to delete friend request")
    class Meta:
        model = Posts
        fields = ['title','author', 'description','content','visibilities','visible_to','published']


class ServerSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        following = Server.objects.create(
                domain=validated_data.get("domain"),
                status=True,
        )

        return following

    class Meta:
        model = Server
        fields = ['id', "domain", 'status']
        read_only_fields = ('status', 'id')