from django.contrib import admin
from backend.models import Book,CustomUser,BookVersion, Rating, FavoriteBookUser,Comment

admin.site.register(Book)
admin.site.register(BookVersion)
admin.site.register(CustomUser)
admin.site.register(Rating)
admin.site.register(FavoriteBookUser)
admin.site.register(Comment)

