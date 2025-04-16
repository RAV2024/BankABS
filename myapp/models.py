from django.db import models
import random

# --- Константы ---
CURRENCY_CODES = {
    'RUB': '810',
    'USD': '840',
    'EUR': '978',
    'CNY': '156'
}

CURRENCY_CHOICES = [
    ('RUB', 'Рубли'),
    ('USD', 'Доллары'),
    ('EUR', 'Евро'),
    ('CNY', 'Юани'),

]


# --- Клиент ---
class Client(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    birth_date = models.DateField("Дата рождения")
    registration_address = models.CharField("Прописка", max_length=255)
    passport_series = models.CharField("Серия паспорта", max_length=10)
    passport_number = models.CharField("Номер паспорта", max_length=10)
    passport_issued_date = models.DateField("Дата выдачи паспорта")
    passport_issued_by = models.CharField("Кем выдан паспорт", max_length=255)
    children = models.PositiveIntegerField("Количество детей", default=0)
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Электронная почта")
    account_purpose = models.TextField("Цель открытия счёта")
    job_title = models.CharField("Должность", max_length=255)
    job_place = models.CharField("Место работы", max_length=255)
    currency = models.CharField("Валюта", max_length=3, choices=CURRENCY_CHOICES)

    def __str__(self):
        return self.full_name


# --- Счёт ---
class Account(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='accounts')
    currency = models.CharField("Валюта", max_length=3, choices=CURRENCY_CHOICES)
    purpose = models.TextField("Цель счёта")
    account_number = models.CharField("Номер счёта", max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField("Дата открытия счёта", auto_now_add=True)  # Дата открытия счёта

    def generate_account_number(self):
        start = '40817'  # Физическое лицо-резидент
        currency_code = CURRENCY_CODES.get(self.currency, '810')
        control_digit = str(random.randint(0, 9))
        branch_number = '0175'  # первое- 01, отделение в Заб. крае 75

        # Реальный порядковый номер — на основе ID
        if Account.objects.exists():
            latest_id = Account.objects.latest('id').id + 1
        else:
            latest_id = 1
        serial_number = f"{latest_id:07}"

        return f"{start}{currency_code}{control_digit}{branch_number}{serial_number}"

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Счёт {self.account_number} для {self.client.full_name}"

