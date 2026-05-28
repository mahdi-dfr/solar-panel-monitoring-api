from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Project, StringReading
from country_division.models import City
from country_division.serializer import CitySerializer
from rest_framework import serializers


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
    







class LiveStringReadingSerializer(serializers.ModelSerializer):

    string_id = serializers.IntegerField(source='string.string_id')
    name = serializers.CharField(source='string.name')

    class Meta:
        model = StringReading

        fields = [
            'string_id',
            'name',
            'voltage',
            'current',
            'power',
            'energy',
        ]


class LiveBoardSerializer(serializers.Serializer):

    board_id = serializers.IntegerField()
    board_name = serializers.CharField()

    temperature = serializers.IntegerField()
    humidity = serializers.IntegerField()

    timestamp = serializers.DateTimeField()

    strings = LiveStringReadingSerializer(many=True)