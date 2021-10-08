from django.contrib import admin
from .models import Product,Ratings,Rent_Amount,Issues,Photo,Bookings,Category,Subcategory


admin.site.register(Product)
admin.site.register(Rent_Amount)
admin.site.register(Ratings)
admin.site.register(Issues)
admin.site.register(Photo)
admin.site.register(Bookings)
admin.site.register(Category)
admin.site.register(Subcategory)



# Register your models here.
