from django.db import models

class Client(models.Model):
    # Личные данные клиента
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество', blank=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    birth_date = models.DateField(verbose_name='Дата рождения')
    address = models.CharField(max_length=255, verbose_name='Место жительства')

    # Контактные данные
    phone = models.CharField(max_length=16, verbose_name='Телефон', blank=True)
    email = models.EmailField(max_length=254, verbose_name='Электронная почта', blank=True)

    # Документы, удостоверяющие личность
    passport_series = models.CharField(max_length=4, verbose_name='Серия паспорта')
    passport_number = models.CharField(max_length=6, verbose_name='Номер паспорта', unique=True)
    passport_issue_date = models.DateField(verbose_name='Дата выдачи паспорта')
    passport_issued_by = models.CharField(max_length=100, verbose_name='Кем выдан паспорт')

    def __str__(self):
        return f"{self.last_name} {self.patronymic}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'



class Account(models.Model):
    ACCOUNT_TYPE_CHOICES_INDIVIDUAL = [
        ('current', 'Текущий'),
        ('credit', 'Кредитный'),
        ('deposit', 'Депозитный'),
        ('saving', 'Накопительный'),
        ('budget', 'Бюджетный'),
    ]

    ACCOUNT_TYPE_CHOICES_LEGAL = [
        ('settlement', 'Расчетный'),
        ('currency', 'Валютный'),
        ('correspondent', 'Корреспондентский'),
        ('trust', 'Доверительного управления'),
        ('special', 'Специальный'),
        ('deposit', 'Депозитный'),
        ('budget', 'Бюджетный'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True, verbose_name="Номер счета")
    is_legal_entity = models.BooleanField(default=False, verbose_name="Юридическое лицо")
    account_type = models.CharField(max_length=30, verbose_name="Тип счета")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_number} ({self.get_account_type_display()})"

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'
