from django.db import models
from apps.authentication.models import User


class IngredientState(models.IntegerChoices):
    PENDING = 0, 'Pending'
    APPROVED = 1, 'Approved'
    DENIED = 2, 'Denied'


class Ingredient(models.Model):

    cocktaildb_id = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    state = models.PositiveSmallIntegerField(
        default=IngredientState.PENDING, choices=IngredientState.choices
    )
    public = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.name)
