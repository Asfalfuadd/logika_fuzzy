import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi matplotlib untuk hasil yang optimal
plt.style.use('default')
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3


# ==========================================================
# 1. RANCANGAN LOGIKA CRISP
# ==========================================================
def crisp_kritis(waktu_tunggu, threshold=8.0):
    """
    Fungsi karakteristik crisp untuk klasifikasi tiket kritis.
    
    Definisi: Tiket dianggap kritis jika waktu tunggu ≥ 8 jam
    
    Formula Matematika:
    χ_Kritis(x) = {1, jika x ≥ 8; 0, jika x < 8}
    
    Parameters:
    -----------
    waktu_tunggu : array_like atau float
        Waktu tunggu penyelesaian tiket dalam jam
    threshold : float, default=8.0
        Batas ambang kritis dalam jam
    
    Returns:
    --------
    array_like atau float
        Nilai keanggotaan crisp (0 atau 1)
        0 = Normal, 1 = Kritis
    
    Examples:
    ---------
    >>> crisp_kritis(7.9)
    0.0
    >>> crisp_kritis(8.0) 
    1.0
    """
    return np.where(waktu_tunggu >= threshold, 1.0, 0.0)


# ==========================================================
# 2. RANCANGAN LOGIKA FUZZY LINEAR
# ==========================================================
def fuzzy_linear_kritis(waktu_tunggu, a=4.0, b=12.0):
    """
    Fungsi keanggotaan fuzzy linear untuk klasifikasi tiket kritis.
    
    Definisi Interval Transisi:
    - Waktu < 4 jam       : derajat kritis = 0 (tidak kritis)
    - 4 ≤ x ≤ 12 jam      : derajat kritis naik linear dari 0 ke 1
    - Waktu > 12 jam      : derajat kritis = 1 (sangat kritis)
    
    Penurunan Formula Matematika:
    Untuk interval linear [a, b] = [4, 12]:
    - Titik awal: (4, 0), Titik akhir: (12, 1)
    - Gradien: m = (1-0)/(12-4) = 1/8 = 0.125
    - Persamaan garis: y = 0.125(x-4) = (x-4)/8
    
    Formula Lengkap:
    μ_Kritis(x) = {
        0,           jika x < 4
        (x-4)/8,     jika 4 ≤ x ≤ 12  
        1,           jika x > 12
    }
    
    Parameters:
    -----------
    waktu_tunggu : array_like atau float
        Waktu tunggu penyelesaian tiket dalam jam
    a : float, default=4.0
        Batas bawah interval transisi (mulai naik dari 0)
    b : float, default=12.0
        Batas atas interval transisi (mencapai nilai 1)
    
    Returns:
    --------
    array_like atau float
        Nilai derajat keanggotaan fuzzy dalam rentang [0, 1]
    
    Examples:
    ---------
    >>> fuzzy_linear_kritis(4)   # 0.000
    >>> fuzzy_linear_kritis(8)   # 0.500  
    >>> fuzzy_linear_kritis(12)  # 1.000
    """
    # Hitung derajat keanggotaan menggunakan formula linear
    derajat = (waktu_tunggu - a) / (b - a)
    
    # Klip hasil ke rentang [0, 1] untuk memastikan validitas
    return np.clip(derajat, 0.0, 1.0)


