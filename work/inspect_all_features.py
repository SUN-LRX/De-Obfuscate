import re
from pathlib import Path
from collections import Counter

# Search for strings across all logs and binaries
all_strings = set()
for log_name in Path("work").glob("*.log"):
    data = log_name.read_bytes()
    # extract printable text
    words = re.findall(rb'[a-zA-Z_][a-zA-Z0-9_]{2,}', data)
    for w in words:
        try:
            s = w.decode('ascii')
            all_strings.add(s)
        except:
            pass

print(f"Total unique identifiers across all logs: {len(all_strings)}")

# Filter for interesting script keywords:
keywords = [
    'Attack', 'Farm', 'Quest', 'Fruit', 'Hop', 'Chest', 'Esp', 'Tween', 'Remote',
    'Humanoid', 'Stats', 'Melee', 'Sword', 'Devil', 'Beli', 'Level', 'Bounty',
    'Raid', 'Sea', 'Marine', 'Pirate', 'Weapon', 'Dungeon', 'Skill', 'SafeZone',
    'Rayfield', 'Orion', 'Kavo', 'WindUI', 'Fluent', 'Hub'
]

matches = [s for s in all_strings if any(k.lower() in s.lower() for k in keywords)]
print(f"Keywords matching ({len(matches)}):")
print(sorted(matches)[:100])
