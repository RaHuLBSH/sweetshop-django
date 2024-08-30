from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    contact_no = models.BigIntegerField()
    email_id = models.EmailField()
    address = models.TextField()
    pincode = models.IntegerField()
    money = models.IntegerField()
    rating = models.IntegerField()
    review = models.TextField()
    isadmin = models.BooleanField(default=False)

class Product(models.Model):
    p_name = models.CharField(max_length=50,unique=True)
    state = models.CharField(max_length=50)
    rate = models.IntegerField()
    img = models.ImageField(upload_to='pics')
    available = models.BooleanField(default=True)

class Orders(models.Model):
    username = models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',db_column='username')
    date1 = models.DateField()
    time1 = models.TimeField()
    order_list = ArrayField(models.CharField(max_length=20))
    quantities = ArrayField(models.IntegerField())
    price = models.IntegerField()
    status = models.CharField(max_length=20,choices=[('w','Ordered, on the way'),('d','Order Delivered'),('c','Order Cancelled')]) 

class Cart_Wishlist(models.Model):
    username = models.ForeignKey(User,on_delete=models.DO_NOTHING,to_field='username',db_column='username')
    p_id = models.ForeignKey(Product,on_delete=models.CASCADE,to_field='id',db_column='p_id')
    quantity = models.IntegerField()
    cw = models.CharField(max_length=10,choices=[('c','Cart'),('w','Wishlist')])

class Sentiment(models.Model):
    state = models.CharField(max_length=50)
    userreview = models.TextField()
    sentment = models.CharField(max_length=10,choices=[('p','Positive'),('n','Neutral'),('b','Negative')])