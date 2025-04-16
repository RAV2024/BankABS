from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('open_account/', views.open_account, name='open_account'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
