# -*- coding: utf-8 -*-
"""
app.py - Antarmuka Streamlit UKT-Fuzzy (Praktikum 13)
Mahasiswa : Asfal Fuad (240306031)

Jalankan dari folder src/:
    streamlit run app.py

Skenario via query param (untuk pengujian otomatis):
    http://localhost:8501/?penghasilan=800000&tanggungan=5

Tema: terang hangat dengan satu aksen teal. Warna kategori (hijau/amber/merah,
biru) muncul di badge, chip mu, dan grafik karena mereka adalah label kategori
nyata, bukan dekorasi.
"""
import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from fuzzy_engine import trapezoid, infer_ukt

# ==========================================================
# 1. KONFIGURASI HALAMAN + SISTEM DESAIN (tema terang)
# ==========================================================
st.set_page_config(
    page_title="UKT-Fuzzy | Sistem Penetapan UKT Mahasiswa",
    layout="wide",
)

INK = "#1B2530"      # teks utama
BODY = "#24303F"     # teks paragraf
MUTED = "#5B6672"    # teks sekunder
ACCENT = "#0F766E"   # satu aksen teal, hanya di elemen hasil
NILAI = "#17564C"    # readout nilai slider (teal tua, kontras tinggi di sidebar)

# warna identitas kategori (badge, chip mu, dan grafik memakai set ini)
KATEGORI_WARNA = {
    "Rendah":  "#15803D",  # hijau
    "Sedikit": "#0369A1",  # biru
    "Sedang":  "#B45309",  # amber
    "Tinggi":  "#B91C1C",  # merah
    "Banyak":  "#B91C1C",  # merah
}

