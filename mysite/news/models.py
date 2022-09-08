from django.db import models
from django.urls import reverse


class News(models.Model):  # Вторичная модель
    # django автоматом создаёт первичный ключ id
    title = models.CharField(max_length=100, verbose_name='Наименование')
    content = models.TextField(blank=True,
                               verbose_name='Контент')  # атрибут blank означает что данное поле необязательно к заполнению
    created_et = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_et = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/', verbose_name='Фото',
        blank=True)  # Мы можем указать куда мы загрузим файл атрибутом upload_to. Разбиваем загрузку по папкам исходя времени
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано')  # Атрибут default отвечает за "значение по умолчанию"
    category = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name='Категория')  # Прописываем связь
    count_views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('view_news', kwargs={"pk": self.pk})

    class Meta:  # Первичная модель
        verbose_name = 'Новость'  # название в ед. числе
        verbose_name_plural = 'Новости'  # название в мн. числе
        ordering = ['-created_et']  # Сортировака новостей

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name="Наименование Категории", db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'  # название в ед. числе
        verbose_name_plural = 'Категории'  # название в мн. числе
        ordering = ['title']  # Сортировака категорий
