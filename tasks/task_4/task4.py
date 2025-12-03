import pandas as pd
import yaml, re
from pathlib import Path
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser
from cleaning.orders import clean_orders_df
from cleaning.users import clean_users_df
from books_m import ext_date, any_price_to_usd, paid_price_func, top5_days
from users_real_best_m import realy_real_users, user_id_in_orders, best_buyer_metrics, plot_daily_revenue
from authors_rev_best_m import col_authors_to_str, count_unique_author_sets, most_popular_author_set


# from processing import process_orders

# books_path = r"C:\iTransition\tasks\task_4\data\DATA1\books.yaml"
# with open(books_path ,encoding = "utf-8") as f:
#     data_books = yaml.safe_load(f)

# users_raw_df = pd.read_csv(r"C:\iTransition\tasks\task_4\data\DATA1\users.csv", na_values=["NULL", "null", ""])
# orders_raw_df = pd.read_parquet(r"C:\iTransition\tasks\task_4\data\DATA1\orders.parquet")
# books_raw_df = pd.DataFrame(data_books)


def run(orders_raw_df, users_raw_df, books_raw_df, label = "DATA1"):
    orders_df = clean_orders_df(orders_raw_df)
    orders_df = ext_date(orders_df)          
    orders_df = any_price_to_usd(orders_df)  
    orders_df = paid_price_func(orders_df)   
    top5 = top5_days(orders_df)

    users_df = clean_users_df(users_raw_df)
    users_df, n_real_users, user_to_real = realy_real_users(users_df, id_col="id")
    orders_df = user_id_in_orders(orders_df,user_to_real=user_to_real,id_col="user_id",real_user_col="real_user_id",)

    best_real_user_id, best_total_spent, best_user_ids = best_buyer_metrics(orders_df,users_df, real_col="real_user_id",paid_col="paid_price",users_id_col="id",)
    books_df = col_authors_to_str(books_raw_df,authors_name_col="author",authors_name_norm="author_norm")

    n_author = count_unique_author_sets(books_df,author_norm_col="author_norm")

    best_author_set, best_sold_count = most_popular_author_set(
        orders_df,
        books_df,
        book_id_col="book_id",
        qty_col="quantity",
        author_set_col="author_set",       
    )
    plot_daily_revenue(
        orders_df,
        date_col="date",
        paid_col="paid_price",
        title=f"Daily revenue ({label})",
    )

    metrics = {
        "label": label,
        "top5_days": top5,
        "n_real_users": int(n_real_users),
        "best_buyer_id": best_user_ids,
        "best_buyer_total_spent": best_total_spent,
        "n_author_sets": int(n_author),
        "best_author": best_author_set,
        "best_author_set_sold": best_sold_count
    }

    return orders_df, users_df, books_df, metrics

def main():
    books_path = r"C:\iTransition\tasks\task_4\data\DATA1\books.yaml"
    with open(books_path ,encoding = "utf-8") as f:
        data_books = yaml.safe_load(f)

    users_raw_df = pd.read_csv(r"C:\iTransition\tasks\task_4\data\DATA1\users.csv", na_values=["NULL", "null", ""])
    orders_raw_df = pd.read_parquet(r"C:\iTransition\tasks\task_4\data\DATA1\orders.parquet")
    books_raw_df = pd.DataFrame(data_books)

    order_1_data, users_1_data, books_1_data, metric_1 = run(orders_raw_df, users_raw_df, books_raw_df, label="DATA1")
    print(metric_1)


if __name__ == "__main__":
    main()
    












    

 # orders_df = ext_date(orders_df)
    # orders_df = any_price_to_usd(orders_df)
    # orders_df = paid_price_func(orders_df)
    # top5_days(orders_df)
    

    # orders_df = paid_price_func(orders_df)

    # # users_df = clean_users_df(users_raw_df)
    # # orders_df = any_price_to_dollar(orders_df)
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