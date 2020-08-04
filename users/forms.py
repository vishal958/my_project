from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, balance


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')


    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address already exists. Did you forget your password?")
       return self.cleaned_data
   
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class VirtualWalletForm(forms.ModelForm):
    username = forms.CharField(
        max_length=30, required=False, help_text='Please provide your friends username')
    amount = forms.IntegerField(help_text='Enter the amount you want to send')

    class Meta:
        model = balance
        fields = ['username', 'amount']
