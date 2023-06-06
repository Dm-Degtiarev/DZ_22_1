# Generated by Django 4.2.1 on 2023-06-06 07:46

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_product_product_create_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_create_date',
            field=models.DateField(default=datetime.date(2023, 6, 6), verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_last_upd_dt',
            field=models.DateField(default=datetime.date(2023, 6, 6), verbose_name='Дата последнего изменения'),
        ),
        migrations.CreateModel(
            name='ProductVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(max_length=10, verbose_name='Номер версии')),
                ('name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Назваине версии')),
                ('actual_flg', models.BooleanField(verbose_name='Признак текущей версии')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Идентификатор продукта')),
            ],
            options={
                'verbose_name': 'Версия продукта',
                'verbose_name_plural': 'Версии продуктов',
            },
        ),
    ]
