from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('film/<int:film_id>/', views.detail_film, name='detail_film'),
    path('jadwal/', views.jadwal, name='jadwal'),
    path('pesan/<int:jadwal_id>/', views.pesan_tiket, name='pesan_tiket'),
    path('proses_pembayaran/<int:jadwal_id>/', views.proses_pembayaran, name='proses_pembayaran'),
    path('pembayaran/<int:pemesanan_id>/', views.halaman_pembayaran, name='halaman_pembayaran'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)