# README_APP.md — Panduan Pengguna Aplikasi UKT-Fuzzy

> **Sistem Penetapan UKT Mahasiswa Berbasis Logika Fuzzy**  
> Praktikum 13 & 14 — Modul 3 Logika Fuzzy  
> Asfal Fuad (240306031) · S1 Teknik Informatika · UIN Mataram

---

## 1. Deskripsi Singkat Aplikasi

**UKT-Fuzzy** adalah sistem pendukung keputusan (Decision Support System) yang merekomendasikan nominal Uang Kuliah Tunggal (UKT) per semester berdasarkan dua faktor ekonomi keluarga:

- **Penghasilan Orang Tua** (Rp/bulan) — semesta 0 hingga Rp10.000.000
- **Jumlah Tanggungan Keluarga** (orang) — semesta 0 hingga 6 orang

Sistem menggunakan **Logika Fuzzy Sugeno Orde 0** dengan **9 aturan fuzzy** (rule base) dan defuzzifikasi **Weighted Average**. Hasilnya adalah nominal UKT yang adil, transparan, dan dapat dipertanggungjawabkan.

**Manfaat:**
- Mengurangi subjektiivitas penetapan UKT manual
- Memberikan dasar komputasi yang konsisten dan terukur
- Memudahkan pihak universitas dalam klasifikasi golongan UKT

---

## 2. Prasyarat Instalasi

| Komponen | Versi Minimum |
|----------|---------------|
| Python   | 3.9+          |
| pip      | 21.0+         |

**Pustaka Python** (terdaftar di `requirements.txt`):
```
streamlit>=1.30.0
numpy>=1.24.0
matplotlib>=3.7.0
pandas>=2.0.0
scikit-fuzzy>=0.4.2
playwright>=1.40.0       # untuk pengujian otomatis (opsional)
python-docx>=1.1.0       # untuk generate laporan DOCX (opsional)
```

---

## 3. Cara Menjalankan

### 3.1 Instalasi Dependensi
```bash
cd Modul-3
pip install -r requirements.txt
```

### 3.2 Menjalankan Server Streamlit
```bash
cd src
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`.

### 3.3 Mode Headless (untuk CI/CD atau pengujian otomatis)
```bash
streamlit run app.py --server.headless true --server.port 8501
```

### 3.4 Parameter Query (untuk skenario uji otomatis)
Aplikasi mendukung query parameter untuk pengujian black-box tanpa interaksi manual:
```
http://localhost:8501/?penghasilan=800000&tanggungan=5
```
- `penghasilan`: integer (0 – 10.000.000)
- `tanggungan`: integer (0 – 6)

---

## 4. Panduan Antarmuka

### 4.1 Sidebar (Panel Masukan)
| Widget | Keterangan |
|--------|------------|
| **Penghasilan Orang Tua (Rp/bulan)** | Slider 0 – 10.000.000, step 100.000. Di bawah slider ditampilkan *readout* nilai besar (fluid, responsif). |
| **Jumlah Tanggungan Keluarga** | Slider 0 – 6, step 1. Readout nilai di bawah slider. |
| **Validasi Input Manual (Uji Batas)** | Expandable panel untuk menguji BVA (Boundary Value Analysis). Masukkan nilai di luar semesta (negatif, >10jt, >6) untuk melihat penanganan error sistem. |

### 4.2 Panel Kiri — Hasil Rekomendasi
- **Badge Kategori**: RINGAN (hijau), SEDANG (amber), TINGGI (merah) — label status nyata, bukan hiasan.
- **Nominal UKT**: Angka besar format Rupiah (contoh: Rp 1.250.000).
- **Skala Visual**: Progress bar 0 – Rp4 juta menunjukkan posisi nominal relatif.
- **Deskripsi**: Penjelasan singkat alasan kategori tersebut diberikan.

### 4.3 Panel Kiri — Derajat Keanggotaan (μ)
- **Chip grid** menampilkan μ untuk setiap label fuzzy:
  - Penghasilan: Rendah / Sedang / Tinggi
  - Tanggungan: Sedikit / Sedang / Banyak
