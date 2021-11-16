from django.views.generic.edit import FormView
from .models import Subscriber
from .forms import SubscriberForm
from django.db.models.signals import post_save
from django.dispatch import receiver


class SubscribeFormView(FormView):
    template_name = 'appointment/make_appointment.html'
    form_class = SubscriberForm
    success_url = '/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        client_name = form.cleaned_data['client_name']
        client_email = form.cleaned_data['client_email']
        sub_category = form.cleaned_data['sub_category']

        subscribe = Subscriber(
            client_name=client_name,
            client_email=client_email,
            sub_category=sub_category,
        )
        subscribe.save()

        return super().form_valid(form)
