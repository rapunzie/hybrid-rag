import glob

# files
input_files = [
    "item1.jsonl",
    "item1a.jsonl",
    "item5.jsonl",
    "item7.jsonl",
    "item7a.jsonl"
]

output_file = "merged_items_2022.jsonl"

# merged
with open(output_file, "w", encoding="utf-8") as outfile:
    for file in input_files:
        with open(file, "r", encoding="utf-8") as infile:
            for line in infile:
                outfile.write(line.strip() + "\n") 
