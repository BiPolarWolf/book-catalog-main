from rest_framework.serializers import ModelSerializer
from books import models
from rest_framework.serializers import SerializerMethodField
from django.contrib.auth.models import User
from django.db.models import Avg


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = models.Author
        fields = "__all__"


class GenreSerializer(ModelSerializer):
    class Meta:
        model = models.Genre
        exclude = ["id"]


class BookListSerializer(ModelSerializer):
    average_rating = SerializerMethodField()
    author_fullname = SerializerMethodField()
    genre = SerializerMethodField()
    is_favorite = SerializerMethodField()

    class Meta:
        model = models.Book
        fields = [
            "id",
            "title",
            "author_fullname",
            "genre",
            "average_rating",
            "is_favorite",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if "request" in self.context and self.context["request"].method == "GET":
            representation["author"] = representation["author_fullname"]
        representation.pop("author_fullname", None)
        return representation

    def get_author_fullname(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    def get_genre(self, obj):
        return obj.genre.name

    def get_average_rating(self, obj):
        reviews = models.Review.objects.filter(book=obj)
        if reviews.exists():
            return reviews.aggregate(Avg("rating"))["rating__avg"]
        return 0

    def get_is_favorite(self, obj):
        user = self.context["request"].user
        if user and user.is_authenticated:
            return models.FavoriteUserBook.objects.filter(user=user, book=obj).exists()
        return False


class BookSerializer(ModelSerializer):
    reviews = SerializerMethodField()
    is_favorite = SerializerMethodField()
    average_rating = SerializerMethodField()
    author_fullname = SerializerMethodField()
    genre_name = SerializerMethodField()

    class Meta:
        model = models.Book
        fields = [
            "id",
            "title",
            "description",
            "publish_date",
            "author",
            "author_fullname",
            "is_favorite",
            "genre",
            "genre_name",
            "reviews",
            "average_rating",
        ]

    def get_author_fullname(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"

    def get_genre_name(self, obj):
        return obj.genre.name

    def get_is_favorite(self, obj):
        user = self.context["request"].user
        if user and user.is_authenticated:
            return models.FavoriteUserBook.objects.filter(user=user, book=obj).exists()
        return False

    def get_reviews(self, obj):
        reviews = models.Review.objects.filter(book=obj)
        return ReviewSerializer(reviews, many=True).data

    def get_average_rating(self, obj):
        reviews = models.Review.objects.filter(book=obj)
        if reviews.exists():
            return reviews.aggregate(Avg("rating"))["rating__avg"]
        return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if "request" in self.context and self.context["request"].method == "GET":
            representation["author"] = representation["author_fullname"]
        representation.pop("author_fullname", None)
        return representation


class ReviewSerializer(ModelSerializer):
    class Meta:
        model = models.Review
        fields = ["rating", "text", "review_author"]
        read_only_fields = ["review_author"]

    def create(self, validated_data):
        validated_data["review_author"] = self.context["request"].user
        return super(ReviewSerializer, self).create(validated_data)

    def get_review_author_username(self, obj):
        return obj.review_author.username
