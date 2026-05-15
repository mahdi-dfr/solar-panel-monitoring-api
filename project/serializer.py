from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Project
from country_division.models import City
from country_division.serializer import CitySerializer


class ProjectSerializer(ModelSerializer):
    
    # برای دریافت city هنگام create
    city = PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        required=True,
        allow_null=False,
    )

    # برای نمایش اطلاعات شهر هنگام GET
    # city_detail = CitySerializer(source='city', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('user',)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['city'] = instance.city.title if instance.city else None
        return data    


# class PanelPowerReadingSerializer(ModelSerializer):
#     """Single power reading for time-series API."""

#     class Meta:
#         model = PanelPowerReading
#         fields = ("recorded_at", "kw")


# class PanelPowerResponseSerializer(ModelSerializer):
#     """Latest power value for a panel."""

#     class Meta:
#         model = Panel
#         fields = ("id", "board_id", "kw", "update_at")