from rest_framework import serializers

class ScheduleSerializer(serializers.Serializer):
    room = serializers.CharField(max_length=10, required=False, allow_blank=False)
    course = serializers.CharField(max_length=10)
    timeslot = serializers.CharField(max_length=10, required=False, allow_blank=False)

    def validate(self, attrs):
        if attrs.get('room') == None and attrs.get('timeslot') == None:
            raise serializers.ValidationError("At least either room or timeslot is defined.")
        return attrs