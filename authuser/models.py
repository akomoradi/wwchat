from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class User(AbstractUser):
    username = models.CharField(null=True ,max_length=60 )
    email = models.EmailField( unique=True , null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6 , null=True, blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    def create_user(username, password):
        IsUser = User()
        user = User.objects.create_user(username=username, password=password)

    # بررسی تعداد کاربران موجود در سیستم
        user_count = User.objects.count()

    # تعداد کاربران مورد نظر برای ایجاد گروه جدید
        threshold = 70

        if user_count % threshold == 0:
        # ایجاد گروه جدید
            group_name = f'Group {user_count // threshold + 1}'
            group = Group.objects.create(name=group_name)

        # انتقال کاربر به گروه جدید
            group.user_set.add(user)

        return user


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_images")

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)


class assets (models.Model):
    assets1= models.IntegerField(max_lenght=1000000,  null= True , default= 0 ,  )
    assets2= models.IntegerField(max_lenght=1000000,  null= True , default= 0 ,  )
    assets3= models.IntegerField(max_lenght=1000000,  null= True , default= 0 ,  )
    assets4= models.IntegerField(max_lenght=1000000,  null= True , default= 0 ,  )

