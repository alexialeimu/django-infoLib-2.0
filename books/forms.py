from django import forms
from books.models import Book, Review
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    ISBN = forms.CharField(max_length=150)
    name = forms.CharField(max_length=150)
    description = forms.CharField(max_length=500)
    author = forms.CharField(max_length=150)
    publication_year = forms.IntegerField(min_value=1000, max_value=2999)
    publisher = forms.CharField(max_length=150)
    page_count = forms.IntegerField(min_value=0, max_value=9999)
    cover_URL = forms.URLField(max_length=200)

    class Meta:
        model = Book
        fields = ('ISBN', 'name', 'description', 'author', 'publication_year', 'publisher', 'page_count', 'cover_URL',)

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class ReviewForm(forms.ModelForm):
    review = forms.CharField(max_length=1000)
    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ('review', 'rating')