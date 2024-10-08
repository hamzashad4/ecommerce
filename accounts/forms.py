from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField(required=True)
    phone_no = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email','phone_no', 'password1', 'password2']

