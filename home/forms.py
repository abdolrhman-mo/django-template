from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ShippingAddress

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AddressForm(forms.Form):
    governerate =  forms.CharField()
    city =  forms.CharField()
    address =  forms.CharField()
    landmark =  forms.CharField()
    notes =  forms.CharField()
    delivery_instruction = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=ShippingAddress.CHOICES
    )