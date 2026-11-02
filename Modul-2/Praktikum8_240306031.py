import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# ==========================================
# 1. DEFINISI VARIABEL INPUT
# ==========================================

# Input penghasilan orang tua dalam juta rupiah
penghasilan = 3.5
# Input jumlah tanggungan
tanggungan = 4
# ==========================================
# 2. FUZZIFIKASI PENGHASILAN
# ==========================================
mu_penghasilan_rendah = max(
    0, min(1, (6 - penghasilan) / 3)
)
mu_penghasilan_sedang = max(
    0, min(
        (penghasilan - 3) / 4.5,
        (12 - penghasilan) / 4.5
    )
)
mu_penghasilan_tinggi = max(
    0, min(1, (penghasilan - 9) / 3)
)

# ==========================================
# 3. FUZZIFIKASI JUMLAH TANGGUNGAN
# ==========================================
if tanggungan <= 2:
    mu_tanggungan_sedikit = 1
elif tanggungan < 4:
    mu_tanggungan_sedikit = (4 - tanggungan) / 2
else:
    mu_tanggungan_sedikit = 0
if tanggungan <= 5:
    mu_tanggungan_sedang = max(
        0, (tanggungan - 2) / 3
    )
else:
    mu_tanggungan_sedang = max(
        0, (8 - tanggungan) / 3
    )
if tanggungan <= 6:
    mu_tanggungan_banyak = 0
elif tanggungan < 8:
    mu_tanggungan_banyak = (tanggungan - 6) / 2
else:
    mu_tanggungan_banyak = 1
# ==========================================
# 4. EVALUASI SEMBILAN ATURAN FUZZY
# ==========================================
# R1: Penghasilan rendah AND tanggungan sedikit
r1 = min(
    mu_penghasilan_rendah,
    mu_tanggungan_sedikit
)
# R2: Penghasilan rendah AND tanggungan sedang
r2 = min(
    mu_penghasilan_rendah,
    mu_tanggungan_sedang
)
# R3: Penghasilan rendah AND tanggungan banyak
r3 = min(
    mu_penghasilan_rendah,
    mu_tanggungan_banyak
)
# R4: Penghasilan sedang AND tanggungan sedikit
r4 = min(
    mu_penghasilan_sedang,
    mu_tanggungan_sedikit
)
# R5: Penghasilan sedang AND tanggungan sedang
r5 = min(
    mu_penghasilan_sedang,
    mu_tanggungan_sedang
)
# R6: Penghasilan sedang AND tanggungan banyak
r6 = min(
    mu_penghasilan_sedang,
    mu_tanggungan_banyak
)

# R7: Penghasilan tinggi AND tanggungan sedikit
r7 = min(
    mu_penghasilan_tinggi,
    mu_tanggungan_sedikit
)
# R8: Penghasilan tinggi AND tanggungan sedang
r8 = min(
    mu_penghasilan_tinggi,
    mu_tanggungan_sedang
)
# R9: Penghasilan tinggi AND tanggungan banyak
r9 = min(
    mu_penghasilan_tinggi,
    mu_tanggungan_banyak
)
# ==========================================
# 5. DEFINISI OUTPUT NOMINAL UKT
# ==========================================

# Semesta output dalam juta rupiah
z = np.linspace(0.5, 4, 1000)
# Fungsi keanggotaan output UKT
mf_rendah = fuzz.trapmf(
    z, [0.5, 0.5, 1, 2]
)
mf_sedang = fuzz.trimf(
    z, [1, 2.25, 3.5]
)
mf_tinggi = fuzz.trapmf(
    z, [2.5, 3.5, 4, 4]
)
# ==========================================
# 6. IMPLIKASI MIN
# ==========================================
# Output Rendah: R1, R2, R3, R6
alpha_rendah = max(r1, r2, r3, r6)
# Output Sedang: R4, R5, R9
alpha_sedang = max(r4, r5, r9)

# Output Tinggi: R7, R8
alpha_tinggi = max(r7, r8)
imp_rendah = np.fmin(
    alpha_rendah, mf_rendah
)
imp_sedang = np.fmin(
    alpha_sedang, mf_sedang
)
imp_tinggi = np.fmin(
    alpha_tinggi, mf_tinggi
)
# ==========================================
# 7. AGREGASI MAX
# ==========================================
agregasi = np.fmax(
    imp_rendah,
    np.fmax(imp_sedang, imp_tinggi)
)
# ==========================================
# 8. LIMA METODE DEFUZZIFIKASI
# ==========================================
metode = [
    'centroid',
    'bisector',
    'mom',
    'som',
    'lom'
]
hasil = {}
if np.max(agregasi) == 0:
    print("Tidak ada aturan fuzzy yang aktif.")
else:
    for nama_metode in metode:
        nilai = fuzz.defuzz(
            z, agregasi, nama_metode
        )
        # Konversi juta rupiah menjadi rupiah
        hasil[nama_metode] = nilai * 1000000
# ==========================================
# 9. MENAMPILKAN HASIL
# ==========================================
print("=" * 55)
print("SISTEM PENENTUAN NOMINAL UKT MAHASISWA")
print("=" * 55)
print(f"Penghasilan orang tua: Rp{penghasilan * 1000000:,.0f}")
print(f"Jumlah tanggungan: {tanggungan} orang")
print("\nDerajat Keanggotaan Penghasilan")
print(f"Rendah : {mu_penghasilan_rendah:.4f}")
print(f"Sedang : {mu_penghasilan_sedang:.4f}")
print(f"Tinggi : {mu_penghasilan_tinggi:.4f}")
print("\nDerajat Keanggotaan Tanggungan")
print(f"Sedikit: {mu_tanggungan_sedikit:.4f}")
print(f"Sedang : {mu_tanggungan_sedang:.4f}")
print(f"Banyak : {mu_tanggungan_banyak:.4f}")
print("\nAktivasi Aturan")
for i, nilai in enumerate(
    [r1, r2, r3, r4, r5, r6, r7, r8, r9],
    start=1
):
    print(f"R{i}: {nilai:.4f}")
print("\nHasil Defuzzifikasi")
for nama_metode, nilai in hasil.items():
    print(
        f"{nama_metode.upper():<10}: "
        f"Rp{nilai:,.2f}"
    )

# ==========================================
# 10. GRAFIK AGREGASI DAN DEFUZZIFIKASI
# ==========================================
plt.figure(figsize=(12, 6))
plt.plot(
    z * 1000000,
    agregasi,
    linewidth=2,
    label='Kurva Agregasi UKT'
)
plt.fill_between(
    z * 1000000,
    0,
    agregasi,
    alpha=0.3,
    label='Daerah Agregasi'
)
for nama_metode, nilai_rupiah in hasil.items():
    plt.axvline(
        x=nilai_rupiah,
        linestyle='--',
        linewidth=1.5,
        label=f'{nama_metode.upper()}'
    )
plt.title(
    'Perbandingan Lima Metode Defuzzifikasi UKT'
)

plt.xlabel('Nominal UKT (Rupiah)')
plt.ylabel('Derajat Keanggotaan')
plt.grid(True, linestyle=':')
plt.legend()
plt.tight_layout()
plt.savefig(
    'komparasi_metode_defuzzifikasi_UKT.png',
    dpi=300
)
plt.show()
