import pandas as pd
# и очистка и расчеты

def col_authors_to_str(books_raw_df: pd.DataFrame,authors_name_col: str = ":author", authors_name_norm: str = "author_norm"):
    author_raw = books_raw_df[authors_name_col].fillna("").astype(str)
    split = author_raw.str.split(r"[;,/]", expand=True)
    
    def cleaned_authors(row) -> list[str]:
        cleaned = []
        for name in row:
            if name is None or (isinstance(name, float) and pd.isna(name)):continue
            name = str(name).strip()
            if not name:continue
            cleaned.append(name)
        return cleaned 

    cleaned_auth_lists = split.apply(cleaned_authors, axis=1)
    def to_sort_tuple(lst):
        if not lst:
            return tuple()
        return tuple(sorted(set(lst)))

    books_df = books_raw_df.copy()
    books_df[authors_name_norm] = cleaned_auth_lists.apply(to_sort_tuple)
    return books_df

def count_unique_author_sets(books_df: pd.DataFrame,author_norm_col: str = "author_norm"):
    return books_df[author_norm_col].nunique()

def most_popular_author_set(orders_df,books_df,order_book_id_col = "book_id",book_id_col = "id",qty_col = "quantity",author_norm_col = "author_norm"):
    books_min = books_df[[book_id_col, author_norm_col]]
    merged = orders_df.merge(books_min,left_on=order_book_id_col,right_on=book_id_col,how="left")
    by_author = merged.groupby(author_norm_col, dropna=True)[qty_col].sum()
    if by_author.empty: return tuple(), 0.0

    best_author = by_author.idxmax()
    best_sold_count = float(by_author.max())
    return best_author, best_sold_count