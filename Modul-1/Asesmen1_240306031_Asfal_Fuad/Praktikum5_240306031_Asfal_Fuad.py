import sys
import io
import numpy as np
import matplotlib.pyplot as plt

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 1. FUNGSI KEANGGOTAAN DASAR (MEMBERSHIP FUNCTIONS)
def triangular(x, a, b, c):
    """
    Fungsi keanggotaan kurva segitiga dengan parameter [a, b, c].
    a = batas kiri, b = puncak (derajat 1.0), c = batas kanan.
    """
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    
    # Area naik: a < x <= b
    mask_up = (x > a) & (x <= b)
    if b > a:
        y[mask_up] = (x[mask_up] - a) / (b - a)
    elif a == b:
        y[mask_up] = 1.0
        
    # Area turun: b < x < c
    mask_down = (x > b) & (x < c)
    if c > b:
        y[mask_down] = (c - x[mask_down]) / (c - b)
        
    # Titik puncak tepat di b
    y[x == b] = 1.0
    
    return float(y) if y.ndim == 0 else y


def trapezoidal(x, a, b, c, d):
    """
    Fungsi keanggotaan kurva trapesium dengan parameter [a, b, c, d].
    a = batas kiri bawah, b = batas kiri atas,
    c = batas kanan atas, d = batas kanan bawah.
    Mendukung bahu kiri (a == b) dan bahu kanan (c == d).
    """
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    
    # Bagian flat atas: b <= x <= c
    mask_top = (x >= b) & (x <= c)
    y[mask_top] = 1.0
    
    # Bagian lereng naik: a < x < b
    mask_up = (x > a) & (x < b)
    if b > a:
        y[mask_up] = (x[mask_up] - a) / (b - a)
    elif a == b:
        y[mask_up] = 1.0
        
    # Bagian lereng turun: c < x < d
    mask_down = (x > c) & (x < d)
    if d > c:
        y[mask_down] = (d - x[mask_down]) / (d - c)
    elif c == d:
        y[mask_down] = 1.0
        
    return float(y) if y.ndim == 0 else y


# 2. DEFINISI BASIS PENGETAHUAN & VARIABEL LINGUISTIK
variabel_fuzzy = {
    "Tingkat Kerusakan": {
        "tipe_var": "input",
        "satuan": "%",
        "domain": (0, 100),
        "himpunan": {
            "Rendah": {"tipe": "trapesium", "parameter": [0, 0, 20, 40], "warna": "#2b5c8f"},
            "Sedang": {"tipe": "segitiga",  "parameter": [30, 50, 70],   "warna": "#e67e22"},
            "Tinggi": {"tipe": "trapesium", "parameter": [60, 80, 100, 100], "warna": "#c0392b"}
        }
    },
    "Jumlah Laporan": {
        "tipe_var": "input",
        "satuan": "tiket",
        "domain": (0, 100),
        "himpunan": {
            "Sedikit": {"tipe": "trapesium", "parameter": [0, 0, 20, 40], "warna": "#16a085"},
            "Sedang":  {"tipe": "segitiga",  "parameter": [30, 50, 70],   "warna": "#f39c12"},
            "Banyak":  {"tipe": "trapesium", "parameter": [60, 80, 100, 100], "warna": "#8e44ad"}
        }
    },
    "Prioritas Perbaikan": {
        "tipe_var": "output",
        "satuan": "skor (0-100)",
        "domain": (0, 100),
        "himpunan": {
            "Rendah": {"tipe": "trapesium", "parameter": [0, 0, 25, 45], "warna": "#27ae60"},
            "Sedang": {"tipe": "segitiga",  "parameter": [35, 55, 75],   "warna": "#d35400"},
            "Tinggi": {"tipe": "trapesium", "parameter": [65, 80, 100, 100], "warna": "#e74c3c"}
        }
    }
}


def hitung_derajat(x, tipe, param):
    """Menghitung derajat keanggotaan berdasarkan jenis kurva."""
    if tipe == "segitiga":
        return triangular(x, *param)
    elif tipe == "trapesium":
        return trapezoidal(x, *param)
    else:
        raise ValueError(f"Tipe kurva '{tipe}' tidak dikenali.")


# 3. FUNGSI FUZZIFIKASI DATA INPUT
def fuzzifikasi(input_dict):
    """
    Menerima kamus input tegas (crisp) dan mengembalikan derajat keanggotaan.
    Contoh input: {"kerusakan": 35.0, "laporan": 35.0}
    """
    hasil = {}
    
    # 1. Fuzzifikasi Variabel Tingkat Kerusakan
    val_k = input_dict.get("kerusakan", 0.0)
    hasil["Tingkat Kerusakan"] = {
        label: round(float(hitung_derajat(val_k, cfg["tipe"], cfg["parameter"])), 4)
        for label, cfg in variabel_fuzzy["Tingkat Kerusakan"]["himpunan"].items()
    }
    
    # 2. Fuzzifikasi Variabel Jumlah Laporan
    val_l = input_dict.get("laporan", 0.0)
    hasil["Jumlah Laporan"] = {
        label: round(float(hitung_derajat(val_l, cfg["tipe"], cfg["parameter"])), 4)
        for label, cfg in variabel_fuzzy["Jumlah Laporan"]["himpunan"].items()
    }
    
    return hasil


