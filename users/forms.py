from django import forms
from django.contrib.auth.forms import UserSignupForm
from django.contrib.auth.models import User
from .models import User as AbstractUser


class AbstractUserSignupForm(UserSignupForm):
    first_name = forms.CharField(label='Name')

    class Meta(UserSignupForm.Meta):
        model = AbstractUser
        fields = ['first_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input'})
