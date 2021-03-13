from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import json


class Profile(models.Model):
    user_id = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, default="anonymous")
    phone = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(
        null=True, blank=True, default="default-profile.png")
    hobby = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


# class CreateUser(models.Model):
#     pass

    # def __str__(self):
    #     return str(self.discuss)


class ListCategory(models.Model):
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class ListForum(models.Model):
    user_id = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    topic = models.CharField(max_length=300)
    category = models.ForeignKey(
        ListCategory, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    num_comment = models.IntegerField(blank=True, null=True, default=0)
    num_like = models.IntegerField(blank=True, null=True, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    user_like = models.IntegerField(blank=True, null=True, default=0)
    like_user = models.CharField(
        max_length=200, blank=True, null=True, default='[]')

    def __str__(self):
        return str(self.topic)


class ForumDiscussion(models.Model):
    user_id = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    forum_id = models.ForeignKey(
        ListForum, blank=True, null=True, on_delete=models.CASCADE)
    discuss = models.CharField(max_length=1000)
    like = models.IntegerField(blank=True, null=True, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return str(self.discuss)


class ListEvent(models.Model):
    user_id = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    penyelenggara = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        ListCategory, null=True, blank=True, on_delete=models.SET_NULL)
    tempat = models.CharField(max_length=100)
    alamat = models.CharField(max_length=500)
    image = models.ImageField(null=True, blank=True,
                              default="default-profile.png", upload_to='images/')
    description = models.TextField(blank=True)
    kuota = models.IntegerField(blank=True, null=True)
    num_hadir = models.IntegerField(blank=True, null=True, default=0)
    num_comment = models.IntegerField(blank=True, null=True, default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    contact_hp = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.CharField(max_length=50, blank=True, null=True)
    contact_website = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    hadir = models.CharField(
        max_length=200, blank=True, null=True, default='[]')

    def __str__(self):
        return str(self.name)

    def set_hadir(self, x):
        self.hadir = json.dumps(x)

    def get_hadir(self):
        return json.loads(str(self.hadir))


class HadirEvent(models.Model):
    event_id = models.ForeignKey(
        ListEvent, null=True, blank=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
