import pandas as pd

file_name = 'dataset_kemacetan_jakarta_1_sheet.xlsx'
df = pd.read_excel(file_name)

print("=== DETAIL DATA AWAL (SEBELUM PREPROCESSING) ===")
print(f"-> Total baris data asli: {df.shape[0]} baris")


print("\n=== MEMULAI PROSES PREPROCESSING ===")

missing_awal = df.isnull().sum().sum()
df_bersih = df.ffill()
print(f"[✓] Step 1: Ditemukan {missing_awal} data kosong -> Sudah otomatis diisi aman.")

duplikat_awal = df_bersih.duplicated().sum()
df_bersih = df_bersih.drop_duplicates()
print(f"[✓] Step 2: Ditemukan {duplikat_awal} data duplikat -> Sudah dihapus.")


for col in df_bersih.select_dtypes(include=['object']).columns:
    df_bersih[col] = df_bersih[col].astype(str).str.strip()
print("[✓] Step 3: Text Cleaning selesai (Spasi berlebih di semua kolom teks sudah dibersihkan).")


kolom_utama = ['Wilayah', 'Waktu', 'Volume Kendaraan', 'Cuaca', 'Penyebab Kemacetan', 'Tingkat Kemacetan']
df_final = df_bersih[kolom_utama].copy()

print(f"\n=== HASIL AKHIR PREPROCESSING ===")
print(f"-> Total baris data bersih sekarang: {df_final.shape[0]} baris")

df_final.to_csv('hasil_preprocessing_kemacetan.csv', index=False)
print("-> BERHASIL! File bersih disimpan dengan nama 'hasil_preprocessing_kemacetan.csv'")