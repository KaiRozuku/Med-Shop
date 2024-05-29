from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Drug(models.Model):
    name = models.CharField(max_length=70)
    developer = models.CharField(max_length=70)
    appointment = models.CharField(max_length=70)
    measurement = models.CharField(max_length=20)
    image = models.ImageField()
    price = models.FloatField(default=0.0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    about_product = models.TextField(blank=True)
    indication = models.TextField(blank=True)
    contraindication = models.TextField(blank=True)
    dose = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('drug', kwargs={'drug_id': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Кошик для {self.user.name} | Препарат {self.drug.name}"

    @property
    def sum(self):
        return self.quantity * self.drug.price


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='main/', default='main/149071.png')

    def __str__(self):
        return self.user.username