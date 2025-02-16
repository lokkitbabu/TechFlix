from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import Movie, Cart, Order

def home(request):
    return render(request, "movies/home.html")

def index(request):
    movies = Movie.objects.all()
    cart_items = Cart.objects.filter(user=request.user).values_list('movie_id', flat=True)
    return render(request, 'movies/index.html', {'movies': movies, 'cart_items': cart_items})

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movies = Movie.objects.all()
    in_cart = Cart.objects.filter(user=request.user, movie=movie).exists()
    return render(request, 'movies/detail.html', {'movie': movie,'in_cart': in_cart, 'movies': movies})

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
    cart_item, created = Cart.objects.get_or_create(user=request.user, movie=movie)
    in_cart = Cart.objects.filter(user=request.user, movie=movie).exists()
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return render(request, 'movies/detail.html', {'movie': movie,'in_cart': in_cart})

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    movies = Movie.objects.all()
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'movies/cart.html', {'cart_items': cart_items, "total_price": total_price, 'movies': movies})

@login_required
def remove_from_cart(request, movie_id):
    cart_item = get_object_or_404(Cart, movie_id=movie_id)
    cart_item.delete()
    return redirect('view_cart')

def searchbar(request):
    movies = Movie.objects.all()
    return render(request, 'movies/searchbar.html', {'movies': movies})

@login_required
def account_page(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, "movies/account.html", {
        "user": request.user,
        "orders": user_orders
    })

def login_redirect(request):
    return redirect('account')
