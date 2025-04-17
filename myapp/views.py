from datetime import date
import random
from dateutil.relativedelta import relativedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from .models import (
    Client, PassportDetail, BankDetail,
    ClientAccountRequisite, CardRequisite, ClientCard,
    DepositRequisite, ClientDeposit
)
from .forms import (
    PassportDetailForm, CardRequisiteForm, DepositRequisiteForm
)


def home(request):
    return render(request, 'home.html')


class ClientListView(ListView):
    model = Client
    template_name = 'clients_list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        qs = super().get_queryset().select_related('passport')
        series = self.request.GET.get('series', '').strip()
        number = self.request.GET.get('number', '').strip()
        if series:
            qs = qs.filter(passport__series__icontains=series)
        if number:
            qs = qs.filter(passport__number__icontains=number)
        return qs


class ClientCreateView(CreateView):
    model = PassportDetail
    form_class = PassportDetailForm
    template_name = 'client_form.html'

    def form_valid(self, form):
        # 1) создаём пустого клиента
        client = Client.objects.create()
        # 2) сохраняем паспортные данные, привязав client
        passport = form.save(commit=False)
        passport.client = client
        passport.save()

        # 3) генерируем счёт
        def gen_account_number():
            return '40817' + ''.join(str(random.randint(0, 9)) for _ in range(13))

        # Привязываем первый попавшийся банк (или создайте банк-«по-умолчанию»
        bank, created = BankDetail.objects.get_or_create(
            bic='000000000',  # какой-то уникальный BIC для «дефолта»
            defaults={
                'correspondent_account': '00000000000000000000',
                'inn': '000000000000',
                'kpp': '000000000',
                'bank_name': 'Дефолтный Банк',
                'address': 'г. Москва, ул. Пушкина, д. 1',
                'post_address': '',
            }
        )
        ClientAccountRequisite.objects.create(
            client=client,
            bank=bank,
            account_number=gen_account_number()
        )
        return redirect('client_detail', pk=client.pk)


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client_detail.html'
    context_object_name = 'client'


class CardCreateView(CreateView):
    model = CardRequisite
    form_class = CardRequisiteForm
    template_name = 'card_form.html'

    def get_initial(self):
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        account_req = client.account_requisites.first()
        return {'account': account_req}

    def form_valid(self, form):
        card = form.save()
        ClientCard.objects.create(
            account_requisite=card.account,
            card_requisite=card
        )
        return redirect('client_detail', pk=card.account.client.pk)


class DepositCreateView(CreateView):
    model = DepositRequisite
    form_class = DepositRequisiteForm
    template_name = 'deposit_form.html'

    def form_valid(self, form):
        deposit = form.save()
        client = get_object_or_404(Client, pk=self.kwargs['pk'])
        # Привяжем к тому же счёту
        acct = client.account_requisites.first()
        ClientDeposit.objects.create(
            account_requisite=acct,
            deposit_requisite=deposit
        )
        return redirect('client_detail', pk=client.pk)
