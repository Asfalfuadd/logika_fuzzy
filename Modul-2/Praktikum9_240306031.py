import numpy as np
# ==========================================================
# SISTEM PENENTUAN UKT - METODE SUGENO ORDE 0
# ==========================================================
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


def fuzzifikasi_penghasilan(penghasilan):
    return {
        "Rendah": trapesium(penghasilan, 0, 0, 2_000_000, 4_000_000),
        "Sedang": trapesium(penghasilan, 2_000_000, 4_000_000,
                            5_000_000, 7_000_000),
        "Tinggi": trapesium(penghasilan, 5_000_000, 7_000_000,
                            10_000_000, 10_000_000),
    }
def fuzzifikasi_tanggungan(tanggungan):
    return {
        "Sedikit": trapesium(tanggungan, 0, 0, 1, 2),
        "Sedang": trapesium(tanggungan, 1, 2, 3, 4),
        "Banyak": trapesium(tanggungan, 3, 4, 6, 6),
    }
# Aturan Sugeno Orde 0 (konsekuen konstanta)
aturan_sugeno = [
    ("R1", "Rendah", "Banyak", 500_000),
    ("R2", "Sedang", "Sedang", 1_500_000),
    ("R3", "Tinggi", "Banyak", 2_500_000),
    ("R4", "Tinggi", "Sedikit", 4_000_000),
]
def hitung_sugeno_ukt(penghasilan, tanggungan):
    mu_p = fuzzifikasi_penghasilan(penghasilan)
    mu_t = fuzzifikasi_tanggungan(tanggungan)
    print("\nDERAJAT KEANGGOTAAN PENGHASILAN")
    for label, nilai in mu_p.items():
        print(f"  {label:<10}: {nilai:.4f}")
    print("\nDERAJAT KEANGGOTAAN TANGGUNGAN")
    for label, nilai in mu_t.items():
        print(f"  {label:<10}: {nilai:.4f}")
    print("\nEVALUASI ATURAN SUGENO ORDE 0")
    print("-" * 70)
    total_alpha = 0.0
    total_ukt = 0.0
    for kode, p_label, t_label, nominal in aturan_sugeno:
        alpha = min(mu_p[p_label], mu_t[t_label])
        print(f"  {kode}: IF Penghasilan {p_label} AND "
              f"Tanggungan {t_label} THEN UKT Rp{nominal:,.0f} "
              f"| Alpha = {alpha:.4f}")
        if alpha > 0:
            total_alpha += alpha
            total_ukt += alpha * nominal
    print("-" * 70)
    if total_alpha == 0:
        print("Tidak ada aturan aktif.")
        return None
    hasil = total_ukt / total_alpha
    print(f"\nNominal UKT (Sugeno Orde 0): Rp{hasil:,.0f}")
    return hasil


if __name__ == "__main__":
    print("=" * 70)
    print("SISTEM PENENTUAN UKT MAHASISWA - METODE SUGENO ORDE 0")
    print("=" * 70)

    penghasilan = float(input("Masukkan penghasilan orang tua per bulan (Rp): "))
    tanggungan = int(input("Masukkan jumlah tanggungan keluarga: "))

    hasil = hitung_sugeno_ukt(penghasilan, tanggungan)

    if hasil is not None:
        print("\n" + "=" * 70)
        print(f"UKT MAHASISWA (SUGENO): Rp{hasil:,.0f}")
        print("=" * 70)
        
# ==========================================================
# SISTEM PENENTUAN UKT - METODE TSUKAMOTO
# ==========================================================

def invers_monoton_naik(alpha, a, b):
    return a + alpha * (b - a)
def invers_monoton_turun(alpha, a, b):
    return b - alpha * (b - a)
# Konfigurasi konsekuen Tsukamoto
# (kode, p_label, t_label, jenis_monoton, batas_bawah, batas_atas)
aturan_tsukamoto = [
    ("R1", "Rendah", "Banyak", "turun", 500_000, 1_500_000),
    ("R2", "Sedang", "Sedang", "naik", 1_000_000, 2_000_000),
    ("R3", "Tinggi", "Banyak", "naik", 2_000_000, 3_000_000),
    ("R4", "Tinggi", "Sedikit", "naik", 3_000_000, 4_000_000),
]
def hitung_tsukamoto_ukt(penghasilan, tanggungan):
    mu_p = fuzzifikasi_penghasilan(penghasilan)
    mu_t = fuzzifikasi_tanggungan(tanggungan)
    print("\nEVALUASI ATURAN TSUKAMOTO")
    print("-" * 70)
    total_alpha = 0.0
    total_ukt = 0.0
    for kode, p_label, t_label, jenis, a, b in aturan_tsukamoto:
        alpha = min(mu_p[p_label], mu_t[t_label])
        if jenis == "naik":
            z = invers_monoton_naik(alpha, a, b)
        else:
            z = invers_monoton_turun(alpha, a, b)

        print(f"  {kode}: Alpha = {alpha:.4f} | "
              f"z = Rp{z:,.0f} (monoton {jenis})")
        if alpha > 0:
            total_alpha += alpha
            total_ukt += alpha * z
    print("-" * 70)
    if total_alpha == 0:
        print("Tidak ada aturan aktif.")
        return None
    hasil = total_ukt / total_alpha
    print(f"\nNominal UKT (Tsukamoto): Rp{hasil:,.0f}")
    return hasil


if __name__ == "__main__":
    print("=" * 70)
    print("SISTEM PENENTUAN UKT MAHASISWA - METODE TSUKAMOTO")
    print("=" * 70)

    penghasilan = float(input("Masukkan penghasilan orang tua per bulan (Rp): "))
    tanggungan = int(input("Masukkan jumlah tanggungan keluarga: "))

    hasil = hitung_tsukamoto_ukt(penghasilan, tanggungan)

    if hasil is not None:
        print("\n" + "=" * 70)
        print(f"UKT MAHASISWA (TSUKAMOTO): Rp{hasil:,.0f}")
        print("=" * 70)
