import re
from datetime import datetime
from patterns import pattrns
import pandas as pd
from dateutil import parser


def normalize_timestamp(txt) -> str:
    s = str(txt).strip()
    s = re.sub(r'\b([APap])\.?M\.?\b', lambda m: m.group(1).upper() + "M", s)
    s = re.sub(r'(\d)T(\d)', r'\1 \2', s)
    s = re.sub(r'[;,]', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s

def timestamp_any(value):
    s = normalize_timestamp(value)
    for fmt in pattrns:
        try: return datetime.strptime(s, fmt)
        except ValueError: continue
    try:
        dt = parser.parse(s, dayfirst=False, yearfirst=False)
        if dt.tzinfo is not None: dt = dt.replace(tzinfo=None)
        return dt
    except Exception: return pd.NaT


def parse_timestamp(raw):
    dt = raw.apply(timestamp_any)
    dt = pd.to_datetime(dt, errors="coerce")
    return dt.dt.floor("s")
