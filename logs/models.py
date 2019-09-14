from django.db import models

from django.contrib.auth import get_user_model


class Page(models.Model):
    """
    Represents the logs for one day.
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} by {}'.format(self.date, self.owner.username)


class Metric(models.Model):
    """
    Represents a metric that a user wishes to track from day to day.
    """
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    name = models.TextField()
    value = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{}: {} for {}'.format(self.name, self.value, self.page)
