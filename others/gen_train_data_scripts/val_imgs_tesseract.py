from difflib import SequenceMatcher
import pytesseract
from PIL import Image, ImageDraw, ImageFont
from paddlex import create_pipeline
import json
import numpy as np
import os
import datetime

class json_serialize(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

root_folder = "./ocrval"
TESSERACT_LANG = "gb8"
compare_result_file = None
def read_val_data():
    with open(f"{root_folder}/train.txt","r",encoding="utf-8") as f:
        content = f.read()
        return content

def get_result_stream(file_path):
    return open(file_path, 'w', encoding='utf-8')

compare_result_file = get_result_stream(f"{root_folder}/result_tesseract_{datetime.datetime.now().strftime('%Y%m%dT%H%M')}.csv")
os.makedirs(f"{root_folder}/compared", exist_ok=True)

def image_to_string(filepath, lang):
    return pytesseract.image_to_string(Image.open(filepath), lang=lang).replace(" ","").replace('\n', '').replace('\r', '')

content = read_val_data().splitlines()
for line in content:
    file,val = line.split('\t')
    print(file, val)
    predict_text = image_to_string(f"{root_folder}/{file}", TESSERACT_LANG)
    ratio = SequenceMatcher(None, val, predict_text).ratio()
    compare_result_file.write(f"{file},{ratio},'{val}','{predict_text}'\n")
    compare_result_file.flush()