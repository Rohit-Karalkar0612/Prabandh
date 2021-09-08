from django import forms
from .models import Profile,Seller
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('bank_acc_no','ifsc','address')
        widgets={
            'bank_acc_no': forms.NumberInput(attrs={'class':'form-control'}),
            'ifsc': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control'}),
        }
    
class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center', 'placeholder':'password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center', 'placeholder':'password'}),
    )

    class Meta:
        model=User
        # forms.EmailField(, required=False)
        fields=('username','email')
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control','type':'email'}),
        }

class SellerForm(forms.ModelForm):
    class Meta:
        model=Seller
        exclude=('seller',)
    