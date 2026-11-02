import numpy as np
import matplotlib.pyplot as plt
# 1. FUNGSI KEANGGOTAAN TRAPESIUM
def trapesium(x, a, b, c, d):
    x = np.asarray(x, dtype=float)
    hasil = np.zeros_like(x)
    if a == b:
        hasil[x <= b] = 1
    else:
        bagian = (x >= a) & (x < b)
        hasil[bagian] = (x[bagian] - a) / (b - a)
    bagian = (x >= b) & (x <= c)
    hasil[bagian] = 1
    if c == d:
        hasil[x >= c] = 1
    else:
        bagian = (x > c) & (x <= d)
        hasil[bagian] = (d - x[bagian]) / (d - c)
    return np.clip(hasil, 0, 1)
# 2. FUNGSI KEANGGOTAAN SEGITIGA
def segitiga(x, a, b, c):
    x = np.asarray(x, dtype=float)
    hasil = np.zeros_like(x)

    bagian_kiri = (x >= a) & (x <= b)
    if b != a:
        hasil[bagian_kiri] = (x[bagian_kiri] - a) / (b - a)
    bagian_kanan = (x >= b) & (x <= c)
    if c != b:
        hasil[bagian_kanan] = np.maximum(
            hasil[bagian_kanan],
            (c - x[bagian_kanan]) / (c - b)
        )
    hasil[x == b] = 1
    return np.clip(hasil, 0, 1)
# 3. CLASS FUZZY INFERENCE SYSTEM
class FuzzyInferenceSystem:
    def __init__(self):
        self.input_variables = {}
        self.output_variable = None
        self.rules = []
    def add_input_variable(self, name, universe, mf_dict):
        self.input_variables[name] = {
            "universe": universe,
            "mf_dict": mf_dict
        }
    def set_output_variable(self, name, universe, mf_dict):
        self.output_variable = {
            "name": name,
            "universe": universe,
            "mf_dict": mf_dict
        }
    def add_rule(self, rule_tuple):
        self.rules.append(rule_tuple)
    def compute(self, input_values_dict):
        if self.output_variable is None:
            raise ValueError("Variabel output belum ditentukan.")
        fuzzifikasi = {}
        # Tahap 1: Fuzzifikasi
        for nama, nilai in input_values_dict.items():
            if nama not in self.input_variables:
                raise ValueError(
                    f"Variabel input {nama} tidak ditemukan."
                )
            variabel = self.input_variables[nama]
            fuzzifikasi[nama] = {}
            for himpunan, fungsi in variabel["mf_dict"].items():
                fuzzifikasi[nama][himpunan] = float(
                    np.interp(
                        nilai,
                        variabel["universe"],
                        fungsi
                    )
                )

        universe_output = self.output_variable["universe"]
        fungsi_output = self.output_variable["mf_dict"]
        agregasi = np.zeros_like(
            universe_output,
            dtype=float
        )
        # Tahap 2 dan 3: Evaluasi aturan dan implikasi
        for kondisi, nama_output in self.rules:
            derajat = []
            for nama_input, nama_himpunan in kondisi.items():
                nilai = fuzzifikasi[nama_input][nama_himpunan]
                derajat.append(nilai)
            if not derajat:
                continue
            alpha = min(derajat)
            hasil_implikasi = np.minimum(
                alpha,
                fungsi_output[nama_output]
            )
            # Tahap 4: Agregasi menggunakan maksimum
            agregasi = np.maximum(
                agregasi,
                hasil_implikasi
            )
        # Tahap 5: Defuzzifikasi centroid
        penyebut = np.sum(agregasi)

        if penyebut == 0:
            hasil_crisp = None
        else:
            hasil_crisp = float(
                np.sum(universe_output * agregasi) / penyebut
            )
        return {
            "fuzzifikasi": fuzzifikasi,
            "agregasi": agregasi,
            "hasil": hasil_crisp
        }
