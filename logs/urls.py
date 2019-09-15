from django.urls import path
from rest_framework_nested import routers

from .views import PageViewSet, MetricViewSet, weather, mood, prompt


router = routers.SimpleRouter()
router.register(r'pages', PageViewSet, basename='pages')

pages_router = routers.NestedSimpleRouter(router, r'pages', lookup='page')
pages_router.register(r'metrics', MetricViewSet, base_name='page-metrics')


urlpatterns = [
    path('weather/', weather),
    path('mood/', mood),
    path('prompt/', prompt)
]
urlpatterns += router.urls
urlpatterns += pages_router.urls
