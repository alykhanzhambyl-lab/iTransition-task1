import pandas as pd
import yaml, re
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser
from orders import clean_orders_df
from users import clean_users_df
from revenue_m import ext_date, any_price_to_usd


books_path = r"C:\iTransition\tasks\task_4\data\DATA1\books.yaml"
with open(books_path ,encoding = "utf-8") as f:
    data_books = yaml.safe_load(f)

users_raw_df = pd.read_csv(r"C:\iTransition\tasks\task_4\data\DATA1\users.csv", na_values=["NULL", "null", ""])
orders_raw_df = pd.read_parquet(r"C:\iTransition\tasks\task_4\data\DATA1\orders.parquet")
books_raw_df = pd.DataFrame(data_books)



def main():
    orders_df = clean_orders_df(orders_raw_df)
    orders_df = any_price_to_usd(orders_df)

    # users_df = clean_users_df(users_raw_df)
    # orders_df = any_price_to_dollar(orders_df)
    # orders_df = ext_date(orders_df)
    orders_df.to_csv("orders_clean.csv", index=False)
    # # users_df.to_csv("users_clean.csv", index=False)



if __name__ == "__main__":
    main()




























# def timestamp_str_normalizing(s):
#     s = s.astype(str).str.strip()
#     s = s.str.replace(r'\s*A\.M\.\s*', ' AM', regex=True, case=False)
#     s = s.str.replace(r'\s*P\.M\.\s*', ' PM', regex=True, case=False)
#     s = s.str.replace(r'\s+', ' ', regex=True)

#     return s

# def parse_timestamps(raw):
#     s = timestamp_str_normalizing(raw)
#     result = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")
#     for pattern, fmt in date_patterns:
#         mask = s.str.match(pattern)
#         if not mask.any(): continue
#         result.loc[mask] = pd.to_datetime(s.loc[mask], format=fmt, errors="coerce")
#     return result

# orders_raw_df["timestamp_raw"] = orders_raw_df["timestamp"].astype(str)
# orders_raw_df["timestamp_parsed"] = pd.to_datetime( orders_raw_df["timestamp_raw"],errors="coerce")
# mask_bad = orders_raw_df["timestamp_parsed"].isna()
# extra_parsed = parse_timestamps(orders_raw_df.loc[mask_bad, "timestamp_raw"])
# orders_raw_df.loc[mask_bad, "timestamp_parsed"] = extra_parsed

# print(orders_raw_df["timestamp"].head(50))

# def unit_price_normalizing(x):
#     if pd.isna(x): return None
#     price = str(x).strip()
#     price = re.sub(r"(\d+)\s*¢\s*(\d+)", r"\1.\2", price)
#     price = re.sub(r"(\d+)\s*[$€]\s*(\d+)\s*¢", r"\1.\2", price)
    
#     price = price.upper()
#     if "EUR" in price or "€" in price: currency = "€"
#     elif "USD" in price or "$" in price: currency = "$"
#     else: currency = "$"
    
#     price = re.sub(r"(?i)\b(?:USD|EUR)\b|[$€]", "", price).strip()
#     s = re.search(r"\d+(?:[.,]\d*)?", price)
#     num = s.group(0).replace(",", ".")
#     if num.endswith("."):
#         num = num[:-1]

#     return f"{num} {currency}"

# orders_raw_df["unit_price"] = orders_raw_df["unit_price"].apply(unit_price_normalizing)
# # def date_time_normilizing(x):
# #     retrun None


# orders_raw_df["timestamp"] = pd.to_datetime(
#     orders_raw_df["timestamp"],
#     errors = "coerce",
    
#     infer_datetime_format = True
# )

# print(orders_raw_df["timestamp"])


# print(orders_raw_df["unit_price"].head(20))

# orders_raw_df["unit_price"] = orders_raw_df["unit_price"].replace(["NULL", ""], pd.NA)
# print(orders_raw_df["unit_price"].isna().sum())





# orders_df.to_csv("orders_preview.csv", index=False)

# ниже строка кода для обработки номера телефона 
# users_raw_df["phone"] = users_raw_df["phone"].astype(str).str.replace(r'\D', '', regex=True).apply(lambda x: x[0:3]+'-'+x[3:6]+'-'+x[6:10])


# print(users_raw_df["phone"].head(20))

# print(users_raw_df.info())
# print(orders_raw_df.info())
# print(books_raw_df.info())


# print(users_raw_df.isnull().sum())
# print(orders_raw_df.isnull().sum())
# print(books_raw_df.isnull().sum())

# orders_raw_df["timestamp_raw"] = orders_raw_df["timestamp"].astype(str)
# orders_raw_df["timestamp_parsed"] = pd.to_datetime(
#     orders_raw_df["timestamp_raw"],
#     errors="coerce",
#     infer_datetime_format=True,
# )
# mask_bad = orders_raw_df["timestamp_parsed"].isna()

# bad_ts_unique = (
#     orders_raw_df.loc[mask_bad, "timestamp_raw"]
#     .dropna()
#     .astype(str)
#     .unique()
# )

# for x in bad_ts_unique[:50]:
#     print(repr(x))