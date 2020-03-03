from comments.models import Comments
from rest_framework import serializers


class CommentsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comments
        fields = ['title', 'root', 'plainText','publish']
