from datetime import timedelta

from django.http import Http404
from django.utils import timezone
from django.utils.text import slugify

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Chore, Room, HistoryEntry, History
from .serializers import ChoreSerializer, RoomSerializer, HistoryEntrySerializer
from assignee.models import Assignee


class UrgentChoreList(APIView):
    def get(self, request, format=None):
        chores = Chore.objects.all()
        serializer = ChoreSerializer(chores, many=True)
        data = serializer.data

        sorted_data = sorted(
            data,
            key=lambda x: x['status'],
        )

        return Response(sorted_data)


class ChoreDetail(APIView):
    def get_object(self, room_slug, chore_slug):
        try:
            return Chore.objects.filter(room__slug=room_slug).get(slug=chore_slug)
        except Chore.DoesNotExist:
            raise Http404

    def get(self, request, room_slug, chore_slug, format=None):
        chore = self.get_object(room_slug, chore_slug)
        serializer = ChoreSerializer(chore)
        return Response(serializer.data)


class RoomDetail(APIView):
    def get_object(self, room_slug):
        try:
            return Room.objects.get(slug=room_slug)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, room_slug, format=None):
        room = self.get_object(room_slug)
        serializer = RoomSerializer(room)
        return Response(serializer.data)


@api_view(['GET'])
def rooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)



@api_view(['POST'])
def create_chore(request):
    room_slug = request.data.get('room_slug')
    try:
        room = Room.objects.get(slug=room_slug)
    except Room.DoesNotExist:
        return Response({'error': f'Room {room_slug} not found.'}, status=status.HTTP_404_NOT_FOUND)

    FREQUENCY_OPTIONS = [timedelta(weeks=1), timedelta(weeks=2), timedelta(weeks=3), timedelta(weeks=4), timedelta(weeks=8), timedelta(weeks=26)]
    chore = Chore(
        name=request.data.get('name'),
        description=request.data.get('description'),
        score=request.data.get('score'),
        frequency=FREQUENCY_OPTIONS[int(request.data.get('frequency'))],
        room=room,
        slug=slugify(request.data.get('name'))
    )
    chore.save()
    History(chore=chore).save()

    serializer = ChoreSerializer(chore)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def complete_chore(request):
    chore_id = request.data.get('chore_id')
    assignee_id = request.data.get('assignee_id')
    print(f"Chore ID - Assignee ID: {chore_id} - {assignee_id}")

    try:
        chore = Chore.objects.get(id=chore_id)
    except Chore.DoesNotExist:
        return Response({'error': f'Chore {chore_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        assignee = Assignee.objects.get(id=assignee_id)
    except Assignee.DoesNotExist:
        return Response({'error': f'Assignee {assignee_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

    history_entry = HistoryEntry(
        done_at=timezone.now(),
        difficulty_score=chore.score,
        history=chore.history,
        assignee=assignee).save()

    serializer = HistoryEntrySerializer(history_entry)
    return Response(serializer.data, status=status.HTTP_200_OK)
