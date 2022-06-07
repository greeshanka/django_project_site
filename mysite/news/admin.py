from django.utils.safestring import mark_safe
from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import News, Category


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ['id', 'title', 'created_et', 'updated_et', 'is_published', 'category',
                    'get_photo']  # Поля которые доступны нам
    list_display_links = ['id', 'title']
    search_fields = ['title', 'content']  # Поля по которым можно производить поиск
    list_editable = ['is_published']  # Поля с галочкой. Изменение сразу в админке
    list_filter = ['is_published', 'category']  # По каким полям можем фильтровать
    fields = ['title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'count_views', 'created_et',
              'updated_et']  # Отображается в каждой новости(записи)
    readonly_fields = ['count_views', 'created_et', 'updated_et', 'get_photo']  # Без редактирования для поля fields

    @staticmethod
    def get_photo(obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="133">')
        else:
            return "Нет фото"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    search_fields = ['title']


admin.site.register(News,
                    NewsAdmin)  # Очерёдность имеет важность! Сначала регистрируем модель, потом мы регистрируем класс который её настроит
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
