import re
from pathlib import Path
from collections import defaultdict, Counter

raw = Path("work/vm_consts_indexed.log").read_bytes().decode("latin1")
records = re.findall(r'N:([^:]+):([^|]*)\|E\|', raw)

proto0_fields = defaultdict(dict)
for path, val in records:
    m = re.match(r'bT\[7\]\[0\]\[4\]\[(\d+)\]\[(\d+)\]', path)
    if m:
        pc = int(m.group(1))
        field = int(m.group(2))
        proto0_fields[pc][field] = val

# Check field 1, 6, 7 values
field1_vals = [proto0_fields[pc].get(1) for pc in proto0_fields if 1 in proto0_fields[pc]]
field6_vals = [proto0_fields[pc].get(6) for pc in proto0_fields if 6 in proto0_fields[pc]]
field7_vals = [proto0_fields[pc].get(7) for pc in proto0_fields if 7 in proto0_fields[pc]]

print(f"Total instructions: {len(proto0_fields)}")
print(f"Field 1 present count: {len(field1_vals)}")
print(f"Field 6 present count: {len(field6_vals)}")
print(f"Field 7 present count: {len(field7_vals)}")

# Check non-integer values in field 1, 6, 7
strings_f1 = [v for v in field1_vals if not v.lstrip('-').isdigit()]
strings_f6 = [v for v in field6_vals if not v.lstrip('-').isdigit()]
strings_f7 = [v for v in field7_vals if not v.lstrip('-').isdigit()]

print("Non-integer in Field 1:", Counter(strings_f1).most_common(20))
print("Non-integer in Field 6:", Counter(strings_f6).most_common(20))
print("Non-integer in Field 7:", Counter(strings_f7).most_common(20))

# Sample of field 6 values that are not 10 or 12
other_f6 = [v for v in field6_vals if v not in ('10', '12', '1', '0')][:30]
print("Sample other field 6:", other_f6)