# ==========================================================
# 3. PENGUJIAN DENGAN DATA SPESIFIK
# ==========================================================
def test_sistem_helpdesk():    
    test_data = [2, 4, 6, 7.9, 8.0, 8.1, 10, 12, 16, 24]
    
    print("SPESIFIKASI SISTEM:")
    print("• Semesta Pembicaraan: 0 ≤ x ≤ 24 jam")
    print("• Logika Crisp: Kritis jika waktu tunggu ≥ 8 jam")
    print("• Logika Fuzzy: Transisi linear dari 4 jam (μ=0) ke 12 jam (μ=1)")
    print()
    
    print("HASIL PENGUJIAN KLASIFIKASI TIKET:")
    print()
    print(f"{'Waktu':<8} | {'Crisp':<8} | {'Fuzzy':<8} | {'% Kritis':<10} | {'Interpretasi Fuzzy':<30} | {'Status Crisp'}")
    print("-" * 95)
    
    results = []
    
    for waktu in test_data:
        # Hitung nilai keanggotaan untuk kedua sistem
        c_val = float(crisp_kritis(waktu))
        f_val = float(fuzzy_linear_kritis(waktu))
        persen_kritis = f_val * 100
        
        # Klasifikasi interpretasi berdasarkan derajat keanggotaan fuzzy
        if f_val == 0.0:
            interpretasi = "Normal (Tidak Perlu Eskalasi)"
        elif f_val <= 0.25:
            interpretasi = "Rendah (Monitor Saja)"
        elif f_val <= 0.5:
            interpretasi = "Sedang (Perhatian Khusus)"
        elif f_val <= 0.75:
            interpretasi = "Tinggi (Prioritas Utama)"
        elif f_val < 1.0:
            interpretasi = "Sangat Tinggi (Eskalasi Segera)"
        else:
            interpretasi = "Kritis (Eskalasi Darurat)"
        
        # Status sistem crisp
        status_crisp = "KRITIS" if c_val == 1.0 else "Normal"
        
        print(f"{waktu:<8.1f} | {c_val:<8.1f} | {f_val:<8.3f} | {persen_kritis:<10.1f} | {interpretasi:<30} | {status_crisp}")
        
        # Simpan hasil untuk analisis lanjutan
        results.append({
            'waktu': waktu,
            'crisp': c_val,
            'fuzzy': f_val,
            'persen': persen_kritis,
            'interpretasi': interpretasi,
            'status_crisp': status_crisp
        })
    
    print("-" * 95)
    return results


# ==========================================================
# 4. ANALISIS MATEMATIS DAN BOUNDARY PROBLEM
# ==========================================================
def analisis_matematis():
    """
    Menampilkan analisis matematis lengkap kedua fungsi.
    """
    print("\n" + "=" * 80)
    print("ANALISIS MATEMATIS FUNGSI KEANGGOTAAN")
    print("=" * 80)
    
    print("\n1. FUNGSI CRISP (KARAKTERISTIK BINER):")
    print("   χ_Kritis(x) = {1, jika x ≥ 8; 0, jika x < 8}")
    print("   • Domain: [0, 24] jam")
    print("   • Range: {0, 1}")
    print("   • Sifat: Diskontinu pada x = 8 jam")
    print("   • Implementasi: np.where(x >= 8.0, 1.0, 0.0)")
    
    print("\n2. FUNGSI FUZZY LINEAR:")
    print("   μ_Kritis(x) = {")
    print("       0,           jika x < 4")
    print("       (x-4)/8,     jika 4 ≤ x ≤ 12")
    print("       1,           jika x > 12")
    print("   }")
    print()
    print("   PENURUNAN MANUAL FORMULA LINEAR:")
    print("   • Interval transisi: [4, 12] jam")
    print("   • Titik koordinat: (4, 0) dan (12, 1)")
    print("   • Gradien: m = (y₂-y₁)/(x₂-x₁) = (1-0)/(12-4) = 1/8")
    print("   • Persamaan point-slope: y - 0 = (1/8)(x - 4)")
    print("   • Simplifikasi: y = (1/8)x - 1/2 = (x-4)/8")
    print("   • Domain: [0, 24] jam")
    print("   • Range: [0, 1]")
    print("   • Sifat: Kontinu dan diferensiabel di semua titik")


def analisis_boundary_problem():
    """
    Analisis khusus masalah boundary pada sistem crisp vs fuzzy.
    """
    print("\n" + "=" * 80)
    print("ANALISIS BOUNDARY PROBLEM (MASALAH BATAS KAKU)")
    print("=" * 80)
    
    # Kasus kritis di sekitar threshold 8 jam
    boundary_cases = [7.8, 7.9, 8.0, 8.1, 8.2]
    
    print(f"\n{'Waktu':<8} | {'Crisp':<8} | {'Fuzzy':<8} | {'Selisih':<10} | {'Keterangan'}")
    print("-" * 60)
    
    for i, waktu in enumerate(boundary_cases):
        c_val = crisp_kritis(waktu)
        f_val = fuzzy_linear_kritis(waktu)
        
        if i > 0:
            c_diff = c_val - crisp_kritis(boundary_cases[i-1])
            f_diff = f_val - fuzzy_linear_kritis(boundary_cases[i-1])
            keterangan = f"ΔCrisp:{c_diff:.1f}, ΔFuzzy:{f_diff:.3f}"
        else:
            keterangan = "Baseline"
        
        print(f"{waktu:<8.1f} | {c_val:<8.1f} | {f_val:<8.3f} | {keterangan:<10} | ", end="")
        
        if waktu < 8.0:
            print("Sebelum threshold")
        elif waktu == 8.0:
            print("Tepat di threshold ← MASALAH CRISP")
        else:
            print("Setelah threshold")
    
    print("\nKESIMPULAN BOUNDARY PROBLEM:")
    print("• MASALAH CRISP: Lompatan ekstrem 0→1 pada perubahan 0.1 jam")
    print("• SOLUSI FUZZY: Transisi halus ~0.0125 per 0.1 jam")
    print("• Fuzzy lebih robust terhadap noise dan variasi pengukuran")


