from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Assignee
from .serializers import AssigneeSerializer


class AssigneeList(APIView):
    def get(self, request, format=None):
        assignees = Assignee.objects.all()
        serializer = AssigneeSerializer(assignees, many=True)
        return Response(serializer.data)
