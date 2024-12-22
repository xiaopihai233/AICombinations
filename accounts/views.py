import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm
from .models import CustomUser

import json
from django.http import JsonResponse
from django.shortcuts import render


def get_history(request):
    if request.method == 'GET':
        # 使用绝对路径读取根目录下的 mem.json 文件
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'mem.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse(data, safe=False)

def history_view(request):
    return render(request, 'history.html')
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 显式指定认证后端
            backend = 'django.contrib.auth.backends.ModelBackend'
            user.backend = backend
            login(request, user, backend=backend)
            return redirect('welcome')
        else:
            # 添加调试信息，打印表单错误
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('welcome')
        else:
            # 添加调试信息，打印表单错误
            print(form.errors)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home_view(request):
    return render(request, 'home.html')

def welcome(request):
    return render(request, 'welcome.html')

def reset_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password1']

            user = CustomUser.objects.get(username=username, email=email)
            user.set_password(new_password)
            user.save()

            return redirect('account_login')  # 重定向到登录页面
        else:
            # 添加调试信息，打印表单错误
            print(form.errors)
    else:
        form = CustomPasswordResetForm()
    return render(request, 'reset_password.html', {'form': form})