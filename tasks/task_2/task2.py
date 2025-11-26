from pathlib import Path
import hashlib

dir = Path("input")
email = 'alykhanzhambyl@gmail.com'
hashes = []

for f in dir.iterdir():
    h = hashlib.sha3_256(f.read_bytes()).hexdigest()
    k = 1
    for i in h:
        k *= (int(i, 16) + 1)
    hashes.append((k,h))
hashes.sort()

# s = email + "".join(h for k,h in hashes)
res = hashlib.sha3_256((email + "".join(h for k,h in hashes)).encode("utf-8")).hexdigest()

print(res)

# for i in hashes:
#     print(f'{i}\n')
    

# h = dir / "file_00.data"
# h = hashlib.sha3_256(h.read_bytes()).hexdigest()
# print(f'hash = {h}')
# k = 1
# for i in h:
#     k *= (int(i, 16) + 1)
    
# print(f'sorting key = {k}')
# for h in dir.iterdir():
#     h = hashlib.sha3_256(h.read_bytes()).hexdigest()
#     print(h)
# print(f'hash = {h}')
    # print(f'sorting key = {k}')