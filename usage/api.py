from rest_framework.routers import DefaultRouter
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import WaterUsage


class WaterUsageSerializer(ModelSerializer):
    """Django-Rest-Framework (DRF) serializer for water usage API endpoint."""
    class Meta:
        model = WaterUsage
        fields = "__all__"


class APIWaterUsageViewSet(ReadOnlyModelViewSet):
    """Water usage in gallons per day."""
    fields = "__all__"
    filterset_fields = ("date",)
    model = WaterUsage
    queryset = model.objects
    serializer_class = WaterUsageSerializer


api_router = DefaultRouter()
api_router.register(prefix=r"usage", viewset=APIWaterUsageViewSet)
