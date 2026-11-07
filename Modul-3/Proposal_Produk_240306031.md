# PROPOSAL PRODUK SISTEM PENDUKUNG KEPUTUSAN FUZZY

## Judul Produk: Sistem Penetapan UKT Mahasiswa Berbasis Logika Fuzzy (UKT-Fuzzy)

> **Mahasiswa:** Asfal Fuad — 240306031
> **Modul:** 3 — Praktikum 11 (Logika Fuzzy)
> **Lanjutan:** Sistem Penentuan UKT (Praktikum 9, metode Sugeno/Tsukamoto)

---

## 1. Latar Belakang & Problem Statement

### Masalah nyata apa yang ingin diselesaikan?
Penetapan kelompok UKT 1–8 mahasiswa selama ini mengandalkan pemotongan kriteria
tegas (penghasilan orang tua, jumlah tanggungan keluarga, kondisi rumah). Akibatnya
banyak terjadi **kasus tepi (boundary case)** yang terasa tidak adil: dua mahasiswa
yang penghasilan orang tuanya hanya berbeda tipis (misal Rp2.999.999 vs Rp3.000.000)
bisa masuk kelompok UKT yang berbeda tajam, dan berujung pada keberatan/banding
mahasiswa.

### Mengapa logika Boolean/aturan kaku gagal menyelesaikannya secara optimal?
1. Aturan kaku tidak mampu merepresentasikan makna linguistik seperti
   **"agak rendah"** atau **"agak tinggi"**.
2. Kemampuan ekonomi keluarga adalah besaran **bergradasi**, tetapi Boolean memaksa
   pemotongan nilai secara biner pada batas tertentu.
3. Ada dua pengaruh yang **arahnya berlawanan**: penghasilan naik → UKT naik,
   tanggungan naik → UKT turun. Aturan kaku cenderung hanya menangkap salah satu sisi.

Logika fuzzy mengatasi hal ini melalui fungsi keanggotaan yang **tumpang tindih**,
sehingga kasus tepi mendapat bobot pada lebih dari satu kelompok dan keputusan
menjadi lebih halus dan konsisten.

### Siapa target pengguna (stakeholder)?
- Mahasiswa pemohon penetapan UKT (pengguna akhir)
- Petugas bagian keuangan/direktorat kemahasiswaan (operator penetapan)
- Unit layanan konsultasi keuangan yang menangani banding

---

## 2. Spesifikasi Variabel Sistem

Semesta & label mengikuti rancangan yang sama dengan Praktikum 9 (fungsi trapesium):

| Variabel | Nama | Satuan | Semesta | Label Linguistik & Domain |
|---|---|---|---|---|
| Input 1 | Penghasilan Orang Tua | Rp/bulan | 0 – 10.000.000 | Rendah: trap(x, 0, 0, 2.000.000, 4.000.000); Sedang: trap(x, 2.000.000, 4.000.000, 5.000.000, 7.000.000); Tinggi: trap(x, 5.000.000, 7.000.000, 10.000.000, 10.000.000) |
| Input 2 | Jumlah Tanggungan Keluarga | orang | 0 – 6 | Sedikit: trap(x, 0, 0, 1, 2); Sedang: trap(x, 1, 2, 3, 4); Banyak: trap(x, 3, 4, 6, 6) |
| Output | Nominal UKT per Semester | Rp | 500.000 – 4.000.000 | Konsekuen konstanta Sugeno (pemetaan kelompok 1-3 sampai 6-8): 500.000 / 1.000.000 / 1.200.000 / 1.500.000 / 2.000.000 / 2.500.000 / 3.000.000 / 4.000.000 |

---

## 3. Rancangan Basis Aturan (Rule Base)

Matriks kombinatorial lengkap **3 x 3 = 9 aturan** (menggabungkan R1–R4 Praktikum 9
dan aturan pengisi yang logis untuk kombinasi sisanya):

