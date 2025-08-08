import pandas as pd

df = pd.read_csv("src/ingestion/item8-appl/parsed_statements_op.csv")

# Misal df sudah ada 3 kolom: A, 2024, 2023, 2022
# Kita reshuffle ke bentuk long (melting)
df.columns = ['Metric', '2024', '2023', '2022']

# Buat long-form table
long_df = df.melt(id_vars='Metric', var_name='Year', value_name='Value')

# Bersihkan nilai kosong dan baris tanpa Metric
long_df = long_df.dropna(subset=['Metric', 'Value'])

# Simpan
long_df.to_csv("src/ingestion/item8-appl/long_statements_op.csv", index=False)
