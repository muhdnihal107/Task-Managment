# task_management/users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('admin/login/', views.admin_login_view, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin/logout/', views.admin_logout_view, name='admin_logout'),
    path('superadmin/users/', views.manage_users, name='manage_users'),
    path('superadmin/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('superadmin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('superadmin/users/promote/<int:user_id>/', views.promote_to_admin, name='promote_to_admin'),
    path('superadmin/admins/', views.manage_admins, name='manage_admins'),
    path('superadmin/admins/edit/<int:admin_id>/', views.edit_admin, name='edit_admin'),
    path('superadmin/admins/delete/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    path('superadmin/admins/demote/<int:user_id>/', views.demote_to_user, name='demote_to_user'),
    path('superadmin/tasks/', views.manage_all_tasks, name='manage_all_tasks'),
    path('superadmin/assign-task/', views.assign_task_superadmin, name='assign_task_superadmin'),
    path('admin/assign-users/', views.assign_users, name='assign_users'),
    path('admin/manage-users/', views.manage_assigned_users, name='manage_assigned_users'),
    path('admin/users/<int:user_id>/', views.user_details, name='user_details'),
    path('admin/users/edit/<int:user_id>/', views.edit_assigned_user, name='edit_assigned_user'),
    path('admin/users/delete/<int:user_id>/', views.delete_assigned_user, name='delete_assigned_user'),
    path('admin/my-tasks/', views.my_users_tasks, name='admin_tasks'),
    path('admin/assign-task/', views.assign_task, name='assign_task'),
]