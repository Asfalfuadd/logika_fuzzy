# ==========================================================
# SISTEM PENENTUAN PENETAPAN UKT MAHASISWA
# Fuzzy Decision Support System - Metode Sugeno Orde 0
# Asesmen Modul 2 - Logika Fuzzy
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# ==========================================================
# 1. FUNGSI KEANGGOTAAN
# ==========================================================

def trapesium(x, a, b, c, d):
    """Fungsi keanggotaan trapesium umum dengan paramater (a, b, c, d)."""
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
# 2. FUZZIFIKASI VARIABEL INPUT
# ==========================================================

def fuzzifikasi_penghasilan(penghasilan):
    """Fuzzifikasi Penghasilan Orang Tua (Rp/bulan, 0-10 juta)."""
    return {
        "Rendah": trapesium(penghasilan, 0, 0, 2_000_000, 4_000_000),
        "Sedang": trapesium(penghasilan, 2_000_000, 4_000_000,
                            5_000_000, 7_000_000),
        "Tinggi": trapesium(penghasilan, 5_000_000, 7_000_000,
                            10_000_000, 10_000_000),
    }


def fuzzifikasi_tanggungan(tanggungan):
    """Fuzzifikasi Jumlah Tanggungan Keluarga (1-6 orang)."""
    return {
        "Sedikit": trapesium(tanggungan, 0, 0, 1, 2),
        "Sedang": trapesium(tanggungan, 1, 2, 3, 4),
        "Banyak": trapesium(tanggungan, 3, 4, 6, 6),
    }


# ==========================================================
# 3. BASIS ATURAN (RULE BASE) - 9 ATURAN
# ==========================================================
# (kode, label_penghasilan, label_tanggungan, nominal_ukt)
aturan = [
    ("R1", "Rendah", "Sedikit", 1_000_000),
    ("R2", "Rendah", "Sedang",    750_000),
    ("R3", "Rendah", "Banyak",    500_000),
    ("R4", "Sedang", "Sedikit", 2_000_000),
    ("R5", "Sedang", "Sedang",  1_500_000),
    ("R6", "Sedang", "Banyak",  1_000_000),
    ("R7", "Tinggi", "Sedikit", 4_000_000),
    ("R8", "Tinggi", "Sedang",  3_000_000),
    ("R9", "Tinggi", "Banyak",  2_500_000),
]


# ==========================================================
# 4. MESIN INFERENSI SUGENO ORDE 0
# ==========================================================

def mesin_inferensi(mu_penghasilan, mu_tanggungan, verbose=False):
    """Evaluasi seluruh aturan, kembalikan (alphas, z_nominals)."""
    alphas, zs, aktif = [], [], []
    for kode, p_label, t_label, nominal in aturan:
        alpha = min(mu_penghasilan[p_label], mu_tanggungan[t_label])
        alphas.append(alpha)
        zs.append(nominal)
        if alpha > 0:
            aktif.append((kode, alpha, nominal))
        if verbose:
            print(f"  {kode}: IF Penghasilan {p_label:<6} AND "
                  f"Tanggungan {t_label:<6} THEN Rp{nominal:>10,.0f} "
                  f"| alpha = {alpha:.4f}")
    return alphas, zs, aktif


# ==========================================================
# 5. DEFUZZIFIKASI: WEIGHTED AVERAGE
# ==========================================================

def defuzzifikasi_sugeno(alphas, zs):
    """Rata-rata berbobot: UKT = sum(alpha_i * z_i) / sum(alpha_i)."""
    total_alpha = sum(alphas)
    if total_alpha == 0:
        return None
    return sum(a * z for a, z in zip(alphas, zs)) / total_alpha


# ==========================================================
# 6. PIPELINE UTUH SISTEM FUZZY
# ==========================================================

def evaluasi_sistem_fuzzy(penghasilan, tanggungan, verbose=False):
    """Fuzzifikasi -> Inferensi -> Defuzzifikasi. Hasil nominal Rupiah."""
    mu_p = fuzzifikasi_penghasilan(penghasilan)
    mu_t = fuzzifikasi_tanggungan(tanggungan)

    if verbose:
        print("\nDERAJAT KEANGGOTAAN PENGHASILAN")
        for label, nilai in mu_p.items():
            print(f"  {label:<10}: {nilai:.4f}")
        print("DERAJAT KEANGGOTAAN TANGGUNGAN")
        for label, nilai in mu_t.items():
            print(f"  {label:<10}: {nilai:.4f}")
        print("\nEVALUASI BASIS ATURAN")
        print("-" * 75)

    alphas, zs, aktif = mesin_inferensi(mu_p, mu_t, verbose=verbose)

    if verbose:
        print("-" * 75)
        print(f"  Aturan aktif: {[k for k, _, _ in aktif]}")

    return defuzzifikasi_sugeno(alphas, zs)


# ==========================================================
# 7. VISUALISASI DECISION SURFACE 3D
# ==========================================================

def plot_decision_surface(nama_file="decision_surface_ukt.png"):
    x1_range = np.linspace(0, 10_000_000, 50)
    x2_range = np.linspace(0, 6, 50)
    X1, X2 = np.meshgrid(x1_range, x2_range)
    Z_out = np.zeros_like(X1)

    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            hasil = evaluasi_sistem_fuzzy(X1[i, j], X2[i, j])
            Z_out[i, j] = hasil if hasil is not None else np.nan

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X1 / 1e6, X2, Z_out / 1e6, cmap="viridis",
                           edgecolor="none", alpha=0.9)
    ax.set_xlabel("Penghasilan Orang Tua (Juta Rp)")
    ax.set_ylabel("Jumlah Tanggungan (orang)")
    ax.set_zlabel("Nominal UKT (Juta Rp)")
    ax.set_title("Decision Surface Plot\nSistem Penentuan UKT Mahasiswa "
                 "(Sugeno Orde 0)", fontweight="bold")
    fig.colorbar(surf, shrink=0.5, aspect=5, label="UKT (Juta Rp)")
    plt.savefig(nama_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"\nDecision surface disimpan: {nama_file}")


# ==========================================================
# 8. PROGRAM UTAMA: INPUT CRISP -> KEPUTUSAN KONKRET
# ==========================================================

if __name__ == "__main__":
    print("=" * 75)
    print("SISTEM PENENTUAN PENETAPAN UKT MAHASISWA")
    print("Fuzzy Decision System - Metode Sugeno Orde 0")
    print("=" * 75)

    penghasilan = float(input("Masukkan penghasilan orang tua/bulan (Rp): "))
    tanggungan = int(input("Masukkan jumlah tanggungan keluarga (orang): "))

    if penghasilan < 0 or tanggungan < 1:
        print("Input tidak valid.")
    elif penghasilan > 10_000_000 or tanggungan > 6:
        print("Input di luar rentang model fuzzy (0-10jt, 1-6 orang).")
    else:
        hasil = evaluasi_sistem_fuzzy(penghasilan, tanggungan, verbose=True)
        if hasil is None:
            print("UKT tidak dapat ditentukan (tidak ada aturan aktif).")
        else:
            print("\n" + "=" * 75)
            print(f"HASIL KEPUTUSAN: UKT MAHASISWA = Rp{hasil:,.0f}")
            print("=" * 75)
