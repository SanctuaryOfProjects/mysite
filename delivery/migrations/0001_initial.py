# Generated by Django 4.0.4 on 2024-05-08 21:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100, verbose_name='ФИО')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('work_phone', models.CharField(max_length=11, verbose_name='Телефон')),
                ('photo', models.FileField(upload_to='couriers/', verbose_name='Фото')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Логин')),
                ('password', models.CharField(max_length=50, verbose_name='Пароль')),
                ('is_courier', models.BooleanField(default=True, verbose_name='Курьер')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Курьер',
                'verbose_name_plural': 'Курьеры',
            },
        ),
        migrations.CreateModel(
            name='Establishment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('photo', models.FileField(upload_to='est/', verbose_name='Фото')),
                ('adress', models.CharField(max_length=120, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=11, verbose_name='Телефон')),
                ('verification', models.BooleanField(default=False, verbose_name='Верификация')),
                ('bin', models.CharField(max_length=20, verbose_name='БИН')),
                ('work_schedule', models.CharField(max_length=100, verbose_name='График работы')),
                ('legal_info', models.TextField(verbose_name='Юридическая информация')),
                ('documentation', models.FileField(upload_to='documentation/', verbose_name='Документация')),
            ],
            options={
                'verbose_name': 'Заведение',
                'verbose_name_plural': 'Заведения',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('start_time', models.TimeField(verbose_name='Начало смены')),
                ('end_time', models.TimeField(verbose_name='Конец смены')),
                ('skip', models.BooleanField(blank=True, default=False, verbose_name='Пропуск')),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.courier', verbose_name='Курьер')),
                ('est', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.establishment', verbose_name='Заведение')),
            ],
            options={
                'verbose_name': 'График работы',
                'verbose_name_plural': 'График работы',
            },
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('working_hours', models.PositiveIntegerField(verbose_name='Часы работы')),
                ('money_per_hour', models.PositiveIntegerField(verbose_name='З/П в час')),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.courier', verbose_name='Курьер')),
            ],
            options={
                'verbose_name': 'Зарплата',
                'verbose_name_plural': 'Зарплата',
            },
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('penalty_type', models.CharField(max_length=100, verbose_name='Тип штрафа')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('reason', models.TextField(verbose_name='Причина')),
                ('courier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.courier', verbose_name='Курьер')),
            ],
            options={
                'verbose_name': 'Штраф',
                'verbose_name_plural': 'Штрафы',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipient', models.CharField(max_length=100, verbose_name='Получатель')),
                ('status', models.CharField(choices=[('Обработан', 'Обработан'), ('Доставляется', 'Доставляется'), ('Доставлен', 'Доставлен'), ('Отменен', 'Отменен')], default='Обработан', max_length=20, verbose_name='Статус')),
                ('origin', models.CharField(max_length=100, verbose_name='Точка отправления')),
                ('destination', models.CharField(max_length=100, verbose_name='Точка назначения')),
                ('route_link', models.URLField(blank=True, verbose_name='Ссылка на маршрут')),
                ('courier_latitude', models.FloatField(blank=True, null=True, verbose_name='Широта курьера')),
                ('courier_longitude', models.FloatField(blank=True, null=True, verbose_name='Долгота курьера')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время заказа')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Комментарий')),
                ('courier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='delivery.courier', verbose_name='Курьер заказа')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_orders', to='delivery.establishment', verbose_name='Отправитель')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='EstCouriers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='establishments', to='delivery.courier', verbose_name='Курьер')),
                ('establishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.establishment', verbose_name='Заведение')),
            ],
            options={
                'verbose_name': 'Курьеры заведения',
                'verbose_name_plural': 'Курьеры заведения',
            },
        ),
    ]
