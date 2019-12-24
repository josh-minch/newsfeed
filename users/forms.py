from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = 'Confirm password'

        self.fields['username'].help_text = 'Alphanumeric and @ / . / + / - / _ only.'
        self.fields['password2'].help_text = 'Just to be sure.'

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
