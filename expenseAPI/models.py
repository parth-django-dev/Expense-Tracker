from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=(
        ('I', 'Income'),
        ('E', 'Expense'),
    ))
    amount = models.IntegerField()
    category = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' - ' + self.type + ' - ' + str(self.amount)
    