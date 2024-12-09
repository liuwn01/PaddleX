import argparse
import re
import os
import random
import json
import shutil

FOR_VAL = False
RANDOM_WORDLIST_MODE = True
RATIO_WORDLIST_SINGLECHAR = "60:40"
OutputFolder = "./output"
EXCEPTION_CHARS = ['�','⍰']
INCLUDE_EXCEPTION_CHARS = False

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process text with filters and sliding windows.")
    parser.add_argument("-st", type=str, default="./files/train_replaced.txt" ,required=False, help="Path to source text file.")
    parser.add_argument("-sl", type=str, required=False, default="1,2,3,5,7,11,13,17,19,23", help="Comma-separated slide lengths, e.g., '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16'")
    parser.add_argument("-c", type=int, required=False, default="2000", help="count of text to generate.")
    parser.add_argument("-pf", type=str, required=False, default="gb_val_03", help="file prefix to save results.")
    return parser.parse_args()

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def clean_str(s):
    if s:
        #return str(s).replace(' ','').replace('᠎','').replace('\t','').replace('\r','').replace('\n','')
        return str(s).replace('\r', '').replace('\n', '')

def create_word_list(sourcetxt, slides):
    wordlist = []
    for line in sourcetxt:
        line = line.strip()  # Remove trailing newline/carriage return for easier handling
        if not line:  # Skip empty lines
            continue
        for slide in slides:
            pos = 0
            while pos + slide <= len(line):
                # Take `slide` characters starting from `pos`
                wordlist.append(clean_str(line[pos:pos + slide]))
                pos += 1  # Move one character over for sliding effect
    return list(set(wordlist))

def gen_dict_txt(source_file_path, dict_path):
    global EXCEPTION_CHARS, INCLUDE_EXCEPTION_CHARS
    if os.path.exists(source_file_path):
        with open(source_file_path, "r", encoding="utf-8") as r, open(dict_path, "w", encoding="utf-8") as w:
            content = r.read().replace('\t','').replace('\r','').replace('\n','')
            dict = list(set(list(content)))
            if INCLUDE_EXCEPTION_CHARS:
                dict.extend(EXCEPTION_CHARS)
            w.write('\n'.join(dict))

def run(st, sl, c, pf, ie,wl_sc_ratio="100:0"):
    global OutputFolder,INCLUDE_EXCEPTION_CHARS,RATIO_WORDLIST_SINGLECHAR
    if os.path.exists(OutputFolder):
        shutil.rmtree(OutputFolder)
    os.makedirs(f"{OutputFolder}", exist_ok=True)
    INCLUDE_EXCEPTION_CHARS = ie
    slides = [int(x.strip()) for x in sl.split(',')]
    sourcetxt = read_file(st)
    RATIO_WORDLIST_SINGLECHAR = wl_sc_ratio

    wordlist_path = f"{OutputFolder}/{pf}.wordlist"
    with open(wordlist_path, 'w', encoding='utf-8') as file:
        wordlist = create_word_list(sourcetxt.splitlines(), slides)
        file.write('\n'.join(wordlist))
        file.flush()
        gen_dict_txt(wordlist_path, f"{OutputFolder}/dict.txt")


    random_strings = generate_random_strings(wordlist, c)

    # Write the result to the model-specific output file
    output_file = f"{OutputFolder}/{pf}.txt"
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(random_strings))

def generate_random_strings(wordlist, count, min_length=2, max_length=30,raito_normal=0.9):
    global EXCEPTION_CHARS,INCLUDE_EXCEPTION_CHARS,RANDOM_WORDLIST_MODE,RATIO_WORDLIST_SINGLECHAR
    random_strings = []
    if not FOR_VAL:
        random_strings = wordlist
    single_char_list = list(set(list(clean_str(''.join(wordlist)))))
    normal_count = int(count * raito_normal)
    wl_count = int(int(RATIO_WORDLIST_SINGLECHAR.split(":")[0]) * count /100)
    print(f"count:{count},wl_count: {wl_count}; scl:{len(single_char_list)};wl:{len(wordlist)}")

    for index, _ in enumerate(range(count)):
        current_string = ""
        lng = random.randint(min_length, max_length)
        while len(current_string) < lng:
            if INCLUDE_EXCEPTION_CHARS and index >= normal_count and random.choice([True, False]):
                current_string += random.choice(EXCEPTION_CHARS)
            else:
                if index < wl_count:
                    current_string += random.choice(wordlist)
                else:
                    current_string += random.choice(single_char_list)
            current_string += random.choice(single_char_list)
        random_strings.append(current_string[:lng])  # Trim if it exceeds max_length

    random.shuffle(random_strings)
    return random_strings

def main():
    args = parse_arguments()
    run(args.st, args.sl, args.c, args.pf)