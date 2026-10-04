import numpy as np
import matplotlib.pyplot as plt

# 1. RANCANG LOGIKA CRISP

def crisp_kritis(waktu_tunggu, threshold=8.0):
    return np.where(waktu_tunggu >= threshold, 1.0, 0.0)

# 2. RANCANG LOGIKA FUZZY

def fuzzy_linear_kritis(waktu_tunggu, a=4.0, b=12.0):
    derajat = (waktu_tunggu - a) / (b - a)
    return np.clip(derajat, 0.0, 1.0)

# 3. IMPLEMENTASI DAN PENGUJIAN

def test_sistem():
    
    # Data pengujian dari soal
    test_data = [2, 4, 6, 7.9, 8.0, 8.1, 10, 12, 16, 24]
    
    print("\nTABEL PERBANDINGAN:")
    print(f"{'Waktu (jam)':<12} | {'Crisp':<8} | {'Fuzzy':<8}")
    print("-" * 35)
    
    for waktu in test_data:
        c_val = float(crisp_kritis(waktu))
        f_val = float(fuzzy_linear_kritis(waktu))
        print(f"{waktu:<12} | {c_val:<8.1f} | {f_val:<8.3f}")
    
    print("-" * 35)
    return test_data

# 4. VISUALISASI

def create_visualization():
    # Generate data untuk plotting
    waktu = np.linspace(0, 24, 500)
    y_crisp = crisp_kritis(waktu)
    y_fuzzy = fuzzy_linear_kritis(waktu)
    
    # Data pengujian
    test_data = [2, 4, 6, 7.9, 8.0, 8.1, 10, 12, 16, 24]
    
    # Buat grafik
    plt.figure(figsize=(12, 8))
    
    # Plot fungsi crisp dan fuzzy
    plt.step(waktu, y_crisp, 'r-', linewidth=2.5, 
             label='Logika Crisp (≥ 8 jam)', where='post')
    plt.plot(waktu, y_fuzzy, 'b-', linewidth=2.5, 
             label='Logika Fuzzy Linear [4-12 jam]')
    
    # Titik data pengujian
    plt.scatter(test_data, [crisp_kritis(t) for t in test_data], 
                color='red', s=60, zorder=5, alpha=0.8)
    plt.scatter(test_data, [fuzzy_linear_kritis(t) for t in test_data], 
                color='blue', s=60, zorder=5, alpha=0.8)
    
    # Garis bantu
    plt.axvline(x=4, color='green', linestyle='--', alpha=0.7, label='Mulai transisi (4h)')
    plt.axvline(x=8, color='red', linestyle='--', alpha=0.7, label='Threshold crisp (8h)')
    plt.axvline(x=12, color='purple', linestyle='--', alpha=0.7, label='Selesai transisi (12h)')
    
    # Konfigurasi grafik
    plt.title('Sistem Prioritas Tiket Helpdesk TI: Crisp vs Fuzzy')
    plt.xlabel('Waktu Tunggu (jam)')
    plt.ylabel('Derajat Keanggotaan')
    plt.xlim(0, 24)
    plt.ylim(-0.05, 1.1)
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Simpan grafik
    plt.show()
    
    print(f"\nGrafik tersimpan")


def main():
    
    # Pengujian
    test_sistem()
    
    # Visualisasi
    create_visualization()

if __name__ == "__main__":
    main()
