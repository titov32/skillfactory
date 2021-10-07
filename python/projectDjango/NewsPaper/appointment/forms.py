from django.forms import ModelForm, Select, EmailInput, DateInput, TextInput, DateField

from .models import Subscriber


# Создаём модельную форму
class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ['client_email', 'client_name', 'sub_category']
        widgets = {

            'client_email': EmailInput(attrs={
                'class': 'form-control'
            }),
            'client_name': TextInput(attrs={
                'class': 'form-control'
            }),
            'sub_category': Select(attrs={
                'class': 'form-control'
            }),

        }