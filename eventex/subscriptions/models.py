from django.db import models

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    cpf = models.CharField(max_length=12)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    created_at = models.DateField(auto_now_add=True)