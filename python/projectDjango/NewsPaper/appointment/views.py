from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail
from datetime import datetime

from .models import Subscriber
from .forms import SubscriberForm


class SubscriberView(View):
    form_class = SubscriberForm

    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        subscribe = Subscriber(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        Subscriber.save()

        # отправляем письмо
        send_mail(
            subject=f'{subscribe.client_name} {subscribe.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=f'{subscribe.sub_category.title}',  # сообщение с кратким описанием проблемы
            from_email='email.infomail@yandex.ru',
            # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=['titov32@gmail.com']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )

        return redirect('appointment:make_appointment')
