import re
import sqlite3
import pandas as pd

class FinancialsDB:
    def __init__(self, db_path):
        self.db_path = db_path

    def query(self, sql, params=None):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(sql, conn, params=params or {})

    def get_table_data(self, table_name, company=None, fy=None):
        sql = f"SELECT * FROM {table_name} WHERE 1=1"
        params = {}
        if company:
            sql += " AND company = :company"
            params["company"] = company.lower()
        if fy:
            sql += " AND fy = :fy"
            params["fy"] = fy
        return self.query(sql, params)

# Structured Retriever
class StructuredRetriever:
    def __init__(self, db_path):
        self.db = FinancialsDB(db_path)

        # mapping kata kunci → tabel
        self.table_map = {
            "assets": "balance_sheets",
            "liabilities": "balance_sheets",
            "equity": "balance_sheets",
            "revenue": "income_statement",
            "net income": "income_statement",
            "cost of sales": "income_statement",
            "gross margin": "income_statement",
            "operating income": "income_statement",
            "eps": "income_statement",
            "cash": "cash_flows",
            "investing": "cash_flows",
            "financing": "cash_flows"
        }

    def extract_company(self, question):
        match = re.search(r"\b(apple|microsoft|tesla|alphabet|p&g)\b", question, re.I)
        return match.group(1).lower() if match else None

    def extract_years(self, question):
        years = re.findall(r"(20\d{2})", question)
        return [int(y) for y in years] if years else []

    def detect_table(self, question):
        for keyword, table in self.table_map.items():
            if keyword in question.lower():
                return table
        return None

    def retrieve(self, query, raw_sql=False):
        if raw_sql:
            return self.db.query(query)

        # Ambil parameter dari pertanyaan
        company = self.extract_company(query)
        years = self.extract_years(query)
        table = self.detect_table(query)

        if not table:
            return f"Tidak bisa menentukan tabel dari pertanyaan: '{query}'"

        dfs = []
        if years:
            for fy in years:
                df_year = self.db.get_table_data(table, company, fy)
                if not df_year.empty:
                    dfs.append(df_year)
        else:
            df_all = self.db.get_table_data(table, company)
            if not df_all.empty:
                dfs.append(df_all)

        if not dfs:
            return f"Data tidak ditemukan untuk {company or 'perusahaan'} {years or 'tahun'} di tabel {table}"

        return pd.concat(dfs, ignore_index=True)
