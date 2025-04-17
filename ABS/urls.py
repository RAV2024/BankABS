from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clients/', views.ClientListView.as_view(), name='clients_list'),
    path('clients/add/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/add-card/', views.CardCreateView.as_view(), name='create_card'),
    path('clients/<int:pk>/add-deposit/', views.DepositCreateView.as_view(), name='create_deposit'),
]
