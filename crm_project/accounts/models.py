from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile1.jpg", null=True, blank=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        try:
            # Get the existing instance from the database
            this = Customer.objects.get(id=self.id)
            if this.profile_pic != self.profile_pic:
                # Ensure the file is not being used and then delete it
                this.profile_pic.delete(save=False)
        except Customer.DoesNotExist:
            pass  # This means it's a new instance, so no file to delete
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name or ''


class Tag(models.Model):
    name = models.CharField(max_length=200,null=True)
  
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY=(
        ('Indoor','Indoor'),
        ('Out Door','Out Door'),
    )
    name =models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    description=models.CharField(max_length=200,null=True,blank=True)
    date_created=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(Tag)

    
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Out of Delivery','Out of Delivery'),
        ('Delivered','Delivered'),
    )
    date_created=models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=200,null=True,choices=STATUS)
    product=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    
