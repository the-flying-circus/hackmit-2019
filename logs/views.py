import requests
import datetime

from django.contrib.auth import get_user_model, login
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, permissions
from django.views.decorators.cache import cache_page

from .models import Page, Metric
from .serializers import PageSerializer, MetricSerializer
from .IBMnlp import getIBMEmotions, getMoodScores


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'date'

    def get_queryset(self):
        return Page.objects.filter(owner=self.request.user)


class MetricViewSet(viewsets.ModelViewSet):
    serializer_class = MetricSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'name'

    def get_queryset(self):
        return Metric.objects.filter(page__date=self.kwargs['page_date'], page__owner=self.request.user)


@cache_page(60)
def weather(request):
    resp = requests.get("http://api.openweathermap.org/data/2.5/weather?id=4931972&APPID=3a2410d61b7127eea64a08e1093fb82c")
    #print(resp)
    resp.raise_for_status()

    return JsonResponse(resp.json())

def mood(request):
    text = request.GET.get('text')
    if not text:
        return JsonResponse({
            'success': False
        })
    return JsonResponse(getMoodScores(getIBMEmotions(text)))


def prompt(request):
    return JsonResponse({
        "question": "What made you feel sad?"
    })


def user(request):
    # TODO: actually implement auth
    if not request.user.is_authenticated:
        User = get_user_model()
        obj, _ = User.objects.get_or_create(
            username='grey',
            first_name='Grey',
            last_name='Golla'
        )
        login(request, obj)

    # TODO: this shouldn't be here
    page, _ = Page.objects.get_or_create(owner=request.user, date=datetime.date.today())

    return JsonResponse({
        "name": request.user.first_name,
        "page": page.date,
        "content": page.content
    })


def graph(request):
    output = []

    for page in Page.objects.filter(owner=request.user).order_by('date'):
        output.append({
            'date': page.date,
            'metrics': {a: b for a, b in page.metric_set.values_list('name', 'value')}
        })

    return JsonResponse({
        'data': output
    })
