from django.urls import include, path

from .api import api_router
from .views import WaterTableView, WaterChartView


urlpatterns = [
    path("api/", include(api_router.urls), name="api"),
    path("", WaterTableView.as_view(), name="table"),
    path("chart/", WaterChartView.as_view(), name="chart")
]
