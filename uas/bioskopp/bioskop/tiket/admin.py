from django.contrib import admin
from .models import Film, JadwalTayang, Pemesanan, Pembayaran

admin.site.register(Film)
admin.site.register(JadwalTayang)
admin.site.register(Pemesanan)
admin.site.register(Pembayaran)