| Penghasilan \ Tanggungan | Sedikit | Sedang | Banyak |
|---|---|---|---|
| **Rendah** | Rp1.500.000 | Rp1.000.000 | Rp500.000 |
| **Sedang** | Rp2.000.000 | Rp1.500.000 | Rp1.200.000 |
| **Tinggi** | Rp4.000.000 | Rp3.000.000 | Rp2.500.000 |

Contoh notasi aturan:
- **R1:** IF Penghasilan ADALAH Rendah AND Tanggungan ADALAH Banyak THEN UKT = Rp500.000
- **R2:** IF Penghasilan ADALAH Sedang AND Tanggungan ADALAH Sedang THEN UKT = Rp1.500.000
- **R3:** IF Penghasilan ADALAH Tinggi AND Tanggungan ADALAH Banyak THEN UKT = Rp2.500.000
- **R4:** IF Penghasilan ADALAH Tinggi AND Tanggungan ADALAH Sedikit THEN UKT = Rp4.000.000

Implementasi rule base (`src/fuzzy_engine.py`, potongan kode / excerpt):

```python
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
```

---

## 4. Metode Inferensi & Defuzzifikasi yang Dipilih

**Pilihan: Sugeno Orde 0 (konsekuen konstanta) dengan defuzzifikasi rata-rata terbobot**

```
z* = Σ(αi × zi) / Σαi
```

Argumentasi ilmiah:
1. Produk berorientasi angka: keluaran nominal rupiah langsung terdefinisi tanpa
   defuzzifikasi kurva/centroid, sehingga komputasi ringan dan waktu respon < 1 detik.
2. Sudah tervalidasi pada Praktikum 9: metode ini memberi output diskret antar-selang
   kelompok yang mudah dipetakan ke regulasi kelompok UKT dan audit banding.
3. Alternatif Mamdani lebih intuitif bagi manusia, tetapi outputnya berupa kurva yang
   harus didefuzzifikasi (lebih berat); Sugeno tetap dapat dikembalikan dari basis
   aturan Mamdani bila nanti dibutuhkan presentasi kurva keanggotaan.
4. Keterlanjutan riset: konsekuen Sugeno mudah dioptimasi (bentuk linear, seperti
   ANFIS) bila tersedia data historis penetapan UKT untuk kalibrasi nominal otomatis.

---

## 5. Rencana Arsitektur Perangkat Lunak

### Diagram alur data (versi teks dari Mermaid `graph TD`)

```text
Pengguna/Dataset --Nilai Input--> Modul UI Streamlit
Modul UI Streamlit --Validasi Data--> Fuzzy Engine Backend
Fuzzy Engine Backend --Fuzzifikasi--> Membership Functions
Fuzzy Engine Backend --Evaluasi--> Rule Base
Fuzzy Engine Backend --Kalkulasi--> Inference & Defuzzifier
Inference & Defuzzifier --Hasil Numerik & Kurva--> Modul UI Streamlit
Modul UI Streamlit --Tampilan Rekomendasi--> Layar Pengguna/Dashboard
```

### Struktur folder proyek

```text
Modul-3/
├── Proposal_Produk_240306031.md
├── src/
│   ├── __init__.py
│   ├── fuzzy_engine.py       # Logika inferensi fuzzy
│   └── app.py                # Antarmuka Streamlit (disiapkan Pertemuan 13)
└── data/
    └── test_cases.csv        # Dataset pengujian (disiapkan Pertemuan 12)
```

### Rencana UI (Streamlit)

- Slider **Penghasilan Orang Tua** (0 – 10.000.000) dan **Jumlah Tanggungan** (0 – 6)
- Tombol **Hitung**
- Kartu hasil: nominal UKT (Rp)
- Tabel derivasi: derajat keanggotaan, aturan aktif + firing strength
- Grafik kurva keanggotaan hasil agregasi (matplotlib)
