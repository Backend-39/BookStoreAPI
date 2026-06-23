from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, get_object_or_404
from main.models import Account, Book, Image
from .serializers import (
    AccountSerializer,
    AccountUpdateSerializer,
    ImageSerializer,
    BookSerializer,
    BookPostSerializer
)
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from .paginations import BookPagination, ImagePagination
from rest_framework.views import APIView
from rest_framework.response import Response

class RegisterApiView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountRetrieveApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountUpdateSerializer

    def get_object(self):
        return self.request.user

class BookLisCreateApiView(ListCreateAPIView):
    queryset = Book.objects.all()
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'details']
    ordering_fields = ['id', 'created_at']
    ordering = '-created_at'
    filterset_fields = ['account', 'cover']
    pagination_class = BookPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return BookSerializer
        else:
            return BookPostSerializer
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated()]
    def get_queryset(self):
        return Book.objects.filter(account=self.request.user)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                required=False,
                type = openapi.TYPE_STRING,
                enum = ['id', '-id', 'created_at', '-created_at']
            ),
            openapi.Parameter(
                'account',
                openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            )
            
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class BookSoldApiView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Kitobni sotilgan yoki sotilmagan deb belgilash",
        responses={
            200: BookSerializer,
            404: "Not found (Bunda berilgan idga mos kitob mavjud emas yoki kitob foydalanuvchiga tegishli emas)"
        },
        manual_parameters=[
            openapi.Parameter(
                'sold',
                openapi.IN_QUERY,
                required=False,
                type = openapi.TYPE_STRING,
                enum=['0','1']
            )
        ]
    )
    def get(self, request, pk):
        book = get_object_or_404(Book, id=pk, account=request.user)
        sold = request.query_params.get('sold')

        if sold == "0" and book.sold:
            book.sold = False
            book.save()
        elif sold == '1' and not book.sold:
            book.sold = True
            book.save()

        book_ser = BookSerializer(book)
        return Response(book_ser.data)
        
class MyBooksApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    pagination_class = BookPagination
    search_fields = ['name', 'details']
    ordering_fields = ["id", "created_at"]
    ordering = "-created_at"
    filterset_fields = ["sold", "cover"]

    def get_queryset(self):
        return Book.objects.filter(account=self.request.user)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                required = False,
                type = openapi.TYPE_STRING,
                enum=['id', '-id', 'created_at', '-created_at'],
                default="-created_at"
            ),
            openapi.Parameter(
                'sold',
                openapi.IN_QUERY,
                required = False,
                type = openapi.TYPE_BOOLEAN
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class FavouriteBooksApiView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Foydalanuvchining yoqtirgan kitoblariga kitob qo'shish",
        responses={
            200: openapi.Schema(
                type = openapi.TYPE_OBJECT,
                properties={
                    "action": openapi.Schema(
                        description="added or removed",
                        type = openapi.TYPE_STRING
                    ),
                    "count": openapi.Schema(
                        description="Count of favourite books",
                        type = openapi.TYPE_INTEGER
                    )
                }
            )
        }
    )
    def get(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        user = request.user
        action = ""
        books = user.favourite_books.all()
        if book in books:
            user.favourite_books.remove(book)
            user.save()
            action = "removed"
        else:
            user.favourite_books.add(book)
            user.save()
            action = 'added'

        count = user.favourite_books.count()

        r_data = {
            'action': action,
            'count': count
        }

        return Response(r_data)

class AccountFavouriteBooks(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    pagination_class = BookPagination
    search_fields = ['name', 'details']
    ordering_fields = ['id', 'created_at']

    def get_queryset(self):
        return self.request.user.favourite_books.all()

    @swagger_auto_schema(
        operation_description="Foydalanuvchining yoqtirgan kitoblari ro'yhati",
        responses = {
            200: BookSerializer
        },
        manual_parameters=[
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                required=False,
                type = openapi.TYPE_STRING,
                enum = ['id','-id','created_at','-created_at']
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class BookAddImageApiView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Kitob uchun rasm qo'shish",
        responses={
            200: ImageSerializer
        }
    )
    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk, account=request.user)
        data = request.data.copy()
        data['book'] = pk
        image_ser = ImageSerializer(data=data)
        image_ser.is_valid(raise_exception=True)
        image_ser.save()
        print(pk)
        print(request.user)
        print(Book.objects.filter(id=pk).exists())
        print(Book.objects.filter(id=pk, account=request.user).exists())
        return Response(image_ser.data)
        
class BookDelImageApiView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Kitobdan rasmni o'chirish"
    )
    def get(self, request, book_id, image_id):
        book = get_object_or_404(Book, id=book_id, account=request.user)
        image = get_object_or_404(Image, id=image_id, book=book)
        image.delete()
        
        return Response(status=200)


class BookImagesListApiView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ImageSerializer
    pagination_class = ImagePagination

    def get_queryset(self):
        id = self.kwargs.get('pk')
        book = get_object_or_404(Book, id=id)
        return book.images.all()
