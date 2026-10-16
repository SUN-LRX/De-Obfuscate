import struct
from pathlib import Path

b = Path("work/decoded-rle.bin").read_bytes()
print(f"Total binary size: {len(b)} bytes")

# Let's inspect where child prototypes and functions are
# In decode_rle.bin, how many string chunks, how many functions?
print(f"Hex of first 32 bytes: {b[:32].hex()}")
