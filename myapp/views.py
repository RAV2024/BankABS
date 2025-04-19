from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Account
from .forms import ClientForm, AccountForm
from django.db.models import Q

def home(request):
    client_count = Client.objects.count()
    return render(request, 'home.html', {
        'client_count': client_count,
    })

def clients_list(request):
    passport_query = request.GET.get('passport', '').replace(' ', '').strip()

    clients = Client.objects.all()

    if passport_query:
        clients = clients.filter(
            Q(passport_series__icontains=passport_query[:4]) &
            Q(passport_number__icontains=passport_query[4:])
        ) | clients.filter(
            Q(passport_series__icontains=passport_query) |
            Q(passport_number__icontains=passport_query)
        )

    clients = clients.order_by('last_name', 'first_name', 'patronymic')
    client_count = clients.count()
    return render(request, 'clients/clients.html', {
        'clients': clients,
        'client_count': client_count
    })

from .utils import passport_needs_update

def client_detail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    is_invalid = passport_needs_update(client.birth_date, client.passport_issue_date)
    return render(request, 'clients/client_detail.html', {
        'client': client,
        'passport_warning': is_invalid  # 👈 передаём результат проверки
    })


def add_client(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        account_form = AccountForm(request.POST)
        if client_form.is_valid() and account_form.is_valid():
            client = client_form.save()
            account = account_form.save(commit=False)
            account.client = client
            # Тут можешь сгенерировать номер счёта
            account.save()
            return redirect('clients_list')
    else:
        client_form = ClientForm()
        account_form = AccountForm()

    return render(request, 'clients/add_client.html', {
        'client_form': client_form,
        'account_form': account_form
    })

from .utils import passport_needs_update

def create_account(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    passport_expired = passport_needs_update(client.birth_date, client.passport_issue_date)

    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid() and not passport_expired:
            account = form.save(commit=False)
            account.client = client
            account.save()
            return redirect('client_detail', client.id)
    else:
        form = AccountForm()

    return render(request, 'clients/create_account.html', {
        'form': form,
        'client': client,
        'passport_expired': passport_expired,
    })

def update_passport(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail', client_id)
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/update_passport.html', {'form': form, 'client': client})

def check_passport_validity(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    is_invalid = passport_needs_update(client.birth_date, client.passport_issue_date)
    return render(request, 'clients/client_detail.html', {
        'client': client,
        'passport_warning': is_invalid
    })


from .forms import UpdatePassportForm


def update_passport(request, client_id):
    client = Client.objects.get(id=client_id)

    if request.method == 'POST':
        form = UpdatePassportForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail', client_id=client.id)
    else:
        form = UpdatePassportForm(instance=client)

    return render(request, 'clients/update_passport.html', {'form': form, 'client': client})


















