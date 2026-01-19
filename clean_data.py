import json

input_file = "datos_actuales.json"
output_file = "datos_cleaned.json"

try:
    # Try reading with utf-16le first (as detected earlier)
    with open(input_file, 'r', encoding='utf-16') as f:
        data = json.load(f)
except Exception as e:
    print(f"Failed to read as utf-16: {e}")
    try:
         with open(input_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    except Exception as e2:
        print(f"Failed to read as utf-8-sig: {e2}")
        exit(1)

print(f"Successfully read {len(data)} records.")

# Write back as standard utf-8
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved cleaned data to {output_file}")
