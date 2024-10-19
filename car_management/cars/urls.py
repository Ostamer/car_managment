from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, CommentViewSet, car_list_page, car_edit_page, car_create_page, car_detail_page,\
    RegisterView, custom_logout,CustomLoginView

router = DefaultRouter()
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('cars/<int:car_id>/comments/', CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('', car_list_page, name='car_list_page'),
    path('cars/<int:car_id>/', car_detail_page, name='car_detail_page'),
    path('cars/new/', car_create_page, name='car_create_page'),
    path('cars/<int:car_id>/edit/', car_edit_page, name='car_edit_page'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
]

urlpatterns += router.urls
