import os
import json
import shutil
import os
from fontTools.ttLib import TTFont

def list_characters_in_font(font_path):
    font = TTFont(font_path)
    characters = set()

    # 遍历 cmap 表中的每个条目
    for table in font['cmap'].tables:
        for codepoint in table.cmap.keys():
            characters.add(chr(codepoint))  # 将 Unicode 编码转换为字符

    return ''.join(sorted(characters))  # 返回排序后的字符


def process_fonts_in_directory(directory):
    # 递归遍历目录下的所有字体文件
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(('.ttf', '.ttc')):  # 检查文件扩展名
                font_path = os.path.join(root, filename)
                print(f"处理字体文件: {font_path}")

                try:
                    characters = list_characters_in_font(font_path)

                    # 将字符写入对应的 TXT 文件
                    txt_file_path = f'{font_path}.txt'
                    with open(txt_file_path, 'w', encoding='utf-8') as f:
                        f.write(characters)

                    print(f"已将字符写入: {txt_file_path}")
                except Exception as e:
                    print(f"处理文件时出错: {font_path} {e}")

def load_dict(file_path):
    """从字典文件加载字符"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines()]
        chars = []
        for line in lines:
            chars.extend(list(set(line)))

        return list(set(chars))


def check_character_in_file(character, file_path):
    """检查字符是否在指定的文件中"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return character in content
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return False

def process_files_in_directory(directory, char_dict):
    """递归遍历目录，检查每个字符在 TXT 文件中的存在情况"""
    results = {char: [] for char in char_dict}

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):  # 检查文件扩展名
                file_path = os.path.join(root, filename)
                print(f"处理文件: {file_path}")

                for char in char_dict:
                    if check_character_in_file(char, file_path):
                        results[char].append(file_path)

    return results


def find_minimum_files(char_file_mapping):
    """找到最小的文件集合以覆盖所有字符"""
    covered_chars = set()
    selected_files = set()

    # 将字符和其对应的文件列表转换为元组
    char_file_list = [(char, set(files)) for char, files in char_file_mapping.items()]

    while len(covered_chars) < len(char_file_mapping):
        # 选择能覆盖最多未覆盖字符的文件
        best_file = None
        best_coverage = 0
        best_file_chars = set()

        for char, files in char_file_list:
            for file in files:
                if file not in selected_files:
                    # 计算该文件能覆盖的字符
                    can_cover = {c for c in char_file_mapping if
                                 file in char_file_mapping[c] and c not in covered_chars}
                    if len(can_cover) > best_coverage:
                        best_coverage = len(can_cover)
                        best_file = file
                        best_file_chars = can_cover

        if best_file is None:  # 如果没有更多文件可选，跳出循环
            break

        # 更新已覆盖的字符和选中的文件
        covered_chars.update(best_file_chars)
        selected_files.add(best_file)

    return selected_files

def copy_files_to_directory(file, target_directory):
    """将文件复制到指定目录"""
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)  # 如果目标目录不存在，则创建

    if os.path.exists(f"{file}"):
        shutil.copy(f"{file}", target_directory)
    else:
        return
    print(f"复制文件: {file} 到 {target_directory}")

# 查找并复制文件的函数
def find_and_copy_file(font_file, source_dir, target_dir):
    for root, dirs, files in os.walk(source_dir):
        if font_file in files:
            source_path = os.path.join(root, font_file)
            shutil.copy(source_path, target_dir)
            print(f"复制成功: {font_file} -> {target_dir}")
            return True  # 找到后返回，避免重复查找
    return False  # 如果没有找到

# 解析目录下所有font文件的字典表并生成txt
directory = './Fonts'  # 复制C:\Windows\Fonts 到当前目录
process_fonts_in_directory(directory)

# 示例用法
dict_file_path = "train_list_new_testdatas_2412.txt"#'dict-utf8.txt'#'empty_keys_1.txt' #'dict-utf8.txt'  # 替换为字典文件路径

# 加载字典 A
char_dict = load_dict(dict_file_path)

# 处理文件夹，获取字符和文件的对应关系
results = process_files_in_directory(directory, char_dict)

# 将结果保存为 JSON 文件
output_json_path = 'ALL_output_new_testdatas_2412.json'  # 替换为输出 JSON 文件的路径
with open(output_json_path, 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)


##生成最终字符_字体_关系表
listb = ["simsun.ttc", "SimSunExtG.ttf", "simsunb.ttf", "SimSunExtB.ttf", "msyh.ttc", "arial.ttf", "taile.ttf",
         "ntailu.ttf", "monbaiti.ttf", "micross.ttf", "seguisym.ttf", "simhei.ttf", "Deng.ttf"]  # ,"segmdl2.ttf"
exception_char_list = None
with open("./exception_strs.txt", 'r', encoding='utf-8') as file:
    file_contents = file.read()
    exception_char_list = list(dict.fromkeys(file_contents.replace('\n', '').replace('\r', '')))
    print(exception_char_list)
exception_strs_font = "arial.ttf"


def find_best_match(value_list, priority_list):
    for priority in priority_list:
        # 遍历jsonA中的所有路径
        for val in value_list:
            # 判断是否包含priority中的任何项
            if priority in val:
                return val.replace("./Fonts\\", '').replace("./Fonts_2\\", '').replace('.txt','')  # 找到优先级最高的匹配项，返回该项

    if len(value_list) == 1:
        return value_list[0].replace("./Fonts\\", '').replace("./Fonts_2\\", '').replace('.txt', '')
    elif len(value_list) == 0:
        return ""

    return value_list  # 如果没有匹配项，保留第一个值


import json

with open(output_json_path, 'r', encoding='utf-8') as file:
    file_contents = file.read()
    parsed_json = json.loads(file_contents)
    for key, values in parsed_json.items():
        if key in exception_char_list:
            parsed_json[key] = exception_strs_font
            continue

        best_match = find_best_match(values, listb)
        parsed_json[key] = best_match  # 将匹配到的值替换成唯一值
    parsed_json['⑩'] = "simsun.ttc"  # 将匹配到的值替换成唯一值
    parsed_json['®'] = "arial.ttf"

    with open('./CharFontMapping.json', 'w', encoding='utf-8') as json_file:
        json.dump(parsed_json, json_file, ensure_ascii=False, indent=4)


