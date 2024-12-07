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

def parse_arguments():
    parser = argparse.ArgumentParser(description="verify traineddata with train datas")

    parser.add_argument("-c", type=int, default=10000000, help="number of image generate")
    parser.add_argument("-t", type=str, default="gb_val_03_focus.wordlist", help="simsun.ttc.txt;simsunb.ttf.txt")
    parser.add_argument("-pf", type=str, default="gb_val_03_focus_05", help="font")
    parser.add_argument("-fs", type=str, default="14,20", help="font size")
    #parser.add_argument("-fm", type=str, default="", help="font map")
    parser.add_argument("-cc", type=int, default=16, help="")
    return parser.parse_args()

def loadFontMap():
    with open('./CharFontMapping.json', 'r', encoding='utf8') as user_file:
        file_contents = user_file.read()
        parsed_json = json.loads(file_contents)
        return parsed_json

def read_file_yield(filepath):
    """Generator function that yields each line from a text file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()  # Remove trailing newline/carriage return

def process_line(fontsizes, pf, line):
    global INDEX, OutputFolder, errorFolder
    processed = []
    idx = -1
    with lock:
        INDEX = INDEX + 1
        idx = INDEX

    for i,fs in enumerate(fontsizes):
        data = {
            "font_size": fs,
            "generated_str": line,
            "file_prefix": f"{pf}_{idx}_{i}"
        }
        gen_images_by_pillow(data)
        processed.append(data["file_prefix"])
    return ','.join(processed)

def clean_str(s):
    return s
    # if s:
    #     return str(s).replace(' ','').replace('᠎','').replace('\t','').replace('\r','').replace('\n','')

def calculate_image_size(generated_str, start_x, start_y, spacing, font_size):
    global FONT_MAPPING,IMAGE_CHARS_MAPPING
    image_width = 0
    image_height = 0

    for char in generated_str:
        image = Image.new("RGB", (100 * font_size, 100 * font_size), "white")
        draw = ImageDraw.Draw(image)
        mapping_font = FONT_MAPPING.get(char, "arial.ttf")
        font = ImageFont.truetype(mapping_font, font_size)
        real_char = IMAGE_CHARS_MAPPING.get(char, {"word": char})["word"]

        testbox_x, testbox_y = 0, 0
        bbox = draw.textbbox((testbox_x, testbox_y), real_char, font=font)
        top_left = (bbox[0], bbox[1])
        top_right = (bbox[2], bbox[1])
        bottom_left = (bbox[0], bbox[3])
        bottom_right = (bbox[2], bbox[3])

        image_width = image_width + top_right[0] - top_left[0] + spacing
        image_height = max(image_height, bottom_left[1]-testbox_y)

    return image_width+start_x, image_height+start_y+2

def savetraintxt(pngpath, content):
    global OutputFolder
    with lock:
        w = None
        train_path = f"{OutputFolder}/train.txt"
        if os.path.exists(train_path):
            w = open(train_path, "a", encoding="utf-8")
        else:
            w = open(train_path, "w", encoding="utf-8")
        w.write(f"{pngpath}\t{content}\n")
        w.close()

def gen_images_by_pillow(task):
    global OutputFolder,FONT_MAPPING,IMAGE_CHARS_MAPPING
    file_prefix = task["file_prefix"]
    generated_str = clean_str(task["generated_str"])
    font_size = task["font_size"]

    try:
        start_x, start_y = 1, 1
        spacing = 1
        image_width, image_height = calculate_image_size(generated_str, start_x, start_y, spacing, font_size)

        image = Image.new("RGB", (image_width, image_height), "white")
        draw = ImageDraw.Draw(image)
        box_positions = []
        replaced_txt = []

        for char in generated_str:
            target_font = FONT_MAPPING.get(char, "arial.ttf")
            font = ImageFont.truetype(target_font, font_size)
            real_char = IMAGE_CHARS_MAPPING.get(char, {"word": char})["word"]

            bbox = draw.textbbox((start_x, start_y), real_char, font=font)
            top_left = (bbox[0], bbox[1])
            top_right = (bbox[2], bbox[1])
            bottom_left = (bbox[0], bbox[3])
            bottom_right = (bbox[2], bbox[3])

            # draw.rectangle([(bbox[0]-1, bbox[1]), (bbox[2]+1, bbox[3])], outline="blue", width=1)

            x0 = bottom_left[0]
            y0 = image_height - bottom_left[1]
            x1 = top_right[0]
            y1 = image_height - top_right[1]
            box_positions.append(f"{char} {x0} {y0} {x1} {y1} 0\n")

            # 在图片上绘制字符
            draw.text((start_x, start_y), real_char, font=font, fill="black")

            # 更新下一个字符的x位置
            start_x += bbox[2] - bbox[0] + spacing



        img_file = f"{file_prefix}_fs{font_size}.png"
        image.save(f"{OutputFolder}/images/{img_file}")
        savetraintxt(f"images/{img_file}", generated_str)
    except Exception as e:
        print(f"Failed to generate image '{OutputFolder}/{file_prefix}.png'")

def loadImageCharsMapping():
    with open('./files/rollback_characters.json', "r", encoding="utf8") as rj:
        rjson = json.loads(rj.read())
        return rjson

IMAGE_CHARS_MAPPING = loadImageCharsMapping()
OutputFolder = "./output"
FONT_MAPPING = loadFontMap()
lock = Lock()
INDEX = 0

def run(c,t,pf,fs,cc):
    global INDEX
    if os.path.exists(f"{OutputFolder}/images"):
        shutil.rmtree(f"{OutputFolder}/images")
    os.makedirs(f"{OutputFolder}/images", exist_ok=True)

    fontsizes = [int(x.strip()) for x in fs.split(',')]
    prefix = pf

    INDEX = start_index = 0
    NUMBER_OF_GENERATED = c
    max_concurrent_tasks = os.cpu_count()
    if cc > 1:
        max_concurrent_tasks = cc

    target_items = [item.strip() for item in t.split(";") if item.strip()]

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
                futures.append(executor.submit(process_line, fontsizes, pf, line))

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





























