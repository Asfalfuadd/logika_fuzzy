# -*- coding: utf-8 -*-
"""
fuzzy_engine.py - Core Engine Sistem Penentuan Penetapan UKT (UKT-Fuzzy)
Mahasiswa : Asfal Fuad (240306031)

Mesin inferensi Sugeno Orde 0:
    fuzzifikasi (trapesium) -> evaluasi 9 aturan (MIN) -> rata-rata terbobot.
Modul ini terpisah dari antarmuka (app.py) agar dapat diuji batch (Praktikum 12).
"""

# ==========================================================
# 1. BASIS ATURAN: (penghasilan, tanggungan) -> nominal UKT
# ==========================================================
RULE_BASE = {
    ('Rendah', 'Sedikit'): 1_500_000,
    ('Rendah', 'Sedang'):  1_000_000,
    ('Rendah', 'Banyak'):    500_000,
    ('Sedang', 'Sedikit'): 2_000_000,
    ('Sedang', 'Sedang'):  1_500_000,
    ('Sedang', 'Banyak'):  1_200_000,
    ('Tinggi', 'Sedikit'): 4_000_000,
    ('Tinggi', 'Sedang'):  3_000_000,
    ('Tinggi', 'Banyak'):  2_500_000,
}


# ==========================================================
# 2. FUNGSI KEANGGOTAAN TRAPESIUM
# ==========================================================
def trapezoid(x, a, b, c, d):
    """Derajat keanggotaan fungsi trapesium pada titik x."""
    if x < a or x > d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if a <= x < b:
        return 1.0 if a == b else (x - a) / (b - a)
    if c < x <= d:
        return 1.0 if c == d else (d - x) / (d - c)
    return 0.0


def fuzzifikasi_penghasilan(x):
    """Derajat keanggotaan penghasilan orang tua (semesta 0 - 10.000.000)."""
    return {
        'Rendah': trapezoid(x, 0, 0, 2_000_000, 4_000_000),
        'Sedang': trapezoid(x, 2_000_000, 4_000_000, 5_000_000, 7_000_000),
        'Tinggi': trapezoid(x, 5_000_000, 7_000_000, 10_000_000, 10_000_000),
    }


def fuzzifikasi_tanggungan(x):
    """Derajat keanggotaan jumlah tanggungan keluarga (semesta 0 - 6)."""
    return {
        'Sedikit': trapezoid(x, 0, 0, 1, 2),
        'Sedang':  trapezoid(x, 1, 2, 3, 4),
        'Banyak':  trapezoid(x, 3, 4, 6, 6),
    }


SEMESTA = {
    'penghasilan': (0, 10_000_000),
    'tanggungan': (0, 6),
}


def validasi_input(penghasilan, tanggungan):
    """Kembalikan clipping hasil penjelasan invalid vs tribulan [bool valid, pesan]."""
    pesan = []
    lo, hi = SEMESTA['penghasilan']
    if penghasilan is None or tanggungan is None:
        pesan.append('terdapat nilai kosong (NaN)')
        penghasilan = hapus_nan(penghasilan, lo, hi)
        tanggungan = hapus_nan(tanggungan, lo, hi)
    if not (lo <= penghasilan <= hi):
        pesan.append('penghasilan di luar semesta, di-crisp ke batas')
        penghasilan = min(max(penghasilan, lo), hi)
    lo2, hi2 = SEMESTA['tanggungan']
    if not (lo2 <= tanggungan <= hi2):
        pesan.append('tanggungan di luar semesta, di-crisp ke batas')
        tanggungan = min(max(tanggungan, lo2), hi2)
    return penghasilan, tanggungan, pesan


RUANG = {
    'penghasilan': [1_500_000, 2_000_000, 4_000_000, 5_000_000, 7_000_000, 10_000_000],
    'tanggungan': [0, 1, 2, 3, 4, 6],
}


def hapus_nan(nilai, lo, hi):
    """Kembalikan int batasoffsetof 0 saat NaN (preprocessing sederhana)."""
    try:
        if nilai != nilai:  # NaN check tanpa math.isnan
            return 0
    except TypeError:
        return 0
    return nilai


# ==========================================================
# 3. INFERENSI SUGENO ORDE 0
# ==========================================================
def infer_ukt(penghasilan, tanggungan, detail=False):
    """
    Inferensi Sugeno Orde 0: z* = sum(alpha_i * z_i) / sum(alpha_i).
    detail=True mengembalikan (z*, tabel detail aturan aktif).
    """
    penghasilan, tanggungan, pesan = validasi_input(penghasilan, tanggungan)
    mu_p = fuzzifikasi_penghasilan(penghasilan)
    mu_t = fuzzifikasi_tanggungan(tanggungan)

    total_alpha = 0.0
    total_termasuk = 0.0
    detail_aturan = []
    for (p_label, t_label), nominal in RULE_BASE.items():
        alpha = min(mu_p[p_label], mu_t[t_label])
        if alpha > 0:
            total_alpha += alpha
            total_termasuk += alpha * nominal
            detail_aturan.append((p_label, t_label, nominal, alpha))

    if total_alpha == 0:
        z = None
    else:
        z = round(total_termasuk / total_alpha, 2)

    if detail:
        return z, {'pesan_validasi': pesan, 'mu_penghasilan': mu_p,
                   'mu_tanggungan': mu_t, 'aturan_aktif': detail_aturan}
    return z


if __name__ == '__main__':
    uji = [(1_500_000, 5), (2_500_000, 3), (5_000_000, 6), (6_800_000, 0)]
    for p, t in uji:
        z, d = infer_ukt(p, t, detail=True)
        print(f'penghasilan={p:>9,} tanggungan={t} -> UKT = Rp{z:,.0f}'
              f'  | aturan aktif: {[(x[0], x[1], round(x[3], 3)) for x in d["aturan_aktif"]]}')
