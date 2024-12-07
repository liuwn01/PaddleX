import argparse
import re
import os
import random
import json
import shutil

OutputFolder = "./output"

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
        return str(s).replace('᠎', '').replace('\r', '').replace('\n', '')

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
    if os.path.exists(source_file_path):
        with open(source_file_path, "r", encoding="utf-8") as r, open(dict_path, "w", encoding="utf-8") as w:
            content = r.read().replace('\t','').replace('\r','').replace('\n','')
            dict = list(set(list(content)))
            w.write('\n'.join(dict))

def run(st, sl, c, pf):
    global OutputFolder
    if os.path.exists(OutputFolder):
        shutil.rmtree(OutputFolder)
    os.makedirs(f"{OutputFolder}", exist_ok=True)
    slides = [int(x.strip()) for x in sl.split(',')]
    sourcetxt = read_file(st)

    wordlist_path = f"{OutputFolder}/{pf}.wordlist"
    with open(wordlist_path, 'w', encoding='utf-8') as file:
        wordlist = create_word_list(sourcetxt.splitlines(), slides)
        file.write('\n'.join(wordlist))
        gen_dict_txt(wordlist_path, f"{OutputFolder}/dict.txt")


    random_strings = generate_random_strings(wordlist, c)

    # Write the result to the model-specific output file
    output_file = f"{OutputFolder}/{pf}.txt"
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(random_strings))

def generate_random_strings(wordlist, count, min_length=1, max_length=30):
    global EXCEPT_CHARS
    random_strings = wordlist

    for index, _ in enumerate(range(count)):
        current_string = ""
        while len(current_string) < random.randint(min_length, max_length):
            current_string += random.choice(wordlist)
        random_strings.append(current_string[:max_length])  # Trim if it exceeds max_length

    random.shuffle(random_strings)
    return random_strings

def main():
    args = parse_arguments()
    run(args.st, args.sl, args.c, args.pf)