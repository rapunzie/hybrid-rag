import json
import html
import os

# Daftar nama file yang ingin dibersihkan
input_files = [
    "data/raw/narrative/items_2022.jsonl",
    "data/raw/narrative/items_2023.jsonl",
    "data/raw/narrative/items_2024.jsonl"
]

# Folder output
output_folder = "cleaned_jsonl"
os.makedirs(output_folder, exist_ok=True)

# Proses setiap file
for input_path in input_files:
    output_path = os.path.join(output_folder, os.path.basename(input_path).replace(".jsonl", "_cleaned.jsonl"))

    with open(input_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            if not line.strip():
                continue  # skip empty lines

            data = json.loads(line)

            if "text" in data:
                data["text"] = html.unescape(data["text"]).replace("\\n", "\n")

            json.dump(data, outfile, ensure_ascii=False)
            outfile.write("\n")

    print(f"✔ File cleaned: {output_path}")
