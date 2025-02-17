from django.contrib import admin
from django.urls import path, include
from movies.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('', home, name='home'),  # Movies app routes
]