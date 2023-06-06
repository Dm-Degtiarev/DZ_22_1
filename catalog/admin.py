from django.contrib import admin
from catalog.models import Product, ProductVersion, Category, Contacts, Blog


# admin.site.register(Product)  -   по дефолту - __str__

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_price', 'product_category', 'product_status')
    search_fields = ('product_name', 'product_info')
    list_filter = ('product_category', 'product_price')
    list_display_links = ('product_name',) # Задаем поле по которому открываем редактироваине объекта


@admin.register(ProductVersion)
class ProductVersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'number', 'name', 'actual_flg')
    search_fields = ('name',)
    list_filter = ('actual_flg',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name')
    search_fields = ('id', 'category_name')
    list_filter = ('category_name',)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_name', 'contact_number')
    search_fields = ('id', 'contact_name', 'contact_number')
    list_filter = ('contact_name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog_name', 'blog_views_count', 'blog_slug')
    search_fields = ('blog_name', 'blog_content')
    list_filter = ('blog_create_date',)
