# import camelot
# import pandas as pd
# import sqlite3
# import os

# pdf_paths = {
#     "statements_op": "src/ingestion/item8-appl/statements_op.pdf",
#     "balance_sheets": "src/ingestion/item8-appl/balance_sheets.pdf",
#     "cash_flows": "src/ingestion/item8-appl/cash_flows.pdf"
# }

# output_dir = "src/ingestion/item8-appl"
# sqlite_path = os.path.join(output_dir, "financials.sqlite")

# # connect to SQLite
# conn = sqlite3.connect(sqlite_path)

# for name, path in pdf_paths.items():
#     print(f"Processing {name}...")
#     tables = camelot.read_pdf(path, pages='all', flavor='lattice') 
    
#     if tables:
#         df = tables[0].df  
#         csv_path = os.path.join(output_dir, f"{name}.csv")
#         df.to_csv(csv_path, index=False)

#         # Save to SQLite
#         df.columns = [f"col_{i}" for i in range(len(df.columns))]  
#         df.to_sql(name, conn, if_exists='replace', index=False)

# conn.close()
# print("Done saving to CSV and SQLite")

import pandas as pd
import re

# Baca data hasil ekstraksi PDF
df = pd.read_csv("src/ingestion/item8-appl/statements_op.csv")

rows = []
for line in df['text']:  # kolom "text" berisi seluruh isi
    # Cari baris yang berisi angka tahun (tiga angka di akhir)
    if re.search(r'(\$\s*)?\d{1,3}(,\d{3})*(\.\d+)?(\s+\$\s*)?\d{1,3}(,\d{3})*(\.\d+)?', line):
        # Pisahkan nama item dan angka
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) >= 4:
            item = parts[0]
            values = parts[1:4]
            rows.append([item] + values)

# Buat dataframe tabular
cleaned_df = pd.DataFrame(rows, columns=["Item", "2024", "2023", "2022"])

# Simpan ulang
cleaned_df.to_csv("src/ingestion/item8-appl/parsed_statements_op.csv", index=False)
# cleaned_df.to_sql("parsed_statements_op", sqlite_conn, if_exists='replace', index=False)
