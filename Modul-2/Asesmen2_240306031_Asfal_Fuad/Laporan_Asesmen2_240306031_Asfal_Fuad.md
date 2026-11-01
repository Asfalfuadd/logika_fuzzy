# LAPORAN ASESMEN MODUL 2 — FINAL PRACTICAL ASSIGNMENT 2

## Fuzzy Decision Support System

---

# 1. Identitas & Judul Proyek

| Keterangan | Isi |
|---|---|
| **Nama** | Asfal Fuad |
| **NIM** | 240306031 |
| **Kelas / Prodi** | Teknologi Informasi — Fakultas Dakwah dan Ilmu Komunikasi |
| **Universitas** | Universitas Islam Negeri Mataram |
| **Mata Kuliah** | Logika Fuzzy — Modul 2 |
| **Nama Proyek** | Sistem Penentuan Penetapan UKT Mahasiswa Berbasis Logika Fuzzy |
| **Tahap** | Tahap 2: Fuzzy Decision System (kelanjutan Modul 1: Tahap Modeling) |
| **Repository** | https://github.com/Asfalfuadd/logika_fuzzy |
| **Berkas Program** | `Praktikum10_240306031.py` |

Proyek ini merupakan kelanjutan dari Modul 1 (Tahap 1: Modeling). Pada Modul 1 telah dibangun model variabel dan fungsi keanggotaan fuzzy untuk penentuan UKT. Pada asesmen ini, model tersebut dikembangkan menjadi **sistem pengambil keputusan (Fuzzy Decision System)** yang lengkap: mulai dari basis aturan, mesin inferensi, defuzzifikasi, visualisasi decision surface, hingga pengujian skenario kasus nyata.

---

# 2. Ringkasan Model Variabel Fuzzy (Review Modul 1)

## 2.1 Deskripsi Kasus

Penetapan Uang Kuliah Tunggal (UKT) merupakan proses menentukan besaran biaya pendidikan yang harus dibayarkan mahasiswa berdasarkan kondisi ekonomi keluarganya. Logika fuzzy digunakan karena kondisi ekonomi bersifat gradasi (tidak tegas): penghasilan "sedikit lebih dari 4 juta" tidak serta-merta mengubah kelompok mampu menjadi tidak mampu begitu saja.

Sistem menerima dua kondisi ekonomi keluarga dan menghasilkan satu nominal UKT langsung dalam rupiah. Model ini bersifat simulasi pembelajaran, bukan ketentuan tarif resmi kampus.

## 2.2 Variabel Input 1: Penghasilan Orang Tua (P)

- **Domain:** Rp0 – Rp10.000.000 per bulan
- **Label linguistik (3 himpunan):**
  - `Rendah`: trapesium (0, 0, 2.000.000, 4.000.000)
  - `Sedang`: trapesium (2.000.000, 4.000.000, 5.000.000, 7.000.000)
  - `Tinggi`: trapesium (5.000.000, 7.000.000, 10.000.000, 10.000.000)

## 2.3 Variabel Input 2: Jumlah Tanggungan Keluarga (T)

- **Domain:** 1 – 6 orang
- **Label linguistik (3 himpunan):**
  - `Sedikit`: trapesium (0, 0, 1, 2)
  - `Sedang`: trapesium (1, 2, 3, 4)
  - `Banyak`: trapesium (3, 4, 6, 6)

## 2.4 Variabel Output: Nominal UKT (Z)

- **Domain:** Rp500.000 – Rp4.000.000
- **Perwakilan numerik (9 nilai konstanta Sugeno):** Rp500.000, Rp750.000, Rp1.000.000, Rp1.500.000, Rp2.000.000, Rp2.500.000, Rp3.000.000, Rp4.000.000 (dan derivasinya)
- Output berupa **nilai tegas dalam rupiah** (bukan grade huruf), sesuai bentuk konsekuen metode Sugeno Orde 0.

## 2.5 Invarian Model dari Modul 1

