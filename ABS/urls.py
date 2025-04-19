from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    path('clients/', views.clients_list, name='clients_list'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/<int:client_id>/', views.client_detail, name='client_detail'),
    path('clients/<int:client_id>/add_account/', views.create_account, name='create_account'),
    path('client/<int:client_id>/update_passport/', views.update_passport, name='update_passport'),
    path('client/<int:client_id>/check_passport/', views.check_passport_validity, name='check_passport'),
    path('clients/<int:client_id>/upload_photo/', views.upload_photo, name='upload_photo'),
    path('photos/<int:photo_id>/delete/', views.delete_photo, name='delete_photo')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