# Desain Read: aplikasi keputusan (dashboard) untuk mahasiswa/dosen,
# bahasa visual minimalis tema terang. Dial: ENERGY 1 / RHYTHM 2 / MOTION 1.
# MOTION 1: hanya animasi pembuka pada kartu hasil saat rerun; non-aktif
# pada prefers-reduced-motion.
CSS = """
<style>
.h1 { font-size: 1.85rem; font-weight: 700; letter-spacing: -0.02em; color: #1B2530; margin: 0; }
.lede { color: #5B6672; max-width: 640px; margin: 0.35rem 0 0; font-size: 0.95rem; line-height: 1.5; }

.card { background: #FFFFFF; border: 1px solid #E6E9EC; border-radius: 14px;
        padding: 1.1rem 1.25rem; }
.result-anim { animation: rise 0.45s ease-out; }
@keyframes rise { from { opacity: 0; transform: translateY(8px); }
                  to   { opacity: 1; transform: none; } }

/* badge = label status golongan UKT nyata, bukan hiasan */
.badge { display: inline-block; font-size: 0.72rem; font-weight: 700;
         letter-spacing: 0.04em; padding: 0.28rem 0.6rem; border-radius: 7px;
         text-transform: uppercase; }
.b-ringan { background: #E7F4EF; color: #155E40; }
.b-sedang { background: #FBF1DC; color: #7A5410; }
.b-tinggi { background: #FBEAEA; color: #8C2B2B; }

.amount { font-size: 2.4rem; font-weight: 800; color: #1B2530;
          margin-top: 0.45rem; letter-spacing: -0.01em;
          font-variant-numeric: tabular-nums; }
.amount-sub { color: #5B6672; font-size: 0.85rem; }

.scale { height: 8px; background: #EEF1F2; border-radius: 6px;
         margin-top: 0.8rem; overflow: hidden; }
.scale-fill { height: 100%; background: #0F766E; border-radius: 6px;
              animation: grow 0.6s ease-out; }
@keyframes grow { from { width: 0; } }
.scale-caption { color: #5B6672; font-size: 0.72rem; margin-top: 0.25rem; }
.explain { color: #24303F; font-size: 0.9rem; margin: 0.7rem 0 0; }

/* label bagian: hierarki tipografi kecil, penanda navigasi dalam satu layar */
.sec-label { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.07em;
             text-transform: uppercase; color: #5B6672; margin: 0.2rem 0 0.55rem; }

.chip-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
             gap: 0.35rem 2rem; }
.chip-title { font-size: 0.78rem; font-weight: 600; color: #5B6672; margin: 0.35rem 0 0.45rem; }
.chip { display: flex; align-items: center; gap: 0.55rem; font-size: 0.85rem; color: #24303F; }
.chip .lbl { width: 64px; flex: none; color: #5B6672; }
.chip .track { flex: 1; height: 6px; background: #EEF1F2; border-radius: 4px; overflow: hidden; }
.chip .fill { height: 100%; border-radius: 4px; animation: grow 0.6s ease-out; }
.chip .val { width: 46px; flex: none; text-align: right; font-variant-numeric: tabular-nums;
             color: #24303F; }

/* Sidebar: permukaan tinted agar jelas terpisah dari konten putih */
[data-testid="stSidebar"] { background: #EAF2EF; border-right: 1px solid #DCE7E2; }
[data-testid="stSidebar"] .sec-label { color: #3D5F55; }
[data-testid="stSidebar"] .stSlider label p { font-size: 1rem !important; color: #1B2530; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
  font-size: 0.86rem !important; color: #46584F;
  overflow-wrap: break-word; padding-right: 0.5rem; line-height: 1.45;
}

/* Readout nilai slider: ukuran fluid, ikut lebar layar (desktop besar, ponsel tetap terbaca) */
.nilai { font-size: clamp(1.15rem, 1.6vw, 1.5rem); font-weight: 800; color: #17564C;
         margin: 0.2rem 0 0.8rem; font-variant-numeric: tabular-nums; }
.nilai .unit { color: #46584F; font-weight: 600; font-size: 0.62em; }

@media (prefers-reduced-motion: reduce) {
  .result-anim, .scale-fill, .chip .fill { animation: none; }
}

/* ===== Layout: biarkan scroll natural, footer terlihat di bawah ===== */
.stMainBlockContainer, .block-container {
  padding-top: 1.5rem !important;
  padding-bottom: 2rem !important;
}
[data-testid="stVerticalBlock"] { row-gap: 0.75rem; }
[data-testid="stCaptionContainer"] p { margin: 0.25rem 0 0 !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def rp(x):
    """Format Rupiah gaya Indonesia (pemisah ribuan titik)."""
    return f"Rp {x:,.0f}".replace(",", ".")


st.markdown(
    '<h1 class="h1">Sistem Penetapan UKT Mahasiswa</h1>'
    '<p class="lede">Rekomendasi nominal UKT per semester dihitung real-time dengan '
    'Sugeno Orde 0 dari dua masukan: penghasilan orang tua dan jumlah tanggungan '
    '(rule base 9 aturan, defuzzifikasi weighted average).</p>',
    unsafe_allow_html=True,
)

# ==========================================================
# 2. SIDEBAR: MASUKAN + VALIDASI
# ==========================================================
st.sidebar.markdown('<p class="sec-label">Masukan</p>', unsafe_allow_html=True)

# ----- Validasi manual input (Black-Box Testing: BVA & Equivalence Partitioning) -----
with st.sidebar.expander("Validasi Input Manual (Uji Batas)", expanded=False):
    st.caption("Masukkan nilai di luar semesta untuk menguji penanganan error sistem.")
    col_p, col_t = st.columns(2)
    with col_p:
        manual_penghasilan = st.number_input(
            "Penghasilan Manual (Rp)",
            value=0,
            step=100_000,
            format="%d",
            help="Semesta valid: 0 - 10.000.000. Nilai di luar akan diklip dan diberi peringatan.",
        )
    with col_t:
        manual_tanggungan = st.number_input(
            "Tanggungan Manual",
            value=0,
            step=1,
            format="%d",
            help="Semesta valid: 0 - 6. Nilai di luar akan diklip dan diberi peringatan.",
        )
    if st.button("Uji Validasi", use_container_width=True):
        from fuzzy_engine import SEMESTA, validasi_input
        p_clip, t_clip, pesan = validasi_input(manual_penghasilan, manual_tanggungan)
        if pesan:
            st.error("⚠️ " + "; ".join(pesan))
            st.info(f"Nilai dikoreksi: Penghasilan = {rp(p_clip)}, Tanggungan = {t_clip}")
        else:
            st.success(f"Input valid: Penghasilan = {rp(p_clip)}, Tanggungan = {t_clip}")

_qp = st.query_params
try:
    _p0 = float(_qp.get("penghasilan", 2_500_000))
    _t0 = float(_qp.get("tanggungan", 3))
except (TypeError, ValueError):
    _p0, _t0 = 2_500_000, 3
_p0 = min(max(_p0, 0), 10_000_000)
_t0 = int(min(max(_t0, 0), 6))

input_penghasilan = st.sidebar.slider(
    "Penghasilan Orang Tua (Rp/bulan)",
    min_value=0,
    max_value=10_000_000,
    value=int(_p0),
    step=100_000,
    help="Total pendapatan kotor orang tua/wali per bulan. Semesta: 0 sampai Rp10 juta.",
)
st.sidebar.markdown(
    f'<p class="nilai">{rp(input_penghasilan)}<span class="unit"> / bulan</span></p>',
    unsafe_allow_html=True,
)

input_tanggungan = st.sidebar.slider(
    "Jumlah Tanggungan Keluarga (orang)",
    min_value=0,
    max_value=6,
    value=_t0,
    step=1,
    help="Jumlah anggota keluarga yang masih menjadi tanggungan orang tua. Semesta: 0 sampai 6.",
)
st.sidebar.markdown(
    f'<p class="nilai">{input_tanggungan}<span class="unit"> orang tanggungan</span></p>',
    unsafe_allow_html=True,
)

st.sidebar.divider()
st.sidebar.caption("Hasil diperbarui otomatis setiap kali salah satu slider digeser.")
st.sidebar.caption("Sumber logika: src/fuzzy_engine.py, rule base 9 aturan (Praktikum 11), "
                   "evaluasi MAE/RMSE pada Praktikum 12.")

# ==========================================================
# 3. INFERENSI (murni memanggil fuzzy_engine)
# ==========================================================
uktn, detail = infer_ukt(input_penghasilan, input_tanggungan, detail=True)
mu_p = detail["mu_penghasilan"]
mu_t = detail["mu_tanggungan"]
aturan_aktif = detail["aturan_aktif"]      # [(p_label, t_label, nominal, alpha)]


def kategori_ukt(z):
    """Threshold berasal dari rule base: 1 juta-an = ringan, 2 juta-an = sedang, 4 juta-an = tinggi."""
    if z < 1_100_000:
        return "b-ringan", "RINGAN", "Golongan UKT 1-3", \
               "Kemampuan ekonomi keluarga tergolong rendah, sistem mengusulkan nominal terendah."
    if z < 2_200_000:
        return "b-sedang", "SEDANG", "Golongan UKT 4-5", \
               "Kemampuan ekonomi keluarga tergolong menengah, nominal dipatok pada tingkat antara."
    return "b-tinggi", "TINGGI", "Golongan UKT 6-8", \
           "Kemampuan ekonomi keluarga mampu, sistem mengusulkan nominal tertinggi."


kiri, kanan = st.columns([5, 6], gap="large")

with kiri:
    st.markdown('<p class="sec-label">Hasil Rekomendasi</p>', unsafe_allow_html=True)

    if uktn is None:
        st.error("Inferensi tidak menghasilkan output: tidak ada aturan aktif untuk kombinasi "
                 "masukan ini. Periksa kembali nilai slider pada semesta yang valid.")
        if detail["pesan_validasi"]:
            st.warning("Peringatan validasi masukan: " + "; ".join(detail["pesan_validasi"]))
    else:
        cls, label_txt, gol, deskripsi = kategori_ukt(uktn)
        pct = min(uktn / 4_000_000, 1.0) * 100

        st.markdown(
            f"""
            <div class="card result-anim" role="status">
              <span class="badge {cls}">{label_txt}</span>
              <div class="amount">{rp(uktn)}</div>
              <div class="amount-sub">per semester, Sugeno Orde 0 · {gol}</div>
              <div class="scale"><div class="scale-fill" style="width:{pct:.1f}%"></div></div>
              <div class="scale-caption">skala Rp0 sampai Rp4 juta</div>
              <p class="explain">{deskripsi}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if detail["pesan_validasi"]:
            st.warning("Peringatan validasi masukan: " + "; ".join(detail["pesan_validasi"]))

        st.markdown('<p class="sec-label">Derajat Keanggotaan</p>', unsafe_allow_html=True)

        def chip_group(nama_variabel, items):
            rows = "".join(
                f"""<div class="chip">
                      <span class="lbl">{lbl}</span>
                      <span class="track"><span class="fill"
                        style="width:{min(val * 100, 100):.0f}%;
                              background:{KATEGORI_WARNA[lbl]}"></span></span>
                      <span class="val">{val:.2f}</span>
                    </div>"""
                for lbl, val in items
            )
            return (f'<div class="chip-group"><div class="chip-title">{nama_variabel}</div>'
                    f'{rows}</div>')

        st.markdown(
            '<div class="chip-grid">'
            + chip_group("Penghasilan", mu_p.items())
            + chip_group("Tanggungan", mu_t.items())
            + '</div>',
            unsafe_allow_html=True,
        )

        st.markdown('<p class="sec-label">Aturan Aktif</p>', unsafe_allow_html=True)
        if not aturan_aktif:
            st.info("Belum ada aturan dengan firing strength di atas nol untuk masukan ini.")
        else:
            df_aturan = pd.DataFrame(
                {
                    "Aturan": [f"Penghasilan {r[0]} dan Tanggungan {r[1]}" for r in aturan_aktif],
                    "Nominal": [int(r[2]) for r in aturan_aktif],
                    "Firing": [round(r[3], 3) for r in aturan_aktif],
                }
            )
            st.dataframe(
                df_aturan,
                column_config={
                    "Nominal": st.column_config.NumberColumn("Nominal", format="Rp %.0f"),
                    "Firing": st.column_config.NumberColumn("Firing", format="%.3f"),
                },
                width="stretch",
                hide_index=True,
            )

