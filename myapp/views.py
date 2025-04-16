from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def open_account(request):
    if request.method == 'POST':
        pass
    return render(request, 'open_account.html')


