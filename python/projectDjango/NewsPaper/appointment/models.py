from django.db import models
from datetime import datetime
from news.models import Category


class Subscriber(models.Model):
    client_name = models.CharField(
        max_length=100
    )
    client_email = models.EmailField()
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField(
        default=datetime.utcnow,
    )

    def __str__(self):
        return f'{self.client_name}: подписчик {self.sub_category}'
