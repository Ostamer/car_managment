from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, CommentViewSet, car_list_page, car_edit_page, car_create_page, car_detail_page\
    ,UserCreate, custom_logout, login_view, register_view
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('cars/<int:car_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('', car_list_page, name='car_list_page'),
    path('cars-info/<int:car_id>/', car_detail_page, name='car_detail_page'),
    path('cars/new/', car_create_page, name='car_create_page'),
    path('cars/<int:car_id>/edit/', car_edit_page, name='car_edit_page'),
    path('logout/', custom_logout, name='logout'),
    path('register/', UserCreate.as_view()),
    path('login/', obtain_auth_token),
    path('app-login/', login_view, name='login'),
    path('app-register/', register_view, name='register'),
]

urlpatterns += router.urls
