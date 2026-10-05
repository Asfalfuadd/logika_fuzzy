import numpy as np
import matplotlib.pyplot as plt

# 1. DEFINISI FUNGSI KEANGGOTAAN FUZZY

def fungsi_segitiga(x, a, b, c):
    """
    Fungsi keanggotaan kurva segitiga: [a, b, c]
    """
    return np.maximum(0.0, np.minimum((x - a) / (b - a), (c - x) / (c - b)))

def fungsi_trapesium(x, a, b, c, d):
    """
    Fungsi keanggotaan kurva trapesium: [a, b, c, d]
    """
    naik = (x - a) / (b - a)
    turun = (d - x) / (d - c)
    return np.maximum(0.0, np.minimum(np.minimum(naik, 1.0), turun))

# 2. DEFINISI OPERATOR FUZZY

# Operasi Irisan (T-Norm / AND)
def zadeh_min(mu_a, mu_b):
    return np.minimum(mu_a, mu_b)

def algebraic_product(mu_a, mu_b):
    return mu_a * mu_b

# Operasi Gabungan (T-Conorm / OR)
def zadeh_max(mu_a, mu_b):
    return np.maximum(mu_a, mu_b)

def algebraic_sum(mu_a, mu_b):
    return mu_a + mu_b - (mu_a * mu_b)

# Operasi Komplemen (NOT)
def komplemen(mu_a):
    return 1.0 - mu_a

# 3. PEMODELAN DATA EVALUASI BANDWIDTH KAMPUS

# Semesta pembicaraan X = [0, 100] Mbps
x = np.linspace(0, 100, 1000)

# Himpunan A: Ketersediaan Bandwidth Cukup (Segitiga: [30, 60, 90])
mu_a = fungsi_segitiga(x, 30, 60, 90)

# Himpunan B: Packet Loss Rendah (Trapesium: [40, 55, 75, 95])
mu_b = fungsi_trapesium(x, 40, 55, 75, 95)

# Perhitungan Operasi
irisan_min = zadeh_min(mu_a, mu_b)
irisan_prod = algebraic_product(mu_a, mu_b)
gabungan_max = zadeh_max(mu_a, mu_b)
gabungan_sum = algebraic_sum(mu_a, mu_b)
komplemen_a = komplemen(mu_a)

# 4. PENGUJIAN PADA 4 NILAI THROUGHPUT

titik_uji = [35, 50, 65, 80]

print("=" * 85)
print("HASIL EVALUASI OPERASI FUZZY PADA TITIK UJI THROUGHPUT (Mbps)")
print("=" * 85)
print(f"{'Throughput':^12} | {'mu_A':^8} | {'mu_B':^8} | {'Zadeh Min':^10} | {'Alg. Prod':^10} | {'Zadeh Max':^10} | {'Alg. Sum':^10} | {'NOT A':^8}")
print("-" * 85)

for val in titik_uji:
    a_val = float(fungsi_segitiga(np.array([val]), 30, 60, 90)[0])
    b_val = float(fungsi_trapesium(np.array([val]), 40, 55, 75, 95)[0])
    
    z_min = float(zadeh_min(a_val, b_val))
    a_prod = float(algebraic_product(a_val, b_val))
    z_max = float(zadeh_max(a_val, b_val))
    a_sum = float(algebraic_sum(a_val, b_val))
    not_a = float(komplemen(a_val))
    
    print(f"{val:^12.1f} | {a_val:^8.4f} | {b_val:^8.4f} | {z_min:^10.4f} | {a_prod:^10.4f} | {z_max:^10.4f} | {a_sum:^10.4f} | {not_a:^8.4f}")

print("=" * 85)

# 5. VISUALISASI GRAFIK HASIL OPERASI

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Himpunan Dasar A, B dan NOT A
axes[0, 0].plot(x, mu_a, label='A (Bandwidth Cukup)', color='blue', linewidth=2)
axes[0, 0].plot(x, mu_b, label='B (Packet Loss Rendah)', color='orange', linewidth=2)
axes[0, 0].plot(x, komplemen_a, label='NOT A (Komplemen)', color='gray', linestyle='--', linewidth=1.8)
axes[0, 0].set_title('1. Fungsi Keanggotaan A, B, dan NOT A', fontweight='bold')
axes[0, 0].set_xlabel('Throughput (Mbps)')
axes[0, 0].set_ylabel('Derajat Keanggotaan (μ)')
axes[0, 0].set_ylim(-0.05, 1.05)
axes[0, 0].grid(True, linestyle=':', alpha=0.6)
axes[0, 0].legend()

