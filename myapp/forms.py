from django import forms
from .models import Client, Account
from .models import CURRENCY_CHOICES

# --- Форма для клиента ---
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['full_name', 'birth_date', 'registration_address',
                  'passport_series', 'passport_number', 'passport_issued_date',
                  'passport_issued_by', 'children', 'phone', 'email',
                  'job_title', 'job_place',]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'passport_issued_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_passport_number(self):
        passport_number = self.cleaned_data.get('passport_number')
        if len(passport_number) != 6:  # Проверка на корректную длину номера паспорта (не более 6 символов)
            raise forms.ValidationError("Номер паспорта должен содержать 6 символов.")
        return passport_number

    def clean_passport_series(self):
        passport_series = self.cleaned_data.get('passport_series')
        if len(passport_series) != 4:  # Проверка на корректную длину серии паспорта (не более 4 символов)
            raise forms.ValidationError("Серия паспорта должна содержать 4 символа.")
        return passport_series

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 10:  # Проверка на корректность телефона
            raise forms.ValidationError("Номер телефона должен содержать минимум 10 символов.")
        return phone

# --- Форма для счёта ---
class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['currency', 'purpose']
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
        }

    def clean_currency(self):
        currency = self.cleaned_data.get('currency')
        if currency not in dict(CURRENCY_CHOICES).keys():  # Проверка на корректность валюты
            raise forms.ValidationError("Выберите корректную валюту.")
        return currency

    def clean_purpose(self):
        purpose = self.cleaned_data.get('purpose')
        if len(purpose) < 10:  # Проверка на минимальную длину цели счета
            raise forms.ValidationError("Цель открытия счета должна быть не менее 10 символов.")
        return purpose

