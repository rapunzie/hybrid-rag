import re
import sqlite3
import pandas as pd

class FinancialsDB:
    def __init__(self, db_path):
        self.db_path = db_path

    def query(self, sql, params=None):
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(sql, conn, params=params or {})

    def get_table_data(self, table_name, company=None, fy=None, column=None):
        if column:
            sql = f"SELECT company, fy, {column} FROM {table_name} WHERE 1=1"
        else:
            sql = f"SELECT * FROM {table_name} WHERE 1=1"
        params = {}
        # if company:
        #     sql += " AND (LOWER(company) = :company OR LOWER(alias) = :company)"
        #     params["company"] = company.lower()
        if fy:
            sql += " AND fy = :fy"
            params["fy"] = fy
        return self.query(sql, params)


class StructuredRetriever:
    def __init__(self, db_path):
        self.db = FinancialsDB(db_path)

        # Keyword ke tabel + kolom langsung
        self.column_map = {
            "assets": ("balance_sheets", "total_assets"),
            "liabilities": ("balance_sheets", "total_liabilities"),
            "equity": ("balance_sheets", "total_equity"),
            "revenue": ("income_statements", "total_revenue"),
            "net income": ("income_statements", "net_income"),
            "cost of sales": ("income_statements", "cost_of_sales"),
            "gross profit": ("income_statements", "gross_profit"),
            "gross profits": ("income_statements", "gross_profit"),
            "gross-profit": ("income_statements", "gross_profit"),
            "basic eps": ("income_statements", "basic"),
            "diluted eps": ("income_statements", "diluted"),
            "earnings per share": ("income_statements", "eps"),
            "operating income": ("income_statements", "op_income"),
            "basic": ("income_statements", "basic"),
            "diluted": ("income_statements", "diluted"),
            "cash from operating": ("cash_flows", "cash_from_ops"),
            "cash from investing": ("cash_flows", "cash_from_investing"),
            "cash from financing": ("cash_flows", "cash_from_financing"),
            "ending cash": ("cash_flows", "ending_cash")
        }

    def extract_company(self, question):
        match = re.search(r"\b(apple|microsoft|tesla|alphabet|google|procter&gamble|p&g)\b", question, re.I)
        if not match:
            return None
        company = match.group(1).lower()
        alias_map = {
            "google": "alphabet",
            "p&g": "procter&gamble"
        }
        return alias_map.get(company, company)

    def extract_year(self, question):
        match = re.search(r"(20\d{2})", question)
        return int(match.group(1)) if match else None

    def detect_table_and_column(self, question):
        q = re.sub(r"[^\w\s]", " ", question.lower())  
        q = re.sub(r"\s+", " ", q)  
        for keyword, (table, column) in self.column_map.items():
            pattern = r"\b" + re.escape(keyword) + r"s?\b" 
            if re.search(pattern, q):
                return table, column
        return None, None

    def retrieve(self, query, raw_sql=False):
        if raw_sql:
            return self.db.query(query).to_string(index=False)

        company = self.extract_company(query)
        fy = self.extract_year(query)
        table, column = self.detect_table_and_column(query)

        if not table:
            return f"Tidak bisa menentukan tabel dari pertanyaan: '{query}'"

        df = self.db.get_table_data(table, company, fy, column)
        if df.empty:
            return f"Data tidak ditemukan untuk {company or 'perusahaan'} {fy or 'tahun'} di tabel {table}"

        # change null to 'not available'
        df = df.fillna("Not available")
        return df.to_string(index=False)
