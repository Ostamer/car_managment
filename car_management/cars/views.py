from rest_framework import viewsets, permissions
from .models import Car, Comment
from .serializers import CarSerializer, CommentSerializer,RegisterSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CarForm, CommentForm, RegisterForm
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status


#Представление для регистрации
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Token.objects.get_or_create(user=user)
            login(request, user)
            return redirect('car_list_page')
        return render(request, 'registration/register.html', {'form': serializer.errors})


# @csrf_exempt
#Представление для выхода
def custom_logout(request):
    logout(request)
    return redirect('car_list_page')


# @csrf_exempt
# Представление для входа
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        user = form.get_user()
        token, created = Token.objects.get_or_create(user=user)
        login(self.request, user)
        self.request.session['auth_token'] = token.key

        # Проверяем, является ли запрос AJAX или API
        if self.request.is_ajax() or self.request.content_type == 'application/json':
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        # Возвращаем стандартный ответ для формы
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('car_list_page')


#Api для машины
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()


#Api для комментариев
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        car_id = self.kwargs['car_id']
        serializer.save(author=self.request.user, car_id=car_id)

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()



# Список автомобилей
def car_list_page(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_list.html', {'cars': cars})



# Информация об автомобиле и комментариях к нему
def car_detail_page(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    comments = car.comments.all()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                content=form.cleaned_data['content'],
                car=car,
                author=request.user
            )
            return redirect('car_detail_page', car_id=car_id)
    else:
        form = CommentForm()

    return render(request, 'cars/car_detail.html', {'car': car, 'comments': comments, 'form': form})




@login_required
def car_create_page(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car_data = {
                'Производитель': form.cleaned_data['make'],
                'Модель': form.cleaned_data['model'],
                'Год выпуска': form.cleaned_data['year'],
                'Описание': form.cleaned_data['description']
            }
            # Убираем токен, сохраняем автомобиль напрямую
            Car.objects.create(**car_data, owner=request.user)
            return redirect('car_list_page')
    else:
        form = CarForm()

    return render(request, 'cars/car_form.html', {'form': form})


# Редактирование и удаление автомобиля
@login_required
def car_edit_page(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if car.owner != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        if 'edit' in request.POST:
            form = CarForm(request.POST, instance=car)
            if form.is_valid():
                form.save()
                return redirect('car_detail_page', car_id=car_id)
        elif 'delete' in request.POST:
            car.delete()
            return redirect('car_list_page')
    else:
        form = CarForm(instance=car)

    return render(request, 'cars/car_edit_form.html', {'form': form, 'car': car})
