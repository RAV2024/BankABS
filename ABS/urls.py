from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('open_account/', views.open_account, name='open_account'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('clients/', views.clients, name='clients'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('account/<int:account_id>/', views.account_detail, name='account_detail'),
    path('client/<int:client_id>/open-account/', views.open_account_for_client, name='open_account_for_client'),

]