1. Fungsi keanggotaan berbentuk **trapesium** dengan overlap 1 unit/2 juta di tiap batas, sehingga derajat keanggotaan setiap input selalu berjumlah 1 (normalisasi alami) pada rentang domain.
2. Operator premis menggunakan **Zadeh min** untuk AND.
3. Semakin besar penghasilan → UKT naik; semakin banyak tanggungan → UKT turun. Arah logika ini menjadi fondasi penyusunan basis aturan pada bagian berikutnya.

---

# 3. Perancangan Basis Aturan (Rule Base Matrix)

## 3.1 Matriks Basis Aturan 3 × 3 = 9 Aturan

| Penghasilan \ Tanggungan | Sedikit | Sedang | Banyak |
|---|---|---|---|
| **Rendah** | R1: Rp1.000.000 | R2: Rp750.000 | R3: Rp500.000 |
| **Sedang** | R4: Rp2.000.000 | R5: Rp1.500.000 | R6: Rp1.000.000 |
| **Tinggi** | R7: Rp4.000.000 | R8: Rp3.000.000 | R9: Rp2.500.000 |

Bentuk IF-THEN:

- **R1:** IF Penghasilan *Rendah* AND Tanggungan *Sedikit* THEN UKT = Rp1.000.000
- **R2:** IF Penghasilan *Rendah* AND Tanggungan *Sedang* THEN UKT = Rp750.000
- **R3:** IF Penghasilan *Rendah* AND Tanggungan *Banyak* THEN UKT = Rp500.000
- **R4:** IF Penghasilan *Sedang* AND Tanggungan *Sedikit* THEN UKT = Rp2.000.000
- **R5:** IF Penghasilan *Sedang* AND Tanggungan *Sedang* THEN UKT = Rp1.500.000
- **R6:** IF Penghasilan *Sedang* AND Tanggungan *Banyak* THEN UKT = Rp1.000.000
- **R7:** IF Penghasilan *Tinggi* AND Tanggungan *Sedikit* THEN UKT = Rp4.000.000
- **R8:** IF Penghasilan *Tinggi* AND Tanggungan *Sedang* THEN UKT = Rp3.000.000
- **R9:** IF Penghasilan *Tinggi* AND Tanggungan *Banyak* THEN UKT = Rp2.500.000

## 3.2 Verifikasi Kualitas Basis Aturan

Persyaratan asesmen: basis aturan harus **konsisten, lengkap (complete), dan bebas konflik**.

| Kriteria | Verifikasi | Status |
|---|---|---|
| **Lengkap** | Semua 9 kombinasi label (3 pengelasan × 3 tanggungan) memiliki aturan; tidak ada sel mati pada matriks. Selain itu, karena fungsi keanggotaan saling menutup (overlap penuh) pada domain, setiap input valid pasti mengaktifkan minimal satu aturan. | ✅ |
| **Konsisten** | Orientasi logika seragam: keanggotaan penghasilan naik → konsekuen turun derajat beban (nominal naik); tanggungan naik → nominal turun. Tidak ada pasangan aturan yang bertentangan arah. | ✅ |
| **Bebas konflik** | Tidak ada dua aturan dengan premis identik tetapi konsekuen berbeda. Setiap sel matriks unik. | ✅ |

**Justifikasi nilai konsekuen:** Nilai konstanta disusun monoton per baris dan kolom. Contoh: pada baris Rendah, tanggungan Sedikit (1.000.000) > Sedang (750.000) > Banyak (500.000), karena semakin sedikit tanggungan, beban keluarga lebih ringan sehingga UKT lebih tinggi. Pola sama berlaku untuk baris Sedang dan Tinggi.

---

# 4. Metode Inferensi & Justifikasi Pemilihan

## 4.1 Metode Terpilih: **Sugeno Orde 0 (Zero-Order TSK)**

## 4.2 Justifikasi