# 4. MEMBUAT DOMAIN VARIABEL
penghasilan = np.linspace(0, 15_000_000, 1501)
tanggungan = np.linspace(0, 10, 1001)
ukt = np.linspace(500_000, 4_000_000, 1501)
# 5. FUNGSI KEANGGOTAAN PENGHASILAN
mf_penghasilan = {
    "Rendah": trapesium(
        penghasilan, 0, 0, 3_000_000, 6_000_000
    ),
    "Sedang": segitiga(
        penghasilan, 3_000_000, 7_500_000, 12_000_000
    ),
    "Tinggi": trapesium(
        penghasilan, 9_000_000, 12_000_000,
        15_000_000, 15_000_000
    )
}
# 6. FUNGSI KEANGGOTAAN TANGGUNGAN
mf_tanggungan = {
    "Sedikit": trapesium(
        tanggungan, 0, 0, 2, 4
    ),
    "Sedang": segitiga(
        tanggungan, 2, 5, 8
    ),
    "Banyak": trapesium(
        tanggungan, 6, 8, 10, 10
    )
}
# 7. FUNGSI KEANGGOTAAN OUTPUT UKT
mf_ukt = {
    "Rendah": trapesium(
        ukt, 500_000, 500_000, 1_000_000, 2_000_000
    ),
    "Sedang": segitiga(
        ukt, 1_000_000, 2_250_000, 3_500_000
    ),
    "Tinggi": trapesium(
        ukt, 2_500_000, 3_500_000, 4_000_000, 4_000_000
    )
}
# 8. MEMBUAT SISTEM FIS
fis = FuzzyInferenceSystem()
fis.add_input_variable(
    "penghasilan", penghasilan, mf_penghasilan
)

fis.add_input_variable(
    "tanggungan", tanggungan, mf_tanggungan
)
fis.set_output_variable(
    "ukt", ukt, mf_ukt
)
# 9. MENAMBAHKAN SEMBILAN ATURAN FUZZY
fis.add_rule((
    {"penghasilan": "Rendah", "tanggungan": "Sedikit"},
    "Rendah"
))
fis.add_rule((
    {"penghasilan": "Rendah", "tanggungan": "Sedang"},
    "Rendah"
))
fis.add_rule((
    {"penghasilan": "Rendah", "tanggungan": "Banyak"},
    "Rendah"
))
fis.add_rule((
    {"penghasilan": "Sedang", "tanggungan": "Sedikit"},
    "Sedang"
))
fis.add_rule((
    {"penghasilan": "Sedang", "tanggungan": "Sedang"},
    "Sedang"
))
fis.add_rule((
    {"penghasilan": "Sedang", "tanggungan": "Banyak"},
    "Rendah"
))
fis.add_rule((
    {"penghasilan": "Tinggi", "tanggungan": "Sedikit"},
    "Tinggi"
))
fis.add_rule((
    {"penghasilan": "Tinggi", "tanggungan": "Sedang"},
    "Tinggi"
))
fis.add_rule((
    {"penghasilan": "Tinggi", "tanggungan": "Banyak"},
    "Sedang"
))
# 10. PENGUJIAN TIGA KOMBINASI INPUT
data_pengujian = [
    {
        "penghasilan": 2_000_000,
        "tanggungan": 5
    },
    {
        "penghasilan": 7_000_000,
        "tanggungan": 4
    },
    {
        "penghasilan": 12_000_000,
        "tanggungan": 8
    }
]
hasil_pengujian = []
for nomor, data in enumerate(data_pengujian, start=1):
    hasil = fis.compute(data)
    hasil_pengujian.append(hasil)
    print(f"\nPengujian {nomor}")
    print(
        f"Penghasilan orang tua: "
        f"Rp{data['penghasilan']:,.0f}"
    )
    print(
        f"Jumlah tanggungan: "
        f"{data['tanggungan']} orang"
    )
    if hasil["hasil"] is None:
        print("Rekomendasi UKT tidak dapat dihitung.")
    else:
        print(
            f"Rekomendasi nominal UKT: "
            f"Rp{hasil['hasil']:,.2f}"
        )


# 11. MENAMPILKAN GRAFIK AGREGASI
hasil_grafik = hasil_pengujian[0]
agregasi = hasil_grafik["agregasi"]
hasil_crisp = hasil_grafik["hasil"]
plt.figure(figsize=(10, 6))
for nama, fungsi in mf_ukt.items():
    plt.plot(ukt, fungsi, label=f"UKT {nama}")
plt.fill_between(
    ukt,
    0,
    agregasi,
    alpha=0.35,
    label="Daerah Agregasi Fuzzy"
)
plt.plot(
    ukt,
    agregasi,
    linewidth=2,
    label="Kurva Agregasi"
)
if hasil_crisp is not None:
    plt.axvline(
        hasil_crisp,
        linestyle="--",
        label=f"Centroid = Rp{hasil_crisp:,.0f}"
    )

plt.title("Hasil Agregasi dan Defuzzifikasi UKT")
plt.xlabel("Nominal UKT (Rp)")
plt.ylabel("Derajat Keanggotaan")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(
    "pipeline_fis_agregasi_defuzzifikasi.png",
    dpi=300
)
plt.show()
