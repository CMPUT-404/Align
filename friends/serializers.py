from django.contrib.auth import get_user_model
from friends.models import Following
from rest_framework import serializers

# new following
class FollowingSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        print(validated_data)
        following = Following.objects.create(
                sender=validated_data.get("sender"),
                receiver=validated_data.get("receiver"),
                status=None,
        )

        return following

    class Meta:
        model = Following
        fields = ['id','sender', 'receiver', 'status']
        read_only_fields = ('status', 'id')
