from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User 

from .models import Order,Customer

class CustomClearableFileInput(forms.ClearableFileInput):
    template_name = 'custom_widgets/custom_clearable_file_input.html'

class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user']
        widgets={
            'profile_pic':CustomClearableFileInput(),
        }


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields='__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']



