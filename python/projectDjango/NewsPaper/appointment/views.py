from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail, mail_managers
from datetime import datetime
from django.views.generic.edit import FormView

from .models import Subscriber
from .forms import SubscriberForm
from django.db.models.signals import post_save
from django.dispatch import receiver




class SubscribeFormView(FormView):
    template_name = 'make_appointment.html'
    form_class = SubscriberForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        client_name = form.cleaned_data['client_name']
        client_email = form.cleaned_data['client_email']
        sub_category = form.cleaned_data['sub_category']

        subscribe = Subscriber(
            client_name=client_name,
            client_email=client_email,
            sub_category=sub_category,
        )
        subscribe.save()
        print(client_name, client_email, sub_category)

        send_mail(
            subject=f'{client_name} оформлена подписка ',
            # имя клиента и дата записи будут в теме для удобства
            message=f'Вы подписаны на {sub_category}',  # сообщение с кратким описанием проблемы
            from_email='email.infomail@yandex.ru',
            # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=[client_email]  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        return super().form_valid(form)


