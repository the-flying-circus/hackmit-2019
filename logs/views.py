from rest_framework import viewsets, permissions

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
