from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.utils.timezone import now

class AuctionUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class AuctionUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AuctionUserManager()

class Area(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Lot(models.Model):
    number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    description = models.TextField()
    area = models.ManyToManyField(Area, blank=True)
    price = models.PositiveIntegerField()
    step_value = models.PositiveIntegerField()
    status = models.CharField(max_length=30, choices=[
        ('open', 'open'),
        ('closed', 'closed'),
        ('cancelled', 'cancelled'),
        ('blocked', 'blocked')
    ])
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.number

class Participant(models.Model):
    number = models.PositiveSmallIntegerField() #нумерация отдельно, а не по id
    user_id = models.ForeignKey(AuctionUser, on_delete=models.CASCADE)
    lot_id = models.ForeignKey(Lot, on_delete=models.CASCADE)
    # date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class Bid(models.Model):
    lot_id = models.ForeignKey(Lot, on_delete=models.CASCADE)
    part_number = models.ForeignKey(Participant, on_delete=models.CASCADE)
    step_number = models.PositiveSmallIntegerField()
    total_price = models.PositiveIntegerField(null=True, blank=True)

