import numpy as np
import matplotlib.pyplot as plt
import random

# Fungsi untuk menghitung jarak Euclidean antara dua kota
def hitung_jarak_euclidean(kota1, kota2):
    return np.sqrt((kota1[0] - kota2[0])**2 + (kota1[1] - kota2[1])**2)

# Fungsi untuk menghitung total jarak perjalanan
def hitung_jarak_total(perjalanan, matriks_jarak):
    perjalanan_lengkap = perjalanan + [perjalanan[0]]
    return sum(matriks_jarak[perjalanan_lengkap[i], perjalanan_lengkap[i+1]] for i in range(len(perjalanan_lengkap)-1))

# Fungsi untuk membuat populasi awal
def buat_populasi_awal(jumlah_kota, ukuran_populasi):
    return [random.sample(range(jumlah_kota), jumlah_kota) for _ in range(ukuran_populasi)]

# Fungsi untuk seleksi orang tua menggunakan metode turnamen
def seleksi_turnamen(populasi, skor, k=3):
    turnamen = random.sample(list(zip(populasi, skor)), k)
    turnamen.sort(key=lambda x: x[1])
    return turnamen[0][0]

# Fungsi untuk melakukan persilangan (reproduksi)
def persilangan(ortu1, ortu2):
    ukuran = len(ortu1)
    p, q = sorted(random.sample(range(ukuran), 2))
    sementara = ortu1[p:q+1]
    anak = [kota for kota in ortu2 if kota not in sementara]
    return anak[:p] + sementara + anak[p:]

# Fungsi untuk melakukan mutasi
def mutasi(perjalanan, tingkat_mutasi):
    if random.random() < tingkat_mutasi:
        i, j = random.sample(range(len(perjalanan)), 2)
        perjalanan[i], perjalanan[j] = perjalanan[j], perjalanan[i]
    return perjalanan

# Fungsi utama untuk menjalankan algoritma genetika
def algoritma_genetika(kota, ukuran_populasi, jumlah_generasi, tingkat_mutasi):
    jumlah_kota = len(kota)
    matriks_jarak = np.array([[hitung_jarak_euclidean(c1, c2) for c2 in kota] for c1 in kota])
    populasi = buat_populasi_awal(jumlah_kota, ukuran_populasi)
    skor = [hitung_jarak_total(perjalanan, matriks_jarak) for perjalanan in populasi]
    skor_terbaik = min(skor)
    perjalanan_terbaik = populasi[skor.index(skor_terbaik)]
    riwayat_fitness = [skor_terbaik]
    for _ in range(jumlah_generasi):
        populasi_baru = []
        for _ in range(ukuran_populasi):
            ortu1 = seleksi_turnamen(populasi, skor)
            ortu2 = seleksi_turnamen(populasi, skor)
            anak = persilangan(ortu1, ortu2)
            anak = mutasi(anak, tingkat_mutasi)
            populasi_baru.append(anak)
        populasi = populasi_baru
        skor = [hitung_jarak_total(perjalanan, matriks_jarak) for perjalanan in populasi]
        skor_terbaik_sekarang = min(skor)
        if skor_terbaik_sekarang < skor_terbaik:
            skor_terbaik = skor_terbaik_sekarang
            perjalanan_terbaik = populasi[skor.index(skor_terbaik)]
        riwayat_fitness.append(skor_terbaik)
    return perjalanan_terbaik, riwayat_fitness, skor_terbaik

# Parameter
jumlah_kota = 20
ukuran_populasi = 300
jumlah_generasi = 1000
tingkat_mutasi = 0.05

# Koordinat kota yang ditentukan secara manual
kota = [
    (10, 20), (22, 34), (31, 47), (10, 10), (55, 25),
    (65, 35), (75, 45), (85, 55), (95, 65), (50, 75),
    (40, 85), (30, 95), (20, 50), (10, 40), (25, 30),
    (35, 20), (45, 10), (55, 5), (65, 15), (75, 25)
]

# Jalankan algoritma genetika
perjalanan_terbaik, riwayat_fitness, skor_terbaik = algoritma_genetika(kota, ukuran_populasi, jumlah_generasi, tingkat_mutasi)

# Konversi jarak dari unit arbitrer ke kilometer
skor_terbaik_km = skor_terbaik

# Tampilkan koordinat kota yang telah diurutkan
print("Koordinat kota yang telah diurutkan:")
for i in perjalanan_terbaik:
    print(f"Kota {i+1}: {kota[i]}")

# Tampilkan jarak terpendek dalam satuan km
print(f"Jarak terpendek: {skor_terbaik_km:.2f} km")

# Fungsi untuk memplot perjalanan
def plot_perjalanan(perjalanan):
    plt.figure(figsize=(10, 6))
    # Plot garis antar kota
    for i in range(len(perjalanan)-1):
        plt.plot([kota[perjalanan[i]][0], kota[perjalanan[i+1]][0]], [kota[perjalanan[i]][1], kota[perjalanan[i+1]][1]], 'bo-')
    # Tambahkan garis kembali ke kota awal
    plt.plot([kota[perjalanan[-1]][0], kota[perjalanan[0]][0]], [kota[perjalanan[-1]][1], kota[perjalanan[0]][1]], 'bo-')
    # Tandai semua kota
    plt.scatter([k[0] for k in kota], [k[1] for k in kota], color='red')
    # Anotasi untuk setiap kota
    for idx, koord in enumerate(kota):
        plt.annotate(f'Kota {idx+1}', (koord[0], koord[1]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.title('Peta Jalur Terpendek TSP dengan Algoritma Genetika')
    plt.xlabel('X Koordinat')
    plt.ylabel('Y Koordinat')
    plt.grid(True)
    plt.show()

# Fungsi untuk memplot grafik fitness
def plot_grafik_fitness(riwayat_fitness):
    plt.figure(figsize=(10, 6))
    plt.plot(riwayat_fitness, 'g-', label='fitness Terbaik per Generasi')
    plt.title('Grafik fitness Algoritma Genetika untuk TSP')
    plt.xlabel('Generasi')
    plt.ylabel('fitness (Jarak Total Terkecil)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Memplot jalur terpendek
plot_perjalanan(perjalanan_terbaik)

# Memplot grafik fitness
plot_grafik_fitness(riwayat_fitness)