# ==========================================================
# 5. VISUALISASI PERBANDINGAN
# ==========================================================
def create_visualization():
    """
    Membuat visualisasi perbandingan sistem crisp vs fuzzy.
    """
    print("\n📊 Membuat visualisasi perbandingan sistem...")
    
    # Generate data dengan resolusi tinggi untuk plotting smooth
    waktu_tunggu = np.linspace(0, 24, 1000)
    
    # Hitung nilai keanggotaan untuk plotting
    y_crisp = crisp_kritis(waktu_tunggu, threshold=8.0)
    y_fuzzy = fuzzy_linear_kritis(waktu_tunggu, a=4.0, b=12.0)
    
    # Data pengujian untuk scatter points
    test_data = [2, 4, 6, 7.9, 8.0, 8.1, 10, 12, 16, 24]
    
    # Create figure dengan 2 subplot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))
    
    # === SUBPLOT 1: PERBANDINGAN UTAMA ===
    # Plot fungsi crisp dengan step function
    ax1.step(waktu_tunggu, y_crisp, 'r-', linewidth=3.5, 
             label='Logika Crisp (Threshold = 8 jam)', where='post', alpha=0.85)
    
    # Plot fungsi fuzzy linear
    ax1.plot(waktu_tunggu, y_fuzzy, 'b-', linewidth=3, 
             label='Logika Fuzzy Linear [4, 12] jam', alpha=0.9)
    
    # Garis vertikal untuk menandai titik-titik penting
    important_points = [4, 8, 12]
    colors_points = ['green', 'red', 'purple']
    labels_points = ['Mulai Transisi (4h)', 'Threshold Crisp (8h)', 'Selesai Transisi (12h)']
    
    for point, color, label in zip(important_points, colors_points, labels_points):
        ax1.axvline(x=point, color=color, linestyle='--', alpha=0.7, linewidth=2)
        ax1.text(point, 1.05, label, rotation=0, ha='center', fontsize=9, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.3))
    # Scatter plot untuk data pengujian
    test_crisp_vals = [crisp_kritis(t) for t in test_data]
    test_fuzzy_vals = [fuzzy_linear_kritis(t) for t in test_data]
    
    ax1.scatter(test_data, test_crisp_vals, color='darkred', s=100, 
               alpha=0.8, zorder=5, marker='o', edgecolors='black', linewidths=1,
               label='Data Uji - Crisp')
    ax1.scatter(test_data, test_fuzzy_vals, color='darkblue', s=100, 
               alpha=0.8, zorder=5, marker='s', edgecolors='black', linewidths=1,
               label='Data Uji - Fuzzy')
    
    # Anotasi untuk menjelaskan masalah boundary
    ax1.annotate('BOUNDARY PROBLEM!\\n7.9h→Normal vs 8.0h→Kritis\\n(Lompatan Ekstrem)', 
                 xy=(8, 0.5), xytext=(15, 0.35),
                 arrowprops=dict(arrowstyle='->', color='red', lw=2.5),
                 fontsize=11, ha='center', fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.5", facecolor='mistyrose', 
                          edgecolor='red', alpha=0.9))
    
    ax1.annotate('TRANSISI HALUS FUZZY\\n(Gradual Escalation)\\nLebih Natural & Robust', 
                 xy=(8, 0.5), xytext=(5, 0.85),
                 arrowprops=dict(arrowstyle='->', color='blue', lw=2.5),
                 fontsize=11, ha='center', fontweight='bold',
                 bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', 
                          edgecolor='blue', alpha=0.9))
    
    # Konfigurasi subplot 1
    ax1.set_title('Sistem Prioritas Tiket Helpdesk TI: Perbandingan Crisp vs Fuzzy\\n' +
                  'Kategori "Kritis/Butuh Eskalasi Cepat"', 
                  fontsize=15, fontweight='bold', pad=20)
    ax1.set_xlabel('Waktu Tunggu Penyelesaian Tiket (jam)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Derajat Keanggotaan μ(x)', fontsize=13, fontweight='bold')
    ax1.set_xlim(0, 24)
    ax1.set_ylim(-0.05, 1.15)
    ax1.grid(True, alpha=0.4, linestyle=':')
    ax1.legend(fontsize=11, loc='center left', bbox_to_anchor=(0.02, 0.75),
              frameon=True, fancybox=True, shadow=True)
    
    # === SUBPLOT 2: DETAIL ANALISIS BOUNDARY (6-10 jam) ===
    boundary_range = np.linspace(6, 10, 200)
    ax2.step(boundary_range, crisp_kritis(boundary_range), 'r-', 
             linewidth=4, label='Crisp', marker='o', markersize=5, 
             markevery=20, where='post')
    ax2.plot(boundary_range, fuzzy_linear_kritis(boundary_range), 'b-', 
             linewidth=3.5, label='Fuzzy Linear', marker='s', markersize=4, markevery=20)
    
    # Garis threshold
    ax2.axvline(x=8, color='black', linestyle=':', linewidth=3, alpha=0.8,
               label='Threshold Crisp (8h)')
    
    # Highlight area masalah boundary
    ax2.axvspan(7.8, 8.2, alpha=0.2, color='yellow', label='Zona Masalah Boundary')
    
    # Konfigurasi subplot 2
    ax2.set_title('Detail Analisis Boundary Problem: Zona Kritis 6-10 jam', 
                  fontsize=13, fontweight='bold')
    ax2.set_xlabel('Waktu Tunggu (jam)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Derajat Keanggotaan', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.4, linestyle=':')
    ax2.legend(fontsize=10, loc='upper left')
    
    # Penyesuaian layout
    plt.tight_layout(pad=3.0)
    
    # Simpan grafik dengan kualitas tinggi
    filename = 'Praktikum1_240306031_Asfal_Fuad.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.show()
    
    print(f"✅ Grafik berhasil disimpan sebagai '{filename}'")
    return filename


