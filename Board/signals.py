import os

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import BoardUserActivateCode


@receiver(post_save, sender=BoardUserActivateCode)
def send_user_confirm_code(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        email = user.email
        html_content = render_to_string('activate_code_email.html', {
            'user': user,
            'code': instance.code,
            'domain': os.environ.get("HOST", default="http://localhost:8000/")
        })
        msg = EmailMultiAlternatives(
                subject=f'Спасибо за регистрацию, {user.username}.',
                body=f'Пожалуйста введите этот код {instance.code} в форму на сайте для активации вашей учетной записи',
                from_email=os.environ['DEFAULT_FROM_EMAIL'],
                to=[email],
            )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

