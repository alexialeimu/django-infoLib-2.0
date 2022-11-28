from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Book(models.Model):
    # ISBN = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    # description = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=150)
    publication_year = models.IntegerField(default=0)
    publisher = models.CharField(max_length=150)
    page_count = models.IntegerField(default=0)
    cover_URL = models.URLField(max_length=250)

    STATUS = (
        ('a', 'Available'),
        ('o', 'On loan'),
        ('n', 'Not for loan'),
    )

    status = models.CharField(
        max_length=1, choices=STATUS, blank=True, default='a')
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    #temporarily
    borrowed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]

class Borrowing(models.Model):
    borrowing_date = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    returning_date = models.DateTimeField(null=True, blank=True)
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

class Review(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    review = models.CharField(max_length=800)
    rating = models.IntegerField(default=1)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewed_book = models.ForeignKey(Book, on_delete=models.CASCADE)