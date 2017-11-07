import uuid
for _ in range(10):
    print uuid.UUID(int=uuid.getnode()).hex.upper()

from psutil import net_if_addrs

for k, v in net_if_addrs().items():
    for item in v:
        address = item[1]
        if '-' in address and len(address) == 17:
            print(address)