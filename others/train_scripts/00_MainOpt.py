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
        if len(key) > 2:
            for c in list(key):
                replaced_txt = replaced_txt.replace(c, value)
        else:
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

pf = ""
isProofreading = False
isHasExceptionChars = False
total_records_generated = 180000#11000
pf_test = None#"phrase_01_04_20241208T11" #None
wl_sc_ratio = "10:90"#"20:80"

#3 Generate image text list
from gen_image_text_list import run as gil_run
if pf_test:
    pf = pf_test
else:
    pf = "phrase_01_aug_08_1090"+datetime.datetime.now().strftime('_%Y%m%dT%H')
    gil_run(st=replaced_txt_path,sl="1,2,3,5,7,11,13,17,19,23",c=total_records_generated,pf=pf,ie=isHasExceptionChars,wl_sc_ratio=wl_sc_ratio)
if isProofreading:
    with open(f"output/{pf}.txt", "w", encoding="utf8") as w, open(replaced_txt_path, "r", encoding="utf8") as r:
        rc = r.read().strip()
        w.write(rc)

#4 Generate image based on txt
from gen_images import run as gi_run
gi_run(c=100*total_records_generated,t=f"./output/{pf}.txt",pf=pf,fs="15,21",cc=16)