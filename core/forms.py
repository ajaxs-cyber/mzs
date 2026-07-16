from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        min_length=3,
        max_length=20,
        error_messages={
            'required': '请输入用户名',
            'min_length': '用户名至少3个字符',
            'max_length': '用户名最多20个字符',
        },
        widget=forms.TextInput(attrs={'placeholder': '3-20位字母/数字/下划线', 'class': 'f-input'}),
    )
    email = forms.EmailField(
        label="邮箱",
        error_messages={
            'required': '请输入邮箱',
            'invalid': '请输入有效的邮箱地址',
        },
        widget=forms.EmailInput(attrs={'placeholder': '用于找回密码', 'class': 'f-input'}),
    )
    password = forms.CharField(
        label="密码",
        min_length=6,
        max_length=30,
        widget=forms.PasswordInput(attrs={'placeholder': '至少6位密码', 'class': 'f-input'}),
        error_messages={
            'required': '请输入密码',
            'min_length': '密码至少6位',
        },
    )
    password_confirm = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={'placeholder': '再次输入密码', 'class': 'f-input'}),
        error_messages={'required': '请确认密码'},
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username.replace('_', '').replace('-', '').isalnum():
            raise forms.ValidationError('用户名只能包含字母、数字、下划线和连字符')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('该用户名已被使用')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册')
        return email

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get('password')
        pwc = cleaned.get('password_confirm')
        if pw and pwc and pw != pwc:
            self.add_error('password_confirm', '两次输入的密码不一致')
        return cleaned


class ProfileForm(forms.Form):
    bio = forms.CharField(
        label="个人简介",
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={'placeholder': '介绍一下自己...', 'rows': 3, 'class': 'f-input'}),
    )
    phone = forms.CharField(
        label="手机号",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '选填', 'class': 'f-input'}),
    )
