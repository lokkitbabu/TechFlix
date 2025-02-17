from django.contrib import admin
from .models import Movie, Cart, Order, Review

admin.site.register(Movie)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Review)