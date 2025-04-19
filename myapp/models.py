from django.db import models
from .utils import passport_needs_update

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

    def is_passport_expired(self):
        return passport_needs_update(self.birth_date, self.passport_issue_date)

    def __str__(self):
        return f"{self.last_name} {self.patronymic}"

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


from django.utils.crypto import get_random_string

CURRENCY_CODES = {
    'RUB': '810',
    'USD': '840',
    'EUR': '978',
    'CNY': '156',
}

ACCOUNT_NUMBER_PREFIX = '40803'  # 1-5 цифры фиксированы

class Account(models.Model):
    CURRENCY_CHOICES = [
        ('RUB', 'Рубли'),
        ('USD', 'Доллары'),
        ('EUR', 'Евро'),
        ('CNY', 'Юани'),
    ]

    ACCOUNT_TYPE_CHOICES = [
        ('current', 'Текущий'),
        ('settlement', 'Расчетный'),
        ('credit', 'Кредитный'),
        ('deposit', 'Депозитный'),
        ('budget', 'Бюджетный (соц. выплаты)'),
        ('standard', 'Стандартный расчетный'),
        ('active', 'Активный'),
        ('passive', 'Пассивный'),
    ]

    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True, verbose_name="Номер счета")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='RUB', verbose_name="Валюта")
    account_type = models.CharField(max_length=30, choices=ACCOUNT_TYPE_CHOICES, verbose_name="Тип счета")
    is_legal_entity = models.BooleanField(default=False, verbose_name="Юридическое лицо")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            currency_code = CURRENCY_CODES.get(self.currency, '810')
            rand_digit = get_random_string(length=1, allowed_chars='0123456789')
            fixed_part = f'{ACCOUNT_NUMBER_PREFIX}{currency_code}{rand_digit}0000'

            account_count = Account.objects.count() + 1
            sequential_number = str(account_count).zfill(7)

            self.account_number = fixed_part + sequential_number
        super().save(*args, **kwargs)

from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from .models import Client  # если Client в той же папке
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Photo(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='images/client_foto/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']


# Сигнал для обработки изображения перед его сохранением
@receiver(pre_save, sender=Photo)
def process_image(sender, instance, **kwargs):
    img = Image.open(instance.image)

    # Преобразуем изображение в формат RGB (если оно в другом формате)
    img = img.convert('RGB')

    # Обрезаем изображение до 72x72 пикселей
    img = img.resize((72, 72), Image.Resampling.LANCZOS)

    # Сохраняем изображение обратно в файл
    from io import BytesIO
    from django.core.files.uploadedfile import InMemoryUploadedFile

    # Сохраняем в памяти, а не в файл
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)

    # Перезаписываем изображение в поле image
    instance.image = InMemoryUploadedFile(img_io, None, instance.image.name, 'image/jpeg', img_io.tell(), None)


