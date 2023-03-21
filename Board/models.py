from django.db import models
from django.contrib.auth.models import User
import random


class BoardUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribe = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class BoardUserActivateCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)

    @staticmethod
    def generate_code():
        return str(random.randrange(10000, 99999))

    @classmethod
    def generate(cls, user):
        obj = cls.objects.create(user=user, code=BoardUserActivateCode.generate_code())
        return obj.code

    def __str__(self):
        return self.user.username

