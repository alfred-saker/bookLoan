from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from backend.views import BookViewSet, UserViewSet, EmpruntViewSet,LoginViewSet,LogoutViewSet
   # Route API
router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'users', UserViewSet)
router.register(r'emprunts', EmpruntViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('admin/clearcache/', include('clearcache.urls')),
    path('login/', LoginViewSet.as_view()),
    path('logout/', LogoutViewSet.as_view()),
    path('admin/', admin.site.urls)
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

