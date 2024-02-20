# Generated by Django 4.2 on 2023-12-08 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="review",
            options={
                "ordering": ["-rating"],
                "verbose_name": "Отзыв",
                "verbose_name_plural": "Отзывы",
            },
        ),
        migrations.AlterField(
            model_name="favoriteuserbook",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_favs",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
