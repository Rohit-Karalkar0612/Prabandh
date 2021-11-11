from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinLengthValidator
# Create your models here.
class Profile(models.Model):

    user=models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    bank_acc_no=models.CharField(max_length=16,validators=[MinLengthValidator(16)])
    ifsc=models.CharField(max_length=11,validators=[MinLengthValidator(11)])
    address=models.TextField()
    seller=models.BooleanField(default=False)
    

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

class Seller (models.Model):
    seller=models.OneToOneField(User,on_delete=models.CASCADE)
    name_of_business=models.CharField(max_length=50)
    gst_no=models.CharField(max_length=15,validators=[MinLengthValidator(15)])
    mobile_no=models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    city=models.CharField(max_length=15)
    PAN=models.CharField(max_length=10,validators=[MinLengthValidator(10)])
    

    def __str__(self):
        return self.seller.username

    # def get_absolute_url(self):
    #     return reverse("_detail", kwargs={"pk": self.pk})