with kanan:
    # ---- Matplotlib mengikuti sistem desain: tinta di atas kartu putih,
    #      garis MF diberi warna per kategori (identitas kategori, bukan dekorasi)
    plt.rcParams.update(
        {
            "figure.facecolor": "#FFFFFF",
            "axes.facecolor": "#FFFFFF",
            "text.color": INK,
            "axes.edgecolor": "#D8DCDE",
            "axes.labelcolor": MUTED,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "font.size": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    if aturan_aktif:
        st.markdown('<p class="sec-label">Aktivasi Aturan</p>', unsafe_allow_html=True)
        fig_b, ax_b = plt.subplots(figsize=(6.0, max(1.7, 0.45 * len(aturan_aktif) + 0.8)))
        label_aturan = [f"{r[0]}-{r[1]}" for r in aturan_aktif]
        alphas = [r[3] for r in aturan_aktif]
        bar_colors = [KATEGORI_WARNA[r[0]] for r in aturan_aktif]   # warna ikut kategori penghasilan
        ax_b.barh(label_aturan, alphas, color=bar_colors, height=0.55)
        ax_b.set_xlim(0, 1.05)
        ax_b.set_xlabel("Firing strength (alpha)")
        for i, r in enumerate(aturan_aktif):
            if r[3] + 0.09 > 1.0:          # label jatuh di dalam bar: putih, rata kanan
                ax_b.text(0.98, i, rp(r[2]), va="center", ha="right",
                          fontsize=8, color="#FFFFFF")
            else:
                ax_b.text(min(r[3] + 0.02, 0.90), i, rp(r[2]), va="center",
                          ha="left", fontsize=8, color=INK)
        ax_b.invert_yaxis()
        ax_b.grid(True, axis="x", linestyle=":", color="#D8DCDE", alpha=0.6)
        fig_b.tight_layout()
        st.pyplot(fig_b)

    st.markdown('<p class="sec-label">Kurva Keanggotaan dan Posisi Input</p>', unsafe_allow_html=True)
    fig2, (axl, axr) = plt.subplots(1, 2, figsize=(6.5, 2.8))

    MF_P = {"Rendah": (0, 0, 2_000_000, 4_000_000),
            "Sedang": (2_000_000, 4_000_000, 5_000_000, 7_000_000),
            "Tinggi": (5_000_000, 7_000_000, 10_000_000, 10_000_000)}
    xs = np.linspace(0, 10_000_000, 250)
    for lbl, (a, b, c, d) in MF_P.items():
        aktif = mu_p[lbl] > 0
        axl.plot(xs / 1e6, [trapezoid(x, a, b, c, d) for x in xs],
                 color=KATEGORI_WARNA[lbl],
                 linewidth=2.4 if aktif else 1.6,
                 alpha=1.0 if aktif else 0.35, label=lbl)
    axl.axvline(input_penghasilan / 1e6, color=INK, linestyle="--", linewidth=1.2)
    axl.set_title("Penghasilan", fontsize=9)
    axl.set_xlabel("Juta Rp/bulan")
    axl.set_ylabel("Derajat keanggotaan")
    axl.legend(fontsize=7, frameon=False)
    axl.grid(True, linestyle=":", color="#D8DCDE", alpha=0.6)

    MF_T = {"Sedikit": (0, 0, 1, 2), "Sedang": (1, 2, 3, 4), "Banyak": (3, 4, 6, 6)}
    xs_t = np.linspace(0, 6, 250)
    for lbl, (a, b, c, d) in MF_T.items():
        aktif = mu_t[lbl] > 0
        axr.plot(xs_t, [trapezoid(x, a, b, c, d) for x in xs_t],
                 color=KATEGORI_WARNA[lbl],
                 linewidth=2.4 if aktif else 1.6,
                 alpha=1.0 if aktif else 0.35, label=lbl)
    axr.axvline(input_tanggungan, color=INK, linestyle="--", linewidth=1.2)
    axr.set_title("Tanggungan", fontsize=9)
    axr.set_xlabel("Orang")
    axr.legend(fontsize=7, frameon=False)
    axr.grid(True, linestyle=":", color="#D8DCDE", alpha=0.6)

    fig2.tight_layout()
    st.pyplot(fig2)

st.caption("Praktikum 13 Modul 3 Logika Fuzzy, Asfal Fuad (240306031), S1 TI UIN Mataram, "
           "arsitektur fuzzy_engine.py (core) + app.py (UI).")

st.markdown("---")
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem; padding: 1.5rem 0; color: #5B6672; font-size: 0.85rem; line-height: 1.6;">
        <div style="flex: 1; min-width: 280px;">
            <p style="margin: 0; font-size: 0.75rem; color: #8A949E;">
                Aplikasi ini adalah implementasi sistem penunjang keputusan untuk menentukan nominal UKT
                mahasiswa berdasarkan penghasilan orang tua dan jumlah tanggungan keluarga.
                Metode: Fuzzy Logic (Mamdani/Sugeno) dengan defuzzifikasi Weighted Average.
            </p>
        </div>
        <div style="flex: 1; min-width: 280px; text-align: right;">
            <p style="margin: 0 0 0.35rem;"><strong>Sistem Penetapan UKT Mahasiswa Berbasis Logika Fuzzy</strong></p>
            <p style="margin: 0 0 0.35rem;">Praktikum 13 · Modul 3 · Logika Fuzzy</p>
            <p style="margin: 0 0 0.35rem;">Asfal Fuad (240306031) · S1 Teknik Informatika · UIN Mataram</p>
            <p style="margin: 0;">Dibangun dengan Streamlit · Fuzzy Engine: Sugeno Orde 0 · Rule Base: 9 Aturan</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
