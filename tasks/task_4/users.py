# users_cleaning.py
import re
import pandas as pd

def normalize_phone_series(s):
    s = s.astype(str).str.replace(r'\D', '', regex=True)
    return s.apply(lambda x: x[0:3] + '-' + x[3:6] + '-' + x[6:10])

def normalize_email_series(s):
    return s.astype(str).str.strip().str.lower().replace(r"^\s*$", pd.NA, regex=True)

def normalize_address_series(s):
    return s.astype(str).str.strip().replace(r"^\s*$", pd.NA, regex=True)

def clean_users_df(users_raw_df):
    df = users_raw_df.copy()
    if "phone" in df.columns: df["phone_norm"] = normalize_phone_series(df["phone"])
    if "email" in df.columns: df["email_norm"] = normalize_email_series(df["email"])
    if "address" in df.columns: df["address"] = normalize_address_series(df["address"])
    return df
