from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, unique=True, blank=False)
    password = models.CharField(max_length=255, blank=False)

    ROLE_CHOICES = (
        ("user", "user"),
        ("admin", "admin"),
    )
    role = models.CharField(max_length=24, choices=ROLE_CHOICES, blank=False, default="user")

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [name, email, password, role]

    def __str__(self):
        return self.username


class Plan(models.Model):
    start_date = models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    title = models.CharField(max_length=255, unique=True, blank=False)
    description = models.TextField(blank=False)
    price = models.IntegerField(blank=False)
    image = models.ImageField(upload_to='planImages', null=False)
    participants = models.ManyToManyField(User, through='PlanWithUserRegistration')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans_created')

    REQUIRED_FIELDS =[start_date, end_date, title, description, price, image]

    def __str__(self):
        return self.title


class PlanWithUserRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
