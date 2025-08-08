from sec_api import QueryApi
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env dari root folder
env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

query_api = QueryApi(api_key=os.getenv("SEC_API_KEY"))

# Company CIK mapping
companies = {
    "apple": "0000320193",
    "microsoft": "0000789019",
    "tesla": "0001318605",
    "pg": "0000080424",  # P&G
    "alphabet": "0001652044"
}

years = ["2022", "2023", "2024"]
filing_urls = []

for company_name, cik in companies.items():
    for year in years:
        query = {
            "query": {
                "query_string": {
                    "query": f"cik:{cik} AND formType:\"10-K\" AND filingDate:[{year}-01-01 TO {year}-12-31]"
                }
            },
            "from": "0",
            "size": "5",
            "sort": [{"filedAt": {"order": "desc"}}]
        }

        filings = query_api.get_filings(query)

        for filing in filings['filings']:
            url = filing['linkToFilingDetails']
            filing_urls.append(url)
            print(f"{company_name.upper()} {year} - {url}")

# Simpan ke txt di folder yang sama dengan script
output_file = Path(__file__).resolve().parent / "filing_urls.txt"
with open(output_file, "w") as f:
    f.write("\n".join(filing_urls))

print(f"✅ Total {len(filing_urls)} filings saved to {output_file}")




