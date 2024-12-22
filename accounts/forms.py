from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("用户名已存在")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("邮箱已存在")
        return email

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class CustomPasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label='用户名')
    email = forms.EmailField(required=True, label='邮箱')
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='新密码')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='确认密码')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if username and email:
            try:
                user = CustomUser.objects.get(username=username, email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("用户名或邮箱不匹配")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("新密码和确认密码不一致")

        return cleaned_data