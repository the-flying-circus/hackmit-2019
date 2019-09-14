import requests

from django.http import JsonResponse
from rest_framework import viewsets, permissions
from django.views.decorators.cache import cache_page

from .models import Page, Metric
from .serializers import PageSerializer, MetricSerializer


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
    #resp = requests.get("https://www.metaweather.com/api/location/2367105/")
    resp = request.get("http://api.openweathermap.org/data/2.5/weather?q=02139")
    resp.raise_for_status()

    return JsonResponse(resp.json())
