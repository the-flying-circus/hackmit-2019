from django.urls import path
from rest_framework_nested import routers

from .views import PageViewSet, MetricViewSet, weather, mood, entry, prompt, user, graph, pointsOfInterest, wiki


router = routers.SimpleRouter()
router.register(r'pages', PageViewSet, basename='pages')

pages_router = routers.NestedSimpleRouter(router, r'pages', lookup='page')
pages_router.register(r'metrics', MetricViewSet, base_name='page-metrics')


urlpatterns = [
    path('weather/', weather),
    path('mood/', mood),
    path('entry/', entry),
    path('prompt/', prompt),
    path('user/', user),
    path('graph/', graph),
    path('pois/', pointsOfInterest),
    path('wiki/', wiki)
]
urlpatterns += router.urls
urlpatterns += pages_router.urls
