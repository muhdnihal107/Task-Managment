from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer,TaskUpdateSerializer
from django.shortcuts import get_object_or_404

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({"detail": "Task not found"}, status=404)

        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Task updated successfully"})
        return Response(serializer.errors, status=400)


class TaskReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"detail": "Unauthorized"}, status=403)

        try:
            task = Task.objects.get(pk=pk, status='Completed')
        except Task.DoesNotExist:
            return Response({"detail": "Completed task not found"}, status=404)

        return Response({
            "task": task.title,
            "assigned_to": task.assigned_to.username,
            "completion_report": task.completion_report,
            "worked_hours": task.worked_hours,
        })