# Panel 2: Operasi Irisan (T-Norm)
axes[0, 1].plot(x, irisan_min, label='Zadeh Min (Standar)', color='green', linewidth=2.5)
axes[0, 1].plot(x, irisan_prod, label='Algebraic Product', color='red', linestyle='-.', linewidth=2)
axes[0, 1].plot(x, mu_a, color='blue', linestyle=':', alpha=0.4, label='Basis A')
axes[0, 1].plot(x, mu_b, color='orange', linestyle=':', alpha=0.4, label='Basis B')
axes[0, 1].set_title('2. Operasi Irisan (AND / T-Norm)', fontweight='bold')
axes[0, 1].set_xlabel('Throughput (Mbps)')
axes[0, 1].set_ylabel('Derajat Keanggotaan (μ)')
axes[0, 1].set_ylim(-0.05, 1.05)
axes[0, 1].grid(True, linestyle=':', alpha=0.6)
axes[0, 1].legend()

# Panel 3: Operasi Gabungan (T-Conorm)
axes[1, 0].plot(x, gabungan_max, label='Zadeh Max (Standar)', color='green', linewidth=2.5)
axes[1, 0].plot(x, gabungan_sum, label='Algebraic Sum', color='purple', linestyle='-.', linewidth=2)
axes[1, 0].plot(x, mu_a, color='blue', linestyle=':', alpha=0.4, label='Basis A')
axes[1, 0].plot(x, mu_b, color='orange', linestyle=':', alpha=0.4, label='Basis B')
axes[1, 0].set_title('3. Operasi Gabungan (OR / T-Conorm)', fontweight='bold')
axes[1, 0].set_xlabel('Throughput (Mbps)')
axes[1, 0].set_ylabel('Derajat Keanggotaan (μ)')
axes[1, 0].set_ylim(-0.05, 1.05)
axes[1, 0].grid(True, linestyle=':', alpha=0.6)
axes[1, 0].legend()

# Panel 4: Perbandingan Titik Uji Evaluasi
axes[1, 1].fill_between(x, irisan_prod, color='red', alpha=0.25, label='Area Alg. Product (Paling Ketat)')
axes[1, 1].plot(x, irisan_min, label='Zadeh Min', color='green', linewidth=2)
axes[1, 1].plot(x, gabungan_max, label='Zadeh Max', color='blue', linestyle='--', linewidth=1.5)

# Penanda titik uji
for val in titik_uji:
    val_min = float(zadeh_min(fungsi_segitiga(val, 30, 60, 90), fungsi_trapesium(val, 40, 55, 75, 95)))
    axes[1, 1].scatter([val], [val_min], color='black', zorder=5)
    axes[1, 1].annotate(f'{val} Mbps\n(μ={val_min:.2f})', (val, val_min),
                        textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8,
                        bbox=dict(boxstyle="round,pad=0.2", fc="yellow", alpha=0.5))

axes[1, 1].set_title('4. Ringkasan & Posisi Titik Pengujian', fontweight='bold')
axes[1, 1].set_xlabel('Throughput (Mbps)')
axes[1, 1].set_ylabel('Derajat Keanggotaan (μ)')
axes[1, 1].set_ylim(-0.05, 1.15)
axes[1, 1].grid(True, linestyle=':', alpha=0.6)
axes[1, 1].legend(loc='upper right')

plt.tight_layout()
plt.savefig('hasil_evaluasi_bandwidth.png', dpi=300)
print("\n[INFO] Grafik berhasil disimpan sebagai 'hasil_evaluasi_bandwidth.png'")

# 6. KESIMPULAN ANALISIS KEBIJAKAN KAMPUS
print("\n" + "=" * 85)
print("KESIMPULAN: OPERATOR YANG TEPAT UNTUK KRITERIA SELEKSI KETAT")
print("=" * 85)
print("""Jika kebijakan kampus menginginkan kriteria seleksi yang KETAT:
1. Operator yang paling tepat adalah operator irisan (T-Norm), khususnya ALGEBRAIC PRODUCT (A * B).
2. Alasan:
   - Nilai Algebraic Product selalu lebih kecil atau sama dengan Zadeh Min (mu_A * mu_B <= min(mu_A, mu_B)).
   - Algebraic Product memperhitungkan kedua parameter secara simultan dan memberikan efek 'penalti' 
     jika salah satu parameter tidak optimal (derajat < 1).
   - Misalnya pada throughput 50 Mbps:
     * Zadeh Min memberikan nilai 0.6667 (cukup longgar/toleran)
     * Algebraic Product menghasilkan 0.4444 (lebih ketat dan selektif)
   - Dengan Algebraic Product, jaringan hanya akan dianggap sangat layak jika KEDUA parameter 
     (Bandwidth Cukup DAN Packet Loss Rendah) sama-sama bernilai tinggi mendekati 1.0.""")
print("=" * 85)