Metode **Sugeno Orde 0** dipilih karena sistem penetapan UKT membutuhkan keluaran berupa **nominal rupiah yang pasti dan langsung dapat dipakai** — bukan kategori atau grade — sehingga konsekuen berbentuk konstanta numerik adalah representasi paling alami untuk kasus ini. Defuzzifikasi cukup menggunakan **rata-rata terbobot (weighted average)** yang hanya melibatkan perkalian dan penjumlahan aljabar sederhana; tidak ada proses integrasi numerik kurva agregasi sebagaimana pada Mamdani yang lebih berat secara komputasi. Keunggulan lainnya, output Sugeno berbentuk fungsi matematis tegas sehingga **mudah diintegrasikan dengan aplikasi web pada Modul 3** (endpoint backend cukup memanggil fungsi Python murni tanpa dependensi grafik atau perhitungan integral), dan struktur aturannya dapat diperluas ke ANFIS apabila di kemudian hari nilai konstanta di-optimalisasi dari data historis penetapan UKT. Tsukamoto tidak dipilih karena keunggulannya (penalaran monoton per aturan) tidak memberi manfaat tambahan pada kasus yang konsekuen-nya memang sudah numerik konstanta, sedangkan Mamdani tidak dipilih karena output kurva fuzzy perlu di-defuzzifikasi ulang padahal nilai konsekuen sistem ini telah disepakati sebagai nominal baku.

## 4.3 Mekanisme Inferensi Sugeno Orde 0

1. **Fuzzifikasi:** hitung μ untuk setiap label pada kedua input.
2. **Firing strength** tiap aturan: αᵢ = min(μPenghasilan(x), μTanggungan(y)).
3. **Inferensi:** konsekuen tiap aturan adalah konstanta zᵢ (nominal UKT).
4. **Defuzzifikasi (weighted average):**

```
             Σ (αᵢ × zᵢ)
  UKT*  =  ─────────────────
              Σ αᵢ
```

Hasil adalah **nominal UKT langsung dalam rupiah**.

---

# 5. Implementasi Program Python (Full Code & Penjelasan)

## 5.1 Struktur Modular Program

| Modul | Fungsi | Tanggung Jawab |
|---|---|---|
| 1 | `trapesium()` | Fungsi keanggotaan trapesium universal |
| 2 | `fuzzifikasi_penghasilan()` | Fuzzifikasi input 1 |
| 3 | `fuzzifikasi_tanggungan()` | Fuzzifikasi input 2 |
| 4 | `aturan` (list) | Basis aturan 9 aturan |
| 5 | `mesin_inferensi()` | Evaluasi firing strength seluruh aturan |
| 6 | `defuzzifikasi_sugeno()` | Weighted average → nominal UKT |
| 7 | `evaluasi_sistem_fuzzy()` | Pipeline utuh: fuzzifikasi → inferensi → defuzzifikasi |
| 8 | `plot_decision_surface()` | Visualisasi 3D permukaan keputusan |
| 9 | `main()` | Input crisp dari pengguna, output keputusan konkret |

## 5.2 Kode Program Lengkap

```python
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
```

## 5.3 Penjelasan Kunci Implementasi

1. **Modularitas:** setiap tahap (fuzzifikasi, inferensi, defuzzifikasi, visualisasi, main) berada pada fungsi terpisah sesuai rubrik "modularitas kode Python". Fungsi `evaluasi_sistem_fuzzy()` juga dipakai ulang oleh `plot_decision_surface()` tanpa duplikasi logika.
2. **Operator AND Zadeh min:** firing strength per aturan dihitung dengan `min()` sesuai konsep Modul 1.
3. **Defuzzifikasi weighted average:** `defuzzifikasi_sugeno()` langsung menghasilkan rupiah. Jika `Σα = 0` dikembalikan `None` dan program menampilkan pesan bahwa UKT tidak dapat ditentukan (defensive check).
4. **Validasi input:** rentang domain divalidasi (Rp0–10jt, 1–6 orang) agar input tak valid tidak menghasilkan keputusan di luar model.

---

# 6. Hasil Pengujian dan Analisis Decision Surface

## 6.1 Lima Skenario Pengujian (kasus ekstrem dan normal)

