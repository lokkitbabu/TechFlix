from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Movie, Cart, Order, Review, OrderItem
from django.http import HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes



def home(request):
    return render(request, "movies/login.html")

@login_required
def index(request):
    movies = Movie.objects.all()
    return render(request, 'movies/index.html', {'movies': movies})

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Fetch all reviews related to the movie
    reviews = Review.objects.filter(movie=movie).select_related('user')

    # Check if the logged-in user has already reviewed the movie
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    return render(request, 'movies/detail.html', {
        'movie': movie,
        'reviews': reviews,  # Pass all reviews
        'user_review': user_review,  # Pass user's review (if exists)
        'in_cart': request.user.is_authenticated and movie.cart_set.filter(user=request.user).exists()
    })

def signup(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('signup')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)  # Automatically log the user in after signup
        messages.success(request, "Signup successful! Welcome to Techflix.")
        return redirect('index')  # Redirect to home page or dashboard

    return render(request, "movies/signup.html")

@login_required
def add_to_cart(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, movie=movie)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"{cart_item.movie.title} added to your cart.")
    else:
        messages.success(request, f"{cart_item.movie.title} added to your cart.")

    return redirect(request.META.get('HTTP_REFERER','index'))

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'movies/cart.html', {'cart_items': cart_items, "total_price": total_price})

@login_required
def remove_from_cart(request, movie_id):
    cart_item = get_object_or_404(Cart, user=request.user, movie_id=movie_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, f" {cart_item.movie.title} removed from cart.")
    else:
        cart_item.delete()
        messages.success(request, f"{cart_item.movie.title} removed from cart.")

    return redirect('view_cart')

@login_required
def searchbar(request):
    if request.method == 'POST':
        search_term = request.POST.get('search_term', '')

        # Replace wildcards `_` and `*` with SQL-compatible wildcards
        search_term = search_term.replace('_', '?').replace('*', '%')

        # Filter movies based on title only
        movies = Movie.objects.extra(
            where=["title LIKE %s"],
            params=[f"%{search_term}%"]
        )

        return render(request, 'movies/index.html', {'movies': movies, 'search_term': search_term})
    else:
        return redirect('index')

@login_required
def account_page(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related("order_items__movie")
    return render(request, "movies/account.html", {
        "user": request.user,
        "orders": user_orders
    })

def login_redirect(request):
    return redirect('account')

@login_required
def add_review(request, movie_id):
    if request.method == "POST":
        movie = get_object_or_404(Movie, id=movie_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        # Ensure rating is provided
        if rating is None or rating.strip() == "":
            messages.error(request, "You must provide a rating between 1 and 5.")
            return redirect('movie_detail', movie_id=movie.id)

        # Convert rating safely to an integer
        try:
            rating = int(rating)
            if not 1 <= rating <= 5:
                raise ValueError
        except ValueError:
            messages.error(request, "Rating must be a number between 1 and 5.")
            return redirect('movie_detail', movie_id=movie.id)

        # Get or create the review with default values
        review, created = Review.objects.get_or_create(
            user=request.user, movie=movie,
            defaults={'rating': rating, 'comment': comment}  # ✅ Set defaults for new reviews
        )

        # If review exists, update it
        if not created:
            review.rating = rating
            review.comment = comment
            review.save()
            messages.success(request, "Review updated successfully.")
        else:
            messages.success(request, "Review added successfully.")

        return redirect('movie_detail', movie_id=movie.id)
    
    return redirect('index')  # Redirect if accessed via GET

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    # Create a new order
    order = Order.objects.create(user=request.user, total_price=0)

    total_price = 0
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            movie=item.movie,
            quantity=item.quantity
        )
        total_price += item.quantity * item.movie.price

    order.total_price = total_price
    order.save()

    # Clear the user's cart after placing the order
    cart_items.delete()
    
    messages.success(request, f"Your order #{order.id} has been placed successfully.")
    return render(request, 'movies/cart.html', {'refresh': True})

def password_reset_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user = User.objects.filter(username=username).first()

        if user:
            # Generate a password reset link manually
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = f"/movies/password_reset_confirm/{uid}/{token}/"

            messages.success(request, f"Use this link to reset your password: {reset_url}")
            return redirect('password_reset_done')
        else:
            messages.error(request, "Username not found.")

    return render(request, "movies/password_reset_form.html")


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == "POST":
        review.delete()
        messages.success(request, "Your review has been deleted.")
    
    return redirect('movie_detail', movie_id=review.movie.id)

@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = Review.objects.filter(movie=movie)
    user_review = reviews.filter(user=request.user).first()  # Get current user's review if it exists

    context = {
        "movie": movie,
        "reviews": reviews,
        "user_review": user_review,
    }
    return render(request, "movies/detail.html", context)

def about(request):
    return render(request, 'movies/about.html')