from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import truncatechars


# Create your models here.
STATE_CHOICES = (
    ('Andaman & Nicobar Islands' , 'Andaman & Nicobar Islands'),
    ('Andhra Pradesh' , 'Andhra Pradesh'),
    ('Arunachal Pradesh' , 'Arunachal Pradesh'),
    ('Assam' , 'Assam'),
    ('Bihar' , 'Bihar'),
    ('Chandigarh' , 'Chandigarh'),
    ('Chhattisgarh' , 'Chhattisgarh'),
    ('Dadar & Nagar Haveli' , 'Dadar & Nagar Haveli'),
    ('Daman and Diu' , 'Daman and Diu'),
    ('Delhi' , 'Delhi'),
    ('Goa' , 'Goa'),
    ('Gujarat' , 'Gujarat'),
    ('Haryana' , 'Haryana'),
    ('Himachal Pradesh' , 'Himachal Pradesh'),
    ('Jammu & Kashmir' , 'Jammu & Kashmir'),
    ('Jharkhand' , 'Jharkhand'),
    ('karnataka' , 'karnataka'),
    ('Kerala' , 'Kerala'),
    ('Lakshadweep' , 'Lakshadweep'),
    ('Madhya Pradesh' , 'Madhya Pradesh'),
    ('Maharashtra' , 'Maharashtra'),
    ('Manipur' , 'Manipur'),
    ('Meghalaya' , 'Meghalaya'),
    ('Mizoram' , 'Mizoram'),
    ('Nagaland' , 'Nagaland'),
    ('Odisha' , 'Odisha'),
    ('Puducherry' , 'Puducherry'),
    ('Punjab' , 'Punjab'),
    ('Rajasthan' , 'Rajasthan'),
    ('Sikkim' , 'Sikkim'),
    ('Tamil Nadu' , 'Tamil Nadu'),
    ('Telangana' , 'Telangana'),
    ('Tripura' , 'Tripura'),
    ('Uttarakhand' , 'Uttarakhand'),
    ('Uttar Pradesh' , 'Uttar Pradesh'),
    ('West Bengal' , 'West Bengal'),
)
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    address = models.CharField(max_length=200, default="")
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50, default="")

    def __str__(self):
        return str(self.id)

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField(default="")
    brand = models.CharField(max_length=100)
    category = models.CharField( max_length=100)
    sub_category = models.CharField( max_length=100, default='')
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

    @property
    def titleshort(self):
        return truncatechars(self.title, 15)
    
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def cost(self):
        return self.quantity*self.product.discounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Canceled', 'Canceled'),
)
class OrderPlaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices= STATUS_CHOICES, default='Pending')

    @property
    def cost(self):
        return self.quantity*self.product.discounted_price

class CustomerService(models.Model):
    user=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    query=models.CharField(max_length=50)
    detail=models.TextField(max_length=50)

class Like(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    status=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

DISCOUNT_TYPE = (
    ('Rupees', 'Rupees'),
    ('%', '%'),
)

class Coupon(models.Model):
    name=models.CharField(max_length=20)
    discount = models.IntegerField(default=0)
    discount_type = models.CharField(max_length=20, choices= DISCOUNT_TYPE, default="")