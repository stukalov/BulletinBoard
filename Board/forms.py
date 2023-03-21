from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BoardUser, BoardUserActivateCode


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, label='e-mail', help_text='Обязательное поле')
    subscribe = forms.BooleanField(label='Подписаться на рассылку новостей', required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'subscribe'
        )

    def save(self):
        user = super().save(False)
        user.email = self.cleaned_data["email"]
        user.is_active = False
        user.save()
        BoardUser.objects.create(user=user, subscribe=self.cleaned_data["subscribe"])
        BoardUserActivateCode.generate(user)
        return user


class CodeConfirmForm(forms.Form):
    code = forms.CharField(label='Код подтверждения', help_text='Введите код подтверждения, полученный на e-mail')

