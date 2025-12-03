import pandas as pd


def realy_real_users( users_df, id_col: str = "id", matches: list | None = None):
    if matches is None: matches = ["name", "phone_norm", "email_norm"]
    user_ids = users_df[id_col].tolist()
    parent = {uid: uid for uid in user_ids}
    
    def find(x):
        if parent[x] != x: parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        root_a = find(a)
        root_b = find(b)
        if root_a != root_b: parent[root_b] = root_a

    for i in matches:
        if i not in users_df.columns:continue
        non_null = users_df[users_df[i].notna()]
        groups = non_null.groupby(i)[id_col].apply(list)
        for j in groups:
            if len(j) < 2: continue
            first = j[0]
            for other in j[1:]: union(first, other)

    root_by_user = {uid: find(uid) for uid in user_ids}
    unique_roots = sorted(set(root_by_user.values()))
    root_to_real = {root: idx for idx, root in enumerate(unique_roots)}
    user_to_real = { uid: root_to_real[root_by_user[uid]] for uid in user_ids }

    users_df = users_df.copy()
    users_df["real_user_id"] = users_df[id_col].map(user_to_real)
    n_real_users = users_df["real_user_id"].nunique()
    return users_df, n_real_users, user_to_real

def user_id_in_orders( orders_df, user_to_real: dict, id_col: str = "user_id", real_user_col: str = "real_user_id"):
    mapping_df = pd.DataFrame(list(user_to_real.items()), columns=[id_col, real_user_col])
    merged = orders_df.merge(mapping_df, on=id_col, how="left")
    return merged

def best_buyer_metrics(
    orders_df, users_df, real_col: str = "real_user_id", paid_col: str = "paid_price", users_id_col: str = "id"):
    spending = orders_df.groupby(real_col)[paid_col].sum()
    best_real_user_id = spending.idxmax()
    best_total_spent = float(spending.loc[best_real_user_id])
    best_user_ids =users_df[users_df[real_col] == best_real_user_id][users_id_col].tolist()
    return best_real_user_id, best_total_spent, best_user_ids
