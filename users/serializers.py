from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(
            username=validated_data.get('username', None),
            email=validated_data.get('email', None),
            firstName=validated_data.get('firstName', ""),
            lastName=validated_data.get('lastName', ""),
            displayName=validated_data.get('displayName', ""),
            host=validated_data.get('host', None),
            github=validated_data.get('github', ""),
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    # block password changes
    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        return instance

     
    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            try:
                if not value:
                    data[key] = ""
            except:
                pass
        return data

    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'email', 'bio', 'host', 'firstName', 'lastName', 'displayName', 'url', 'github', 'groups']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
