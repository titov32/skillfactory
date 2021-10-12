from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail, mail_managers
from datetime import datetime
from django.views.generic.edit import FormView

from .models import Subscriber
from .forms import SubscriberForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from news.models import Post

# создаём функцию обработчик с параметрами под регистрацию сигнала
@receiver(post_save, sender=Subscriber)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message='fdfdf',
    )

@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, created, **kwargs):
    list_email = []
    post = instance.postCategory.all()
    for cat in post:
        list1 = Subscriber.objects.filter(sub_category=cat)
        for mail in list1:
            list_email.append(mail.client_email)
        print('__________')

    print(set(list_email))
    recipient_list = []

    # for mail in recipient_list_qs:
    #     print(mail)

    # if created:
    #     subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    # else:
    #     subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'
    #
    # send_mail(
    #     subject=subject,
    #     message='Появилась новый пост в вашей категории',
    #     from_email='mail.email@yandex.ru',
    #     recipient_list=recipient_list,
    # )