| No | Penghasilan | Tanggungan | Karakter Kasus | UKT (Sugeno) |
|:--:|---|:--:|---|---:|
| S1 | Rp1.500.000 | 5 | Ekstrem miskin (penghasilan rendah penuh, tanggungan banyak penuh) | **Rp500.000** |
| S2 | Rp2.500.000 | 3 | Normal (transisi rendah–sedang, tanggungan sedang penuh) | **Rp937.500** |
| S3 | Rp3.500.000 | 2 | Normal (transisi rendah–sedang, tanggungan sedang penuh) | **Rp1.312.500** |
| S4 | Rp6.000.000 | 4 | Ekstrem campuran (sedang & tinggi 0,5–0,5, tanggungan banyak penuh) | **Rp1.750.000** |
| S5 | Rp8.000.000 | 1 | Ekstrem kaya (penghasilan tinggi penuh, tanggungan sedikit penuh) | **Rp4.000.000** |

## 6.2 Detail Perhitungan tiap Skenario

**S1 — Rp1.500.000, 5 tanggungan:** μPenghasilan = (Rendah 1,0; Sedang 0; Tinggi 0), μTanggungan = (Sedikit 0; Sedang 0; Banyak 1,0). Hanya R3 aktif (α=1,0; z=500.000). Hasil = 500.000.

**S2 — Rp2.500.000, 3 tanggungan:** μPenghasilan = (Rendah 0,75; Sedang 0,25; Tinggi 0), μTanggungan = (Sedang 1,0). Aturan aktif: R2 (α=0,75; z=750.000) dan R5 (α=0,25; z=1.500.000).
UKT* = (0,75×750.000 + 0,25×1.500.000) / (0,75+0,25) = (562.500 + 375.000) / 1,0 = **Rp937.500**.

**S3 — Rp3.500.000, 2 tanggungan:** μPenghasilan = (Rendah 0,25; Sedang 0,75); μTanggungan = (Sedang 1,0). Aktif: R2 (α=0,25) dan R5 (α=0,75).
UKT* = (0,25×750.000 + 0,75×1.500.000) / 1,0 = **Rp1.312.500**.

**S4 — Rp6.000.000, 4 tanggungan:** μPenghasilan = (Sedang 0,5; Tinggi 0,5), μTanggungan = (Banyak 1,0). Aktif: R6 (α=0,5; z=1.000.000) dan R9 (α=0,5; z=2.500.000).
UKT* = (0,5×1.000.000 + 0,5×2.500.000) / 1,0 = **Rp1.750.000**.

**S5 — Rp8.000.000, 1 tanggungan:** μPenghasilan = (Tinggi 1,0), μTanggungan = (Sedikit 1,0). Hanya R7 aktif (α=1,0; z=4.000.000). Hasil = **Rp4.000.000**.

## 6.3 Tabel Analisis Perbandingan

| No | Kasus | Perilaku Sistem | Flutter/Halus? | Sesuai Logika Ekonomi? |
|:--:|---|---|:--:|:--:|
| S1 | Ekstrem miskin | Hanya 1 aturan aktif (R3); output = konstanta aturan dominan. | Ya (stabil) | ✅ UKT terendah |
| S2 | Transisi rendah→sedang | 2 aturan aktif; hasil interpolasi 0,75:0,25 antara 750rb dan 1,5jt. | Ya | ✅ |
| S3 | Transisi rendah→sedang (kabalik S2) | Domino balik dari S2 — makin besar porsi "Sedang", makin naik UKT. | Ya | ✅ Monoton naik |
| S4 | Sesama jenis (sedang↔tinggi) | Interpolasi 0,5:0,5 antara R6 dan R9; hasil tepat di tengah kedua konstanta. | Ya | ✅ |
| S5 | Ekstrem mampu | Hanya R7 aktif; output = konstanta tertinggi. | Ya (stabil) | ✅ UKT tertinggi |

**Analisis umum:**

