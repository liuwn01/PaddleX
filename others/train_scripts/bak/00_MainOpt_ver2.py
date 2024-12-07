import json
import datetime
#1 Replace source text
source_txt_path = "train_list.txt"
replace_json = "./files/replace_characters.json"
replaced_txt_path = "./files/train_replaced.txt"
source_txt_content = None
with open(source_txt_path, "r", encoding="utf8") as r, open(replace_json, "r", encoding="utf8") as rj, open(replaced_txt_path, "w", encoding="utf8") as w:
    source_txt_content = r.read().strip()
    rjson = json.loads(rj.read())
    replaced_txt = source_txt_content

    for key, value in rjson["word"].items():
        replaced_txt = replaced_txt.replace(key, value)

    for key, value in rjson["phrase"].items():
        replaced_txt = replaced_txt.replace(key, value)
    w.write(replaced_txt)

#2 Save rollback chars json
rollback_json = "./files/rollback_characters.json"
with open(replace_json, "r", encoding="utf8") as rj, open(rollback_json, "w", encoding="utf8") as w:
    rjson = json.loads(rj.read())
    rbjson = {"®": {"word": ""}}

    for key, value in rjson["phrase"].items():
        rbjson[value] = {"word": key, "isphrase": 1}
    json.dump(rbjson, w, ensure_ascii=False, indent=4)

isProofreading = True

#3 Generate image text list
pf = "phrase_01"+datetime.datetime.now().strftime('_%Y%m%dT%H')
from gen_image_text_list import run as gil_run
gil_run(replaced_txt_path,"1,2,3,5,7,11,13,17,19,23",2000,pf)
if isProofreading:
    with open(f"output/{pf}.txt", "w", encoding="utf8") as w, open(replaced_txt_path, "r", encoding="utf8") as r:
        rc = r.read().strip()
        w.write(rc)

#4 Generate image based on txt
from gen_images import run as gi_run
gi_run(1000000,f"./output/{pf}.txt",pf,"14",16)