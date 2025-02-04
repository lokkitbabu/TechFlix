from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from movies.users import views as user_views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('cart/add/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:movie_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('register/', auth_views.LoginView.as_view(template_name='users/register.html'), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('password_reset/', auth_views.LoginView.as_view(template_name='users/password_reset.html'), name='password_reset'),
]
