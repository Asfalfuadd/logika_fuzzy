import numpy as np
import matplotlib.pyplot as plt

# 1. DEFINISI FUNGSI KEANGGOTAAN LINGUISTIK

def mf_rendah(x):
    kondisi = [
        x <= 20.0,
        (x > 20.0) & (x < 40.0),
        x >= 40.0
    ]
    pilihan = [
        1.0,
        (40.0 - x) / (40.0 - 20.0),
        0.0
    ]
    return np.select(kondisi, pilihan)


def mf_normal(x):
    kondisi = [
        (x <= 30.0) | (x >= 70.0),
        (x > 30.0) & (x <= 50.0),
        (x > 50.0) & (x < 70.0)
    ]
    pilihan = [
        0.0,
        (x - 30.0) / (50.0 - 30.0),
        (70.0 - x) / (70.0 - 50.0)
    ]
    return np.select(kondisi, pilihan)


def mf_tinggi(x):
    kondisi = [
        x <= 60.0,
        (x > 60.0) & (x < 80.0),
        x >= 80.0
    ]
    pilihan = [
        0.0,
        (x - 60.0) / (80.0 - 60.0),
        1.0
    ]
    return np.select(kondisi, pilihan)

# 2. DEFINISI STRUKTUR VARIABEL LINGUISTIK

variabel_cpu_server = {
    "nama": "Penggunaan CPU Server",
    "satuan": "persen (%)",
    "semesta": (0.0, 100.0),
    "label": {
        "Rendah": mf_rendah,
        "Normal": mf_normal,
        "Tinggi": mf_tinggi
    }
}

# 3. FUNGSI FUZZIFIKASI INPUT TUNGGAL

def fuzzifikasi(nilai_crisp, variabel):
    """
    Melakukan pemetaan nilai crisp ke semua derajat label linguistik.
    """
    hasil = {}
    u_min, u_max = variabel["semesta"]
    
    if not (u_min <= nilai_crisp <= u_max):
        raise ValueError(f"Input {nilai_crisp} di luar semesta [{u_min}, {u_max}]")
        
    for nama_label, fungsi_mf in variabel["label"].items():
        derajat = float(fungsi_mf(np.array([nilai_crisp]))[0])
        hasil[nama_label] = round(derajat, 4)
        
    return hasil

# Pengujian fuzzifikasi untuk nilai-nilai yang diminta
test_values = [10, 35, 50, 65, 75, 95]

print("TABEL OUTPUT DERAJAT KEANGGOTAAN:")
print(f"{'CPU (%)':>8} | {'Rendah':>9} | {'Normal':>9} | {'Tinggi':>9}")
print("-" * 50)

for cpu_val in test_values:
    hasil_fuzzy = fuzzifikasi(cpu_val, variabel_cpu_server)
    print(f"{cpu_val:>8} | {hasil_fuzzy['Rendah']:>9.3f} | {hasil_fuzzy['Normal']:>9.3f} | {hasil_fuzzy['Tinggi']:>9.3f}")

print("-" * 50)
print()

# Generate data untuk plotting
x_semesta = np.linspace(0.0, 100.0, 1001)

y_rendah = mf_rendah(x_semesta)
y_normal = mf_normal(x_semesta)
y_tinggi = mf_tinggi(x_semesta)

# Membuat plot
plt.figure(figsize=(12, 7))
plt.plot(x_semesta, y_rendah, label='Rendah', color='#1f77b4', linewidth=2.5)
plt.plot(x_semesta, y_normal, label='Normal', color='#ff7f0e', linewidth=2.5)
plt.plot(x_semesta, y_tinggi, label='Tinggi', color='#d62728', linewidth=2.5)

# Menandai titik-titik uji
for cpu_val in test_values:
    hasil_fuzzy = fuzzifikasi(cpu_val, variabel_cpu_server)
    if hasil_fuzzy['Rendah'] > 0:
        plt.scatter(cpu_val, hasil_fuzzy['Rendah'], color='#1f77b4', s=50, zorder=5)
    if hasil_fuzzy['Normal'] > 0:
        plt.scatter(cpu_val, hasil_fuzzy['Normal'], color='#ff7f0e', s=50, zorder=5)
    if hasil_fuzzy['Tinggi'] > 0:
        plt.scatter(cpu_val, hasil_fuzzy['Tinggi'], color='#d62728', s=50, zorder=5)

plt.title(f'Variabel Linguistik: {variabel_cpu_server["nama"]}', fontsize=14, fontweight='bold')
plt.xlabel(f'CPU Utilization ({variabel_cpu_server["satuan"]})', fontsize=12)
plt.ylabel('Derajat Keanggotaan μ(x)', fontsize=12)
plt.xlim(0, 100)
plt.ylim(-0.05, 1.1)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='center right', fontsize=11)
plt.tight_layout()

# Simpan grafik
plt.savefig('CPU_Utilization_Membership_Functions.png', dpi=300, bbox_inches='tight')

plt.show()

# Tampilkan hasil fuzzifikasi untuk semua nilai uji
print("Hasil Fuzzifikasi untuk semua nilai uji:")
for cpu_val in test_values:
    hasil_fuzzy = fuzzifikasi(cpu_val, variabel_cpu_server)
    print(f"\nCPU = {cpu_val}%:")
    for label, derajat in hasil_fuzzy.items():
        print(f" - {label:<8}: {derajat}")
