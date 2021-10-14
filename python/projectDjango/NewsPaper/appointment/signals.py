from django.core.mail import mail_managers
from django.template.loader import render_to_string
from .models import Subscriber
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from news.models import Post
from django.core.mail import EmailMultiAlternatives
import datetime
from django.shortcuts import redirect

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


def notify_users_appointment(sender, instance, **kwargs):
    list_email = []
    categories = instance.postCategory.all()
    text = instance.text[:50]
    title = instance.title
    for cat in categories:
        list1 = Subscriber.objects.filter(sub_category=cat)
        for mail in list1:
            list_email.append(mail.client_email)
    recipient_list = list(set(list_email))

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
        from_email='email.infomail@yandex.ru',
        to=recipient_list,  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем

# коннект фунции со связими мани_ту_мани
m2m_changed.connect(notify_users_appointment, sender=Post.postCategory.through)

@receiver(pre_save, sender=Post)
def restrict_new_post(sender, instance, **kwargs):
    author = instance.created_by
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    count_posts = Post.objects.filter(created_by=author, timeCreation__range=(today_min, today_max)).count()
    print('kol-vo postov',count_posts)
    if count_posts > 1:
        return redirect('/')
