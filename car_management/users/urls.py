from django.urls import path
from .views import UserCreate
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token),
    path('', UserCreate.as_view()),
]