from datetime import timezone

from django.utils import timezone
from rest_framework import serializers

from .models import Room, Chore, History, HistoryEntry


class ChoreSerializer(serializers.ModelSerializer):
    history = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    room_name = serializers.SerializerMethodField()
    room_slug = serializers.SerializerMethodField()

    class Meta:
        model = Chore
        fields = (
            "id",
            "name",
            "slug",
            "room_name",
            "room_slug",
            "get_absolute_url",
            "description",
            "score",
            "frequency",
            "status",
            "get_image",
            "get_thumbnail",
            "history"
        )

    def get_history(self, obj):
        try:
            history_entries = obj.history.entries.all()
            if history_entries:
                return [{
                    "done_at": entry.done_at,
                    "assignee": entry.assignee.name if entry.assignee else None,
                    "difficulty_score": entry.difficulty_score
                } for entry in history_entries]
            return []
        except History.DoesNotExist:
            return None

    def get_status(self, obj):
        try:
            latest_entry = obj.history.entries.order_by('-done_at').first()
            if latest_entry:
                latest_done_at = latest_entry.done_at
                current_timestamp = timezone.now()
                next_deadline = latest_done_at + obj.frequency
                return max(1 - ((current_timestamp - latest_done_at) / (next_deadline - latest_done_at)), 0)
            return 0
        except History.DoesNotExist:
            print(f"No history found for {obj=}")
            return None

    def get_room_name(self, obj):
        return obj.room.name

    def get_room_slug(self, obj):
        return obj.room.slug


class RoomSerializer(serializers.ModelSerializer):
    chores = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "slug",
            "chores",
            "get_absolute_url",
        )

    def get_chores(self, obj):
        data = ChoreSerializer(obj.chores, many=True).data

        sorted_data = sorted(
            data,
            key=lambda x: x['status'],
        )
        return sorted_data


class HistoryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryEntry
        fields = (
            'done_at',
            'difficulty_score',
            'history',
            'assignee'
        )
