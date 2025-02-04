from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('cart/add/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:movie_id>/', views.remove_from_cart, name='remove_from_cart'),
]
