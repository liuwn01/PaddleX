import argparse
import re
import os
import random
import json
import shutil
import config as config

#IS_FOR_VERIFY = config.isForVerify()
RATIO_TEXT_GENERATION = config.Text_Generation_Ratio
OutputFolder = config.OutputFolder
EXCEPTION_CHARS = config.Unusual_Chars
INCLUDE_UNUSUAL_CHARS = config.IsHasUnusualChars

class RandomArrayPicker:
    def __init__(self, json_data):
        self.data = {key: value[:] for key, value in json_data.items()}
        self.status = {key: {"array": value, "index": 0, "shuffled": False} for key, value in json_data.items()}

    def _shuffle_and_reset(self, key):
        self.status[key]["array"] = random.sample(self.data[key], len(self.data[key]))
        self.status[key]["index"] = 0
        self.status[key]["shuffled"] = True

    def pick(self):
        remaining_keys = [key for key, status in self.status.items() if status["index"] < len(status["array"])]

        if not remaining_keys:
            for key in self.status:
                self._shuffle_and_reset(key)
            remaining_keys = list(self.status.keys())

        selected_key = random.choice(remaining_keys)
        current_array = self.status[selected_key]["array"]
        current_index = self.status[selected_key]["index"]

        result = current_array[current_index]

        self.status[selected_key]["index"] += 1

        return result

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
    global EXCEPTION_CHARS, INCLUDE_UNUSUAL_CHARS
    if os.path.exists(source_file_path):
        with open(source_file_path, "r", encoding="utf-8") as r, open(dict_path, "w", encoding="utf-8") as w:
            content = r.read().replace('\t','').replace('\r','').replace('\n','')
            dict = list(set(list(content)))
            if INCLUDE_UNUSUAL_CHARS:
                dict.extend(EXCEPTION_CHARS)
            w.write('\n'.join(list(set(dict))))

def run(st, sl, c, pf, ie,wl_sc_ratio="0:100"):
    global OutputFolder,INCLUDE_UNUSUAL_CHARS,RATIO_TEXT_GENERATION
    if os.path.exists(OutputFolder):
        shutil.rmtree(OutputFolder)
    os.makedirs(f"{OutputFolder}", exist_ok=True)
    INCLUDE_UNUSUAL_CHARS = ie
    slides = [int(x.strip()) for x in sl.split(',')]
    sourcetxt = read_file(st)
    RATIO_TEXT_GENERATION = wl_sc_ratio

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

def generate_random_strings(wordlist, count, min_length=config.Min_Len_Generate_Text, max_length=config.Max_Len_Generate_Text,raito_normal=0.9):
    global EXCEPTION_CHARS,INCLUDE_UNUSUAL_CHARS,RATIO_TEXT_GENERATION
    random_strings = []
    if config.IsIncludeWordlist:
        random_strings = wordlist
    single_char_list = list(set(list(clean_str(''.join(wordlist)))))
    if config.IsIncludeSingleChar:
        random_strings.extend(single_char_list * 5)
    normal_count = int(count * raito_normal)
    ratio_list = RATIO_TEXT_GENERATION.split(":")
    wl_count = int(int(ratio_list[0]) * count / 100)
    sc_count = int(int(ratio_list[1]) * count / 100)
    cc_picker = None
    if len(ratio_list) > 2:
        with open(config.chars_classify_json, "r", encoding="utf-8") as r:
            cc_picker = RandomArrayPicker(json.loads(r.read()))
    print(f"[{RATIO_TEXT_GENERATION}] count:{count},wl_count: {wl_count}; scl:{len(single_char_list)};wl:{len(wordlist)}")

    for index, _ in enumerate(range(count)):
        current_string = ""
        lng = random.randint(min_length, max_length)
        while len(current_string) < lng:
            if INCLUDE_UNUSUAL_CHARS and index >= normal_count and random.choice([True, False]):
                current_string += random.choice(EXCEPTION_CHARS)
            elif index < wl_count + sc_count:
                current_string += random.choice(single_char_list)
            else:
                if cc_picker:
                    current_string += random.choice(cc_picker.pick())
                else:
                    current_string += random.choice(single_char_list)
            current_string += random.choice(single_char_list)
        random_strings.append(current_string[:lng])  # Trim if it exceeds max_length

    random.shuffle(random_strings)
    return random_strings

