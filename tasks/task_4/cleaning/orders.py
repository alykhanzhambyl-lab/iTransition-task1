import re
import pandas as pd
from timestamp import parse_timestamp
from patterns import pattrns

def cents(price):
    price = re.sub(r"(\d+)\s*¢\s*(\d+)", r"\1.\2", price)
    price = re.sub(r"(\d+)\s*[$€]\s*(\d+)\s*¢", r"\1.\2", price)
    return price
    

def currencies(price):
    price = price.upper()
    if "EUR" in price or "€" in price: currency = "€"
    elif "USD" in price or "$" in price: currency = "$"
    else: currency = "$"
    return currency


def delete_currency(price):
    price = re.sub(r"(?i)\b(?:USD|EUR)\b|[$€]", "", price).strip()
    return price


def number_extract(price):
    x = re.search(r"\d+(?:[.,]\d*)?", price)
    if not x: return None
    num = x.group(0).replace(",", ".")
    if num.endswith("."): num = num[:-1]
    return f"{num}"


def unit_price_norm(x):
    if pd.isna(x): return None
    price = str(x).strip()
    price = cents(price)
    currency = currencies(price)
    clean_price = delete_currency(price)
    num = number_extract(clean_price)
    if num is None:
        return None
    return f"{num} {currency}"


def shipping_norm(s):
    return s.astype(str).str.strip().str.lower().replace(r"^\s*$", pd.NA, regex=True)


def clean_orders_df(orders_raw_df):
    df = orders_raw_df.copy()
    if "timestamp" in df.columns:
        df["timestamp_raw"] = df["timestamp"].astype(str)
        df["timestamp"] = parse_timestamp(df["timestamp_raw"])
    if "unit_price" in df.columns: df["unit_price_norm"] = df["unit_price"].apply(unit_price_norm)
    if "shipping" in df.columns: df["shipping_norm"] = shipping_norm(df["shipping"])

    return df








# def cents(price):
#     # if pd.isna(x): return None
#     # price = str(x).strip()
#     price = re.sub(r"(\d+)\s*¢\s*(\d+)", r"\1.\2", price)
#     price = re.sub(r"(\d+)\s*[$€]\s*(\d+)\s*¢", r"\1.\2", price)
#     return price
    
# def currencies(price):
#     price = price.upper()
#     if "EUR" in price or "€" in price: currency = "€"
#     elif "USD" in price or "$" in price: currency = "$"
#     else: currency = "$"
#     return currency

# def delete_currency(price):
#     price = re.sub(r"(?i)\b(?:USD|EUR)\b|[$€]", "", price).strip()

# def number_extract(price):
#     x = re.search(r"\d+(?:[.,]\d*)?", price)
#     num = x.group(0).replace(",", ".")
#     if num.endswith("."):
#         num = num[:-1]
#     return f"{num}"

# def unit_price_norm(x):
#     if pd.isna(x): return None
#     price = str(x).strip()
#     currency = currencies(price)
#     num = number_extract(delete_currency(cents(price)))
#     return f"{num} {currency}"



# def shipping_norm(s):
#     return s.astype(str).str.strip().str.lower().replace(r"^\s*$", pd.NA, regex=True)

# def clean_orders_df(orders_raw_df):
#     df = orders_raw_df.copy()
#     if "timestamp" in df.columns:
#         df["timestamp_raw"] = df["timestamp"].astype(str)
#         df["timestamp"] = parse_timestamp(df["timestamp_raw"])
#     if "unit_price" in df.columns: df["unit_price_norm"] = df["unit_price"].apply(unit_price_norm)
#     if "shipping" in df.columns: df["shipping_norm"] = shipping_norm(df["shipping"])
#     return df



# if pd.isna(x): return None
#     price = str(x).strip()
#     price = cents(price)
#     currency = currencies(price)
#     del_cur_price = delete_currency(price)
#     num = number_extract(del_cur_price)
#     return f"{num} {currency}"