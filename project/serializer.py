from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Project, StringReading, Board, String
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
    

class BoardSerializer(serializers.ModelSerializer):

    project_name = serializers.CharField(
        source='project.project_name',
        read_only=True
    )

    strings_count = serializers.SerializerMethodField()

    class Meta:
        model = Board

        fields = [
            'id',
            'project',
            'project_name',
            'board_id',
            'name',
            'strings_count',
        ]

        read_only_fields = [
            'id',
            'strings_count',
        ]

    def get_strings_count(self, obj):
        return obj.strings.count()

    def validate_board_id(self, value):

        board_id = self.instance.id if self.instance else None

        query = Board.objects.filter(
            board_id=value
        )

        if board_id:
            query = query.exclude(
                id=board_id
            )

        if query.exists():
            raise serializers.ValidationError(
                'این شناسه برد قبلاً استفاده شده است.'
            )

        return value
    

class StringSerializer(serializers.ModelSerializer):

    board_name = serializers.CharField(
        source='board.name',
        read_only=True
    )

    project_name = serializers.CharField(
        source='board.project.project_name',
        read_only=True
    )

    class Meta:
        model = String

        fields = [
            'id',
            'board',
            'board_name',
            'project_name',
            'string_id',
            'name',
        ]

        read_only_fields = [
            'id',
            'board_name',
            'project_name',
        ]

    def validate(self, attrs):

        board = attrs.get(
            'board',
            self.instance.board if self.instance else None
        )

        string_id = attrs.get(
            'string_id',
            self.instance.string_id if self.instance else None
        )

        existing_string = String.objects.filter(
            board=board,
            string_id=string_id
        )

        if self.instance:
            existing_string = existing_string.exclude(
                id=self.instance.id
            )

        if existing_string.exists():
            raise serializers.ValidationError(
                'این شناسه استرینگ برای این برد قبلاً استفاده شده است.'
            )

        return attrs


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


class AdminStatisticsSerializer(serializers.Serializer):

    total_users = serializers.IntegerField()

    total_projects = serializers.IntegerField()

    total_boards = serializers.IntegerField()

    total_strings = serializers.IntegerField()    