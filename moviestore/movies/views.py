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
            user.email = request.POST.get("email")
            user.save()
            login(request, user)
            return redirect('account') 
    else:
        form = UserCreationForm()

    return render(request, "movies/signup.html", {"form": form})


@login_required
def add_to_cart(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    cart_items, created = Cart.objects.get_or_create(user=request.user, movie=movie)
    
    if not created:
        cart_items.quantity += 1  
        cart_items.save()

        cart_items = Cart.objects.filter(user=request.user)

    return render(request, 'movies/cart.html', {'cart_items': cart_items})


@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'movies/cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, movie_id):
    cart_items = get_object_or_404(Cart, user=request.user, movie_id=movie_id)
    cart_items.delete()
    return render(request, 'movies/cart.html', {'cart_items': cart_items})

@login_required
def account_page(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, "movies/account.html", {
        "user": request.user,
        "orders": user_orders
    })

def login_redirect(request):
    return redirect('account')