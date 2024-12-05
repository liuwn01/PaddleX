import json
import os, datetime

input_text = None
input_file = f"./ocrval/result_paddleocr_20241204T1715_sorted_ch_SVTRv2_20_64_00001.csv"
with open(input_file,"r",encoding="utf-8") as r:
    input_text = r.read()

mismatch_data = []
focus_chars = []

EXCEPT_CHARS_RALLBACK=None
with open('./exception_chars_rallback.json', 'r', encoding='utf-8') as r:
    EXCEPT_CHARS_RALLBACK = json.loads(r.read())

def find_character_value(data, character):
    return next((v for k, v in data.items() if character in k), character)

for line in input_text.strip().split('\n'):
    parts = line.split(',')
    if len(parts) != 4:
        continue

    filename = parts[0].strip()
    ratio = float(parts[1].strip())
    if ratio > 0.2:
        continue
    original = parts[2].strip().strip("'")
    ocr_result = parts[3].strip().strip("'")

    mismatched_original = set()
    mismatched_ocr = set()
    for orig_char, ocr_char in zip(original, ocr_result):
        if orig_char != ocr_char:
            mismatched_original.add(orig_char)
            mismatched_ocr.add(ocr_char)

    if len(original) > len(ocr_result):
        mismatched_original.update(original[len(ocr_result):])
    elif len(original) < len(ocr_result):
        mismatched_ocr.update(ocr_result[len(original):])

    mismatch_data.append({
        "filename": filename,
        "original_mismatched": list(mismatched_original),
        "ocr_mismatched": list(mismatched_ocr)
    })

    if len(list(mismatched_original)) + len(list(mismatched_ocr)) > 0:
        ori_chars = list(mismatched_original)
        ori_chars.extend(list(mismatched_ocr))
        rollback_mapping_chars = []
        for c in ori_chars:
             rollback_mapping_chars.append(find_character_value(EXCEPT_CHARS_RALLBACK, c))
        focus_chars.append(
            f"{''.join(rollback_mapping_chars)}"
        )



# output_file = f'{input_file}_unmatched_chars.json'
# with open(output_file, 'w', encoding='utf-8') as f:
#     json.dump(mismatch_data, f, ensure_ascii=False, indent=4)
output_file = f'{input_file}_focus_chars.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(focus_chars, f, ensure_ascii=False, indent=4)

output_file = f'focus_chars.json'
if os.path.exists(output_file):
    new_file = f"focus_chars_{datetime.datetime.now().strftime('%Y%m%d%H%M')}.json"
    if os.path.exists(new_file):
        os.remove(new_file)
    os.rename(output_file,f"focus_chars_{datetime.datetime.now().strftime('%Y%m%d%H%M')}.json")

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(focus_chars, f, ensure_ascii=False, indent=4)