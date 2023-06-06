from django.db import models
from pytils.translit import slugify
from datetime import date


NULLABLE = {'null': True, 'blank': True}

class Product(models.Model):
    #Задаем статус, и прописываем все варианты для данного атрибута. active - хранится в базе, Активный - отображается в админке
    STATUS = (
        ('active', 'Активный'),
        ('archive', 'В архиве'),
        ('await', 'На модерации')
    )

    product_name = models.CharField(max_length=200, verbose_name='Наименование')
    product_info = models.CharField(max_length=300, verbose_name='Описание')
    product_image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    product_category = models.CharField(max_length=200, verbose_name='Категория')
    product_price = models.FloatField(max_length=20, verbose_name='Цена')
    product_create_date = models.DateField(verbose_name='Дата создания', default=date.today())
    product_last_upd_dt = models.DateField(verbose_name='Дата последнего изменения', default=date.today())
    product_status = models.CharField(max_length=10, choices=STATUS, default='active', verbose_name='Статус')

    def __str__(self):
        return f"{self.pk} - {self.product_name}"

    # def save(self, *args, **kwargs):
    #     """При изменении товара архивирует предудыщую версию, а новую делает актуальной. счетчик версии +1"""
    #     if self.pk:
    #         ProductVersion.objects.filter(product=self).update(actual_flg=False)
    #     super().save(*args, **kwargs)
    #
    #     latest_version = ProductVersion.objects.filter(product=self).order_by('-number').first()
    #     number = latest_version.number if latest_version else 0
    #
    #     ProductVersion.objects.create(
    #         product=self,
    #         number=number,
    #         actual_flg=True,
    #         name=f'Изменено {date.today()}'
    #     )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductVersion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    number = models.IntegerField(max_length=10, verbose_name='Номер версии', **NULLABLE)
    name = models.CharField(max_length=150, verbose_name='Назваине версии', **NULLABLE)
    actual_flg = models.BooleanField(verbose_name='Признак текущей версии')

    def __str__(self):
        return f"ID: {self.product} - {self.name} - {self.actual_flg}"

    class Meta:
        verbose_name = 'Версия продукта'
        verbose_name_plural = 'Версии продуктов'


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Наименование')
    category_info = models.CharField(max_length=300, verbose_name='Описание категории')

    # created_dt = models.DateField(verbose_name='Дата создания', **NULLABLE)

    def __str__(self):
        return f"{self.pk} - {self.category_name}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Contacts(models.Model):
    contact_name = models.CharField(max_length=100, verbose_name='Наименование')
    contact_number = models.CharField(max_length=17, verbose_name='Телефонный номер')

    def __str__(self):
        return f"{self.pk} - {self.contact_name}"

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Blog(models.Model):
    blog_name = models.CharField(max_length=200, verbose_name='Заголовок', unique=True)
    blog_slug = models.CharField(max_length=100, verbose_name='Slug', unique=True, **NULLABLE)
    blog_content = models.TextField(verbose_name='Содержимое', **NULLABLE)
    blog_image = models.ImageField(upload_to='blog/', verbose_name='Превью (изображение)', **NULLABLE)
    blog_create_date = models.DateField(verbose_name='Дата создания', default=date.today)
    blog_publicate_flg = models.BooleanField(verbose_name='Признак публикации', default=True)
    blog_views_count = models.IntegerField(verbose_name='Количество просмотров', default=0)
    
    def __str__(self):
        return self.blog_name

    def save(self, *args, **kwargs):
        self.blog_slug = slugify(self.blog_name)[:100]
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.blog_publicate_flg = False
        self.save()

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'