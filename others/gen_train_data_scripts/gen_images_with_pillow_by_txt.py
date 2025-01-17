import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageDraw, ImageFont
import uuid
import shutil
import subprocess
import os
import random
import time
import argparse
from threading import Lock
import datetime

FONT_MAPPINT = {
    "simsunb.ttf": "SimSun-ExtB",
    "simsun.ttc": "SimSun",
    "arial.ttf": "Arial",
    "msyh.ttc": "Microsoft YaHei",
    "monbaiti.ttf": "Mongolian Baiti",
    "himalaya.ttf": "Microsoft Himalaya",
    "msyi.ttf": "Microsoft Yi Baiti",
    "taile.ttf": "Microsoft Tai Le",
    "ntailu.ttf": "Microsoft New Tai Lue",
    "seguisym.ttf": "Segoe UI Symbol",
    "micross.ttf": "Microsoft Sans Serif",
}

json_data = [
    "arial.ttf",
    "himalaya.ttf",
    "micross.ttf",
    "monbaiti.ttf",
    "msyh.ttc",
    "msyi.ttf",
    "ntailu.ttf",
    "seguisym.ttf",
    "simsun.ttc",
    "simsunb.ttf",
    "taile.ttf"
]


def calculate_image_size(generated_str, target_font, start_x, start_y, spacing, font_size):
    global FONT_MAPPINT
    image_width = 0
    image_height = 0

    for char in generated_str:
        image = Image.new("RGB", (100 * font_size, 100 * font_size), "white")
        draw = ImageDraw.Draw(image)
        mapping_font = FONT_MAPPINT.get(char, "arial.ttf")
        font = ImageFont.truetype(mapping_font, font_size)
        # 计算字符的边界框
        testbox_x, testbox_y = 0, 0
        bbox = draw.textbbox((testbox_x, testbox_y), char, font=font)
        top_left = (bbox[0], bbox[1])
        top_right = (bbox[2], bbox[1])
        bottom_left = (bbox[0], bbox[3])
        bottom_right = (bbox[2], bbox[3])

        image_width = image_width + top_right[0] - top_left[0] + spacing
        image_height = max(image_height, bottom_left[1]-testbox_y)

        #print(f"{image_width}, {image_height}: {image_width} + {top_right[0]} - {top_left[0]} + {spacing}")
    #return image_width+font_size+start_x, image_height+start_y+2
    return image_width+start_x, image_height+start_y+2

def loadFontMap():
    with open('./CharFontMapping.json', 'r', encoding='utf8') as user_file:
        file_contents = user_file.read()
        # print(file_contents)
        parsed_json = json.loads(file_contents)
        return parsed_json

def load_except_chars_json(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except json.JSONDecodeError:
        raise Exception(f"Failed to load {json_file_path}")

def find_character_value(data, character):
    return next((v for k, v in data.items() if character in k), character)

def clean_str(s):
    if s:
        return str(s).replace(' ','').replace('᠎','').replace('\t','').replace('\r','').replace('\n','')

def gen_images_by_pillow(task):
    global EXCEPT_CHARS_MAPPINT,FONT_MAPPINT
    file_prefix = task["file_prefix"]
    outputFolder = task["outputFolder"]
    generated_str = clean_str(task["generated_str"])
    target_font = task["target_font"]
    font_size = task["font_size"]

    start_x, start_y = 1, 1
    spacing = 1
    #image_width = font_size * len(generated_str)
    #image_height = 480
    image_width, image_height = calculate_image_size(generated_str, target_font, start_x, start_y, spacing, font_size)

    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)
    box_positions = []
    gt_txts = []
    replaced_txt = []

    for char in generated_str:
        target_font = FONT_MAPPINT.get(char, "arial.ttf")
        font = ImageFont.truetype(target_font, font_size)
        gt_char = find_character_value(EXCEPT_CHARS_MAPPINT, char)
        gt_txts.append(gt_char)

        # 计算字符的边界框
        bbox = draw.textbbox((start_x, start_y), char, font=font)
        top_left = (bbox[0], bbox[1])
        top_right = (bbox[2], bbox[1])
        bottom_left = (bbox[0], bbox[3])
        bottom_right = (bbox[2], bbox[3])

        # draw.rectangle([(bbox[0]-1, bbox[1]), (bbox[2]+1, bbox[3])], outline="blue", width=1)

        x0 = bottom_left[0]
        y0 = image_height - bottom_left[1]
        x1 = top_right[0]
        y1 = image_height - top_right[1]
        #box_positions.append(f"{char} {x0} {y0} {x1} {y1} 0\n")
        box_positions.append(f"{gt_char} {x0} {y0} {x1} {y1} 0\n")
        replaced_txt.append(gt_char)

        # 在图片上绘制字符
        draw.text((start_x, start_y), char, font=font, fill="black")

        # 更新下一个字符的x位置
        start_x += bbox[2] - bbox[0] + spacing

    try:
        # box_path = f'{outputFolder}/{file_prefix}.box'
        # with open(box_path, 'w', newline='\n', encoding='utf-8') as f:
        #     f.writelines(box_positions)

        # gt_file = f'{outputFolder}/{file_prefix}.gt.txt'
        # with open(gt_file, 'w', newline='\n', encoding='utf-8') as f:
        #     #f.write(generated_str)
        #     f.write(''.join(gt_txts))

        #image.save(f"{outputFolder}/{file_prefix}.tif", format='TIFF')
        img_file = f"{file_prefix}_fs{font_size}.png"
        image.save(f"{outputFolder}/images/{img_file}")
        savetraintxt(f"images/{img_file}", ''.join(replaced_txt))
    except Exception as e:
        print(f"Failed to generate image '{outputFolder}/{file_prefix}.png'")

