from django.shortcuts import render, get_object_or_404, redirect
from .models import Film, JadwalTayang, Pemesanan, Pembayaran
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    films = Film.objects.all()
    return render(request, 'tiket/index.html', {'films': films})

def detail_film(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    jadwal_tayang = JadwalTayang.objects.filter(film=film)
    return render(request, 'tiket/detail_film.html', {'film': film, 'jadwal_tayang': jadwal_tayang})

def jadwal(request):
    jadwal = JadwalTayang.objects.all()
    return render(request, 'tiket/jadwal.html', {'jadwal': jadwal})

@login_required
def pesan_tiket(request, jadwal_id):
    jadwal = get_object_or_404(JadwalTayang, id=jadwal_id)

    if request.method == 'POST':
        jumlah_tiket = int(request.POST.get('jumlah_tiket', 1))

        if jumlah_tiket > jadwal.kapasitas:
            messages.error(request, "Jumlah tiket melebihi kapasitas tersedia.")
        else:
            total_harga = jumlah_tiket * 50000  # Harga per tiket Rp50.000
            Pemesanan.objects.create(
                user=request.user,
                jadwal=jadwal,
                jumlah_tiket=jumlah_tiket,
                total_harga=total_harga,
                status='pending'
            )
            messages.success(request, "Tiket berhasil dipesan! Silakan lakukan pembayaran.")
            return redirect('index')

    return render(request, 'tiket/pesan_tiket.html', {'jadwal': jadwal})

def proses_pembayaran(request, jadwal_id):
    jadwal = get_object_or_404(JadwalTayang, id=jadwal_id)

    if request.method == 'POST':
        jumlah_tiket = int(request.POST.get('jumlah_tiket', 1))
        metode_pembayaran = request.POST.get('metode_pembayaran')

        if jumlah_tiket > jadwal.kapasitas:
            messages.error(request, "Jumlah tiket melebihi kapasitas tersedia.")
            return redirect('pesan_tiket', jadwal_id=jadwal.id)

        total_harga = jumlah_tiket * 50000  # Harga per tiket Rp50.000

        # Simpan pemesanan tiket
        pemesanan = Pemesanan.objects.create(
            user=request.user,
            jadwal=jadwal,
            jumlah_tiket=jumlah_tiket,
            total_harga=total_harga,
            status='pending'
        )

        # Simpan data pembayaran
        Pembayaran.objects.create(
            pemesanan=pemesanan,
            metode=metode_pembayaran
        )

        messages.success(request, "Tiket berhasil dipesan! Silakan lakukan pembayaran.")
        return redirect('halaman_pembayaran', pemesanan.id)

    return redirect('index')

@login_required
def halaman_pembayaran(request, pemesanan_id):
    pemesanan = get_object_or_404(Pemesanan, id=pemesanan_id)
    pembayaran = Pembayaran.objects.get(pemesanan=pemesanan)

    return render(request, 'tiket/pembayaran.html', {
        'pemesanan': pemesanan,
        'pembayaran': pembayaran
    })
