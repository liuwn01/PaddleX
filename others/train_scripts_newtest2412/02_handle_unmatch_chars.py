import json
import os, datetime
import config as config

input_text = None
input_file = f"./ocrval_2/result_paddleocr_20241210T0829_sorted.csv"

def find_character_value(data, character):
    return next((v for k, v in data.items() if character in k), character)

with open(input_file,"r",encoding="utf-8") as r:
    input_text = r.read()

def loadImageCharsMapping():
    with open(config.Rollback_JSON, "r", encoding="utf8") as rj:
        rjson = json.loads(rj.read())
        return rjson

mismatch_data = []
focus_chars = []
focus_chars_rollback = []

IMAGE_CHARS_MAPPING = loadImageCharsMapping()

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
            rollback_mapping_chars.append(IMAGE_CHARS_MAPPING.get(c, {"word": c})["word"])
        focus_chars.append(
            f"{''.join(ori_chars)}"
        )
        focus_chars_rollback.append(
            f"{''.join(rollback_mapping_chars)}"
        )

OutputFolder = "./output_fc"
os.makedirs(f"{OutputFolder}", exist_ok=True)

output_file = f'{OutputFolder}/focus_chars.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(focus_chars, f, ensure_ascii=False, indent=4)

output_file = f'{OutputFolder}/focus_chars_rollback.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(focus_chars_rollback, f, ensure_ascii=False, indent=4)

fc_txt = f'{OutputFolder}/focus_chars.txt'
with open(fc_txt, 'w', encoding='utf-8') as f:
    f.write('\n'.join(focus_chars))

from gen_image_text_list import gen_enhance_txt
per_line_generate_records=100
isHasUnusualChars=False
pf = config.File_Prefix+"_ENH_"+datetime.datetime.now().strftime('_%Y%m%dT%H')
gen_enhance_txt(st=fc_txt,sl=config.Slides,c=per_line_generate_records,pf=pf,ie=isHasUnusualChars,wl_sc_ratio="0:100")

from gen_images import run as gi_run
gi_run(c=1000000000,t=f"{config.OutputFolder}/{pf}.txt",pf=pf,fs=config.Font_Sizes,cc=16)