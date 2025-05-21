from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from tasks.models import Task
from .models import UserAssignment



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "user successfully registered"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'You are not authorized to access the admin panel.')
                return redirect('admin_login')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_dashboard_view(request):
    return render(request, 'users/dashboard.html', {'user': request.user})

def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')

def is_superadmin(user):
    return user.is_superuser

def is_admin(user):
    return user.is_staff and not user.is_superuser

# SuperAdmin Views
@login_required
@user_passes_test(is_superadmin)
def manage_users(request):
    users = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'admin_panel/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_superadmin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        user.username = username
        user.email = email
        user.save()
        messages.success(request, f"{user.username} updated successfully.")
        return redirect('manage_users')
    return render(request, 'admin_panel/edit_user.html', {'user': user})

@login_required
@user_passes_test(is_superadmin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"{username} deleted successfully.")
        return redirect('manage_users')
    return render('manage_users')

@login_required
@user_passes_test(is_superadmin)
def promote_to_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_staff = True
    user.save()
    messages.success(request, f"{user.username} promoted to Admin.")
    return redirect('manage_users')

@login_required
@user_passes_test(is_superadmin)
def manage_admins(request):
    admins = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'admin_panel/manage_admins.html', {'admins': admins})

@login_required
@user_passes_test(is_superadmin)
def edit_admin(request, admin_id):
    admin = get_object_or_404(User, id=admin_id, is_staff=True, is_superuser=False)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        admin.username = username
        admin.email = email
        admin.save()
        messages.success(request, f"{admin.username} updated successfully.")
        return redirect('manage_admins')
    return render(request, 'admin_panel/edit_admin.html', {'admin': admin})

@login_required
@user_passes_test(is_superadmin)
def delete_admin(request, admin_id):
    admin = get_object_or_404(User, id=admin_id, is_staff=True, is_superuser=False)
    if request.method == 'POST':
        username = admin.username
        admin.delete()
        messages.success(request, f"{username} deleted successfully.")
        return redirect('manage_admins')
    return redirect('manage_admins')

@login_required
@user_passes_test(is_superadmin)
def demote_to_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_staff = False
    user.is_superuser = False
    user.save()
    messages.success(request, f"{user.username} demoted to User.")
    return redirect('manage_admins')

@login_required
@user_passes_test(is_superadmin)
def manage_all_tasks(request):
    tasks = Task.objects.all()
    return render(request, 'admin_panel/all_tasks.html', {'tasks': tasks})

@login_required
@user_passes_test(is_superadmin)
def assign_task_superadmin(request):
    users = User.objects.filter(is_staff=False)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        assigned_to_id = request.POST['assigned_to']
        assigned_to = User.objects.get(id=assigned_to_id)
        Task.objects.create(title=title, description=description, due_date=due_date, assigned_to=assigned_to)
        messages.success(request, 'Task assigned successfully.')
        return redirect('manage_all_tasks')
    return render(request, 'admin_panel/assign_task_superadmin.html', {'users': users})

# Admin Views
@login_required
@user_passes_test(is_admin)
def assign_users(request):
    available_users = User.objects.filter(is_staff=False, is_superuser=False).exclude(assigned_to__admin=request.user)
    if request.method == 'POST':
        user_ids = request.POST.getlist('users')
        for user_id in user_ids:
            user = get_object_or_404(User, id=user_id)
            UserAssignment.objects.create(admin=request.user, user=user)
        messages.success(request, 'Users assigned successfully.')
        return redirect('manage_assigned_users')
    return render(request, 'admin_panel/assign_users.html', {'available_users': available_users})

@login_required
@user_passes_test(is_admin)
def manage_assigned_users(request):
    assigned_users = User.objects.filter(assigned_to__admin=request.user)
    return render(request, 'admin_panel/manage_assigned_users.html', {'assigned_users': assigned_users})

@login_required
@user_passes_test(is_admin)
def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id, assigned_to__admin=request.user)
    tasks = Task.objects.filter(assigned_to=user)
    return render(request, 'admin_panel/user_details.html', {'user': user, 'tasks': tasks})

@login_required
@user_passes_test(is_admin)
def edit_assigned_user(request, user_id):
    user = get_object_or_404(User, id=user_id, assigned_to__admin=request.user)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        user.username = username
        user.email = email
        user.save()
        messages.success(request, f"{user.username} updated successfully.")
        return redirect('manage_assigned_users')
    return render(request, 'admin_panel/edit_assigned_user.html', {'user': user})

@login_required
@user_passes_test(is_admin)
def delete_assigned_user(request, user_id):
    user = get_object_or_404(User, id=user_id, assigned_to__admin=request.user)
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"{username} deleted successfully.")
        return redirect('manage_assigned_users')
    return redirect('manage_assigned_users')

@login_required
@user_passes_test(is_admin)
def my_users_tasks(request):
    tasks = Task.objects.filter(assigned_to__in=User.objects.filter(assigned_to__admin=request.user))
    return render(request, 'admin_panel/admin_tasks.html', {'tasks': tasks})

@login_required
@user_passes_test(is_admin)
def assign_task(request):
    users = User.objects.filter(assigned_to__admin=request.user)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        assigned_to_id = request.POST['assigned_to']
        assigned_to = User.objects.get(id=assigned_to_id, assigned_to__admin=request.user)
        Task.objects.create(title=title, description=description, due_date=due_date, assigned_to=assigned_to)
        messages.success(request, 'Task assigned successfully.')
        return redirect('admin_tasks')
    return render(request, 'admin_panel/assign_task.html', {'users': users})