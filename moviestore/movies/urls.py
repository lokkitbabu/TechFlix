from django.urls import path, include
from django.contrib.auth import views as auth_views
from movies.views import index, movie_detail, add_to_cart, view_cart, remove_from_cart, home, signup, account_page

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('add/<int:movie_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove/<int:movie_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('searchbar', views.searchbar, name='searchbar'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="movies/login.html"), name="login"),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name="logout"),  # ✅ Redirects to home
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('account/', account_page, name='account'),

]
