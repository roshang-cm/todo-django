from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import JsonResponse
from todo.models import Todo, UserProfile
from todo.forms import AddTodoForm, ChangeStatusForm

import pdb
# Create your views here.


@login_required(login_url="todo:login_view")
def index(request):
    if not request.user.is_authenticated:
        return redirect('todo:login_view')
    logged_in_user = request.user
    todos = Todo.objects.filter(user=logged_in_user)
    new_todos = todos.filter(status='new')
    working_todos = todos.filter(status='working')
    done_todos = todos.filter(status='done')
    context = {
        'user': logged_in_user,
        'change_status_form': ChangeStatusForm(),
        'add_todo_form': AddTodoForm(),
        'new_todos': list(new_todos),
        'working_todos': list(working_todos),
        'done_todos': list(done_todos)
    }
    return render(request, 'todo/index.html', context)


def signup(request):
    logout(request)
    if request.method == 'POST':
        username, password = request.POST.get(
            'username', None), request.POST.get('password', None)
        try:
            if username is not None and password is not None:
                new_user = UserProfile.objects.create_user(
                    username=username, password=password)
                auth_login(request, new_user)
                return redirect('todo:index_view')
            else:
                messages.error(
                    request, 'Username / Password cannot be empty. Please provide proper details')
                return redirect('todo:signup_view')
        except Exception as e:
            messages.error(request, f'Error during signup: {e}')
            return redirect('todo:signup_view')
    context = {
        'user': None
    }
    return render(request, 'todo/signup.html', context)


def login(request):
    logout(request)
    if request.method == 'POST':
        username, password = request.POST.get(
            'username'), request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid credentials, please try again.')
        else:
            auth_login(request, user)
            return redirect('todo:index_view')
    context = {
        'user': None
    }
    return render(request, 'todo/login.html', context)


@login_required(login_url="todo:login_view")
@require_POST
def add_todo(request):
    todo_text = request.POST.get('todo_text', None)
    logged_in_user = request.user
    if Todo.objects.filter(text=todo_text, user=logged_in_user).count() != 0:
        messages.error(
            request, 'A todo with this text already exists. Try some other text.')
    else:
        new_todo = Todo(text=todo_text, user=logged_in_user)
        new_todo.save()
    return redirect('todo:index_view')


@login_required(login_url="todo:login_view")
@require_POST
def change_status(request, todo_id):
    req_data = request.POST
    new_status = req_data.get('status', None)
    if new_status is None:
        return JsonResponse({'success': False, 'error': 'status is missing in request'}, status=400)
    todo_to_change = get_object_or_404(Todo, pk=todo_id)
    todo_to_change.status = new_status
    todo_to_change.save()
    return redirect('todo:index_view')


@login_required(login_url="todo:login_view")
@require_POST
def delete_todo(request, todo_id):
    todo_to_delete = get_object_or_404(Todo, pk=todo_id)
    todo_to_delete.delete()
    return redirect('todo:index_view')
