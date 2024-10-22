from rest_framework import serializers

from .models import Assignee


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignee
        fields = (
            "id",
            "name"
        )
