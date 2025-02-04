from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Movie, Cart, Order

def home(request):
    return render(request, "movies/home.html")

def index(request):
    movies = Movie.objects.all()
    return render(request, 'movies/index.html', {'movies': movies})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/detail.html', {'movie': movie})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "movies/signup.html", {"form": form})


@login_required
def add_to_cart(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, movie=movie)
    return redirect('index')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'movies/cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, movie_id):
    cart_item = Cart.objects.get(user=request.user, movie_id=movie_id)
    cart_item.delete()
    return redirect('view_cart')
