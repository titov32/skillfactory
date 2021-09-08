from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from allauth.account.forms import LoginForm


class CustomLoginForm(LoginForm):

    def login(self, *args, **kwargs):

        # Add your own processing here.
        print('Print login')
        print('self:', self)
        print(type(self))
        user=self.user
        print(user)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        # You must return the original result.
        return super(CustomLoginForm, self).login(*args, **kwargs)


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        print(user)
        return user
