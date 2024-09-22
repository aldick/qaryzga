# Generated by Django 5.1.1 on 2024-09-20 09:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=150, verbose_name='Адрес')),
                ('stage', models.CharField(choices=[('1', 'Упаковка'), ('2', 'Готов к доставке'), ('3', 'Доставляется'), ('4', 'Завершен')], default='1', max_length=20, verbose_name='Этап заказа')),
                ('type_of_payment', models.CharField(choices=[('1', 'Kaspi QR'), ('2', 'Перевод'), ('3', 'Наличные')], max_length=20, verbose_name='Тип оплаты')),
                ('type_of_order', models.CharField(choices=[('1', 'Онлайн'), ('2', 'Оффлайн')], max_length=20, verbose_name='Тип заказа')),
                ('review', models.TextField(blank=True, max_length=200, null=True, verbose_name='Отзыв клиента')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phone_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='clients.client')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='storage.product', verbose_name='Продукт')),
            ],
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['-created_at'], name='orders_orde_created_f0ce29_idx'),
        ),
    ]
