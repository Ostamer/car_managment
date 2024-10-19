from django.db import models
from django.contrib.auth.models import User


#Модель машины
class Car(models.Model):
    make = models.CharField(max_length=16)
    model = models.CharField(max_length=32)
    year = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


#Модель комментария
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    car = models.ForeignKey(Car, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Комментарий от {self.author} на машину {self.car}"
