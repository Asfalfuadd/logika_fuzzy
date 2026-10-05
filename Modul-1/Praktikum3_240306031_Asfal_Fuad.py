import sys
import io
import mysql.connector

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Koneksi database ──────────────────────────────────────────
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="fuzzy_modul1"
)
print("Koneksi database berhasil!")

# ── Fungsi keanggotaan (berdasarkan Tugas 1 PDF) ───────────────

# 1. Bayi / Anak Usia Dini: (0, 2.5, 5)
def fungsi_bayi_naik(x):    return x / 2.5         
def fungsi_bayi_turun(x):   return (5 - x) / 2.5   

# 2. Anak-anak: (5, 8.5, 11)
def fungsi_anak_naik(x):    return (x - 5) / 3.5   
def fungsi_anak_turun(x):   return (11 - x) / 2.5   

# 3. Remaja: (10, 14.5, 19)
def fungsi_remaja_naik(x):  return (x - 10) / 4.5   
def fungsi_remaja_turun(x): return (19 - x) / 4.5   

# 4. Pemuda: (15, 19.5, 24)
def fungsi_pemuda_naik(x):  return (x - 15) / 4.5   
def fungsi_pemuda_turun(x): return (24 - x) / 4.5   

# 5. Dewasa: (20, 42.5, 65)
def fungsi_dewasa_naik(x):  return (x - 20) / 22.5  
def fungsi_dewasa_turun(x): return (65 - x) / 22.5  

# 6. Lanjut Usia (Lansia): (60, 70, 80)
def fungsi_lansia_naik(x):  return (x - 60) / 10    
def fungsi_lansia_turun(x): return (80 - x) / 10   

# ── Mapping nama fungsi database ke fungsi Python ─────────────

FUNGSI = {
    "fungsi_bayi_naik"    : fungsi_bayi_naik,
    "fungsi_bayi_turun"   : fungsi_bayi_turun,
    "fungsi_anak_naik"    : fungsi_anak_naik,
    "fungsi_anak_turun"   : fungsi_anak_turun,
    "fungsi_remaja_naik"  : fungsi_remaja_naik,
    "fungsi_remaja_turun" : fungsi_remaja_turun,
    "fungsi_pemuda_naik"  : fungsi_pemuda_naik,
    "fungsi_pemuda_turun" : fungsi_pemuda_turun,
    "fungsi_dewasa_naik"  : fungsi_dewasa_naik,
    "fungsi_dewasa_turun" : fungsi_dewasa_turun,
    "fungsi_lansia_naik"  : fungsi_lansia_naik,
    "fungsi_lansia_turun" : fungsi_lansia_turun,
}

# ── Fuzzifikasi ───────────────────────────────────────────────

def fuzzifikasi_usia(x, nama_tabel):
    cursor = db.cursor(buffered=True)
    query = f"""
        SELECT usia_min, usia_max, nilai_fuzzy
        FROM   {nama_tabel}
        WHERE  %s >= usia_min AND %s <= usia_max
    """
    try:
        cursor.execute(query, (x, x))
        data = cursor.fetchone()
    except mysql.connector.Error:
        return None, None, None
    finally:
        cursor.close()

    if data is None:
        return None, None, None

    usia_min, usia_max, nama_fungsi = data
    interval_str = f"[{usia_min:g}, {usia_max:g}]"

    if nama_fungsi == "0":
        return interval_str, "0 (konstan)", 0.0
    if nama_fungsi == "1":
        return interval_str, "1 (konstan)", 1.0
    if nama_fungsi in FUNGSI:
        nilai = FUNGSI[nama_fungsi](x)
        nilai_clamped = max(0.0, min(1.0, float(nilai)))
        return interval_str, nama_fungsi, nilai_clamped

    raise ValueError(f"Fungsi '{nama_fungsi}' belum dibuat di Python.")

# ── Input dinamis ─────────────────────────────────────────────

KATEGORI = {
    "1": "bayi",
    "2": "anak",
    "3": "remaja",
    "4": "pemuda",
    "5": "dewasa",
    "6": "lansia",
}
LEBAR = 73

print()
print("SISTEM FUZZIFIKASI USIA - PRAKTIKUM 3")
print("Kategori Usia:")
print("  1. Bayi     2. Anak      3. Remaja")
print("  4. Pemuda   5. Dewasa    6. Lansia")
print("Ketik '0' untuk selesai dan melihat tabel.")

hasil_semua = []
nomor = 1

while True:
    print()
    pilihan = input(f"[{nomor:>2}] Kategori (1-6) : ").strip()

    if pilihan == "0":
        break
    if pilihan not in KATEGORI:
        print("        Pilihan tidak valid! Masukkan angka 1-6 (atau '0' untuk selesai).")
        continue

    variabel = KATEGORI[pilihan]

    try:
        usia = float(input(f"     Usia ({variabel.upper()}): ").strip())
    except ValueError:
        print("        Usia tidak valid!")
        continue

    if not (0 <= usia <= 150):
        print("        Usia harus 0–150 tahun.")
        continue

    interval_str, nama_fungsi, mu_x = fuzzifikasi_usia(usia, f"usia_{variabel}")

    if mu_x is None:
        print(f"        Nilai {usia} tidak ditemukan dalam database.")
        continue

    print(f"     Interval : {interval_str}  |  Fungsi : {nama_fungsi}  |  mu(x) = {mu_x:.3f}")
    hasil_semua.append((nomor, usia, variabel.upper(), interval_str, nama_fungsi, mu_x))
    nomor += 1


# ── Tabel akhir ───────────────────────────────────────────────

print()
print("TABEL HASIL VERIFIKASI FUNGSI KEANGGOTAAN")

if not hasil_semua:
    print("Tidak ada data.")
else:
    print(f"{'No':>3}  {'Usia':>6}  {'Variabel':<8}  {'Interval':<12}  {'Fungsi':<22}  {'mu(x)':>6}")
    print("-" * LEBAR)
    for no, usia, var, interval, fn, mu in hasil_semua:
        print(f"{no:>3}  {usia:>6.1f}  {var:<8}  {interval:<12}  {fn:<22}  {mu:>6.3f}")
    print("-" * LEBAR)
    print(f"Total: {len(hasil_semua)} pengujian")

print()
db.close()
print("Koneksi database ditutup.")
