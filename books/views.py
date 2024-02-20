from rest_framework.viewsets import ModelViewSet
from .filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend
from books import models
from books import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import FavoriteUserBook
from drf_yasg.utils import swagger_auto_schema


class AuthorViewSet(ModelViewSet):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer
    permission_classes=[IsAuthenticated]
    my_tags = ["Authors"]


class GenreViewSet(ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes=[IsAuthenticated]
    my_tags = ["Genres"]


class BookViewSet(ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes=[IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    my_tags = ["Books"]

    @action(detail=True, methods=["post"])
    def add_to_favorites(self, request, pk=None):
        book = self.get_object()
        user = self.request.user

        if FavoriteUserBook.objects.filter(user=user, book=book).exists():
            return Response(
                {"error": "This book is already in favorites"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        FavoriteUserBook.objects.create(user=user, book=book)
        return Response({"status": "book added to favorites"})

    @action(detail=True, methods=["post"])
    def remove_from_favorites(self, request, pk=None):
        book = self.get_object()
        user = self.request.user

        favorite = FavoriteUserBook.objects.filter(user=user, book=book)
        if favorite.exists():
            favorite.delete()
            return Response({"status": "book removed from favorites"})
        return Response(
            {"error": "This book is not in your favorites"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(method="post", request_body=serializers.ReviewSerializer)
    @action(detail=True, methods=["post"])
    def add_review(self, request, pk=None):
        book = self.get_object()
        review = models.Review.objects.filter(
            review_author=self.request.user, book=book
        )
        if review:
            return Response(
                {"message": "Вы уже оставили отзыв на эту книгу"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = serializers.ReviewSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.BookListSerializer
        return serializers.BookSerializer
