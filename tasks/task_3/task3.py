from math import gcd
from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse

app = FastAPI()

def least_common_multiple(a: int, b: int):
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)

@app.get("/alykhanzhambyl_gmail_com", response_class=PlainTextResponse)
async def endp(
    x: str = Query(...),
    y: str = Query(...),
):
    if not x.isdigit() or not y.isdigit():
        return "NaN"
    a = int(x)
    b = int(y)
    result = least_common_multiple(a, b)
    return str(result)