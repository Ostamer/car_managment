from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics


class UserCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

