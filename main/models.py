from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_delete
import os



class Account(AbstractUser):
    image = models.ImageField(upload_to = 'accounts/', null=True, blank=True)
    favourite_books = models.ManyToManyField(
        "Book", related_name="liked_accounts", blank=True
    )
    
    def __str__(self):
        return self.username


class Book(models.Model):
    name = models.CharField(max_length = 255)
    details = models.TextField(null=True, blank=True)
    price = models.FloatField(validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    cover = models.CharField(max_length = 50, null=True, blank=True)
    sold = models.BooleanField(default=False)
    

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='books'
    )

    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to='books/')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE,
        related_name="images"
    )

    def __str__(self):
        return self.book.name
@receiver(post_delete, sender=Image)
def delete_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(post_delete, sender=Account)
def delete_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            
