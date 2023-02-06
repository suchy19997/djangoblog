from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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



class Profile_data(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name= models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def update_profile_data_signal(sender, instance, created, **kwargs):
        if created:
            Profile_data.objects.create(user=instance)
        instance.profile.save()
# Create your models here.