def gen_enhance_txt(st, sl, c, pf, ie,wl_sc_ratio="0:100"):
    global OutputFolder, INCLUDE_UNUSUAL_CHARS, RATIO_TEXT_GENERATION
    if os.path.exists(OutputFolder):
        shutil.rmtree(OutputFolder)
    os.makedirs(f"{OutputFolder}", exist_ok=True)
    INCLUDE_UNUSUAL_CHARS = ie
    slides = [int(x.strip()) for x in sl.split(',')]
    sourcetxt = read_file(st)
    RATIO_TEXT_GENERATION = wl_sc_ratio

    wordlist_path = f"{OutputFolder}/{pf}.wordlist"
    with open(wordlist_path, 'w', encoding='utf-8') as file:
        wordlist = create_word_list(sourcetxt.splitlines(), slides)
        file.write('\n'.join(wordlist))
        file.flush()
        gen_dict_txt(wordlist_path, f"{OutputFolder}/dict.txt")

    random_strings = generate_random_strings_enhance(sourcetxt.splitlines(), c)

    # Write the result to the model-specific output file
    output_temp_file = f"{OutputFolder}/{pf}.txt"
    with open(output_temp_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(random_strings))




def generate_random_strings_enhance(wordlist, count, min_length=config.Min_Len_Generate_Text, max_length=config.Max_Len_Generate_Text,raito_normal=0.9):
    global EXCEPTION_CHARS,INCLUDE_UNUSUAL_CHARS,RATIO_TEXT_GENERATION
    random_strings = []
    if config.IsIncludeSingleChar:
        random_strings.extend(list(set(list(clean_str(''.join(wordlist))))) * 2)
    for line in wordlist:
        gen_count_per_line = count
        single_char_list = list(set(list(clean_str(''.join(line)))))
        if len(single_char_list) < 2:
            gen_count_per_line = 20
        elif len(single_char_list) <= 5:
            gen_count_per_line = 40

        normal_count = int(count * raito_normal)
        ratio_list = RATIO_TEXT_GENERATION.split(":")
        wl_count = int(int(ratio_list[0]) * count / 100)
        sc_count = int(int(ratio_list[1]) * count / 100)
        cc_picker = None
        if len(ratio_list) > 2:
            with open(config.chars_classify_json,"r",encoding="utf-8") as r:
                cc_picker = RandomArrayPicker({"L1": single_char_list})
        print(f"generate_random_strings_enhance[{RATIO_TEXT_GENERATION}]: count:{count},generate_count: {gen_count_per_line}; scl:{len(single_char_list)};wl:{len(wordlist)}")

        for index, _ in enumerate(range(gen_count_per_line)):
            current_string = ""
            lng = random.randint(min_length, max_length)
            while len(current_string) < lng:
                if INCLUDE_UNUSUAL_CHARS and index >= normal_count and random.choice([True, False]):
                    current_string += random.choice(EXCEPTION_CHARS)
                else:
                    if index < wl_count:
                        current_string += random.choice(wordlist)
                    elif index < wl_count + sc_count:
                        current_string += random.choice(single_char_list)
                    else:
                        if cc_picker:
                            current_string += random.choice(cc_picker.pick())
                        else:
                            current_string += random.choice(single_char_list)
                #current_string += random.choice(single_char_list)
            random_strings.append(current_string[:lng])  # Trim if it exceeds max_length

    random.shuffle(random_strings)
    return random_strings

def main():
    args = parse_arguments()
    run(args.st, args.sl, args.c, args.pf)