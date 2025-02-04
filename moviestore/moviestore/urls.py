from django.contrib import admin
from django.urls import path, include
from movies.views import index, home, movie_detail, add_to_cart, view_cart, remove_from_cart

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('', home, name='home'),  # Movies app routes
]
