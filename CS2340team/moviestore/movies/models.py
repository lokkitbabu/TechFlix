from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='movies/')

    def __str__(self):
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.movie.price

    def __str__(self):
        return f"{self.quantity} x {self.movie.title}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)
    created_at = models.DateTimeField(auto_now_add=True)
