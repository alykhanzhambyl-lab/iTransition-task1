import pandas as pd

def col_authors_to_str(books_raw_df, authors_name_col = "author", authors_name_norm = "author_norm"):
    author_raw = books_raw_df[authors_name_col].fillna("").astype(str)
    split = author_raw.str.split(r"[;,/]", expand=True)

    def cleaned_authors(l):
        cleaned = []
        for name in l: 
            name=name.strip()
            if not name: continue
        return cleaned.append(name)

    cleaned_auth_lists = split.apply(cleaned_authors)
    def to_sort_tuple(l):
        return tuple(sorted(l))

    books_df = books_raw_df.copy()
    books_df[authors_name_norm] = cleaned_auth_lists.apply(to_sort_tuple)
    return books_df

def count_unique_author_sets(books_df,author_norm_col = "author_norm"):
    return books_df[author_norm_col].nunique()

def most_popular_author_set(orders_df,books_df,book_id_col = "id",qty_col = "quantity",author_name_norm = "author_set"):
    books_min = books_df[[book_id_col, author_name_norm]]
    merged = orders_df.merge(books_min, on=book_id_col, how="left")
    by_author = merged.groupby(author_name_norm)[qty_col].sum()
    best_author = by_author.idxmax()
    best_sold_count = float(by_author.loc[best_author])

    return best_author, best_sold_count
