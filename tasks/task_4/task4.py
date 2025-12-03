import pandas as pd
import yaml, re
from pathlib import Path
import matplotlib.pyplot as plt
# from datetime import datetime
# from dateutil import parser
from cleaning.orders import clean_orders_df
from cleaning.users import clean_users_df
from reviews.books_m import ext_date, any_price_to_usd, paid_price_func, top5_days
from reviews.users_real_best_m import realy_real_users, user_id_in_orders, best_buyer_metrics, plot_daily_revenue
from reviews.authors_rev_best_m import col_authors_to_str, count_unique_author_sets, most_popular_author_set
import json


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

    best_real_user_id, best_total_spent, best_user_ids = best_buyer_metrics(orders_df,users_df, real_col="real_user_id",paid_col="paid_price",users_id_col="id")
    best_users_rows = users_df[users_df["id"].isin(best_user_ids)]
    name_col = "name_norm" if "name_norm" in best_users_rows.columns else "name"
    best_buyer_name =(
        best_users_rows[name_col].dropna().astype(str).iloc[0]
        if not best_users_rows.empty
        else None
    )

    # все варианты имён по алиасам
    best_buyer_all_names = best_users_rows[name_col].dropna().astype(str).unique().tolist()
    
    books_df = col_authors_to_str(books_raw_df,authors_name_col=":author",authors_name_norm="author_norm")
    books_df = books_df.rename(columns={":id": "id"})

    n_author = count_unique_author_sets(books_df,author_norm_col="author_norm")

    best_author_set, best_sold_count = most_popular_author_set(
        orders_df,books_df,order_book_id_col="book_id",
        book_id_col="id",qty_col="quantity",author_norm_col="author_norm")
    
    daily_revenue_df = plot_daily_revenue(orders_df,date_col="date",paid_col="paid_price",title=f"Daily revenue ({label})",ret_df=True)

    metrics = {
        "label": label,
        "top5_days": top5,
        "n_real_users": int(n_real_users),
        "best_buyer_id": best_user_ids,
        "best_buyer_name": best_buyer_name,
        "best_buyer_all_names": best_buyer_all_names,
        "best_buyer_total_spent": best_total_spent,
        "n_author_sets": int(n_author),
        "best_author": best_author_set,
        "best_author_set_sold": best_sold_count
    }

    return orders_df, users_df, books_df, daily_revenue_df, metrics

def print_metrics(m: dict):
    print("\nResults:", m["label"], "\n")
    print("Top 5 days by revenue:")
    for d, rev in m["top5_days"][0].items():
        print(f"   • {d.strftime('%Y-%m-%d')}: {rev:.2f} USD")
    print(f"\nNumber of real users: {m['n_real_users']}")
    print(f"\nNumber of unique author:  {m['n_author_sets']}")
    print("\nThe most popular set of authors:")
    print("   ", ", ".join(m["best_author"]))
    print(f"\nRevenue for this author: {m['best_author_set_sold']}")
    print("\nBest buyer:")
    print(f"   user_ids: {m['best_buyer_id']}")
    print(f"   total money spent: {m['best_buyer_total_spent']}\n")
    if m.get("best_buyer_name"):
        print(f"   name: {m['best_buyer_name']}")
    if m.get("best_buyer_all_names"):
        print(f"   all names: {m['best_buyer_all_names']}")
    

def run_for_datasets(label: str, base_dir = r"C:\iTransition\tasks\task_4\data", dashboard_dir = Path):
    dashboard_dir = Path("dashboard")
    data_dir = Path(base_dir) / label
    books_path = data_dir / "books.yaml"
    users_path = data_dir / "users.csv"
    orders_path = data_dir / "orders.parquet"

    print(f"\nобработка {label} ===")
    print("books_path: ", books_path)
    print("users_path: ", users_path)
    print("orders_path:", orders_path)

    with open(books_path, encoding="utf-8") as f:
        data_books = yaml.safe_load(f)
    users_raw_df = pd.read_csv(users_path, na_values=["NULL", "null", ""])
    orders_raw_df = pd.read_parquet(orders_path)
    books_raw_df = pd.DataFrame(data_books)

    orders_df, users_df, books_df, daily_rev_df, metrics = run(orders_raw_df,users_raw_df,books_raw_df,label=label)
    print_metrics(metrics)

    top5_list = []
    for d, v in metrics["top5_days"][0].items():
        top5_list.append({
            "date": d.strftime("%Y-%m-%d"),
            "revenue": float(v),
        })
    metrics_for_json = {
        "label": metrics["label"],
        "top5_days": top5_list,
        "n_real_users": metrics["n_real_users"],
        "n_author_sets": metrics["n_author_sets"],
        "best_author": list(metrics["best_author"]),
        "best_author_set_sold": metrics["best_author_set_sold"],
        "best_buyer_id": metrics["best_buyer_id"],
        "best_buyer_total_spent": metrics["best_buyer_total_spent"],
        "best_buyer_name": metrics["best_buyer_name"],
        "best_buyer_all_names": metrics["best_buyer_all_names"],
    }

    dashboard_dir.mkdir(exist_ok=True)
    with open(dashboard_dir / f"metrics_{label}.json", "w", encoding="utf-8") as f:
        json.dump(metrics_for_json, f, ensure_ascii=False, indent=2)
    daily_rev_df = daily_rev_df.copy()
    daily_rev_df["date"] = daily_rev_df["date"].astype(str)
    daily_rev_df.to_json(dashboard_dir / f"daily_revenue_{label}.json",orient="records",force_ascii=False,indent=2)

    return orders_df, users_df, books_df, metrics

