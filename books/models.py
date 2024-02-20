from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name}"

    class Meta:
        ordering = ["-last_name"]
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("жанр"))
    description = models.TextField(
        null=True, blank=True, verbose_name=_("Описание жанра")
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["-name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("название"))
    description = models.TextField(verbose_name=_("описание"))
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name="book_genres"
    )
    publish_date = models.DateField(verbose_name=_("Дата публикации"))

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["-publish_date"]
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name=_("Книга"))
    review_author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("Автор отзыва")
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0,
        verbose_name=_("Рейтинг"),
    )
    text = models.TextField(verbose_name=_("Текст отзыва"))

    class Meta:
        unique_together = ["book", "review_author"]
        ordering = ["-rating"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Book {self.book.title} rated {self.rating} by User {self.review_author.username}"


class FavoriteUserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_favs")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="books")

    def __str__(self) -> str:
        return f"{self.user} - {self.book}"

    class Meta:
        unique_together = ["book", "user"]
        verbose_name = "избранные"
        verbose_name_plural = "избранные"
