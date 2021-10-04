from django.forms import ModelForm, TextInput, Textarea, Select, EmailInput, DateInput
from .models import Subscriber


# Создаём модельную форму
class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber
        fields = ['client_email', 'client_email', 'sub_category', 'date']
        widgets = {
            'client_email': EmailInput(attrs={
                'class': 'form-control'
            }),
            'sub_category': Select(attrs={
                'class': 'form-control'
            }),
            'date': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'заголовок статьи'
            }),
        }