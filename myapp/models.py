from django.db import models
from datetime import date
from dateutil.relativedelta import relativedelta


class Client(models.Model):
    phone = models.CharField("Телефон", max_length=20, blank=True)
    email = models.EmailField("Электронная почта", blank=True)

    def __str__(self):
        return f"Клиент #{self.pk}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class PassportDetail(models.Model):
    client = models.OneToOneField(
        Client, on_delete=models.CASCADE, related_name='passport',
        verbose_name="Клиент"
    )
    last_name = models.CharField("Фамилия", max_length=100)
    first_name = models.CharField("Имя", max_length=100)
    patronymic = models.CharField("Отчество", max_length=100, blank=True)
    birth_date = models.DateField("Дата рождения")
    registration_address = models.CharField("Адрес регистрации", max_length=255)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    series = models.CharField("Серия паспорта", max_length=10)
    number = models.CharField("Номер паспорта", max_length=20, unique=True)
    issued_by = models.CharField("Кем выдан", max_length=255)
    issued_date = models.DateField("Когда выдан")

    def is_passport_valid(self) -> bool:
        # Проверяем, что паспорт выдан не раньше 14 лет
        milestone_14 = self.birth_date + relativedelta(years=14)
        if self.issued_date < milestone_14:
            return False

        today = date.today()

        # Функция: просрочен ли паспорт после указанного возраста?
        def expired_after(age):
            milestone = self.birth_date + relativedelta(years=age)
            if today > milestone and (today - milestone).days > 90:
                return True
            return False

        # 20 и 45 лет
        if expired_after(20) or expired_after(45):
            return False
        return True

    def __str__(self):
        return f"Паспорт {self.series} {self.number}"

    class Meta:
        verbose_name = "Реквизиты паспорта"
        verbose_name_plural = "Реквизиты паспортов"


class BankDetail(models.Model):
    bic = models.CharField("БИК", max_length=20, unique=True)
    correspondent_account = models.CharField("Корреспондентский счёт", max_length=50)
    inn = models.CharField("ИНН", max_length=20)
    kpp = models.CharField("КПП", max_length=20)
    okpo = models.CharField("ОКПО", max_length=20, blank=True)
    ogrn = models.CharField("ОГРН", max_length=20, blank=True)
    swift = models.CharField("SWIFT‑код", max_length=20, blank=True)
    bank_name = models.CharField("Банк‑получатель", max_length=255)
    address = models.CharField("Юридический адрес банка", max_length=255)
    post_address = models.CharField("Почтовый адрес банка", max_length=255, blank=True)

    def __str__(self):
        return f"{self.bank_name} ({self.bic})"

    class Meta:
        verbose_name = "Реквизиты банка"
        verbose_name_plural = "Реквизиты банков"


class ClientAccountRequisite(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='account_requisites',
        verbose_name="Клиент"
    )
    bank = models.ForeignKey(
        BankDetail, on_delete=models.PROTECT, related_name='client_accounts',
        verbose_name="Банк"
    )
    account_number = models.CharField("Номер счёта", max_length=50, unique=True)

    def __str__(self):
        return f"Счёт {self.account_number}"

    class Meta:
        verbose_name = "Реквизиты счёта клиента"
        verbose_name_plural = "Реквизиты счёта клиентов"


class CardRequisite(models.Model):
    account = models.OneToOneField(
        ClientAccountRequisite, on_delete=models.CASCADE, related_name='card_requisite',
        verbose_name="Реквизиты счёта"
    )
    card_number = models.CharField("Номер карты", max_length=20, unique=True)
    card_type = models.CharField("Тип карты", max_length=50)
    holder_name = models.CharField("Имя владельца", max_length=100)
    expiry_date = models.DateField("Срок действия")
    security_code = models.CharField("Код безопасности", max_length=10)

    def __str__(self):
        return f"Карта {self.card_number}"

    class Meta:
        verbose_name = "Реквизиты карты"
        verbose_name_plural = "Реквизиты карт"


class ClientCard(models.Model):
    account_requisite = models.ForeignKey(
        ClientAccountRequisite, on_delete=models.CASCADE, related_name='cards',
        verbose_name="Реквизиты счёта клиента"
    )
    card_requisite = models.ForeignKey(
        CardRequisite, on_delete=models.CASCADE, related_name='clients',
        verbose_name="Реквизиты карты"
    )

    class Meta:
        verbose_name = "Клиентская карта"
        verbose_name_plural = "Клиентские карты"


class DepositRequisite(models.Model):
    name = models.CharField("Название счёта", max_length=100)
    account_number = models.CharField("Номер счёта", max_length=50, unique=True)
    product_type = models.CharField("Тип депозита (продукт)", max_length=100)
    currency = models.CharField("Валюта", max_length=10)
    balance = models.DecimalField("Сумма на счёте", max_digits=18, decimal_places=2)
    nominal_rate = models.DecimalField("Номинальная ставка", max_digits=5, decimal_places=2)
    current_rate = models.DecimalField("Текущая ставка", max_digits=5, decimal_places=2)
    interest_payout = models.CharField("Проценты выплачиваются", max_length=100)
    status = models.CharField("Текущее состояние", max_length=50)
    max_amount = models.DecimalField("Максимальная сумма", max_digits=18, decimal_places=2, null=True, blank=True)
    min_amount = models.DecimalField("Минимальная сумма", max_digits=18, decimal_places=2, null=True, blank=True)
    open_date = models.DateField("Дата открытия")
    next_accrual_date = models.DateField("Дата следующего начисления")
    close_date = models.DateField("Закрытие счёта", null=True, blank=True)
    visibility = models.CharField("Видимость счёта", max_length=100)

    def __str__(self):
        return f"Депозит {self.account_number}"

    class Meta:
        verbose_name = "Реквизиты депозита клиента"
        verbose_name_plural = "Реквизиты депозитов клиентов"


class ClientDeposit(models.Model):
    account_requisite = models.ForeignKey(
        ClientAccountRequisite, on_delete=models.CASCADE, related_name='deposits',
        verbose_name="Реквизиты счёта клиента"
    )
    deposit_requisite = models.ForeignKey(
        DepositRequisite, on_delete=models.CASCADE, related_name='clients',
        verbose_name="Реквизиты депозита клиента"
    )

    class Meta:
        verbose_name = "Клиентский депозит"
        verbose_name_plural = "Клиентские депозиты"