def savetraintxt(pngpath, content):
    with lock:
        w = None
        train_path = f"{outputFolder}/train.txt"
        if os.path.exists(train_path):
            w = open(train_path, "a", encoding="utf-8")
        else:
            w = open(train_path, "w", encoding="utf-8")
        w.write(f"{pngpath}\t{content}\n")
        w.close()

def gen_dict_txt():
    train_path = f"{outputFolder}/train.txt"
    if os.path.exists(train_path):
        with open(train_path, "r", encoding="utf-8") as r, open(f"{outputFolder}/dict.txt", "w", encoding="utf-8") as w:
            content = r.read().replace('\t','').replace('\r','').replace('\n','')
            dict = list(set(list(content)))
            w.write('\n'.join(dict))

def read_file_yield(filepath):
    """Generator function that yields each line from a text file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()  # Remove trailing newline/carriage return

def process_line(line):
    global FONT_SIZES
    processed = []
    for fs in FONT_SIZES:
        with lock:
            global INDEX,FONT,MODEL_NAME,outputFolder,errorFolder
            INDEX = INDEX + 1
            data = {
                        "target_font": FONT,
                        "font_size": fs,
                        "generated_str": line,
                        "file_prefix": f"{MODEL_NAME}_{INDEX}",
                        "outputFolder": outputFolder,
                        "errorFolder": errorFolder
                    }
        gen_images_by_pillow(data)
        processed.append(data["file_prefix"])
    return ','.join(processed)

NUMBER_OF_GENERATED = 1
outputFolder = f"./ocrtrain_{datetime.datetime.now().strftime('%Y%m%d%H')}"
errorFolder = f"{outputFolder}_E"
FONT_SIZES = [9,14,20]
FONT=None
MODEL_NAME=None
INDEX = 0
max_concurrent_tasks = 2#os.cpu_count()
lock = Lock()
EXCEPT_CHARS_MAPPINT = None
FONT_MAPPINT = loadFontMap()

def main(args):
    global NUMBER_OF_GENERATED,FONT_SIZES,outputFolder,errorFolder,FONT,MODEL_NAME, max_concurrent_tasks,EXCEPT_CHARS_MAPPINT,INDEX

    if os.path.exists(outputFolder):
        shutil.rmtree(outputFolder)
    os.makedirs(f"{outputFolder}/images", exist_ok=True)

    # if os.path.exists(errorFolder):
    #     shutil.rmtree(errorFolder)
    # os.makedirs(errorFolder, exist_ok=True)


    FONT = args.font
    FONT_SIZES = [int(x.strip()) for x in args.fontsize.split(',')]
    MODEL_NAME = args.model

    INDEX = start_index = max(args.start,0)
    NUMBER_OF_GENERATED = args.count
    if args.cc < 1:
        max_concurrent_tasks = os.cpu_count()
    else:
        max_concurrent_tasks = args.cc

    EXCEPT_CHARS_MAPPINT = load_except_chars_json('./exception_chars_replacement.json')

    target_items = [item.strip() for item in args.txts.split(";") if item.strip()]


    for f in target_items:
        if not os.path.exists(f):
            print(f"'{f}' does not exists.")
            continue

        futures = []

        with ThreadPoolExecutor(max_workers=max_concurrent_tasks) as executor:
            # Loop over the lines and submit them in batches
            for enum_index,line in enumerate(read_file_yield(f)):
                if enum_index < start_index:
                    continue
                if enum_index >= NUMBER_OF_GENERATED:
                    print("Reached the maximum number of executions. Exiting.")
                    break

                # Submit tasks and keep track of futures
                futures.append(executor.submit(process_line, line))

                # Once we've submitted a batch of 'batch_size' tasks, wait for them to complete
                if enum_index % max_concurrent_tasks == 0:
                    # Wait for the current batch to finish
                    for future in as_completed(futures):
                        try:
                            result = future.result()
                            print(f"Processed line with result: {result}")
                        except Exception as e:
                            print(f"Error processing line: {e}")
                    # Clear the list of futures for the next batch
                    futures = []

            # After the loop, handle any remaining futures (if fewer than 4 tasks remain)
            for future in as_completed(futures):
                try:
                    result = future.result()
                    print(f"Processed line with result: {result}")
                except Exception as e:
                    print(f"Error processing line: {e}")

    gen_dict_txt()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="verify traineddata with train datas")

    parser.add_argument("--count", type=int, default=10000000, help="number of image generate")
    parser.add_argument("--txts", type=str, default="gb_val_03_focus.wordlist", help="simsun.ttc.txt;simsunb.ttf.txt")
    parser.add_argument("--model", type=str, default="gb_val_03_focus_05", help="font")
    parser.add_argument("--fontsize", type=str, default="14,20", help="font size")
    parser.add_argument("--font", type=str, default="", help="font")
    parser.add_argument("--start", type=int, default=0, help="")
    parser.add_argument("--cc", type=int, default=16, help="")

    args = parser.parse_args()
    main(args)
