from django import forms
from django.core.exceptions import ValidationError
import re

from .models import (
    PassportDetail, BankDetail,
    ClientAccountRequisite, CardRequisite, ClientCard,
    DepositRequisite, ClientDeposit
)


# ---------- Паспортные данные ----------
class PassportDetailForm(forms.ModelForm):
    class Meta:
        model = PassportDetail
        fields = '__all__'
        exclude = ['client']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={
                'placeholder': '+7(___)___-__-__',
                'autocomplete': 'off',
                'data-mask': 'phone',
            }),
            'series': forms.TextInput(attrs={
                'placeholder': '0000',
                'maxlength': '4',
                'data-mask': 'passport_series',
            }),
            'number': forms.TextInput(attrs={
                'placeholder': '000000',
                'maxlength': '6',
                'data-mask': 'passport_number',
            }),
            'registration_address': forms.TextInput(attrs={
                'placeholder': 'Регистрация (улица, дом, кв.)'
            }),
            'issued_by': forms.TextInput(attrs={
                'placeholder': 'Кем выдан паспорт'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        digits = re.sub(r'[^\d+]', '', phone)
        if not re.fullmatch(r'\+?7\d{10}', digits):
            raise ValidationError('Неверный формат телефона. Должно быть +7XXXXXXXXXX.')
        return digits

    def clean_series(self):
        series = re.sub(r'\D', '', self.cleaned_data.get('series', ''))
        if not re.fullmatch(r'\d{4}', series):
            raise ValidationError('Серия паспорта: ровно 4 цифры.')
        return series

    def clean_number(self):
        number = re.sub(r'\D', '', self.cleaned_data.get('number', ''))
        if not re.fullmatch(r'\d{6}', number):
            raise ValidationError('Номер паспорта: ровно 6 цифр.')
        return number


# ---------- Реквизиты банка ----------
class BankDetailForm(forms.ModelForm):
    class Meta:
        model = BankDetail
        fields = '__all__'
        widgets = {
            'bic': forms.TextInput(attrs={'placeholder': 'БИК'}),
            'correspondent_account': forms.TextInput(attrs={'placeholder': 'Корреспондентский счёт'}),
            'inn': forms.TextInput(attrs={'placeholder': 'ИНН'}),
            'kpp': forms.TextInput(attrs={'placeholder': 'КПП'}),
            'okpo': forms.TextInput(attrs={'placeholder': 'ОКПО'}),
            'ogrn': forms.TextInput(attrs={'placeholder': 'ОГРН'}),
            'swift': forms.TextInput(attrs={'placeholder': 'SWIFT‑код'}),
            'bank_name': forms.TextInput(attrs={'placeholder': 'Банк‑получатель'}),
            'address': forms.TextInput(attrs={'placeholder': 'Юридический адрес'}),
            'post_address': forms.TextInput(attrs={'placeholder': 'Почтовый адрес'}),
        }


# ---------- Реквизиты счёта клиента ----------
class ClientAccountRequisiteForm(forms.ModelForm):
    class Meta:
        model = ClientAccountRequisite
        fields = '__all__'
        widgets = {
            'account_number': forms.TextInput(attrs={'placeholder': 'Номер счёта'}),
        }


# ---------- Реквизиты карты ----------
class CardRequisiteForm(forms.ModelForm):
    class Meta:
        model = CardRequisite
        fields = '__all__'
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'card_number': forms.TextInput(attrs={'placeholder': 'Номер карты'}),
            'security_code': forms.TextInput(attrs={'placeholder': 'CVC/CVV'}),
        }


# ---------- Связь клиент‑карта ----------
class ClientCardForm(forms.ModelForm):
    class Meta:
        model = ClientCard
        fields = '__all__'


# ---------- Реквизиты депозита ----------
class DepositRequisiteForm(forms.ModelForm):
    class Meta:
        model = DepositRequisite
        fields = '__all__'
        widgets = {
            'open_date': forms.DateInput(attrs={'type': 'date'}),
            'next_accrual_date': forms.DateInput(attrs={'type': 'date'}),
            'close_date': forms.DateInput(attrs={'type': 'date'}),
            'balance': forms.NumberInput(attrs={'step': '0.01'}),
            'nominal_rate': forms.NumberInput(attrs={'step': '0.01'}),
            'current_rate': forms.NumberInput(attrs={'step': '0.01'}),
            'max_amount': forms.NumberInput(attrs={'step': '0.01'}),
            'min_amount': forms.NumberInput(attrs={'step': '0.01'}),
        }


# ---------- Связь клиент‑депозит ----------
class ClientDepositForm(forms.ModelForm):
    class Meta:
        model = ClientDeposit
        fields = '__all__'
