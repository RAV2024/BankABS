# Generated by Django 4.2.16 on 2025-04-16 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=50, verbose_name='Отчество')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
                ('address', models.CharField(max_length=255, verbose_name='Место жительства')),
                ('phone', models.CharField(blank=True, max_length=15, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Электронная почта')),
                ('passport_number', models.CharField(max_length=10, unique=True, verbose_name='Номер паспорта')),
                ('passport_series', models.CharField(max_length=4, verbose_name='Серия паспорта')),
                ('passport_issue_date', models.DateField(verbose_name='Дата выдачи паспорта')),
                ('passport_issued_by', models.CharField(max_length=100, verbose_name='Кем выдан паспорт')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
    ]
