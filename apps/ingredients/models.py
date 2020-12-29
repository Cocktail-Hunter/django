from django.db import models
from django.contrib.auth import get_user_model


class IngredientState(models.IntegerChoices):
    PENDING = 0, 'Pending'
    APPROVED = 1, 'Approved'
    DENIED = 2, 'Denied'


class Ingredient(models.Model):

    cocktaildb_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)
    state = models.PositiveSmallIntegerField(
        default=IngredientState.PENDING, choices=IngredientState.choices
    )
    public = models.BooleanField(default=True)
    alcoholic = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        get_user_model(), null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)
