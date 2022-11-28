from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from .models import Book, Borrowing, Review
from books.forms import BookForm, UserForm, ReviewForm
from django.urls import reverse
from django.utils.formats import get_format
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.core.paginator import Paginator
# Authorization:
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
# Search functionality:
from django.template import RequestContext, Context
from django.db.models import Q

def index(request):
    all_books = Book.objects.all()
    all_borrowings = Borrowing.objects.all()
    context = {'all_books': all_books, 'all_borrowings': all_borrowings}
    return render(request, 'books/index.html', context)

@user_passes_test(lambda u: u.is_superuser)
def add_book(request):
    booksurl = request.build_absolute_uri(reverse('books:index'))
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        book_form = BookForm(request.POST)
        print (book_form.errors)
        # check whether it's valid:
        if book_form.is_valid():
            # process the data in form.cleaned_data as required
            book_name = book_form.cleaned_data['name']
            book_description = book_form.cleaned_data['description']
            book_author = book_form.cleaned_data['author']
            book_publication_year = book_form.cleaned_data['publication_year']
            book_publisher = book_form.cleaned_data['publisher']
            book_page_count = book_form.cleaned_data['page_count']
            book_cover_URL = book_form.cleaned_data['cover_URL']
            new_book = Book(name=book_name, description=book_description, author=book_author,
                            publication_year=book_publication_year, publisher=book_publisher, page_count=book_page_count, cover_URL=book_cover_URL)
            new_book.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        book_form = BookForm()
    return render(request, 'books/add_book.html', {'booksurl': booksurl, 'book_form': book_form})

@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    try:
        all_users = User.objects.all()
        all_reviews = Review.objects.all()
        all_borrowings = Borrowing.objects.all().order_by('-borrowing_date')
        borrowings_paginator = Paginator(all_borrowings, 15)
        borrowings_page_number = request.GET.get('page')
        borrowings_page_obj = borrowings_paginator.get_page(borrowings_page_number)
    except Book.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'admin.html', {'all_users': all_users, 'all_borrowings': all_borrowings, 'all_reviews': all_reviews, 'borrowings_page_obj': borrowings_page_obj})

# unique page for every book
def detail(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
        all_borrowings = Borrowing.objects.filter(book=book_id)
        all_reviews = Review.objects.filter(reviewed_book=book)
    except Book.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'books/detail.html', {'book': book, 'all_borrowings': all_borrowings, 'all_reviews': all_reviews})

@login_required
def profile(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        all_borrowings = Borrowing.objects.filter(borrower=user_id).order_by('-borrowing_date')
        all_reviews = Review.objects.filter(reviewer=user_id)
        borrowings_paginator = Paginator(all_borrowings, 15)
        borrowings_page_number = request.GET.get('page')
        borrowings_page_obj = borrowings_paginator.get_page(borrowings_page_number)
    except User.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'profile.html', {'user': user, 'all_borrowings': all_borrowings, 'all_reviews': all_reviews, 'borrowings_page_obj': borrowings_page_obj})

def search(request):
    query = request.GET.get('q')
    if query:
        results = Book.objects.filter(Q(name__icontains=query) | Q(author__icontains=query) | Q(publication_year__icontains=query) | Q(publisher__icontains=query))
    else:
        results = Book.objects.all()
    all_borrowings = Borrowing.objects.all()
    context = {'results': results, 'q': query, 'all_borrowings': all_borrowings}
    return render(request, 'books/index.html', context) 

@login_required
def borrow(request, book_id, user_id):
    if request.user.id == user_id:
        detailurl = request.build_absolute_uri(
            reverse('books:detail', args=[book_id]))
        book = Book.objects.get(pk=book_id)
        user = User.objects.get(pk=user_id)
        book.borrowed = True
        book.borrower = user
        book.status = 'o'
        book.save()
        date = DateFormat(datetime.now()).format(get_format('DATE_FORMAT'))
        new_borrowing = Borrowing(borrowing_date=date, book=book, borrower=user)
        new_borrowing.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise PermissionDenied

@login_required
def return_book(request, book_id, user_id):
    if request.user.id == user_id:
        detailurl = request.build_absolute_uri(
            reverse('books:detail', args=[book_id]))
        book = Book.objects.get(pk=book_id)
        book.borrowed = False
        book.borrower = None
        book.status = 'a'
        book.save()
        # return render(request, 'books/detail.html', {'detailurl': detailurl, 'book': book})
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        raise PermissionDenied

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print (user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'signup.html', {'user_form': user_form, 'registered': registered})

# function to get every review for a specific book
def reviews(request, book_id, user_id):
    detailurl = request.build_absolute_uri(
        reverse('books:detail', args=[book_id]))
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        print (review_form.errors)
        if review_form.is_valid():
            date = DateFormat(datetime.now()).format(get_format('DATE_FORMAT'))
            review = review_form.cleaned_data['review']
            rating = review_form.cleaned_data['rating']
            book = Book.objects.get(pk=book_id)
            reviewer = request.user
            new_review = Review(
                date=date, review=review, rating=rating, reviewed_book=book, reviewer=reviewer)
            new_review.save()
            return HttpResponseRedirect(detailurl)
    else:
        review_form = ReviewForm()
        book = Book.objects.get(pk=book_id)
    return render(request, 'books/review_book.html', {'book': book, 'detailurl': detailurl, 'review': review_form})

# function to let the admin to delete books
@user_passes_test(lambda u: u.is_superuser)
def delete_book(request, book_id):
    booksurl = request.build_absolute_uri(reverse('books:index'))
    detailurl = request.build_absolute_uri(reverse('books:detail', args=[book_id]))
    book = Book.objects.get(pk=book_id)
    if request.method == 'POST':
        book.delete()
        return HttpResponseRedirect('/')
    return render(request, 'books/delete.html', {'booksurl': booksurl, 'detailurl': detailurl, 'book': book})