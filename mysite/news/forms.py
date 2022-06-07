from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=25, label='Имя пользователя',
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=25, label='Пароль',
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=25, label='Имя пользователя',
                               help_text="Подсказка для примера что бы не сломать свой компуктер...",
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(max_length=25, label='Ваше имя',
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=25, label='Ваша фамилия',
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=25, label='E-mail', widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(max_length=25, label='Пароль',
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(max_length=25, label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    captcha = CaptchaField()

    class Meta:
        """Неизвестно Почему не разрешает использовать виджеты на все поля, кроме поля username.
        В подклассе Meta мы связываем наш   у форму с моделью User"""
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_title(self):
        """
        В этом методе мы получаем уже очищенные данные внутри словаря clean_title по ключу 'title'(это наименование поля).
        Дальше проверка не начинается ли эта строка с цифры. Если начинается, тогда исключение. Если
        """
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title