# 4. FUNGSI VISUALISASI GRAFIK FUNGSI KEANGGOTAAN
def plot_variabel(nama_variabel, output_filename):
    """
    Menghasilkan dan menyimpan visualisasi kurva fungsi keanggotaan ke file gambar PNG.
    """
    var_cfg = variabel_fuzzy[nama_variabel]
    d_min, d_max = var_cfg["domain"]
    x = np.linspace(d_min, d_max, 1000)
    
    plt.figure(figsize=(9, 5), dpi=300)
    
    for label, cfg in var_cfg["himpunan"].items():
        y = hitung_derajat(x, cfg["tipe"], cfg["parameter"])
        warna = cfg.get("warna", "#333333")
        plt.plot(x, y, label=f"{label} ({cfg['tipe']})", color=warna, linewidth=2.5)
        plt.fill_between(x, 0, y, color=warna, alpha=0.15)
        
    plt.title(f"Fungsi Keanggotaan Variabel: {nama_variabel}", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel(f"{nama_variabel} [{var_cfg['satuan']}]", fontsize=11, labelpad=8)
    plt.ylabel("Derajat Keanggotaan (μ)", fontsize=11, labelpad=8)
    plt.xlim(d_min, d_max)
    plt.ylim(-0.05, 1.05)
    plt.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    plt.axhline(1, color="gray", linewidth=0.8, linestyle="--")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper right", framealpha=0.9, fontsize=10)
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    plt.close()
    print(f"[*] Grafik berhasil disimpan: {output_filename}")


# 5. PENGUJIAN 5 SKENARIO KASUS NYATA
def run_pengujian_skenario():
    skenario_list = [
        {
            "id": 1,
            "nama": "Skenario 1 (Ekstrem Bawah)",
            "kondisi": "Kerusakan minimal, nihil laporan komplain",
            "kerusakan": 0.0,
            "laporan": 0.0
        },
        {
            "id": 2,
            "nama": "Skenario 2 (Batas Transisi Rendah - Sedang)",
            "kondisi": "Kerusakan mulai tampak, laporan masuk bertahap (zona tumpang tindih)",
            "kerusakan": 35.0,
            "laporan": 35.0
        },
        {
            "id": 3,
            "nama": "Skenario 3 (Kondisi Sedang / Nominal)",
            "kondisi": "Kerusakan moderat dan laporan rata-rata normal (puncak himpunan Sedang)",
            "kerusakan": 50.0,
            "laporan": 50.0
        },
        {
            "id": 4,
            "nama": "Skenario 4 (Batas Transisi Sedang - Tinggi)",
            "kondisi": "Kerusakan meningkat signifikan, laporan komplain melonjak",
            "kerusakan": 65.0,
            "laporan": 65.0
        },
        {
            "id": 5,
            "nama": "Skenario 5 (Ekstrem Atas)",
            "kondisi": "Kerusakan total/lumpuh, laporan darurat massal memenuhi sistem",
            "kerusakan": 100.0,
            "laporan": 100.0
        }
    ]
    
    print("\n" + "=" * 90)
    print("HASIL EVALUASI FUZZIFIKASI - 5 SKENARIO KASUS PENGUJIAN")
    print("=" * 90)
    
    for sk in skenario_list:
        hasil = fuzzifikasi({"kerusakan": sk["kerusakan"], "laporan": sk["laporan"]})
        print(f"\n[{sk['nama']}] - {sk['kondisi']}")
        print(f"  Input: Kerusakan = {sk['kerusakan']}% | Laporan = {sk['laporan']} tiket")
        print(f"  μ_Kerusakan -> Rendah: {hasil['Tingkat Kerusakan']['Rendah']:.2f}, Sedang: {hasil['Tingkat Kerusakan']['Sedang']:.2f}, Tinggi: {hasil['Tingkat Kerusakan']['Tinggi']:.2f}")
        print(f"  μ_Laporan   -> Sedikit: {hasil['Jumlah Laporan']['Sedikit']:.2f}, Sedang: {hasil['Jumlah Laporan']['Sedang']:.2f}, Banyak: {hasil['Jumlah Laporan']['Banyak']:.2f}")


# 6. EKSEKUSI UTAMA
if __name__ == "__main__":
    print("Menjalankan pemodelan fuzzy dan visualisasi kurva...")
    
    # Buat grafik visualisasi
    plot_variabel("Tingkat Kerusakan", "grafik_tingkat_kerusakan.png")
    plot_variabel("Jumlah Laporan", "grafik_jumlah_laporan.png")
    plot_variabel("Prioritas Perbaikan", "grafik_prioritas_perbaikan.png")
    
    # Jalankan pengujian
    run_pengujian_skenario()
