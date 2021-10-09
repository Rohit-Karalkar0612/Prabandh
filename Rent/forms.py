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
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(Categories_id=category_id).order_by('subcategories')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty subcategory queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.category_self.order_by('subcategories')