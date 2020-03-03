from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from comments.models import Comments
from comments.serializers import CommentsSerializer

class CommentsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Comments.objects.all().order_by("-publish")
    serializer_class = CommentsSerializer
