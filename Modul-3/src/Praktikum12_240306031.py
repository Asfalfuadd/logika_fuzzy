# -*- coding: utf-8 -*-
"""
Praktikum12_240306031.py - Evaluasi Sistem Fuzzy UKT dengan Dataset
Mahasiswa : Asfal Fuad (240306031)

Tugas:
1. Baca dataset PENGHARGAAN uji (data/test_cases.csv) via Pandas
2. Preprocessing: penanganan nilai kosong + validasi semesta
3. Batch testing mesin inferensi fuzzy (fuzzy_engine.py)
4. Metrik MAE & RMSE
5. Grafik garis target vs prediksi + analisis sensitivitas
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')                    # headless: simpan file tanpa window
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE, 'src'))
from fuzzy_engine import infer_ukt, SEMESTA

CATATAN = []                             # log preprocessing


# ==========================================================
# 1. LOAD + PREPROCESSING SEDERHANA
# ==========================================================
CSV = os.path.join(BASE, 'data', 'test_cases.csv')
df = pd.read_csv(CSV)

print('=' * 70)
print('PREPROCESSING DATASET PENGUJIAN UKT (n =', len(df), ')')
print('=' * 70)

# a) penanganan nilai kosong
for kolom in ['penghasilan', 'tanggungan']:
    n_kosong = df[kolom].isna().sum()
    if n_kosong > 0:
        CATATAN.append(f'{kolom}: {n_kosong} nilai kosong -> isi median')
        df[kolom] = df[kolom].fillna(df[kolom].median())
    df[kolom] = df[kolom].astype(float)
df['ukt_expert'] = df['ukt_expert'].astype(float)

# b) validasi rentang semesta (clip ke batas)
lo_p, hi_p = SEMESTA['penghasilan']
lo_t, hi_t = SEMESTA['tanggungan']
di_luar_p = (df['penghasilan'] < lo_p) | (df['penghasilan'] > hi_p)
di_luar_t = (df['tanggungan'] < lo_t) | (df['tanggungan'] > hi_t)
if di_luar_p.any():
    CATATAN.append(f"penghasilan: {int(di_luar_p.sum())} baris di luar semesta -> clip")
    df['penghasilan'] = df['penghasilan'].clip(lo_p, hi_p)
if di_luar_t.any():
    CATATAN.append(f"tanggungan: {int(di_luar_t.sum())} baris di luar semesta -> clip")
    df['tanggungan'] = df['tanggungan'].clip(lo_t, hi_t)

if CATATAN:
    for c in CATATAN:
        print('  -', c)
else:
    print('  - semua data bersih: tanpa nilai kosong & dalam rentang semesta')

print()
print('5 DATA TERATAS:')
print(df.head().to_string(index=False))


# ==========================================================
# 2. EKSEKUSI BATCH TESTING (SUGENO ORDE 0)
# ==========================================================
prediksi = []
for _, row in df.iterrows():
    prediksi.append(infer_ukt(row['penghasilan'], row['tanggungan']))
df['ukt_fuzzy'] = prediksi

df['error_absolut'] = (df['ukt_expert'] - df['ukt_fuzzy']).abs()
df['error_kuadrat'] = (df['ukt_expert'] - df['ukt_fuzzy']) ** 2


# ==========================================================
# 3. METRIK EVALUASI: MAE & RMSE
# ==========================================================
mae = df['error_absolut'].mean()
rmse = float(np.sqrt(df['error_kuadrat'].mean()))

print()
print('=' * 70)
print('HASIL PENGUKURAN KINERJA SISTEM FUZZY UKT (SUGENO ORDE 0):')
print('=' * 70)
print(f'Total Sampel Uji (N)            : {len(df)}')
print(f'Mean Absolute Error (MAE)       : Rp {mae:,.0f}')
print(f'Root Mean Squared Error (RMSE)  : Rp {rmse:,.0f}')
print(f'RMSE/MAE                        : {rmse / mae:.2f}  (>1 = ada outlier besar)')
print('=' * 70)


# ==========================================================
# 4. VISUALISASI: TARGET AKTUAL vs PREDIKSI FUZZY
# ==========================================================
x_idx = np.arange(1, len(df) + 1)
plt.figure(figsize=(10, 5.5))
plt.plot(x_idx, df['ukt_expert'] / 1e6, 'ro-', label='Target Aktual (Pakar)', linewidth=2)
plt.plot(x_idx, df['ukt_fuzzy'] / 1e6, 'bs--', label='Output Sistem Fuzzy', linewidth=2)
plt.title(f'Evaluasi UKT-Fuzzy: Target Pakar vs Prediksi Fuzzy (MAE: Rp{mae:,.0f})',
          fontsize=13, fontweight='bold')
plt.xlabel('Nomor Kasus Uji')
plt.ylabel('Nominal UKT (Juta Rupiah)')
plt.xticks(x_idx, df['id'].astype(int))
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'evaluasi_prediksi_vs_aktual.png'), dpi=300)
plt.close()
print('\nGrafik disimpan: evaluasi_prediksi_vs_aktual.png')


# ==========================================================
# 5. DUA KASUS ERROR TERBESAR (TUGAS E.5)
# ==========================================================
worst = df.nlargest(2, 'error_absolut')
print('\n2 KASUS ERROR ABSOLUT TERBESAR:')
for _, r in worst.iterrows():
    print(f"  Kasus {int(r['id'])} ({r['kasus']}): penghasilan Rp{r['penghasilan']:,.0f}, "
          f"tanggungan {r['tanggungan']:.0f} -> fuzzy Rp{r['ukt_fuzzy']:,.0f} "
          f"vs pakar Rp{r['ukt_expert']:,.0f} (selisih Rp{r['error_absolut']:,.0f})")


# ==========================================================
# 6. ANALISIS SENSITIVITAS (BAGIAN D)
# ==========================================================
p_sweep = np.arange(0, 10_000_001, 100_000)     # tanggungan ditahan = 2
t_sweep = np.arange(0, 6.0001, 0.05)            # penghasilan ditahan = 5.500.000
y_p = [infer_ukt(p, 2) for p in p_sweep]
y_t = [infer_ukt(5_500_000, t) for t in t_sweep]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.6))
ax1.plot(p_sweep / 1e6, np.array(y_p) / 1e6, 'b-', linewidth=2)
ax1.set_title('Sensitivitas Penghasilan (tanggungan ditekan = 2)', fontsize=11, fontweight='bold')
ax1.set_xlabel('Penghasilan Orang Tua (Juta Rp)')
ax1.set_ylabel('UKT (Juta Rp)')
ax1.grid(True, linestyle=':', alpha=0.6)

ax2.plot(t_sweep, np.array(y_t) / 1e6, 'g-', linewidth=2)
ax2.set_title('Sensitivitas Tanggungan (penghasilan ditekan = Rp5,5 jt)', fontsize=11, fontweight='bold')
ax2.set_xlabel('Jumlah Tanggungan (orang)')
ax2.set_ylabel('UKT (Juta Rp)')
ax2.grid(True, linestyle=':', alpha=0.6)

fig.suptitle('Analisis Sensitivitas UKT-Fuzzy', fontsize=13, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(BASE, 'analisis_sensitivitas.png'), dpi=300)
plt.close(fig)
print('Grafik sensitivitas disimpan: analisis_sensitivitas.png')

# ringkasan sensitivitas numerik (perubahan total output)
d_p = np.array(y_p)
d_t = np.array(y_t)
print('\nRINGKASAN SENSITIVITAS:')
print(f'  Penghasilan 0->10 jt (tanggungan 2): UKT berubah Rp{d_p[0]:,.0f} -> Rp{d_p[-1]:,.0f}'
      f'  (rentang Rp{(d_p.max() - d_p.min())/1e6:.1f} juta)')
print(f'  Tanggungan 0->6   (penghasilan 5,5jt): UKT berubah Rp{d_t[0]:,.0f} -> Rp{d_t[-1]:,.0f}'
      f'  (rentang Rp{(d_t.max() - d_t.min())/1e6:.1f} juta)')

print('\nSelesai - Praktikum 12.')
