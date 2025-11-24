import json
import re
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "task1_d.json"
DB_PATH = BASE_DIR / "task1.db"

def extract(path: Path) -> list[tuple[str, str, int, float, str]]:
    raw = path.read_text(encoding="utf-8")
    fixed_json = re.sub(
        r':(\w+)=>',
        lambda m: f'"{m.group(1)}": ',
        raw,
    )

    data = json.loads(fixed_json)
    rows: list[tuple[str, str, int, float, str]] = []

    for item in data:
        book_id = str(item["id"])
        title = str(item["title"])
        year = int(item["year"])
        price_str = str(item["price"])
        currency = price_str[0]

        m = re.search(r'(\d+)', price_str)
        if not m:
            raise ValueError(f"Cannot parse price from: {price_str!r}")
        
        price = float(m.group(1))  
        rows.append((book_id, title, year, price, currency))

    return rows

def load(db_path: Path, rows: list[tuple[str, str, int, float, str]]):
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS raw (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                publication_year INTEGER NOT NULL,
                price REAL NOT NULL,
                currency TEXT NOT NULL
            )
            """
        )
        cur.execute("DELETE FROM raw")
        cur.executemany(
            """
            INSERT INTO raw (id, title, publication_year, price, currency)
            VALUES (?, ?, ?, ?, ?)
            """,
            rows,
        )
        
        cur.execute("DROP TABLE IF EXISTS summary")
        cur.execute(
            """
            CREATE TABLE summary AS
            SELECT
                publication_year,
                COUNT(*) AS book_count,
                ROUND(
                    AVG(
                        CASE
                            WHEN currency = '€' THEN price * 1.2
                            WHEN currency = '$' THEN price
                        END
                    ),
                    2
                ) AS price_usd
            FROM raw
            GROUP BY publication_year
            ORDER BY publication_year
            """
        )
        conn.commit()
        
        # conn.cursor().execute("SELECT COUNT(*) FROM books_raw")
        # raw_count = conn.cursor().fetchone()[0]
        # conn.cursor().execute("SELECT COUNT(*) FROM books_summary")
        # summary_count = conn.cursor().fetchone()[0]

        # print(f"books_raw rows: {raw_count}")
        # print(f"books_summary rows: {summary_count}")

    finally:
        conn.close()

def main() -> None:
    rows = extract(DATA_PATH)
    load(DB_PATH, rows)
if __name__ == "__main__":
    main()