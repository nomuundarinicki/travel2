from __future__ import unicode_literals

from django.db import models
from ..loginreg.models import User
# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=255)

class Trip(models.Model):
    title = models.CharField(max_length=255)
    place = models.ForeignKey(Place)

class Review(models.Model):
    user = models.ForeignKey(User)
    Trip = models.ForeignKey(Trip)
    rating = models.IntegerField()
    review = models.TextField(max_length=1000)
    created_at = models.DateField(auto_now_add=True)
