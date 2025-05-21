from django.urls import path
from .views import TaskListView, TaskUpdateView, TaskReportView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('<int:pk>/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/report/', TaskReportView.as_view(), name='task_report'),
]
