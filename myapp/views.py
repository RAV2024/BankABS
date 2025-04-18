from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Account
from .forms import ClientForm
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

def client_detail(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'clients/client_detail.html', {'client': client})


def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm()
    return render(request, 'clients/add_client.html', {'form': form})














