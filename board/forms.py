import datetime

from ckeditor.fields import RichTextFormField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingFormField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BoardUserActivateCode, Category, Bulletin, Replay


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    def save(self):
        user = super().save(False)
        user.is_active = False
        user.save()
        BoardUserActivateCode.generate(user)
        return user

    def clean_username(self):
        username = self.cleaned_data['username']
        # Удаляем пользователя из базы если срок активации у него уже истек
        User.objects.filter(
            username=username,
            boarduseractivatecode__valid_till__lt=datetime.datetime.now(),
        ).delete()
        return username


class CodeConfirmForm(forms.Form):
    code = forms.CharField(label='Код подтверждения', help_text='Введите код подтверждения, полученный на e-mail')


class BulletinForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок')
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория:',
    )
    body = RichTextUploadingFormField(
        label='Содержание объявления'
    )

    class Meta:
        model = Bulletin
        fields = [
            'title',
            'category',
            'body',
        ]


class ReplayForm(forms.ModelForm):
    body = forms.CharField(
        label='Здесь вы можете оставить отзыв на объявление',
        widget=forms.Textarea
    )

    class Meta:
        model = Replay
        fields = [
            'body',
        ]