1. **Kelengkapan terbukti:** kelima skenario (termasuk dua kasus ekstrem dan tiga kasus transisi/mixed) selalu menghasilkan keputusan — tidak pernah ada `Σα = 0`.
2. **Kontinitas keputusan:** pada kasus transisi (S2, S3, S4), output berupa interpolasi halus antara nominal-nominal baku, bukan lompatan diskrit — inilah nilai tambah fuzzy dibanding klasifikasi tegas.
3. **Monotonisitas:** sistem konsisten dengan arah logika: penghasilan naik → UKT naik (S2→S3); kondisi ekonomi memburuk → UKT turun (S5 vs S1).
4. **Perilaku di tepi domain:** pada ekstrem (S1, S5) hanya satu aturan aktif sehingga hasil persis konstanta aturan — wajar untuk Sugeno Orde 0, dan tetap berada dalam rentang nominal baku.

## 6.4 Analisis Decision Surface

`plot_decision_surface()` menghasilkan `decision_surface_ukt.png` (300 dpi) dengan sumbu X = Penghasilan, Y = Tanggungan, Z = Nominal UKT.

Interpretasi permukaan keputusan:

1. **Gradien stabil dua arah:** permukaan naik konsisten dari kuadran (penghasilan rendah, banyak tanggungan) menuju (penghasilan tinggi, sedikit tanggungan) — tidak ada cekungan maupun puncak liar, menandakan basis aturan bebas konflik.
2. **Tangga berlegar halus:** karena konsekuen Sugeno konstanta, permukaan tersusun atas gradasi termodulasi antara 9 nilai baku, namun transisinya kontinu (bukan anak tangga kaku) karena bobot α berubah mulus.
3. **Dataran di tepi:** pada sudut ekstrem (0 juta & 6 tanggungan; 10 juta & 1 tanggungan) permukaan datar — satu aturan dominan memegang kendali penuh.
4. **Kualitas untuk integrasi:** permukaan yang kontinu dan monoton membuat fungsi `evaluasi_sistem_fuzzy()` aman dipanggil dari aplikasi web — output prediktif dan tidak berosilasi di dekat batas overlap.

---

# 7. Rencana Integrasi ke Aplikasi Web (Tahap Modul 3)

## 7.1 Arsitektur Perencanaan

```text
[Browser/Form Input]          [Backend Python]                 [Mesin Fuzzy]
penghasilan, tanggungan  -->  endpoint /api/ukt          -->   evaluasi_sistem_fuzzy()
                          <--  JSON {ukt: 937500}          <--   (fungsi murni, tanpa GUI)
```

## 7.2 Langkah Integrasi

| Tahap | Rencana |
|---|---|
| 1. Refactoring | Pindahkan `trapesium`, fungsi fuzzifikasi, basis aturan, inferensi, dan defuzzifikasi ke modul `fuzzy_engine.py` agar bisa diimpor web app tanpa memicu plot/input interaktif. |
| 2. API Layer | Bungkus `evaluasi_sistem_fuzzy()` sebagai endpoint (mis. Flask/FastAPI) yang menerima JSON dan memvalidasi rentang input (0–10jt, 1–6) — validasi sama dengan bagian 5.2. |
| 3. Respons | Kembalikan nominal UKT **beserta detail transparansi**: derajat keanggotaan tiap label, aturan aktif + α-nya, sehingga halaman web bisa menampilkan "penjelasan keputusan" ke mahasiswa. |
| 4. Batasan | Migrasi dari 4 (→9) aturan Sugeno Orde 0 tetap dipertahankan; fungsi murni tanpa dependensi matplotlib memungkinkan deploy ringan sebagai fungsi murni di server. |
| 5. Pengujian Web | Gunakan kelima skenario S1–S5 sebagai test case otomatis endpoint (unit test) agar perilaku web = perilaku matematika yang telah diverifikasi di bagian 6. |

Sistem sudah dirancang sejak awal agar **"siap diintegrasikan ke Web App Modul 3"** — pemilihan Sugeno memang sebagian didasarkan pada target integrasi ini.

