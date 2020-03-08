from django.shortcuts import render
from django.http import HttpResponse, QueryDict

# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from pytz import unicode
from rest_framework import viewsets, status, permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer, GroupSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer



class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# login user
class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        if username is None or password is None:
            return Response(status=400, data={'errors': 'username or password is None'})
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.check_password(password):
                serializer = UserSerializer(user, context={'request': request})
                # if no token, generate a new token
                if not Token.objects.filter(user=user).exists():
                    Token.objects.create(user=user)
                return Response({'token': Token.objects.get(user=user).key, 'user': serializer.data})
            else:
                return Response(status=400, data={'errors': 'Username or password is incorrect'})
        else:
            return Response(status=400, data={'errors': 'Username or password is incorrect'})

# register user
class RegisterView(CreateAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = QueryDict.copy(request.data)
        data["host"] = self.get_client_ip(request)
        print(data)
        serializer = UserSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            token, created = Token.objects.get_or_create(user=serializer.instance)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(status=400, data={'errors': serializer.errors})

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# Validate Your User Token
class ValidateView(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(status=200, data={'user': UserSerializer(user, context={'request': request}).data})

''' # ignore me please
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})
'''

######### get user by token #######################
# from rest_framework.authtoken.models import Token
# user = Token.objects.get(key='token string').user
###################################################



