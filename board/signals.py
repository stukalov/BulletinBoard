import os

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import BoardUserActivateCode, Bulletin, Replay


@receiver(post_save, sender=BoardUserActivateCode)
def send_user_confirm_code(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        email = user.email
        html_content = render_to_string('activate_code_email.html', {
            'user': user,
            'code': instance.code,
        })
        msg = EmailMultiAlternatives(
            subject=f'Спасибо за регистрацию, {user.username}.',
            body=f'Пожалуйста введите этот код {instance.code} в форму на сайте для активации вашей учетной записи',
            from_email=os.environ['DEFAULT_FROM_EMAIL'],
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

@receiver(post_save, sender=User)
def user_activate(sender, instance, created, **kwargs):
    if not created and instance.is_active:
        BoardUserActivateCode.objects.filter(user=instance.pk).delete()


@receiver(post_save, sender=Replay)
def send_user_replay_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        bulletin = instance.bulletin
        author = bulletin.author
        email = author.email
        text_content = render_to_string('replay_email.txt', {
            'user': user,
            'author': author,
            'bulletin': bulletin,
            'replay': instance,
        })
        html_content = render_to_string('replay_email.html', {
            'user': user,
            'author': author,
            'bulletin': bulletin,
            'replay': instance,
        })
        msg = EmailMultiAlternatives(
            subject=f'Отклик на ваше объявление.',
            body=text_content,
            from_email=os.environ['DEFAULT_FROM_EMAIL'],
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

@receiver(post_save, sender=Replay)
def send_user_replay_accepted(sender, instance, created, **kwargs):
    if not created and instance.accepted:
        user = instance.user
        bulletin = instance.bulletin
        author = bulletin.author
        email = author.email
        text_content = render_to_string('replay_accepted_email.txt', {
            'user': user,
            'author': author,
            'bulletin': bulletin,
            'replay': instance,
        })
        html_content = render_to_string('replay_accepted_email.html', {
            'user': user,
            'author': author,
            'bulletin': bulletin,
            'replay': instance,
        })
        msg = EmailMultiAlternatives(
            subject=f'Ваш отклик на объявление принят.',
            body=text_content,
            from_email=os.environ['DEFAULT_FROM_EMAIL'],
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
