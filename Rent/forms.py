from django import forms
from .models import Product,Category,Subcategory,Photo
from django.contrib.auth.forms import UserCreationForm
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        exclude=('seller_of_item','availability')
        widgets={
        'title': forms.TextInput(attrs={'placeholder': 'Enter Product Title'}),
        'about': forms.Textarea(
            attrs={'placeholder': 'Enter description here'}),
       'Category' : forms.Select(attrs={'placeholder': 'Select Category'}),
        'rental_price': forms.NumberInput(
            attrs={'placeholder': 'Enter rent price(per day)'}),
        'deposit': forms.NumberInput(
            attrs={'placeholder': 'Enter deposit here(should be greater than rent price)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(Categories_id=category_id).order_by('subcategories')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty subcategory queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.category_self.order_by('subcategories')


class PhotoForm(forms.ModelForm):
    
    class Meta:
        model = Photo
        exclude=('product_photo',)