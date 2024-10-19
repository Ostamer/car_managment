from django.contrib import admin
from .models import Car, Comment


#Админ панель для машины
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'owner', 'created_at', 'updated_at')
    list_filter = ('make', 'year', 'owner')
    search_fields = ('make', 'model', 'owner__username')


#Админ панель для комментариев
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('car', 'author', 'created_at')
    list_filter = ('car', 'author')
    search_fields = ('car__make', 'car__model', 'author__username')