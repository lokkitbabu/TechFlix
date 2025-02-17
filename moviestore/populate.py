import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviestore.settings')
django.setup()

from django.contrib.auth.models import User
from movies.models import Movie, Cart, Order, OrderItem, Review

# Setup Django environment


def create_users():
    """Create sample users"""
    users_data = [
    {"username": "john_doe", "email": "john@example.com", "password": "password123"},
    {"username": "jane_doe", "email": "jane@example.com", "password": "password123"},
    {"username": "admin_user", "email": "admin@example.com", "password": "adminpass"},
    {"username": "alex_smith", "email": "alex@example.com", "password": "test123"},
    {"username": "chris_evans", "email": "chris@example.com", "password": "marvel123"},
    {"username": "tony_stark", "email": "tony@example.com", "password": "ironman"},
    {"username": "natasha_romanoff", "email": "natasha@example.com", "password": "blackwidow"},
    {"username": "steve_rogers", "email": "steve@example.com", "password": "captainamerica"},
    {"username": "bruce_wayne", "email": "bruce@example.com", "password": "batman"},
    {"username": "peter_parker", "email": "peter@example.com", "password": "spiderman"},
    {"username": "clark_kent", "email": "clark@example.com", "password": "superman"},
    {"username": "diana_prince", "email": "diana@example.com", "password": "wonderwoman"},
    {"username": "wade_wilson", "email": "wade@example.com", "password": "deadpool"},
    {"username": "logan_wolverine", "email": "logan@example.com", "password": "wolverine"},
    {"username": "dr_strange", "email": "strange@example.com", "password": "sorcerer"},
    {"username": "thor_odinson", "email": "thor@example.com", "password": "mjolnir"},
    {"username": "black_panther", "email": "panther@example.com", "password": "wakanda"},
    {"username": "harry_potter", "email": "harry@example.com", "password": "hogwarts"},
    {"username": "frodo_baggins", "email": "frodo@example.com", "password": "onering"},
    {"username": "neo_matrix", "email": "neo@example.com", "password": "thereisnospoon"}
]


    for user_data in users_data:
        if not User.objects.filter(username=user_data["username"]).exists():
            user = User.objects.create_user(username=user_data["username"], email=user_data["email"], password=user_data["password"])
            print(f"✅ Created user: {user.username}")

def create_movies():
    """Create sample movies"""
    movies_data = [
    {"title": "Inception", "description": "A mind-bending thriller.", "price": 10.99, "image": "movies/inception.jpg"},
    {"title": "Interstellar", "description": "A journey beyond space.", "price": 12.99, "image": "movies/interstellar.jpg"},
    {"title": "The Dark Knight", "description": "Batman vs Joker.", "price": 9.99, "image": "movies/dark_knight.jpg"},
    {"title": "Titanic", "description": "A tragic love story on the Titanic.", "price": 8.99, "image": "movies/titanic.jpg"},
    {"title": "Avatar", "description": "An epic sci-fi adventure on Pandora.", "price": 14.99, "image": "movies/avatar.jpg"},
    {"title": "The Matrix", "description": "A hacker discovers reality isn't what it seems.", "price": 11.49, "image": "movies/matrix.jpg"},
    {"title": "Gladiator", "description": "A general turned slave fights for honor.", "price": 10.49, "image": "movies/gladiator.jpg"},
    {"title": "The Godfather", "description": "A mafia family's rise and struggle.", "price": 13.99, "image": "movies/godfather.jpg"},
    {"title": "Forrest Gump", "description": "The extraordinary life journey of Forrest Gump.", "price": 9.49, "image": "movies/forrest_gump.jpg"},
    {"title": "The Shawshank Redemption", "description": "A wrongly convicted man's hope and escape.", "price": 9.99, "image": "movies/shawshank.jpg"},
    {"title": "Pulp Fiction", "description": "A series of interwoven crime stories.", "price": 10.99, "image": "movies/pulp_fiction.jpg"},
    {"title": "The Lord of the Rings: The Fellowship of the Ring", "description": "An epic journey to destroy the One Ring.", "price": 15.99, "image": "movies/lotr_fellowship.jpg"},
    {"title": "The Avengers", "description": "Marvel superheroes unite to save the world.", "price": 14.49, "image": "movies/avengers.jpg"},
    {"title": "Spider-Man: No Way Home", "description": "Spider-Man faces multiverse chaos.", "price": 16.99, "image": "movies/spiderman_nwh.jpg"},
    {"title": "Joker", "description": "A dark origin story of the Joker.", "price": 12.49, "image": "movies/joker.jpg"},
    {"title": "Deadpool", "description": "A wisecracking mercenary gets superpowers.", "price": 10.99, "image": "movies/deadpool.jpg"},
    {"title": "Django Unchained", "description": "A freed slave seeks revenge and justice.", "price": 11.99, "image": "movies/django.jpg"},
    {"title": "Black Panther", "description": "A new king must protect Wakanda.", "price": 13.99, "image": "movies/black_panther.jpg"},
    {"title": "The Lion King", "description": "A lion cub grows to reclaim his throne.", "price": 9.99, "image": "movies/lion_king.jpg"}
]


    for movie_data in movies_data:
        movie, created = Movie.objects.get_or_create(title=movie_data["title"], defaults=movie_data)
        if created:
            print(f" Created movie: {movie.title}")

def add_movies_to_cart():
    """Add movies to users' carts"""
    users = User.objects.all()
    movies = Movie.objects.all()

    for user in users:
        for movie in movies:
            cart_item, created = Cart.objects.get_or_create(user=user, movie=movie, defaults={"quantity": 1})
            if created:
                print(f" Added {movie.title} to {user.username}'s cart.")

def create_orders():
    """Create sample orders"""
    users = User.objects.all()

    for user in users:
        cart_items = Cart.objects.filter(user=user)
        if cart_items.exists():
            order = Order.objects.create(user=user, total_price=0)
            total_price = 0

            for cart_item in cart_items:
                OrderItem.objects.create(order=order, movie=cart_item.movie, quantity=cart_item.quantity)
                total_price += cart_item.quantity * cart_item.movie.price
            
            order.total_price = total_price
            order.save()
            cart_items.delete()  # Clear the cart after order creation
            print(f"📦 Created order {order.id} for {user.username} - Total: ${order.total_price:.2f}")

def create_reviews():
    """Create sample reviews for movies"""
    users = User.objects.all()
    movies = Movie.objects.all()

    reviews_data = [
        "Amazing movie! Must watch.",
        "Really enjoyed it, great acting.",
        "The visuals were stunning!",
        "Good, but could have been better.",
        "Not my cup of tea.",
        "Fantastic story and characters!",
        "I would watch this again!",
        "Overrated, in my opinion.",
        "An instant classic!",
        "Pretty good, but too long.",
    ]

    for user in users:
        for movie in movies:
            if not Review.objects.filter(user=user, movie=movie).exists():
                review = Review.objects.create(
                    user=user,
                    movie=movie,
                    rating=random.randint(1, 5),
                    comment=random.choice(reviews_data),
                )
                print(f"📝 Added review for {movie.title} by {user.username}")


if __name__ == "__main__":
    print(" Populating database...\n")
    
    create_users()
    create_movies()
    add_movies_to_cart()
    create_orders()
    create_reviews()  # ✅ Add this function call


    print("\n Database populated successfully!")
