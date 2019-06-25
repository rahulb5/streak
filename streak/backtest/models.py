from django.db import models

# Create your models here.
class conditions(models.Model):
    first_parameter = models.IntegerField()
    condition = models.IntegerField()
    second_parameter = models.IntegerField()
    