# ==========================================================
# 6. TABEL PERBANDINGAN SISTEM
# ==========================================================
def create_comparison_table():
    """
    Membuat tabel perbandingan karakteristik sistem crisp vs fuzzy.
    """
    print("\n" + "=" * 80)
    print("TABEL PERBANDINGAN KARAKTERISTIK SISTEM")
    print("=" * 80)
    
    print(f"{'Aspek Perbandingan':<25} | {'Logika Crisp':<22} | {'Logika Fuzzy Linear'}")
    print("-" * 80)
    
    comparisons = [
        ("Batas Klasifikasi", "≥ 8 jam (Kaku)", "4-12 jam (Bertahap)"),
        ("Nilai Output", "{0, 1}", "[0, 1] Kontinu"),
        ("Jumlah Kategori", "2 (Normal/Kritis)", "5+ Level Prioritas"),
        ("Sensitivitas Noise", "Sangat Tinggi", "Rendah (Toleran)"),
        ("Boundary Problem", "Ada (7.9→8.0)", "Tidak Ada"),
        ("Implementasi", "if-else Sederhana", "Fungsi Matematis"),
        ("Interpretasi", "Binary Ya/Tidak", "Gradasi Bertingkat"),
        ("False Alarm", "Tinggi", "Rendah"),
        ("Fleksibilitas", "Rendah", "Tinggi"),
        ("Kasus 7.9 vs 8.1h", "Beda Kategori Total", "Hampir Identik"),
        ("Stabilitas Sistem", "Tidak Stabil", "Sangat Stabil"),
        ("Cocok untuk", "Sistem Sederhana", "Sistem Kompleks")
    ]
    
    for aspect, crisp_char, fuzzy_char in comparisons:
        print(f"{aspect:<25} | {crisp_char:<22} | {fuzzy_char}")
    
    print("-" * 80)


# ==========================================================
# 7. FUNGSI UTAMA
# ==========================================================
def main():
    print()
    
    # 1. Pengujian dengan data spesifik dari soal
    results = test_sistem_helpdesk()
    
    # 2. Analisis matematis lengkap
    analisis_matematis()
    
    # 3. Analisis boundary problem
    analisis_boundary_problem()
    
    # 4. Tabel perbandingan sistem
    create_comparison_table()
    
    # 5. Visualisasi
    filename = create_visualization()
    
if __name__ == "__main__":
    main()
