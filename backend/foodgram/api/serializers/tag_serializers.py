from recipes.models import Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    color = serializers.CharField(source='hex_code')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
