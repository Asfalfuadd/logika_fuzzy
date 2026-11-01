# ==========================================================
# SISTEM PENENTUAN UKT MAHASISWA BERBASIS LOGIKA FUZZY
# Praktikum 6 - Fuzzy Rule dan Knowledge Base
# ==========================================================

# Fungsi keanggotaan trapesium
def trapesium(x, a, b, c, d):
    if x < a or x > d:
        return 0.0

    if b <= x <= c:
        return 1.0

    if a <= x < b:
        if a == b:
            return 1.0
        return (x - a) / (b - a)

    if c < x <= d:
        if c == d:
            return 1.0
        return (d - x) / (d - c)

    return 0.0


# ==========================================================
# 1. FUZZIFIKASI PENGHASILAN ORANG TUA
# ==========================================================

def fuzzifikasi_penghasilan(penghasilan):
    return {
        "Rendah": trapesium(
            penghasilan, 0, 0, 2_000_000, 4_000_000
        ),
        "Sedang": trapesium(
            penghasilan, 2_000_000, 4_000_000,
            5_000_000, 7_000_000
        ),
        "Tinggi": trapesium(
            penghasilan, 5_000_000, 7_000_000,
            10_000_000, 10_000_000
        )
    }


# ==========================================================
# 2. FUZZIFIKASI JUMLAH TANGGUNGAN KELUARGA
# ==========================================================

def fuzzifikasi_tanggungan(tanggungan):
    return {
        "Sedikit": trapesium(
            tanggungan, 0, 0, 1, 2
        ),
        "Sedang": trapesium(
            tanggungan, 1, 2, 3, 4
        ),
        "Banyak": trapesium(
            tanggungan, 3, 4, 6, 6
        )
    }


# ==========================================================
# 3. BASIS ATURAN FUZZY (RULE BASE)
# ==========================================================

aturan = [
    ("R1", "Rendah", "Sedikit", 1_000_000),
    ("R2", "Rendah", "Sedang", 750_000),
    ("R3", "Rendah", "Banyak", 500_000),

    ("R4", "Sedang", "Sedikit", 2_000_000),
    ("R5", "Sedang", "Sedang", 1_500_000),
    ("R6", "Sedang", "Banyak", 1_000_000),

    ("R7", "Tinggi", "Sedikit", 4_000_000),
    ("R8", "Tinggi", "Sedang", 3_000_000),
    ("R9", "Tinggi", "Banyak", 2_500_000)
]


# ==========================================================
# 4. PROSES INFERENSI FUZZY
# ==========================================================

def tentukan_ukt(penghasilan, tanggungan):
    mu_penghasilan = fuzzifikasi_penghasilan(penghasilan)
    mu_tanggungan = fuzzifikasi_tanggungan(tanggungan)

    print("\nDERAJAT KEANGGOTAAN PENGHASILAN")
    for label, nilai in mu_penghasilan.items():
        print(f"{label:<10}: {nilai:.2f}")

    print("\nDERAJAT KEANGGOTAAN TANGGUNGAN")
    for label, nilai in mu_tanggungan.items():
        print(f"{label:<10}: {nilai:.2f}")

    print("\nEVALUASI BASIS ATURAN FUZZY")
    print("-" * 75)

    total_alpha = 0.0
    total_ukt = 0.0
    jumlah_aktif = 0

    for kode, penghasilan_label, tanggungan_label, nominal in aturan:
        alpha = min(
            mu_penghasilan[penghasilan_label],
            mu_tanggungan[tanggungan_label]
        )

        print(
            f"{kode}: IF Penghasilan {penghasilan_label} "
            f"AND Tanggungan {tanggungan_label} "
            f"THEN UKT Rp{nominal:,.0f} "
            f"| Alpha = {alpha:.2f}"
        )

        if alpha > 0:
            total_alpha += alpha
            total_ukt += alpha * nominal
            jumlah_aktif += 1

    print("-" * 75)

    if total_alpha == 0:
        print("UKT tidak dapat ditentukan.")
        print("Tidak ada aturan fuzzy yang aktif.")
        return None

    nominal_ukt = total_ukt / total_alpha

    print("\nRINGKASAN HASIL")
    print(f"Jumlah aturan aktif : {jumlah_aktif}")
    print(f"Total firing strength: {total_alpha:.2f}")
    print(f"Total hasil berbobot : Rp{total_ukt:,.2f}")
    print(f"Nominal UKT         : Rp{nominal_ukt:,.2f}")

    return nominal_ukt


# ==========================================================
# 5. PENGUJIAN DATA MAHASISWA
# ==========================================================

print("=" * 75)
print("SISTEM PENENTUAN UKT MAHASISWA BERBASIS LOGIKA FUZZY")
print("=" * 75)

penghasilan = float(
    input("Masukkan penghasilan orang tua per bulan (Rp): ")
)

tanggungan = int(
    input("Masukkan jumlah tanggungan keluarga: ")
)

if penghasilan < 0 or tanggungan < 1:
    print("Input tidak valid.")
elif penghasilan > 10_000_000 or tanggungan > 6:
    print("Input berada di luar rentang model fuzzy.")
    print("Sesuaikan rentang keanggotaan sebelum menghitung UKT.")
else:
    hasil = tentukan_ukt(penghasilan, tanggungan)

    if hasil is not None:
        print("\n" + "=" * 75)
        print(f"UKT MAHASISWA: Rp{hasil:,.0f}")
        print("=" * 75)