- Warna chip mengikuti identitas kategori (hijau/biru/amber/merah), bukan dekorasi.
- Track visualisasi μ (0.00 – 1.00) dengan fill berwarna per kategori.

### 4.4 Panel Kiri — Aturan Aktif
Tabel aturan yang *fire* (firing strength > 0) dengan kolom:
- Aturan (contoh: "Penghasilan Rendah dan Tanggungan Banyak")
- Nominal (konsekuen aturan)
- Firing strength (α = min(μ_penghasilan, μ_tanggungan))

### 4.5 Panel Kanan — Visualisasi Grafik
1. **Aktivasi Aturan**: Bar chart horizontal firing strength tiap aturan aktif, berwarna per kategori penghasilan.
2. **Kurva Keanggotaan & Posisi Input**: Dua plot (Penghasilan & Tanggungan) menampilkan fungsi keanggotaan trapesium. Garis putus-putus vertikal = posisi input pengguna. Garis aktif (tebal, opasitas penuh) vs tidak aktif (tipis, transparan).

---

## 5. Tabel Interpretasi Keputusan

| Kategori UKT | Rentang Nominal | Golongan UKT | Interpretasi Ekonomi | Tindakan Lanjutan |
|--------------|-----------------|--------------|----------------------|-------------------|
| **RINGAN**   | < Rp1.100.000   | Golongan 1–3 | Kemampuan ekonomi keluarga tergolong rendah | Prioritaskan beasiswa penuh / subsidi penuh |
| **SEDANG**   | Rp1.100.000 – < Rp2.200.000 | Golongan 4–5 | Kemampuan ekonomi keluarga menengah | Beasiswa parsial / cicilan fleksibel |
| **TINGGI**   | ≥ Rp2.200.000   | Golongan 6–8 | Kemampuan ekonomi keluarga mampu | UKT penuh / skema cross-subsidi |

> **Catatan**: Threshold di atas berasal dari distribusi konsekuen rule base (Rp500rb – Rp4jt). Sistem tidak memaksa pengguna ke golongan tetap; output bersifat kontinu (Sugeno Orde 0) lalu dikategorikan untuk keperluan administrasi.

---

## 6. Arsitektur Kode (Ringkas)

```
Modul-3/
├── src/
│   ├── app.py              # Antarmuka Streamlit (UI)
│   ├── fuzzy_engine.py     # Core engine: fuzzifikasi, inferensi, validasi (stateless)
│   └── .streamlit/
│       └── config.toml     # Tema warna (teal light)
├── requirements.txt        # Dependensi proyek
├── data/
│   └── test_cases.csv      # 15 kasus uji evaluasi (Praktikum 12)
├── screenshot_skenario1.png
├── screenshot_skenario2.png
├── screenshot_skenario3.png
└── Laporan Praktikum 13.docx
```

- **fuzzy_engine.py** bersifat *stateless* (tidak menyimpan state) → aman untuk rerun Streamlit.
- **app.py** hanya menangani presentasi & interaksi pengguna.

---

## 7. Pengujian Black-Box (Ringkasan Praktikum 14)

Lengkapnya lihat **Praktikum14.md** bagian F.1–F.3.  
10+ skenario uji mencakup:
- Equivalence Partitioning: valid / invalid (negatif, melebihi batas)
- Boundary Value Analysis: 0, 2jt, 4jt, 5jt, 7jt, 10jt (penghasilan); 0, 1, 2, 3, 4, 6 (tanggungan)
- Kasus tipikal representatif tiap golongan UKT

Semua skenario **PASS** — sistem mengklip input di luar semesta ke batas terdekat dan menampilkan pesan validasi yang ramah.

---

## 8. Lisensi & Penghargaan

Proyek ini dikembangkan untuk keperluan akademik **Praktikum Logika Fuzzy Modul 3** (Praktikum 11–14), Program Studi S1 Teknik Informatika, UIN Mataram.

Dibangun dengan:
- [Streamlit](https://streamlit.io/)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)
- [scikit-fuzzy](https://pythonhosted.org/scikit-fuzzy/)

---

> **Versi**: 1.0 (Praktikum 14)  
> **Tanggal**: November 2026  
> **Penulis**: Asfal Fuad (240306031)
