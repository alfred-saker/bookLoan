from django.contrib import admin
from backend.models import Book,CustomUser,BookVersion, Rating, FavoriteBookUser,Comment

from django.utils.translation import gettext_lazy as _

# Customize title admin page
admin.site.site_header = _("BookLoan Admin ")
admin.site.site_title = _("BookLoan Admin")
admin.site.index_title = _("Welcome to BookLoan Administration")


admin.site.register(Book)
admin.site.register(BookVersion)
admin.site.register(CustomUser)
admin.site.register(Rating)
admin.site.register(FavoriteBookUser)
admin.site.register(Comment)



