from django.db import models
from django.contrib.auth import get_user_model


class CocktailState(models.IntegerChoices):
    PENDING = 0, 'Pending'
    APPROVED = 1, 'Approved'
    DENIED = 2, 'Denied'


class Cocktail(models.Model):

    cocktaildb_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)
    picture = models.ImageField(upload_to='cocktails/thumbnails')

    state = models.PositiveSmallIntegerField(
        default=CocktailState.PENDING,
        choices=CocktailState.choices
    )

    public = models.BooleanField(default=True)
    alcoholic = models.BooleanField(default=True)

    ingredients = models.ManyToManyField(
        'ingredients.Ingredient',
        blank=True,
        related_name='cocktails',
        related_query_name='cocktail'
    )

    author = models.ForeignKey(
        get_user_model(),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)
