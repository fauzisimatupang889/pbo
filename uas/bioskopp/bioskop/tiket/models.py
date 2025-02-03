from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.text import slugify

def film_image_path(instance, filename):
    """
    Mengatur jalur penyimpanan gambar film dan memastikan tidak ada duplikasi.
    Gambar akan disimpan dengan nama yang bersih berdasarkan judul film.
    """
    ext = filename.split('.')[-1]  # Ambil ekstensi file
    filename = f"{slugify(instance.title)}.{ext}"  # Buat nama file unik berdasarkan judul film
    return os.path.join('film_images/', filename)

class Film(models.Model):
    title = models.CharField(max_length=255)
    gambar = models.ImageField(upload_to=film_image_path, null=True, blank=True)
    description = models.TextField()
    duration = models.PositiveIntegerField()  # Durasi dalam menit
    release_date = models.DateField()

    def __str__(self):
        return self.title

class JadwalTayang(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    tanggal = models.DateField()
    waktu = models.TimeField()
    kapasitas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.film.title} - {self.tanggal} {self.waktu}"

class Pemesanan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jadwal = models.ForeignKey(JadwalTayang, on_delete=models.CASCADE)
    jumlah_tiket = models.PositiveIntegerField()
    total_harga = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=[('pending', 'Pending'), ('lunas', 'Lunas')], max_length=10)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Pembayaran(models.Model):
    pemesanan = models.ForeignKey(Pemesanan, on_delete=models.CASCADE)
    metode = models.CharField(max_length=50, choices=[('transfer', 'Transfer Bank'), ('ewallet', 'E-Wallet')])
    tanggal_bayar = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pembayaran {self.pemesanan.id}"
