from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('<int:book_id>/<int:user_id>/return/', views.return_book, name='return'),
    path('<int:book_id>/<int:user_id>/borrow/', views.borrow, name='borrow'),
    path('<int:book_id>/', views.detail, name="detail"),
    path('reviews/<int:book_id>/<int:user_id>/', views.reviews, name='reviews'),
    path('profile/<int:user_id>/', views.profile, name="profile"),
    # url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile, name="profile"),
    path('add_book/', views.add_book, name='add_book'),
    path('search/', views.search, name='search'),
    path('', views.index, name='index'),
    path('admin/', views.admin, name="admin"),
    path('delete/<int:book_id>/', views.delete_book, name='delete'),
    path('signup/', views.signup, name="signup"),
]

# From Django 2.0 release notes:

# Simplified URL routing syntax
# - previous:   url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
# - new:        path('articles/<int:year>/', views.year_archive),