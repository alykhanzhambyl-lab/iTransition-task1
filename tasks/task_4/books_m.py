import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

def ext_date(orders_df, ts = "timestamp", orders_dt = "date"):
    orders_df[orders_dt] = orders_df[ts].dt.date
    return orders_df

def any_price_to_usd(orders_df, orders_unit_price_norm = "unit_price_norm", num_price="unit_price_num", cur_price = "unit_price_currency", in_usd = "unit_price_usd"):
    prices = orders_df[orders_unit_price_norm].astype(str).str.strip()
    ext_num_curr = prices.str.extract(r'(\d+(?:\.\d+)?)\s*([$€])')
    orders_df[num_price] = ext_num_curr[0].astype(float).round(2)
    orders_df[cur_price] = ext_num_curr[1]
    orders_df[in_usd] = np.where( orders_df[cur_price] == "€", orders_df[num_price] * 1.2, orders_df[num_price])
    return orders_df

def paid_price_func(orders_df, in_usd = "unit_price_usd", paid_price_col = "paid_price", quant = "quantity"):
    orders_df[paid_price_col] = orders_df[in_usd] * orders_df[quant]
    return orders_df

def top5_days(orders_df, paid = "paid_price", ord_date = "date"):
    # orders_df.groupby(ord_date)[paid]
    # top_5 = heapq.nlargest(5, orders_df.groupby(ord_date)[paid].sum())
    # return print(top_5)
    daily = orders_df.groupby(ord_date)[paid].sum()
    top5 = daily.nlargest(5)
    res = [{day: round(float(total), 3) for day, total in top5.items()}]
    return res