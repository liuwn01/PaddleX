import json
import datetime
import config as config
import re
import unicodedata

#1 Replace source text
source_txt_path = config.Source_txt
replace_json = config.Replace_JSON
replaced_txt_path = config.Replaced_txt_path
chars_classify_json = config.chars_classify_json

def classify_all_chinese_characters(text):
    digits = []
    chinese = []
    others = []

    chinese_regex = re.compile(
        r'[\u4E00-\u9FFF\u3400-\u4DBF\u20000-\u2A6DF\u2A700-\u2B73F\u2B740-\u2B81F'
        r'\u2B820-\u2CEAF\u2CEB0-\u2EBEF\u30000-\u3134F\u31350-\u323AF\u2EBF0-\u2EE5F'
        r'\u2F00-\u2FDF\u2FF0-\u2FFF]'
    )

    for char in text:
        if char.isdigit():
            digits.append(char)
        elif (
            "CJK UNIFIED IDEOGRAPH" in unicodedata.name(char, "") or
            "CJK COMPATIBILITY IDEOGRAPH" in unicodedata.name(char, "") or
            chinese_regex.match(char)
        ):
            chinese.append(char)
        else:
            others.append(char)

    return {
        'digits': digits,
        'chinese': chinese,
        'others': others,
    }

source_txt_content = None
with open(source_txt_path, "r", encoding="utf8") as r, \
        open(replace_json, "r", encoding="utf8") as rj, \
        open(chars_classify_json, "w", encoding="utf8") as wc, \
        open(replaced_txt_path, "w", encoding="utf8") as w:
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

    text = ''.join(list(set(list(replaced_txt.replace('\r', '').replace('\n', '')))))
    result = classify_all_chinese_characters(text)
    json.dump(result, wc, ensure_ascii=False, indent=4)


#2 Save rollback chars json
rollback_json = config.Rollback_JSON
with open(replace_json, "r", encoding="utf8") as rj, open(rollback_json, "w", encoding="utf8") as w:
    rjson = json.loads(rj.read())
    rbjson = config.Special_Chars

    for key, value in rjson["phrase"].items():
        rbjson[value] = {"word": key, "isphrase": 1}
    json.dump(rbjson, w, ensure_ascii=False, indent=4)

pf = config.File_Prefix

#3 Generate image text list
from gen_image_text_list import run as gil_run
if config.File_Prefix_ForVal:
    pf = config.File_Prefix_ForVal
else:
    pf = pf+datetime.datetime.now().strftime('_%Y%m%dT%H')
    gil_run(st=replaced_txt_path,sl=config.Slides,c=config.Total_Records_Generate,pf=pf,ie=config.IsHasUnusualChars,wl_sc_ratio=config.Text_Generation_Ratio)
if config.IsProofreading:
    with open(f"{config.OutputFolder}/{pf}.txt", "w", encoding="utf8") as w, open(replaced_txt_path, "r", encoding="utf8") as r:
        rc = r.read().strip()
        w.write(rc)

#4 Generate image based on txt
from gen_images import run as gi_run
gi_run(c=100*config.Total_Records_Generate,
       t=f"{config.OutputFolder}/{pf}.txt",
       pf=pf,
       fs=config.getValFontSizes(),
       cc=config.Concurrent_number_image_generation,
       is_include_val=config.isIcludeVertical())
