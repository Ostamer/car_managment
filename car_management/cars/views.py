from rest_framework import viewsets, permissions
from .models import Car, Comment
from .serializers import CarSerializer, CommentSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CarForm, CommentForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


#Api для машины
class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Устанавливаем owner в текущего аутентифицированного пользователя
        serializer.save(owner=self.request.user)


#Api для комментариев
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        car_id = self.kwargs['car_id']  # Получаем car_id из URL
        return Comment.objects.filter(car_id=car_id)  # Фильтруем комментарии по car_id

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
                'make': form.cleaned_data['make'],
                'model': form.cleaned_data['model'],
                'year': form.cleaned_data['year'],
                'description': form.cleaned_data['description']
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


class UserCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def custom_logout(request):
    logout(request)
    return redirect('car_list_page')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('car_list_page')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('car_list_page')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
