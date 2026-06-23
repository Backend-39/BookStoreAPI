from django.urls import path, include
from .views import (
    RegisterApiView,
    AccountRetrieveApiView,
    BookLisCreateApiView,
    BookSoldApiView,
    MyBooksApiView,
    FavouriteBooksApiView,
    AccountFavouriteBooks,
    BookAddImageApiView,
    BookDelImageApiView,
    BookImagesListApiView,
)

urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('account/', AccountRetrieveApiView.as_view()),
    path('books/', BookLisCreateApiView.as_view()),
    path('books/<int:pk>/change-sold/', BookSoldApiView.as_view()),
    path('books/my-books/', MyBooksApiView.as_view()),
    path('books/<int:pk>/add-remove-favourites/', FavouriteBooksApiView.as_view()),
    path('books/my-favourite-books/', AccountFavouriteBooks.as_view()),
    path('books/<int:pk>/add-image/', BookAddImageApiView.as_view()),
    path('books/<int:book_id>/images/<int:image_id>/delete/', BookDelImageApiView.as_view()),
    path('books/<int:pk>/images/', BookImagesListApiView.as_view()),
    
]
