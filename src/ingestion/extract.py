# import os
# import re
# import json
# import requests
# from bs4 import BeautifulSoup
# from tqdm import tqdm


# # Load URLs dari file
# def load_urls(file_path):
#     with open(file_path, "r") as f:
#         return [line.strip() for line in f if line.strip()]

# # Ekstrak metadata dari URL
# def extract_metadata_from_url(url):
#     cik_search = re.search(r'data/(\d+)/', url)
#     year_search = re.search(r'(\d{8})\.htm', url)

#     company_map = {
#         "320193": "Apple",
#         "789019": "Microsoft",
#         "1318605": "Tesla",
#         "732712": "P&G",
#         "1652044": "Alphabet"
#     }

#     cik = cik_search.group(1) if cik_search else "Unknown"
#     company = company_map.get(cik, "Unknown")
#     year = int("20" + year_search.group(1)[:2]) if year_search else None
#     return company, cik, year

# # Ekstrak bagian penting dari text HTML
# def extract_sections(text):
#     section_titles = ["Item 1", "Item 1A", "Item 5", "Item 7", "Item 7A", "Item 8"]
#     sections = {}

#     # Bersihkan dulu text dari karakter aneh
#     text = text.replace('\xa0', ' ').replace('\u200a', ' ')
#     pattern = r"(Item\s+\d+[A-Z]?)\s*[\.:–-]?\s*(.*?)\s*(?=\nItem\s+\d+[A-Z]?[\.:–-]?|\Z)"
#     matches = list(re.finditer(pattern, text, flags=re.IGNORECASE | re.DOTALL))

#     for match in matches:
#         title, content = match.group(1).strip(), match.group(2).strip()
#         normalized_title = title.lower().replace('\n', ' ')
#         for desired in section_titles:
#             if desired.lower() in normalized_title:
#                 sections[desired] = content
#     return sections

# # Scraping dan parsing per URL
# def parse_filing(url):
#     headers = {"User-Agent": "Mozilla/5.0"}
#     response = requests.get(url, headers=headers, timeout=30)

#     if response.status_code != 200:
#         print(f"❌ Failed to fetch: {url}")
#         return None

#     soup = BeautifulSoup(response.text, "lxml")
#     text = soup.get_text(separator="\n")
#     company, cik, year = extract_metadata_from_url(url)
#     sections = extract_sections(text)

#     if not sections:
#         print(f"⚠️ No sections extracted from {url}")
#         return None

#     return {
#         "company": company,
#         "cik": cik,
#         "year": year,
#         "filing_url": url,
#         "sections": sections
#     }

# # Main loop
# def main():
#     urls = load_urls("src/ingestion/filing_urls.txt")
#     output_path = "src/ingestion/parsed_filings.jsonl"

#     with open(output_path, "w", encoding="utf-8") as fout:
#         for url in tqdm(urls, desc="Processing 10-K filings"):
#             try:
#                 result = parse_filing(url)
#                 if result:
#                     fout.write(json.dumps(result, ensure_ascii=False) + "\n")
#             except Exception as e:
#                 print(f"❌ Exception for {url}: {e}")

# if __name__ == "__main__":
#     main()

# print(f"🔍 Fetching: {url}")
# response = requests.get(url, headers=headers, timeout=30)
# print(f"✅ Status: {response.status_code}")


import requests
from bs4 import BeautifulSoup
import re

# URL 10-K Apple 2023
# from sec_api import ExtractorApi

# extractor = ExtractorApi("04b330d7905866e9ab92b088fcb2f8f7b721046ed12421a96c9013cfbf97d678")
# url = "https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm"
# item7 = extractor.get_section(url, "7", "text")
# print(item7[:16100])

from sec_api import ExtractorApi
import json

# API
extractor = ExtractorApi("04b330d7905866e9ab92b088fcb2f8f7b721046ed12421a96c9013cfbf97d678")

# URL 10-K Apple
url = "https://www.sec.gov/ix?doc=/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm"

# extract item
item7a_text = extractor.get_section(url, "7A", "text")

# save to .jsonl
with open("item7a.jsonl", "w", encoding="utf-8") as f:
    json_line = json.dumps({"company": "Apple", "item": "7a", "section": "Quantitative and Qualitative Disclosures About Market Risk", "text": item7a_text})
    f.write(json_line + "\n")
