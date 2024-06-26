import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from loanBook.settings import AUTH_USER_MODEL as User_model
from django.utils.text import slugify

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Editeur'),
        (2, 'Lecteur'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)
    biography = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100,null=True, blank=True)
    total_book_download = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="avatar_user/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username


class Book(models.Model):
    CATEGORY_BOOK = (
        ('Romance', 'Romance'),
        ('Biography', 'Biography'),
        ('Autobiography', 'Autobiography'),
        ('Business', 'Business'),
        ('Finance', 'Finance'),
        ('Personal Development', 'Personal Development'),
        ('Science', 'Science'),
        ('Guide', 'Guide'),
        ('Cooking', 'Cooking'),
        ('Technology', 'Technology'),
        ('Philosophy', 'Philosophy'),
        ('Religion', 'Religion'),
        ('Spirituality', 'Spirituality'),
        ('Economics', 'Economics'),
        ('Entrepreneurship', 'Entrepreneurship'),
        ('Politics', 'Politics'),
        ('Environment', 'Environment'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True, blank=True, unique=True)
    summary = models.TextField(null=True, blank=True)
    year_publication = models.DateField(null=False, blank=False)
    category = models.CharField(max_length=200, choices=CATEGORY_BOOK)
    slug = models.SlugField(null=True, blank=True, unique=True)  # added slug field
    download_count = models.PositiveIntegerField(default=0)
    rating_sum = models.PositiveIntegerField(default=0)  # Somme totale des notes
    rating_count = models.PositiveIntegerField(default=0)  # Nombre total de votes
    user = models.ForeignKey(User_model, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Creation automatique du slug associé au livre 
    def save(self, *args, **kwargs):
        if not self.slug:  # Si un slug n'est pas déjà défini
            self.slug = slugify(self.title)  # Créer un slug à partir du titre
        super(Book, self).save(*args, **kwargs)  # Appeler la méthode save originale
        
    def __str__(self):
        return f"{self.slug}: {self.title}"
    
    @property
    def average_rating(self):
        if self.rating_count == 0:
            return 0
        return self.rating_sum / self.rating_count

class Rating(models.Model):
    book = models.ForeignKey(Book, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User_model, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()  # Vous pouvez limiter cela à un score maximal, par exemple 1-5

    class Meta:
        unique_together = (('user', 'book'),)  # S'assurer qu'un utilisateur ne peut noter qu'une seule fois un livre

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.pk:  # Vérifie que c'est une création de note et non une mise à jour
            book = self.book
            book.rating_sum += self.score
            book.rating_count += 1
            book.save()
    

class FavoriteBookUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User_model, on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.book.title} put favorite by {self.user.username}"
    
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='comments', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.book.title}'

class BookVersion(models.Model):
    BOOK_TYPES = (
        ('pdf', 'PDF'),
        ('audio', 'Audio'),
        ('ebook', 'E-book'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(Book, related_name='versions', on_delete=models.CASCADE)
    book_type = models.CharField(max_length=10, choices=BOOK_TYPES)
    language = models.CharField(max_length=30)
    file = models.FileField(upload_to='book_versions/')
    picture_file = models.FileField(upload_to='book_versions/covers/')
    number_pages = models.PositiveIntegerField(default=0, blank=True, null=True)
    time_read_book = models.PositiveIntegerField(default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (('book', 'book_type', 'language'),)  


    def __str__(self):
        return f"{self.book.title} - {self.language} ({self.book_type})"

    
    
    