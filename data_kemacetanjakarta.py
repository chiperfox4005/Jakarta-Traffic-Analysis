import pandas as pd
import tabula

# File PDF
file_pdf = r"E:\FILE VSC!!\Datmin_projek\data-titik-rawan-kemacetan-di-dki-jakarta-komponen-data.pdf"

print("=== LOAD DATA PDF ===")

try:
    # baca tabel tanpa header
    tables = tabula.read_pdf(
        file_pdf,
        pages="all",
        multiple_tables=True,
        pandas_options={'header': None}
    )

    if len(tables) == 0:
        print("Tidak ada tabel ditemukan")
        exit()

    # gabungkan semua tabel
    df = pd.concat(tables, ignore_index=True)

    print("\n=== DATA MENTAH ===")
    print(df.head())

    # Hapus baris kosong total
    df.dropna(how='all', inplace=True)

    # Reset index
    df.reset_index(drop=True, inplace=True)

    # Rename kolom sesuai jumlah kolom yang terbaca
    if len(df.columns) == 3:
        df.columns = ['wilayah', 'lokasi', 'jenis_kendaraan']

    elif len(df.columns) == 5:
        df.columns = [
            'wilayah',
            'lokasi',
            'jenis_kendaraan',
            'keterangan',
            'periode_data'
        ]

    else:
        print(f"Jumlah kolom terbaca: {len(df.columns)}")
        print("Kolom tidak sesuai format PDF")

    print("\n=== DATA SETELAH DIBERSIHKAN ===")
    print(df.head())

    print("\n=== INFO DATA ===")
    print(df.info())

    print("\n=== MISSING VALUES ===")
    print(df.isnull().sum())

    # Analisis wilayah
    if 'wilayah' in df.columns:
        print("\n=== JUMLAH DATA PER WILAYAH ===")
        print(df['wilayah'].value_counts())

    # Analisis kendaraan
    if 'jenis_kendaraan' in df.columns:
        print("\n=== JUMLAH JENIS KENDARAAN ===")
        print(df['jenis_kendaraan'].value_counts())

    # Simpan CSV
    output_file = "hasil_kemacetan_jakarta.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')

    print(f"\nData berhasil disimpan ke {output_file}")

except Exception as e:
    print("Error membaca file:", e)