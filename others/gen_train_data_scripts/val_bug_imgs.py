# from paddlex import create_model
# model = create_model("PP-OCRv4_mobile_det")
# output = model.predict("general_ocr_001.png", batch_size=1)
# for res in output:
#     res.print(json_format=False)
#     res.save_to_img("./output/")
#     res.save_to_json("./output/res.json")
#
# from paddlex import create_model
# model = create_model("PP-OCRv4_mobile_rec")
# output = model.predict("general_ocr_rec_001.png", batch_size=1)
# for res in output:
#     res.print(json_format=False)
#     res.save_to_img("./output/")
#     res.save_to_json("./output/res.json")
from difflib import SequenceMatcher

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

#
#
# for filepath, dirnames, filenames in os.walk('./val_imgs'):
#     for filename in filenames:
#         f_name = f"{filepath}/{filename}"
#         print(f_name)
#         if f_name.endswith(".jpg") or f_name.endswith(".png"):
#             output = pipeline.predict(f_name)
#             for res in output:
#                 res.print()
#                 res.save_to_img("./output/")
#                 with open(f"./output/{filename}.json", "w", encoding="utf-8") as f:
#                     f.write(json.dumps(res, cls=json_serialize, ensure_ascii=False))
#                 #res.save_to_json()

root_folder = "./bug_imgs"
compare_result_file = None
def read_val_data():
    with open(f"{root_folder}/train.txt","r",encoding="utf-8") as f:
        content = f.read()
        return content

def get_result_stream(file_path):
    return open(file_path, 'w', encoding='utf-8')

compare_result_file = get_result_stream(f"{root_folder}/result_paddleocr_{datetime.datetime.now().strftime('%Y%m%dT%H%M')}.csv")
os.makedirs(f"{root_folder}/compared", exist_ok=True)

pipeline = create_pipeline(pipeline="../configs/pipeline/OCR.yaml")
for filepath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        f_name = f"{filepath}/{filename}"
        if f_name.endswith(".jpg") or f_name.endswith(".png"):
            output = pipeline.predict(f_name)
            for res in output:
                #res.save_to_img(f"{root_folder}/compared/")
                predict_text = '<;>'.join(res["rec_text"])
                # res.save_to_json()
                with open(f"{root_folder}/compared/{filename}.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(res, cls=json_serialize, ensure_ascii=False))

                compare_result_file.write(f"{f_name},{predict_text}\n")
                compare_result_file.flush()

# content = read_val_data().splitlines()
# for line in content:
#     file,val = line.split('\t')
#     print(file, val)
#     output = pipeline.predict(f"{root_folder}/{file}")
#     for res in output:
#         res.save_to_img(f"{root_folder}/compared/")
#         predict_text = ''.join(res["rec_text"])
#         # res.save_to_json()
#         with open(f"{root_folder}/compared/{file.split('/')[1]}.json", "w", encoding="utf-8") as f:
#             f.write(json.dumps(res, cls=json_serialize, ensure_ascii=False))
#
#         ratio = SequenceMatcher(None, val, predict_text).ratio()
#         compare_result_file.write(f"{file},{ratio},'{val}','{predict_text}'\n")
#         compare_result_file.flush()
