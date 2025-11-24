import csv
from pathlib import Path
from pprint import pprint
from datetime import datetime, timedelta
from collections import defaultdict

def convert_type_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def row_to_dict(row):
    return {
        "date": row[0],
        "department": row[1],
        "value": row[2],
        "beneficiary": row[3],
        "status": "MISSING"
    }

def reconcile_accounts(transactions1, transactions2):
    # Converter listas em dicionários
    t1 = [row_to_dict(r) for r in transactions1]
    t2 = [row_to_dict(r) for r in transactions2]

    # Para cada transação da lista 1
    for row1 in t1:
        date1 = convert_type_date(row1["date"])

        # Datas: -1 dia, mesma, +1 dia
        possible_dates = [
            (date1 - timedelta(days=1)).strftime("%Y-%m-%d"),
            row1["date"],
            (date1 + timedelta(days=1)).strftime("%Y-%m-%d")
        ]

        # Procurar um match na lista 2
        for row2 in t2:
            if row2["status"] == "FOUND":
                continue 

            same_date = row2["date"] in possible_dates
            same_dep = row2["department"] == row1["department"]
            same_val = row2["value"] == row1["value"]
            same_ben = row2["beneficiary"] == row1["beneficiary"]

            if same_date and same_dep and same_val and same_ben:
                row1["status"] = "FOUND"
                row2["status"] = "FOUND"
                break 

    return t1, t2


if __name__ == "__main__":
    transactions1 = list(csv.reader(Path('transactions1.csv').open()))
    transactions2 = list(csv.reader(Path('transactions2.csv').open()))
    out1, out2 = reconcile_accounts(transactions1, transactions2)
    pprint(out1)
    pprint(out2)