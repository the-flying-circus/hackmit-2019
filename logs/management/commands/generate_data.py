import datetime
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from logs.models import Page, Metric


class Command(BaseCommand):
    help = 'Generate fake data for pretty graphs.'

    def handle(self, *args, **options):
        username = 'grey'
        user = get_user_model().objects.get(username=username)
        now = datetime.date.today()

        metrics = {
            'mood': 3,
            'anxiety': 3,
            'cynicism': 3
        }

        for i in range(31):
            self.stdout.write('Generating page: {}'.format(now))
            page, _ = Page.objects.get_or_create(owner=user, date=now, defaults={
                'content': 'autogenerated'
            })
            now -= datetime.timedelta(days=1)

            for key in metrics:
                diff = 0
                if random.random() < 0.2:
                    diff = 2
                elif random.random() < 0.8:
                    diff = 1
                if random.random() < 0.5:
                    diff *= -1
                metrics[key] = min(5, max(1, metrics[key] + diff))
                Metric.objects.get_or_create(page=page, name=key, defaults={
                    'value': metrics[key]
                })
                print('\tGenerating metric: {} -> {}'.format(key, metrics[key]))