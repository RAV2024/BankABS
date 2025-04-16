from django.shortcuts import render, redirect
from .forms import ClientForm,AccountForm
from .models import Client, Account
from django.core.paginator import Paginator

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

from django.contrib import messages


def open_account(request):
    account_form = None  # Инициализация переменной account_form до всех условий

    if request.method == 'POST':
        passport_series = request.POST.get('passport_series')
        passport_number = request.POST.get('passport_number')
        full_name = request.POST.get('full_name')

        # Проверка, существует ли уже клиент с таким паспортом
        existing_client = Client.objects.filter(passport_series=passport_series, passport_number=passport_number).first()

        if existing_client:
            # Если ФИО не совпадают, показываем ошибку
            if existing_client.full_name.strip().lower() != full_name.strip().lower():
                messages.error(request, 'Паспорт уже используется другим клиентом. Проверьте корректность данных.')
                return redirect('open_account')

            account_form = AccountForm(request.POST)
            if account_form.is_valid():
                account = account_form.save(commit=False)
                account.client = existing_client
                account.save()
                messages.success(request, f'Клиент найден по паспорту: {existing_client.full_name}. Открыт новый счёт.')
                return redirect('client_detail', client_id=existing_client.id)

        else:
            client_form = ClientForm(request.POST)
            if client_form.is_valid():
                new_client = client_form.save()
                account_form = AccountForm(request.POST)
                if account_form.is_valid():
                    account = account_form.save(commit=False)
                    account.client = new_client
                    account.save()
                    messages.success(request, 'Создан новый клиент и открыт счёт.')
                    return redirect('client_detail', client_id=new_client.id)
            else:
                # Добавление вывода ошибок формы
                for field, errors in client_form.errors.items():
                    for error in errors:
                        messages.error(request, f"Ошибка в поле '{field}': {error}")
                messages.error(request, 'Пожалуйста, проверьте данные клиента.')

    else:
        client_form = ClientForm()
        account_form = AccountForm()

    return render(request, 'open_account.html', {
        'client_form': client_form,
        'account_form': account_form
    })








def clients(request):
    query = request.GET.get('q', '')  # Получаем поисковый запрос
    if query:
        # Фильтруем клиентов по имени
        all_clients = Client.objects.filter(
            full_name__icontains=query  # Ищем по имени клиента
        )
    else:
        all_clients = Client.objects.all()  # Если нет запроса, показываем всех клиентов

    # Группировка клиентов по паспорту
    grouped_clients = {}
    for client in all_clients:
        passport_key = f"{client.passport_series}-{client.passport_number}"
        if passport_key not in grouped_clients:
            grouped_clients[passport_key] = {'clients': [], 'accounts': set()}
        grouped_clients[passport_key]['clients'].append(client)

        # Добавляем номера счетов клиента в set, чтобы избежать повторений
        for account in client.accounts.all():
            grouped_clients[passport_key]['accounts'].add(account.account_number)

    # Передаем сгруппированных клиентов в шаблон
    return render(request, 'clients.html', {'grouped_clients': grouped_clients, 'query': query})

from django.shortcuts import render, get_object_or_404

def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)  # Получаем клиента по id

    return render(request, 'client_detail.html', {'client': client})


from django.http import JsonResponse
from .models import Client


def search_clients(request):
    query = request.GET.get('q', '')
    if query:
        clients = Client.objects.filter(full_name__icontains=query)[:10]  # Ограничим до 10 результатов
        client_data = [{'id': client.id, 'full_name': client.full_name} for client in clients]
    else:
        client_data = []

    return JsonResponse({'clients': client_data})


from django.shortcuts import render, get_object_or_404

def account_detail(request, account_id):
    account = get_object_or_404(Account, id=account_id)

    return render(request, 'account_detail.html', {'account': account})

from django.shortcuts import get_object_or_404
from django.contrib import messages

def open_account_for_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)

    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.client = client
            account.save()
            messages.success(request, 'Новый счёт успешно создан.')
            return redirect('client_detail', client_id=client.id)
    else:
        form = AccountForm()

    return render(request, 'open_account_for_client.html', {
        'client': client,
        'form': form
    })



