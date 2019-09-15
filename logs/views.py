import requests

from django.http import JsonResponse
from rest_framework import viewsets, permissions
from django.views.decorators.cache import cache_page

from .models import Page, Metric
from .serializers import PageSerializer, MetricSerializer
from .IBMnlp import getIBMEmotions, getMoodScores


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Page.objects.filter(owner=self.request.user)


class MetricViewSet(viewsets.ModelViewSet):
    serializer_class = MetricSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Metric.objects.filter(page=self.kwargs['page_pk'], page__owner=self.request.user)


@cache_page(60)
def weather(request):
    resp = requests.get("http://api.openweathermap.org/data/2.5/weather?id=4931972&APPID=3a2410d61b7127eea64a08e1093fb82c")
    #print(resp)
    resp.raise_for_status()

    return JsonResponse(resp.json())

def mood(request):
    text = request.GET['text']
    return JsonResponse(getMoodScores(getIBMEmotions(text)))
