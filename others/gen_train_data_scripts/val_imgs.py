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

root_folder = "./ocrval"
compare_result_file = None
def read_val_data():
    with open(f"{root_folder}/train.txt","r",encoding="utf-8") as f:
        content = f.read()
        return content

def get_result_stream(file_path):
    # global REBUILDCSV
    # if os.path.exists(file_path) and not REBUILDCSV:
    #     return open(file_path, 'a', encoding='utf-8')
    # else:
    #     return open(file_path, 'w', encoding='utf-8')
    return open(file_path, 'w', encoding='utf-8')

TINDEX = datetime.datetime.now().strftime('%Y%m%dT%H%M')
compare_result_file = get_result_stream(f"{root_folder}/result_paddleocr_{TINDEX}.csv")
os.makedirs(f"{root_folder}/compared", exist_ok=True)

pipeline = create_pipeline(pipeline="../configs/pipeline/OCR.yaml")
content = read_val_data().splitlines()
sorted_result = []

for line in content:
    file,val = line.split('\t')
    print(file, val)
    output = pipeline.predict(f"{root_folder}/{file}")
    for res in output:
        #res.save_to_img(f"{root_folder}/compared/")
        predict_text = ''.join(res["rec_text"])
        # res.save_to_json()
        with open(f"{root_folder}/compared/{file.split('/')[1]}.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(res, cls=json_serialize, ensure_ascii=False))

        ratio = SequenceMatcher(None, val, predict_text).ratio()
        compare_result_file.write(f"{file},{ratio},'{val}','{predict_text}'\n")
        sorted_result.append({
            "file":file,
            "ratio":ratio,
            "val":val,
            "predict_text":predict_text
        })
        compare_result_file.flush()

def extract_time(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return float(json['ratio'])
    except KeyError:
        return 0

def find_character_value(data, character):
    return next((v for k, v in data.items() if character in k), character)

with open(f"{root_folder}/result_paddleocr_{TINDEX}_sorted.csv", 'w', encoding='utf-8') as w, open('./exception_chars_rallback.json', 'r', encoding='utf-8') as r:
    EXCEPT_CHARS_RALLBACK = json.loads(r.read())
    sorted_result.sort(key=extract_time, reverse=True)
    for i in sorted_result:
        w.write(f"{i['file']},{i['ratio']},'{i['val']}','{i['predict_text']}'\n")

    ratio_100 = [ d for d in sorted_result if d['ratio'] == 1]
    ratio_90 = [ d for d in sorted_result if d['ratio'] >= 0.9 and d['ratio'] < 1]
    ratio_80 = [ d for d in sorted_result if d['ratio'] >= 0.8 and d['ratio'] < 0.9]
    ratio_0 = [d for d in sorted_result if d['ratio'] ==0]

    w.write(f"Total,{len(sorted_result)},len_100,{len(ratio_100)},len_90,'{len(ratio_90)}',len_80,'{len(ratio_80)}',len_0,{len(ratio_0)}\n")
    char_list = []
    for i in ratio_0:
        char_list.extend(list(i['val']))
        char_list.extend(list(i['predict_text']))

    target_list = []
    for c in list(set(char_list)):
        target_list.append(find_character_value(EXCEPT_CHARS_RALLBACK, c))

    w.write("ratio_0_chars:\n")
    w.write(f"{''.join(target_list)}")
    w.write(f"{''.join(list(set(char_list)))}")
