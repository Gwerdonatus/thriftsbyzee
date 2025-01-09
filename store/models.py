from django.db import models
from cloudinary.models import CloudinaryField  # Import CloudinaryField

# Create your models here.

class Dress(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField('image')  # Use CloudinaryField for images
    video = models.URLField(blank=True, null=True)  
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)  # In stock or out of stock
    size = models.CharField(max_length=10)  # Example: S, M, L, XL

    def __str__(self):
        return self.name
