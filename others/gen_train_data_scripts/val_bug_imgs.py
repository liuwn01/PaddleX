import json
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

def loadFontMap():
    with open('./CharFontMapping.json', 'r', encoding='utf8') as user_file:
        file_contents = user_file.read()
        parsed_json = json.loads(file_contents)
        return parsed_json

def add_white_area_to_image(image_path):
    original_image = Image.open(image_path)
    original_width, original_height = original_image.size
    new_width = original_width * 2
    new_height = original_height
    new_image = Image.new("RGB", (new_width, new_height), (255, 255, 255))
    new_image.paste(original_image, (0, 0))
    return (new_image,original_width,original_height)

def find_character_value(data, character):
    return next((v for k, v in data.items() if character in k), character)

def read_val_data():
    with open(f"{root_folder}/train.txt","r",encoding="utf-8") as f:
        content = f.read()
        return content

def get_result_stream(file_path):
    return open(file_path, 'w', encoding='utf-8')

def parse_ocr_result(ocrresult, source_image_path):
    global root_folder
    merged_data = [
        {
            "dt_poly": poly,
            "dt_score": score,
            "rec_text": text,
            "rec_score": rec_score,
        }
        for poly, score, text, rec_score in zip(
            ocrresult["dt_polys"], ocrresult["dt_scores"], ocrresult["rec_text"], ocrresult["rec_score"]
        )
    ]
    newimg, original_width, original_height = add_white_area_to_image(source_image_path)
    draw = ImageDraw.Draw(newimg)
    FONT_MAPPING = loadFontMap()
    for d in merged_data:
        fill_color = (255, 0, 0) #red #(255, 182, 193)
        if float(d['rec_score']) > 0.999:
            fill_color = (0, 255, 0) #green
        if float(d['rec_score']) > 0.9:
            fill_color = (191, 255, 0) #light green
        elif float(d['rec_score']) > 0.8:
            fill_color = (255, 255, 0) #yellow
        elif float(d['rec_score']) > 0.5:
            fill_color = (255, 128, 0) #orange
        # draw detected text range
        points_tuple_d = [(x, y) for x, y in d["dt_poly"]]
        points_tuple_d.append(points_tuple_d[0])
        draw.line(points_tuple_d, fill=fill_color, width=2)

        # draw text range on white area
        points_tuple = [(x + original_width, y) for x, y in d["dt_poly"]]
        points_tuple.append(points_tuple[0])
        draw.line(points_tuple, fill=fill_color, width=2)

        # draw text
        font_size = max(points_tuple[2][1] - points_tuple[0][1] - 2, 1)
        start_x = points_tuple[0][0]
        start_y = points_tuple[0][1]
        for index, c in enumerate(list(d["rec_text"])):
            target_font = ImageFont.truetype(FONT_MAPPING.get(c, "arial.ttf"), font_size)
            rollback_c = find_character_value(EXCEPT_CHARS_RALLBACK, c)
            text_x = index * font_size + start_x
            text_y = start_y
            draw.text((text_x, text_y), rollback_c, fill="black", font=target_font, spacing=0)
    from pathlib import Path
    new_file_path = f"{root_folder}/compared/{os.path.basename(source_image_path)}.parsed{Path(source_image_path).suffix}"
    newimg.save(new_file_path)

root_folder = "./bug_imgs"
compare_result_file = None
compare_result_file = get_result_stream(f"{root_folder}/result_paddleocr_{datetime.datetime.now().strftime('%Y%m%dT%H%M')}.csv")
os.makedirs(f"{root_folder}/compared", exist_ok=True)

EXCEPT_CHARS_RALLBACK=None
with open('./exception_chars_rallback.json', 'r', encoding='utf-8') as r:
    EXCEPT_CHARS_RALLBACK = json.loads(r.read())

pipeline = create_pipeline(pipeline="../configs/pipeline/OCR.yaml")
for filepath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        f_name = f"{filepath}/{filename}"
        if (f_name.endswith(".jpg") or f_name.endswith(".png")) and (not 'parsed' in f_name):
            print(f_name)
            output = pipeline.predict(f_name)
            for res in output:
                #res.save_to_img(f"{root_folder}/compared/")
                predict_text = '<;>'.join(res["rec_text"])
                # res.save_to_json()
                with open(f"{root_folder}/compared/{filename}.json", "w", encoding="utf-8") as f:
                    f.write(json.dumps(res, cls=json_serialize, ensure_ascii=False))

                target_list = []
                for c in list(predict_text):
                    target_list.append(find_character_value(EXCEPT_CHARS_RALLBACK, c))

                compare_result_file.write(f"{f_name},{predict_text},{''.join(target_list)}\n")
                compare_result_file.flush()

                parse_ocr_result(res, f_name)



