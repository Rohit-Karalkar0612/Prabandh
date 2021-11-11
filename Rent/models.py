from django.db import models
from User.models import Seller
from django.contrib.auth.models import User

# Create your models here.

class Subcategory(models.Model):
    subcategories = models.CharField(max_length=50)
    Categories = models.ForeignKey("Category",on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategories


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category
        
class Product(models.Model):

    seller_of_item=models.ForeignKey(Seller,related_name='seller_of_item', on_delete=models.CASCADE)
    availability=models.BooleanField(default=True)
    title=models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    subcategory=models.ForeignKey(Subcategory,on_delete=models.SET_NULL, blank=True, null=True)
    rental_price=models.IntegerField()
    about=models.TextField()
    deposit=models.IntegerField()
    image_of_product=models.ImageField(upload_to='title_photos')

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

class Rent_Amount (models.Model):
    customer_of_item=models.ForeignKey(User,related_name='customer_of_item',on_delete=models.CASCADE)
    delivered_date=models.DateField()
    sent_date=models.DateField()
    related_product=models.OneToOneField(Product,related_name='rented_product',on_delete=models.CASCADE)
    payment=models.IntegerField()
    satisfaction=models.BooleanField(default=True)
    expected=models.DateField()

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

class Issues(models.Model):
    complainer=models.ForeignKey(User,related_name='complainer',on_delete=models.CASCADE)
    complain_against=models.ForeignKey(Product,related_name='complain_against',on_delete=models.CASCADE)
    issue=models.TextField()
    resolved=models.BooleanField(default=False)

class Photo (models.Model):
    photo=models.ImageField(upload_to='product_photos')
    product_photo=models.ForeignKey(Product, related_name='product_name', on_delete=models.CASCADE)


class Ratings(models.Model):
    rating_for_product=models.ForeignKey(Product, related_name='rating_for_product', on_delete=models.CASCADE)
    rating_by=models.ForeignKey(User, related_name='rating_by', on_delete=models.CASCADE)
    rating=models.FloatField()
    review=models.TextField()

class Bookings(models.Model):
    booking=models.OneToOneField(Product,on_delete=models.CASCADE)
    customer_who_booked=models.OneToOneField(User, on_delete=models.CASCADE)
    start_time=models.DateField()
    end_time=models.DateField()
    confirmation=models.BooleanField()

class Cart(models.Model):
    user=models.ForeignKey(User,related_name='user', on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,related_name='product_id', on_delete=models.CASCADE)
    def _str_(self):
        return self.product_id