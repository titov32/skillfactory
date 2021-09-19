from allauth.socialaccount.forms import SignupForm
from django.contrib.auth.models import Group

class MyCustomSocialSignupForm(SignupForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSocialSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        print('!!!!!!!!!!!!!!!!!!')
        print(user)
        print(self)
        print(request)
        # Add your own processing here.

        # You must return the original result.
        return user