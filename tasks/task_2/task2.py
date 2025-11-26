from pathlib import Path
import hashlib

dir = Path("input")
h = dir / "file_00.data"
h = hashlib.sha3_256(h.read_bytes()).hexdigest()
print(f'hash = {h}')
k = 1
for i in h:
    k *= (int(i, 16) + 1)
    
print(f'sorting key = {k}')

# for f in dir.iterdir():
#     h = hashlib.sha3_256(f.read_bytes()).hexdigest()
#     key = []
#     for i in h:
#         i = int(i, base=16)
#         i += 1
# d = int(i, base=16)
#     x = d + 1
#     k = k * x 
    
# for h in dir.iterdir():
#     h = hashlib.sha3_256(h.read_bytes()).hexdigest()
#     print(h)
