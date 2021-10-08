from django import forms
from .models import Product,Category,Subcategory
from django.contrib.auth.forms import UserCreationForm
class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        exclude=('seller_of_item','availability')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()
        if 'category' in self.data:
            try:
                country_id = int(self.data.get(''))
                self.fields['subcategories'].queryset = Category.objects.filter(country_id=country_id).order_by('category')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategories'].queryset = self.instance.country.city_set.order_by('category')