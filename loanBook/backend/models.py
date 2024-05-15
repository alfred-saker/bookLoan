import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Book(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True, unique=True)
    year_publication = models.DateField(null=False, blank=False)
    date_online = models.DateField(auto_now_add=True)
    number_dowload = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=200)
    status_book = models.BooleanField(default=False)
    type_book = models.CharField(max_length=200, default="Numeric")
    
    pdf_file = models.FileField(upload_to='pdf_books/', null=True, blank=True)
    
    picture_books = models.FileField(upload_to='picture_books/')
    
    def __str__(self):
        return self.title or "sans titre"
    
    #asus2024

class Borrow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    books = models.ForeignKey(Book, on_delete=models.CASCADE, default="9dfdd4c2-0247-48b0-8450-fb6d726ed545")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField(default=timezone.now)
    return_date = models.DateField(default=timezone.now)

    
    
    