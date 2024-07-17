from rest_framework import serializers
from . import preset

class AdvancedSerializer(serializers.Serializer):
    length = serializers.IntegerField()
    preset = preset.PresetSerializer(many=True)

    def validate(self, attrs):
        if self.preset.is_valid(): return super().validate(attrs)