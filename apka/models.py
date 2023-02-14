from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(null=True,blank=True, upload_to='images/', default='images/car.png')

    def publish(self):
        self.publish_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #profile_image = models.ImageField(null=True, blank=True, upload_to='images/', default='images/car.png')
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    signup_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_profile_data_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
# Create your models here.

# class KeepSafeUserModel(AbstractBaseUser):
#     first_name = models.CharField(verbose_name='first_name',max_length=30,default="",unique=True)
#     last_name = models.CharField(verbose_name='last_name',max_length=30,default="")
#     email= models.TextField(verbose_name='email',max_length=60,unique=True,primary_key=True)
#     username = models.CharField(max_length=30,unique=True)
#     date_joined = models.DateTimeField(verbose_name="date joined",auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='last_login',auto_now=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.title
#
#
#     def clean_name(self):
#         data = self.cleaned_data.get('username')
#         existing = User.objects.filter(username=data).exists()
#
#         if existing:
#             raise ValidationError('username', "Name already in use")
#             print("działa")
#         return data