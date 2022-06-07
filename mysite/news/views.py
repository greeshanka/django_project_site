from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from .utils import MyMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gooooood!')
            return redirect('login')
        else:
            messages.error(request, 'WTF?!')

    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', context={'form': form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', context={"form": form})


def user_logout(request):
    logout(request)
    return redirect('login')


class HomeNews(MyMixin, ListView):
    model = News  # Будут получены все данные из модели News Для данной страницы. Заменяет функцию index
    template_name = 'news/index.html'  # дефолтное название шаблона
    context_object_name = 'news'  # дефолтное название объекта в шаблоне
    mixin_prop = 'hello world'
    paginate_by = 3  # Подключение пагинации по 3 записи на стр

    def get_context_data(self, *, object_list=None, **kwargs):
        """Метод объединяет(сливает вместе) данные контекста всех родительских классов с данными текущего класса """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        """Метод для фильтрации данных. Корректировка запроса под получение данных"""
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'  # дефолтное название объекта в шаблоне
    allow_empty = False  # Не разрешает показ пустых списков
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        """Метод объединяет(сливает вместе) данные контекста всех родительских классов с данными текущего класса """
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        """Метод для фильтрации данных"""
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'  # дефолтное название объекта в шаблоне


class CreateNews(LoginRequiredMixin, CreateView):
    """Предназначен для работы с формами. Созданием объектов."""
    form_class = NewsForm  # Связываем с формой
    template_name = 'news/add_news.html'
