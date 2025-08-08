import os
import requests
from dotenv import load_dotenv

load_dotenv()
SEC_API_KEY = os.getenv("SEC_API_KEY")

# EXTRACTOR_URL = "https://api.sec-api.io/extractor"

# def get_section(company_ticker, year, form_type="10-K", section="1"):
#     base_url = "https://sec-api.com/api/section"
#     params = {
#         "section": section,
#         "formType": form_type,
#         "ticker": company_ticker,
#         "year": year,
#         "token": SEC_API_KEY
#     }

#     response = requests.get(base_url, params=params)
    
#     # Debug
#     print("Status Code:", response.status_code)
#     print("Response Text (first 300):", response.text[:300])
    
#     if response.status_code == 200:
#         try:
#             return response.json()
#         except Exception as e:
#             print("❌ JSON decode error:", e)
#             return None
#     else:
#         print("❌ Request failed:", response.status_code)
#         return None

# def save_text(data, filename):
#     os.makedirs("data/raw/narrative", exist_ok=True)
#     with open(f"data/raw/narrative/{filename}.txt", "w", encoding="utf-8") as f:
#         f.write(data.get("text", ""))

# if __name__ == "__main__":
#     company = "AAPL"     # Apple Inc
#     year = "2022"
#     section = "1"        # Item 1: Business

#     data = get_section(company, year, section)
#     if data:
#         save_text(data, f"{company}_{year}_section{section}")
#         print("Saved success:", f"{company}_{year}_section{section}.txt")


from sec_api import RenderApi

renderApi = RenderApi(api_key="SEC_API_KEY")

def download_filing(url):
  try:
    filing = renderApi.get_filing(url)
    # file_name example: 000156459019027952-msft-10k_20190630.htm
    file_name = url.split("/")[-2] + "-" + url.split("/")[-1] 
    download_to = "./filings/" + file_name
    with open(download_to, "w") as f:
      f.write(filing)
  except Exception as e:
    print("Problem with {url}".format(url=url))
    print(e)

# load URLs from log file
def load_urls():
  log_file = open("filing_urls.txt", "r")
  urls = log_file.read().split("\n") # convert long string of URLs into a list 
  log_file.close()
  return urls

import os
import multiprocessing

def download_all_filings():
  print("Start downloading all filings")

  download_folder = "./filings" 
  if not os.path.isdir(download_folder):
    os.makedirs(download_folder)
    
  # uncomment next line to process all URLs
  # urls = load_urls()
  urls = load_urls()[1:40]
  print("{length} filing URLs loaded".format(length=len(urls)))

  number_of_processes = 20

  with multiprocessing.Pool(number_of_processes) as pool:
    pool.map(download_filing, urls)
  
  print("All filings downloaded")