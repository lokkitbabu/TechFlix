from django.urls import path
from movies.views import index, movie_detail, add_to_cart, view_cart, remove_from_cart, home

urlpatterns = [
    path('', index, name='index'),
    path('<int:movie_id>/', movie_detail, name='movie_detail'),
    path('cart/add/<int:movie_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('cart/remove/<int:movie_id>/', remove_from_cart, name='remove_from_cart'),
]