from django import forms
from .models import Client,Account
from django.core.exceptions import ValidationError
import re

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'passport_issue_date': forms.DateInput(attrs={'type': 'date'}),
            'phone': forms.TextInput(attrs={
                'placeholder': '+7(___)___-__-__',
                'autocomplete': 'off',
                'data-mask': 'phone',  # Флаги для JS
            }),
            'passport_series': forms.TextInput(attrs={
                'placeholder': '0000',
                'maxlength': '4',
                'data-mask': 'passport_series',
            }),
            'passport_number': forms.TextInput(attrs={
                'placeholder': '000000',
                'maxlength': '6',
                'data-mask': 'passport_number',
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Читинская область г. Чита, ул. Ленина, д. 10, кв. 15'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@email.ru'
            }),
            'passport_issued_by': forms.TextInput(attrs={
                'placeholder': 'ОТДЕЛОМ УФМС РОССИИ ПО Г. ЧИТЕ'
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        phone = re.sub(r'[^\d+]', '', phone)
        if not re.fullmatch(r'\+?7\d{10}', phone):
            raise ValidationError('Введите номер телефона в формате +7 (999) 999-99-99.')
        return phone

    def clean_passport_series(self):
        series = self.cleaned_data.get('passport_series', '')
        digits = re.sub(r'\D', '', series)
        if not re.fullmatch(r'\d{4}', digits):
            raise ValidationError("Серия паспорта должна состоять из 4 цифр.")
        return digits

    def clean_passport_number(self):
        number = self.cleaned_data.get('passport_number', '')
        digits = re.sub(r'\D', '', number)
        if not re.fullmatch(r'\d{6}', digits):
            raise ValidationError("Номер паспорта должен состоять из 6 цифр.")
        return digits

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['currency', 'account_type']




