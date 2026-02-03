from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class user(AbstractUser):
    mobile = models.CharField(max_length=11,verbose_name='تلفن همراه')
    address = models.CharField(max_length=500,null=True,verbose_name='آدرس')
    avatar = models.ImageField(upload_to='account',default='media/account/03.jpg',verbose_name='آواتار')

    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربران'

    def __str__(self):
        return self.get_full_name()


