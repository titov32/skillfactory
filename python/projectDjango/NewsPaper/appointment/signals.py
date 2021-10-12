from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail, mail_managers
from datetime import datetime
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from .models import Subscriber
from .forms import SubscriberForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from news.models import Post
from django.core.mail import EmailMultiAlternatives


# создаём функцию обработчик с параметрами под регистрацию сигнала
@receiver(post_save, sender=Subscriber)
def notify_managers_appointment(sender, instance, created, **kwargs):
    if created:
        subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
    else:
        subject = f'Appointment changed for {instance.client_name} {instance.date.strftime("%d %m %Y")}'

    mail_managers(
        subject=subject,
        message=f'Вы подписаны на {instance.sub_category}',
    )

@receiver(post_save, sender=Post)
def notify_managers_appointment(sender, instance, **kwargs):

    list_email = []
    categories = instance.postCategory.all()
    print('categories',categories)
    text = instance.text[:50]
    title = instance.title
    for cat in categories:
        print('cat',cat)
        list1 = Subscriber.objects.filter(sub_category=cat)
        for mail in list1:
            list_email.append(mail.client_email)
    recipient_list = list(set(list_email))
    print('Печать списка email', recipient_list)


    html_content = render_to_string(
        'appointment_created.html',
        {
            'text': text,
            'title': title,

        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Новый пост в подписке',
        body=text,  # это то же, что и message
        from_email= 'email.infomail@yandex.ru',
        to= recipient_list,  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()  # отсылаем