def main():
    dashboard_dir = Path("dashboard")
    dashboard_dir.mkdir(exist_ok=True)
    datasets = ["DATA1", "DATA2", "DATA3"]
    for label in datasets:run_for_datasets(label, dashboard_dir=dashboard_dir)


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

#def run(orders_raw_df, users_raw_df, books_raw_df, label = "DATA1"):
#     orders_df = clean_orders_df(orders_raw_df)
#     orders_df = ext_date(orders_df)          
#     orders_df = any_price_to_usd(orders_df)  
#     orders_df = paid_price_func(orders_df)   
#     top5 = top5_days(orders_df)

#     users_df = clean_users_df(users_raw_df)
#     users_df, n_real_users, user_to_real = realy_real_users(users_df, id_col="id")
#     orders_df = user_id_in_orders(orders_df,user_to_real=user_to_real,id_col="user_id",real_user_col="real_user_id",)

#     best_real_user_id, best_total_spent, best_user_ids = best_buyer_metrics(orders_df,users_df, real_col="real_user_id",paid_col="paid_price",users_id_col="id")
#     best_users_rows = users_df[users_df["id"].isin(best_user_ids)]
#     name_col = "name_norm" if "name_norm" in best_users_rows.columns else "name"
#     best_buyer_name =(best_users_rows[name_col].dropna().astype(str).iloc[0]
#     if not best_users_rows.empty
#         else None
#     )

#     # все варианты имён по алиасам
#     best_buyer_all_names = best_users_rows[name_col].dropna().astype(str).unique().tolist()
    
#     books_df = col_authors_to_str(books_raw_df,authors_name_col=":author",authors_name_norm="author_norm")
#     books_df = books_df.rename(columns={":id": "id"})

#     n_author = count_unique_author_sets(books_df,author_norm_col="author_norm")

#     best_author_set, best_sold_count = most_popular_author_set(
#         orders_df,books_df,order_book_id_col="book_id",
#         book_id_col="id",qty_col="quantity",author_norm_col="author_norm")
    
#     daily_revenue = plot_daily_revenue(orders_df,date_col="date",paid_col="paid_price",title=f"Daily revenue ({label})")

#     metrics = {
#         "label": label,
#         "top5_days": top5,
#         "n_real_users": int(n_real_users),
#         "best_buyer_id": best_user_ids,
#         "best_buyer_name": best_buyer_name,
#         "best_buyer_all_names": best_buyer_all_names,
#         "best_buyer_total_spent": best_total_spent,
#         "n_author_sets": int(n_author),
#         "best_author": best_author_set,
#         "best_author_set_sold": best_sold_count
#     }

#     return orders_df, users_df, books_df, metrics

# def main():
#     books_path = r"C:\iTransition\tasks\task_4\data\DATA3\books.yaml"
#     with open(books_path ,encoding = "utf-8") as f:
#         data_books = yaml.safe_load(f)

#     users_raw_df = pd.read_csv(r"C:\iTransition\tasks\task_4\data\DATA3\users.csv", na_values=["NULL", "null", ""])
#     orders_raw_df = pd.read_parquet(r"C:\iTransition\tasks\task_4\data\DATA3\orders.parquet")
#     books_raw_df = pd.DataFrame(data_books)

#     # print(books_raw_df.columns.tolist())
#     # print(books_raw_df.head())


#     order_1_data, users_1_data, books_1_data, metric_1 = run(orders_raw_df, users_raw_df, books_raw_df, label="DATA3")
#     def print_metrics(m: dict):
#         print("\nРезультаты:", m["label"], "\n")
#         print("Топ-5 дней по выручке:")
#         for d, rev in m["top5_days"][0].items():
#             print(f"   • {d.strftime('%Y-%m-%d')}: {rev:.2f} USD")
#         print(f"\nКоличество реальных пользователей: {m['n_real_users']}")
#         print(f"\nКоличество уникальных сетов авторов: {m['n_author_sets']}")
#         print("\nСамый популярный набор авторов:")
#         print("   ", ", ".join(m["best_author"]))
#         print(f"\nВыручка по этому автору: {m['best_author_set_sold']}")
#         print("\nЛучший покупатель:")
#         print(f"   user_ids: {m['best_buyer_id']}")
#         print(f"   total spent: {m['best_buyer_total_spent']}\n")
#         if m.get("best_buyer_name"):
#             print(f"   main name: {m['best_buyer_name']}")
#         if m.get("best_buyer_all_names"):
#             print(f"   all names: {m['best_buyer_all_names']}")
    
#     print_metrics(metric_1)



# if __name__ == "__main__":
#     main()
