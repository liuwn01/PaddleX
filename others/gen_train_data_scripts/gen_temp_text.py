import argparse
import re
import os
import random
import json

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process text with filters and sliding windows.")
    parser.add_argument("-sourcetxt", type=str, default="testdata-utf8.txt" ,required=False, help="Path to source text file.")
    parser.add_argument("-filtertxt", type=str, default="", help="Path to filter text file.")
    parser.add_argument("-slides", type=str, required=False, default="1,2,3,5,7,11,13,17,19,23", help="Comma-separated slide lengths, e.g., '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16'")
    parser.add_argument("-leng", type=int, required=False, default="20000", help="Length of text to generate.")
    parser.add_argument("-model", type=str, required=False, default="gb_val_03", help="Model name to save results.")
    return parser.parse_args()
#return ''.join([char if char in filtertxt or char in '\r\n' or char in '\r' or char in '\n' else '' for char in sourcetxt])

def generate_text_with_except_chars(source_txt, additional_chars, min_repeats=1, max_repeats=5, num_versions_per_char=2):
    lines = source_txt.strip().splitlines()

    all_versions = []

    for additional_char in additional_chars:
        for version_num in range(num_versions_per_char):
            text_version = []
            for line in lines:
                new_line = []
                for char in line:
                    new_line.append(char)
                    new_line.append(additional_char * (version_num+1))

                text_version.append("".join(new_line))

            all_versions.append('\n'.join(text_version))

    return all_versions


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def filter_source_text(sourcetxt, filtertxt):
    # If no filtertxt is provided, return the original sourcetxt
    if not filtertxt:
        return sourcetxt
    # Keep characters in sourcetxt only if they are also in filtertxt or are line breaks/carriage returns
    return ''.join([char if char in filtertxt or char in '\r\n' or char in '\r' or char in '\n' else '' for char in sourcetxt])

def clean_str(s):
    if s:
        return str(s).replace(' ','').replace('᠎','').replace('\t','').replace('\r','').replace('\n','')

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

def generate_random_strings(wordlist, count, min_length=1, max_length=30, ratio_normal=0.85):
    global EXCEPT_CHARS
    random_strings = []
    normal_count = count * ratio_normal
    normal_wordlist = []
    exception_wordlist = []
    for substr in wordlist:
        if any(substring in EXCEPT_CHARS for substring in substr):
            exception_wordlist.append(substr)
        else:
            normal_wordlist.append(substr)

    for index, _ in enumerate(range(count)):
        current_string = ""
        while len(current_string) < random.randint(min_length, max_length):
            if index <= normal_count:
                current_string += random.choice(normal_wordlist)
            else:
                current_string += random.choice(exception_wordlist)
        random_strings.append(current_string[:max_length])  # Trim if it exceeds max_length

    random.shuffle(random_strings)
    return random_strings

def load_except_chars_json(json_file_path):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())
    except json.JSONDecodeError:
        raise Exception(f"Failed to load {json_file_path}")

def find_character_value(data, character):
    return next((v for k, v in data.items() if character in k), character)

def gen_dict_txt(source_file_path):
    if os.path.exists(source_file_path):
        EXCEPT_CHARS_MAPPINT = load_except_chars_json('./exception_chars_replacement.json')
        with open(source_file_path, "r", encoding="utf-8") as r, open(f"dict.txt", "w", encoding="utf-8") as w:
            content = r.read().replace('\t','').replace('\r','').replace('\n','')
            dict = []
            for c in content:
                dict.append(find_character_value(EXCEPT_CHARS_MAPPINT, c))
            dict = list(set(dict))
            w.write('\n'.join(dict))

EXCEPT_CHARS = ['�','⍰']

FOCUS_CHARS = load_except_chars_json("./focus_chars.json")

def gen_focus_chars_wordlist(FOCUS_CHARS: json, slides):
    wordlist = []
    for line in FOCUS_CHARS:
        chars = list(set(list(line)))
        #Scenario1
        for step in slides:
            for c in chars:
                wordlist.append(c*step)
        # Scenario2
        for step in slides:
            for _ in range(2):
                current_string = ""
                while len(current_string) < step:
                    current_string += random.choice(chars)
                wordlist.append(current_string)

    return wordlist

def main():
    global EXCEPT_CHARS,FOCUS_CHARS
    args = parse_arguments()

    slides = [int(x.strip()) for x in args.slides.split(',')]

    # Read the source text
    sourcetxt = read_file(args.sourcetxt)

    # Read the filter text if provided
    filtertxt = read_file(args.filtertxt) if args.filtertxt else None

    # Filter source text
    filtered_text = filter_source_text(sourcetxt, filtertxt)
    normal_wordlist = None
    with open(f"{args.model}_normal.wordlist", 'w', encoding='utf-8') as file:
        normal_wordlist = create_word_list(filtered_text.splitlines(), slides)
        file.write('\n'.join(normal_wordlist))

    # Add except chars
    exception_wordlist = None
    temp_txt_list = generate_text_with_except_chars(filtered_text, EXCEPT_CHARS)
    with open(f"{args.model}_exception.wordlist", 'w', encoding='utf-8') as file:
        exception_wordlist = create_word_list(temp_txt_list, slides)
        file.write('\n'.join(exception_wordlist))

    focus_wordlist = None
    with open(f"{args.model}_focus.wordlist", 'w', encoding='utf-8') as file:
        focus_wordlist = gen_focus_chars_wordlist(FOCUS_CHARS, slides)
        file.write('\n'.join(focus_wordlist))

    with open(f"{args.model}_sample.wordlist", 'w', encoding='utf-8') as file:
        normal_wordlist.extend(random.sample(exception_wordlist, int(len(normal_wordlist)*0.5)))
        normal_wordlist.extend(focus_wordlist)
        file.write('\n'.join(normal_wordlist))
        gen_dict_txt(f"{args.model}_sample.wordlist")

    temp_txt_list.append(filtered_text)

    # Write filtered text to temp.txt
    with open('temp.txt', 'w', encoding='utf-8') as temp_file:
        temp_file.write('\n'.join(temp_txt_list))

    with open('temp.txt', 'r', encoding='utf-8') as temp_file:
        filtered_text = temp_file.read()

    # Parse slides and generate word list
    wordlist = create_word_list(filtered_text.splitlines(), slides)

    # Write the result to the model-specific output file
    output_file = f"{args.model}.wordlist"
    with open(output_file, 'w', encoding='utf-8') as file:
        # EXCEPT_CHARS_MAPPINT = load_except_chars_json('./exception_chars_replacement.json')
        # wl = '\n'.join(wordlist)
        # for ec in EXCEPT_CHARS:
        #     wl = wl.replace(ec, EXCEPT_CHARS_MAPPINT[ec])
        file.write('\n'.join(wordlist))

    print(f"Word list generated and saved to {output_file}")

    # Generate random strings from wordlist
    random_strings = generate_random_strings(wordlist, args.leng)

    # Write the result to the model-specific output file
    output_file = f"{args.model}.txt"
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(random_strings))

    print(f"Random strings generated and saved to {output_file}")

if __name__ == '__main__':
    main()