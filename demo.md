### Django框架

#### 安装Django和MySQL客户端

```
pip install django
pip install mysqlclient
```

#### 1. 创建Django项目

首先，在 `Open-LLM-VTuber` 目录下创建一个名为 `sakura_django` 的Django项目：

```
cd /path/to/Open-LLM-VTuber
django-admin startproject sakura_django .
```

注意这里使用了`.`来表示在当前目录下创建项目，这样就不会多出一层嵌套的文件夹。



#### 2. 调整Django项目的配置

##### 修改 `manage.py`

打开 `Open-LLM-VTuber/manage.py` 文件，确保内容如下：

```
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sakura_django.settings')  # 确保这里指向正确的 settings 模块
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
```

##### 修改 `settings.py`

打开 `Open-LLM-VTuber/sakura_django/settings.py` 文件，确保以下内容正确：

```
import os

SILENCED_SYSTEM_CHECKS = [
    'models.W036',  # 忽略 MySQL 不支持条件唯一约束的警告
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'your-secret-key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts',  # 确保 accounts 应用已包含
    'allauth.account',
    'allauth.socialaccount',
]

SITE_ID = 1

AUTH_USER_MODEL = 'accounts.CustomUser'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # 开发环境中使用控制台输出邮件
LOGIN_REDIRECT_URL = '/welcome/'
LOGOUT_REDIRECT_URL = '/'

# 配置多个认证后端
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'sakura_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sakura_django.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ai',  # 你的数据库名
        'USER': 'root',  # 你的 MySQL 用户名
        'PASSWORD': '123456',  # 你的 MySQL 密码
        'HOST': 'localhost',  # MySQL 主机地址
        'PORT': '3306',  # MySQL 端口号
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'zh-hans'  # 设置默认语言为简体中文
TIME_ZONE = 'Asia/Shanghai'  # 设置时区为中国
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```



#### 3. 创建Django应用

在 `Open-LLM-VTuber` 目录下创建一个新的Django应用 `accounts`：

```
cd /path/to/Open-LLM-VTuber
python manage.py startapp accounts
```



#### 4. 配置Django应用

##### 创建URL配置

在 `accounts` 应用目录下创建一个 `urls.py` 文件，并定义登录和注册的URL：

```
# accounts/urls.py

from django.urls import path
from .views import login_view, register_view, logout_view

urlpatterns = [
    path('login/', login_view, name='account_login'),
    path('logout/', logout_view, name='account_logout'),
    path('register/', register_view, name='account_register'),
]
```

##### 创建视图函数

在 `accounts/views.py` 中创建登录和注册的视图函数。为了简化示例，我们将使用Django自带的认证系统和表单。 首先，安装 `django-allauth` 库以简化用户认证系统的实现：

```
pip install django-allauth
```

然后在 `accounts/views.py` 中创建视图函数：

```
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('welcome')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def welcome(request):
    return render(request, 'welcome.html')
```

##### 创建模型文件

在 `accounts/models.py` 中创建一个模型文件：

```
# accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)  # 添加 email 字段
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
        verbose_name='user permissions'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # 将 email 添加到必填字段

    class Meta:
        db_table = 'user'
```

##### 创建表单文件

在 `accounts/forms.py` 中创建一个表单文件：

```
# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
```

##### 创建认证文件

在 `accounts/admin.py` 中创建一个认证文件：

```
# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    # 定义要显示的字段
    list_display = ('username', 'email', 'is_staff', 'is_active')
    # 定义搜索字段
    search_fields = ('username', 'email')
    # 定义过滤器
    list_filter = ('is_staff', 'is_active')
    # 定义表单字段
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    # 定义添加用户时的表单字段
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, UserAdmin)
```

##### 创建前端模板

在项目根目录下创建一个 `templates` 目录，然后创建以下模板文件：

- `login.html`
- `register.html`
- `base_generic.html`
- `welcome.html`
- `home.html`

###### 登录模板 (`templates/login.html`)

```
{% extends "base_generic.html" %}

{% block content %}
<h2>登录</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">登录</button>
</form>
{% endblock %}
```

###### 注册模板 (`templates/registration/register.html`)

```
{% extends "base_generic.html" %}

{% block content %}
<h2>注册</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">注册</button>
</form>
{% endblock %}
```

###### 主页模板 (`templates/home.html`)

```
{% extends "base_generic.html" %}

{% block content %}
<h2>主页面</h2>
<a href="{% url 'account_login' %}">登录</a>
<a href="{% url 'account_register' %}">注册</a>
{% endblock %}
```

###### 默认模板 (`templates/base_generic.html`)

```
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}我的主页{% endblock %}</title>
</head>
<body>
    <header>
        <h1>我的主页</h1>
    </header>
    <main>
        {% block content %}
        {% endblock %}
    </main>
    <footer>
        <p>&copy; 2024 My Site</p>
    </footer>
</body>
</html>
```

###### 欢迎模板 (`templates/welcome.html`)

```
{% extends "base_generic.html" %}

{% block content %}
<h2>您好, {{ user.username }}!</h2>
<a href="{% url 'account_logout' %}">退出</a>
{% endblock %}
```



#### 5. 运行Django迁移

创建MySQL数据库 `ai`，然后运行Django迁移以创建必要的数据库表：

```
python manage.py makemigrations
python manage.py migrate
```

####  

#### 6. 启动Django开发服务器

启动Django开发服务器以测试配置是否正确：

```
python manage.py runserver
```

访问 `http://127.0.0.1:8000/` 查看主页页面，访问 `http://127.0.0.1:8000/accounts/login/` 和 `http://127.0.0.1:8000/accounts/register/` 以查看登录和注册页面。
