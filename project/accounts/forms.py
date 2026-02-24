from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm 
from .models import Account, Plan, AccountCustomers, AccountFilters, AccountCustomerPreferries

class AccountCreationForm(UserCreationForm):
    terms_accepted = forms.BooleanField(label='Terms and Conditions', required=True)

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = UserCreationForm.Meta.fields + ('email','terms_accepted')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder':'İstifadəçi adı'})
        self.fields['email'].widget.attrs.update({'class': 'form-control','placeholder':'E-mail'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control','placeholder':'Şifrə'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control','placeholder':'Şifrəni təkrar yazın'})


class VerifyRegisterOtpForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        required=True,
        label="OTP kodu",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXXXXX'
        })
    )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder':'İstifadəçi adı'})
        self.fields['password'].widget.attrs.update({'class': 'form-control','placeholder':'Şifrə'})
        
        

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control','placeholder':'E-mail'})
        
        
class VerifyForgotPasswordOtpForm(forms.Form):
    otp = forms.CharField(max_length=6)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['otp'].widget.attrs.update({'class': 'form-control','placeholder':'OTP kodu'})
        
        

class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control','placeholder':'Yeni şifrə'})
        self.fields['confirm_password'].widget.attrs.update({'class': 'form-control','placeholder':'Yeni şifrəni təkrar yazın'})