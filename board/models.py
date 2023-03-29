import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
import random

from django.urls import reverse


class BoardUserActivateCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    valid_till = models.DateTimeField()

    @staticmethod
    def generate_code():
        return str(random.randrange(10000, 99999))

    def check_code(self, code):
        return self.code == code.strip()

    @classmethod
    def generate(cls, user):
        date = datetime.datetime.now() + datetime.timedelta(hours=1)
        obj = cls.objects.create(user=user, code=BoardUserActivateCode.generate_code(), valid_till=date)
        return obj.code

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Bulletin(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    body = RichTextUploadingField()
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bulletin_detail', kwargs={'pk': self.pk})

    def is_author(self, user):
        return self.author == user

    def can_edit(self, user):
        return self.is_author(user)

    def can_replay(self, user):
        return user.is_authenticated and not self.is_author(user)


class Replay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author}: {self.body[:50]}'

    def is_bulletin_author(self, user):
        return self.bulletin.is_author(user)

    def can_accept(self, user):
        return self.is_bulletin_author(user)

    def can_accept_decline(self, user):
        return self.can_accept(user) and not self.accepted

    def do_accept(self, user):
        if self.can_accept(user):
            if not self.accepted:
                self.accepted = True
                self.save()
            return True
        return False

    def do_decline(self, user):
        if self.can_accept_decline(user):
            self.delete()
            return True
        return False
