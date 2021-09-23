from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        exclude=('Product',)
