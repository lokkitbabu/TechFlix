from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('add/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove/<int:movie_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('searchbar', views.searchbar, name='searchbar'),
]
