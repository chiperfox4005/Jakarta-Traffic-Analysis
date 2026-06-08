import pandas as pd
import tabula
import matplotlib.pyplot as plt

from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# ==================================================
# 1. LOAD DATA PDF (IKUT CARA FIKRY)
# ==================================================
# Membaca langsung file PDF yang ada di folder DATMIN kamu
file_pdf = "data-titik-rawan-kemacetan-di-dki-jakarta-komponen-data.pdf"

print("=== LOAD DATA PDF ===")

try:
    tables = tabula.read_pdf(
        file_pdf,
        pages="all",
        multiple_tables=True,
        pandas_options={"header": None}
    )

    if len(tables) == 0:
        raise Exception("Tidak ada tabel ditemukan di file PDF")

    df_raw = pd.concat(
        tables,
        ignore_index=True
    )

    print("\n=== DATA MENTAH ===")
    print(df_raw.head())

    print("\nJumlah Data Awal:")
    print(df_raw.shape)

    print("\nMissing Value Awal:")
    print(df_raw.isnull().sum())

# ==================================================
# 2. PREPROCESSING
# ==================================================
    print("\n=== PREPROCESSING ===")
    df = df_raw.copy()

    df.dropna(how="all", inplace=True)
    df.reset_index(drop=True, inplace=True)

    if len(df.columns) == 3:
        df.columns = ["wilayah", "lokasi", "jenis_kendaraan"]
    elif len(df.columns) == 5:
        df.columns = ["wilayah", "lokasi", "jenis_kendaraan", "keterangan", "periode_data"]

    # Bersihkan text
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    # Replace karakter tidak valid
    df.replace("-", pd.NA, inplace=True)

    # Isi missing value
    if "wilayah" in df.columns:
        df["wilayah"] = df["wilayah"].fillna("UNKNOWN")

    if "jenis_kendaraan" in df.columns:
        df["jenis_kendaraan"] = df["jenis_kendaraan"].fillna("UNKNOWN")

    # Hapus duplicate
    before = len(df)
    df.drop_duplicates(inplace=True)
    after = len(df)
    df.reset_index(drop=True, inplace=True)

# ==================================================
# 3. HASIL CLEANING
# ==================================================
    print("\n=== DATA SETELAH CLEANING ===")
    print(df.head())
    print("\nJumlah Data:", df.shape)
    print("\nMissing Value:\n", df.isnull().sum())
    print("\nData Terhapus:", before - after)

# ==================================================
# 4. EDA (GRAFIK)
# ==================================================
    print("\n=== EXPLORATORY DATA ANALYSIS ===")
    
    wilayah = df["wilayah"].value_counts()
    print("\nDistribusi Wilayah:\n", wilayah)

    plt.figure(figsize=(8,5))
    wilayah.plot(kind="bar", color="skyblue")
    plt.title("Distribusi Titik Kemacetan Per Wilayah")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    kendaraan = df["jenis_kendaraan"].value_counts()
    print("\nDistribusi Kendaraan:\n", kendaraan)

    plt.figure(figsize=(8,5))
    kendaraan.plot(kind="bar", color="salmon")
    plt.title("Jenis Kendaraan")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# ==================================================
# 5. DATA MINING (K-MEANS)
# ==================================================
    print("\n=== KMEANS CLUSTERING ===")
    encoder = OneHotEncoder(sparse_output=False)
    X = encoder.fit_transform(df[["wilayah", "jenis_kendaraan"]])

# ==================================================
# 6. CARI CLUSTER TERBAIK
# ==================================================
    scores = []
    for k in range(2, 6):
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X)
        score = silhouette_score(X, labels)
        scores.append(score)
        print(f"K={k} → Silhouette Score: {score:.3f}")

    best_k = scores.index(max(scores)) + 2
    print("\nCluster terbaik:", best_k)

# ==================================================
# 7. MODEL FINAL
# ==================================================
    model = KMeans(n_clusters=best_k, random_state=42, n_init=10)
    df["Cluster"] = model.fit_predict(X)

# ==================================================
# 8. EVALUASI
# ==================================================
    score = silhouette_score(X, df["Cluster"])
    print("\nSilhouette Score Akhir:", round(score, 3))

# ==================================================
# 9. INSIGHT
# ==================================================
    print("\n=== HASIL CLUSTER ===")
    print(df["Cluster"].value_counts())

    for c in sorted(df["Cluster"].unique()):
        print(f"\nCluster {c}")
        print(df[df["Cluster"] == c][["wilayah", "jenis_kendaraan"]].mode())

# ==================================================
# 10. VISUALISASI CLUSTER
# ==================================================
    plt.figure(figsize=(8,5))
    df["Cluster"].value_counts().plot(kind="bar", color="lightgreen")
    plt.title("Distribusi Cluster")
    plt.show()

# ==================================================
# 11. SAVE OUTPUT
# ==================================================
    df.to_csv("hasil_kemacetan_jakarta.csv", index=False, encoding="utf-8-sig")
    df.groupby("Cluster").size().to_csv("ringkasan_cluster.csv")
    print("\n[✓] Data dan Ringkasan Berhasil Disimpan!")

except Exception as e:
    print("\nERROR:", e)