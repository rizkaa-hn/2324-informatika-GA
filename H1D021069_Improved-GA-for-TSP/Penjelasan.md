# Algoritma Genetika untuk Traveling Salesman Problem (TSP)

## Deskripsi

Algoritma genetika ini dirancang untuk menyelesaikan masalah Traveling Salesman Problem (TSP). TSP adalah masalah optimasi di mana seorang penjual harus mengunjungi sejumlah kota tepat satu kali dan kembali ke kota awal dengan total jarak perjalanan terpendek.

## Fungsi Utama

### calculate_cost(route, distance_matrix):

Menghitung biaya total (jarak) dari rute yang diberikan berdasarkan matriks jarak.

### create_distance_matrix(problem):

Membuat matriks jarak dari instance TSP yang diberikan.

### mutate(route, mutation_rate):

Melakukan mutasi pada rute dengan menukar posisi dua kota secara acak berdasarkan tingkat mutasi yang diberikan.

## Operator Crossover

### mscx_radius(parent1, parent2, distance_matrix, r):

Operator crossover yang menghasilkan keturunan dengan radius tertentu dari orang tua.

### rx_crossover(parent1, parent2, pr):

Operator crossover berbasis persen yang memilih sejumlah kota dari orang tua untuk dibuat keturunan.

### fill_offspring(offspring, parent):

Mengisi keturunan dengan kota-kota yang belum dikunjungi dari orang tua.

## Algoritma Genetika yang Dimodifikasi
### genetic_algorithm(problem, population_size, generations, crossover_rate, mutation_rate, r, prx, pr):

* Inisialisasi populasi dengan rute acak.
* Selama jumlah generasi:
    * Mengurutkan populasi berdasarkan biaya rute.
    * Menyimpan individu terbaik.
    * Membentuk populasi baru melalui crossover dan mutasi.
    * Mencetak biaya terbaik setiap generasi.
* Mengembalikan solusi terbaik dan biayanya.

## Algoritma Genetika Standar
### standard_genetic_algorithm(problem, population_size, generations, crossover_rate, mutation_rate):

* Inisialisasi populasi dengan rute acak.
* Selama jumlah generasi:
    * Mengurutkan populasi berdasarkan biaya rute.
    * Menyimpan individu terbaik.
    * Membentuk populasi baru melalui crossover dan mutasi.
    * Mencetak biaya terbaik setiap generasi.
* Mengembalikan solusi terbaik dan biayanya.

## Implementasi Order Crossover
### order_crossover(parent1, parent2):
Operator crossover yang mempertahankan urutan relatif kota.

### fill_order_crossover(offspring, parent, start, end):
Mengisi keturunan dengan kota-kota yang belum dikunjungi dari orang tua.

## Fungsi Utilitas
### load_tsp_file(instance):
Memuat instance TSP dari file.

## Eksekusi dan Perbandingan
Algoritma dijalankan untuk instance 'eil51' dan 'pr76' dari TSPLIB95 dengan berbagai parameter dan hasilnya dibandingkan. Algoritma dijalankan sebanyak 3 kali dengan 500 generasi setiap kali.

## Hasil
Hasil menunjukkan perbandingan biaya minimum, biaya rata-rata, deviasi standar, dan waktu rata-rata untuk algoritma genetika standar dan yang dimodifikasi pada kedua instance TSP.

## Kesimpulan
Dari hasil di atas, kita dapat menganalisis kinerja algoritma berdasarkan biaya perjalanan terpendek yang ditemukan, konsistensi hasil, dan efisiensi waktu eksekusi.


# Cara Run Program

## Cek Library
Pastikan library berikut sudah diinstal, apabila belum maka masukan perintah ini pada terminal:

```
pip install numpy tsplib95
```

## Run Program
Ketika library sudah terinstall masukan ini di terminal:

```
python TwoCrossover.py
```