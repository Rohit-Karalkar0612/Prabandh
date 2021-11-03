from django import forms
from .models import Profile,Seller
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class RegisterForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model=Profile
        fields=('bank_acc_no','ifsc','address','seller','captcha')
        widgets={
            'bank_acc_no': forms.NumberInput(attrs={'class':'form-control textinput'}),
            'ifsc': forms.TextInput(attrs={'class':'form-control textinput'}),
            'address': forms.Textarea(attrs={'class':'form-control textinput textareaclass','rows':'3'}),
            'seller':forms.CheckboxInput(attrs={'class':'form-check-input','onclick':'changeText()'}),
            'captcha':forms.TextInput(attrs={'class':'form-control'})
        }
    
class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control textinput', 'type':'password', 'align':'center',}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control textinput', 'type':'password', 'align':'center',}),
    )

    class Meta:
        model=User
        # forms.EmailField(, required=False)
        fields=('username','email')
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control textinput','onfocus':'move()','autocomplete':'off'}),
            'email': forms.TextInput(attrs={'class':'form-control textinput','type':'email','onclick':'move()'}),
        }

class SellerForm(forms.ModelForm):
    class Meta:
        model=Seller
        exclude=('seller',)
        widgets={
            'name_of_business':forms.TextInput(attrs={'class':'form-control textinput'}),
            'gst_no':forms.TextInput(attrs={'class':'form-control textinput'}),
            'mobile_no':forms.NumberInput(attrs={'class':'form-control textinput'}),
            'city':forms.TextInput(attrs={'class':'form-control textinput'}),
            'PAN':forms.TextInput(attrs={'class':'form-control textinput'}),
        }
    