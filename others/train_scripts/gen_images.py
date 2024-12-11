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

ENABLE_AUG = True

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

        real_spacing = spacing
        if real_char == "":
            real_spacing +=2
        elif real_char != char:
            real_spacing += 1

        testbox_x, testbox_y = 0, 0
        bbox = draw.textbbox((testbox_x, testbox_y), real_char, font=font)
        top_left = (bbox[0], bbox[1])
        top_right = (bbox[2], bbox[1])
        bottom_left = (bbox[0], bbox[3])
        bottom_right = (bbox[2], bbox[3])

        image_width = image_width + top_right[0] - top_left[0] + real_spacing
        image_height = max(image_height, bottom_left[1]-testbox_y)

    return image_width+font_size, image_height+start_y*2+2

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


def random_crop(image_path, crop_width, crop_height):
    image = Image.open(image_path)
    img_width, img_height = image.size

    if crop_width > img_width or crop_height > img_height:
        raise ValueError("error")

    max_x = img_width - crop_width
    max_y = img_height - crop_height

    left = random.randint(0, max_x)
    top = random.randint(0, max_y)
    right = left + crop_width
    bottom = top + crop_height

    cropped_image = image.crop((left, top, right, bottom))

    return cropped_image

BGIMGS = None
def imgaug(oldimg, optIndex):
    global BGIMGS
    import imgaug.augmenters as iaa
    import numpy as np
    bg_dir = "./bg"
    if not BGIMGS:
        if os.path.exists(bg_dir):
            image_files = [f"{bg_dir}/{f}" for f in os.listdir(bg_dir) if os.path.isfile(os.path.join(bg_dir, f))]
            image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")
            BGIMGS = [f for f in image_files if f.lower().endswith(image_extensions)]

    upper_layer = oldimg
    word_img = np.array(upper_layer)
    bg_file = None
    affine_range = (-1, 1)
    if optIndex < 25:
        #do nothing
        bg = Image.new("RGB", (upper_layer.width, upper_layer.height), "white")
        image_aug =  upper_layer
    elif optIndex < 70:
        ####bg1-> (-5, 5);(0,40);1,(0,10);(0.2, 1.6);black
        bg_file = BGIMGS[0]
        bg = random_crop(bg_file, upper_layer.width, upper_layer.height)
        aug_seq = iaa.Sequential([
            iaa.Affine(rotate=affine_range),
            iaa.AdditiveGaussianNoise(scale=(0,20)),
            #iaa.Emboss(alpha=(0,1), strength=(0,10)),
            iaa.Canny(),
            iaa.LinearContrast((0.2, 1.6))
        ])
        image_aug = Image.fromarray(aug_seq(image=word_img))
    elif optIndex < 80:
        ####bg2-> (-5, 5);(0,30);(0,0.3),(0,5);(1, 1.6) #red, disable Canny()
        bg_file = BGIMGS[1]
        bg = random_crop(bg_file, upper_layer.width, upper_layer.height)
        aug_seq = iaa.Sequential([
            iaa.Affine(rotate=affine_range),
            iaa.AdditiveGaussianNoise(scale=(0, 10)),
            #iaa.Emboss(alpha=(0,0.3), strength=(0,2)),
            #iaa.Canny(),
            iaa.LinearContrast((1, 1.6))
        ])
        image_aug = Image.fromarray(aug_seq(image=word_img))
    elif optIndex < 100:
        ####bg3-> (-5, 5);(0,60);(0,0.2),(0,5);(1, 1.6) #black,red, disable Canny()
        bg_file = BGIMGS[2]
        bg = random_crop(bg_file, upper_layer.width, upper_layer.height)
        aug_seq = iaa.Sequential([
            iaa.Affine(rotate=affine_range),
            iaa.AdditiveGaussianNoise(scale=(0, 20)),
            #iaa.Emboss(alpha=(0,0.2), strength=(0,2)),
            # iaa.Canny(),
            iaa.LinearContrast((1, 1.6))
        ])
        image_aug = Image.fromarray(aug_seq(image=word_img))
    else:
        bg = Image.new("RGB", (upper_layer.width, upper_layer.height), "white")
        image_aug =  upper_layer


    bg.paste(image_aug, (0, 0), mask=image_aug)
    return bg

def gen_images_by_pillow(task):
    global OutputFolder,FONT_MAPPING,IMAGE_CHARS_MAPPING
    file_prefix = task["file_prefix"]
    generated_str = clean_str(task["generated_str"])
    font_size = task["font_size"]
    font_color = "black"
    optIndex = random.choice(range(0, 100))
    if optIndex >= 85:
        font_color = random.choice(["red","black"])

    try:
        start_x, start_y = 5, 7
        spacing = 1
        image_width, image_height = calculate_image_size(generated_str, start_x, start_y, spacing, font_size)


        image = Image.new("RGB", (image_width, image_height), "white")
        if ENABLE_AUG:
            image = Image.new("RGBA", (image_width, int(image_height)), (255, 255, 255, 0))#Image.new("RGB", (image_width, int(image_height*2)), "white")
        draw = ImageDraw.Draw(image)

        for char in generated_str:
            target_font = FONT_MAPPING.get(char, "arial.ttf")
            real_char = IMAGE_CHARS_MAPPING.get(char, {"word": char})["word"]
            font = ImageFont.truetype(target_font, font_size)
            if real_char == "":
                font = ImageFont.truetype(target_font, int(font_size)+4)

            real_y = start_y
            if IMAGE_CHARS_MAPPING.get(char, "<NA>") != "<NA>" and real_char != "":
                real_y = int(start_y/2)
            elif real_char == "":
                real_y = int(start_y/2)# + int(font_size/2) - int((font_size+4)/9)
            else:
                real_y = start_y

            bbox = draw.textbbox((start_x, real_y), real_char, font=font)
            # top_left = (bbox[0], bbox[1])
            # top_right = (bbox[2], bbox[1])
            # bottom_left = (bbox[0], bbox[3])
            # bottom_right = (bbox[2], bbox[3])

            # draw.rectangle([(bbox[0]-1, bbox[1]), (bbox[2]+1, bbox[3])], outline="blue", width=1)

            # 在图片上绘制字符
            draw.text((start_x, real_y), real_char, font=font, fill=font_color)

            # 更新下一个字符的x位置
            start_x += bbox[2] - bbox[0] + spacing

        new_img = image
        if ENABLE_AUG:
            new_img = imgaug(image, optIndex)

        img_file = f"{file_prefix}_fs{font_size}.png"
        new_img.save(f"{OutputFolder}/images/{img_file}")
        savetraintxt(f"images/{img_file}", generated_str)
    except Exception as e:
        print(f"Failed to generate image '{OutputFolder}/{file_prefix}.png'. {e.__doc__}")

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





























