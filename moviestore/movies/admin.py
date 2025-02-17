from django.contrib import admin
from .models import *

admin.site.register(Movie)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(OrderItem)
