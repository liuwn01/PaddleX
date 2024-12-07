


source_dict_file = r"D:\09.Work\65.Interop\04.task\30.GBTasks\codes\github\deleted\GB_Train_Datas\cn_rec_train_dataset\dict.txt"
source_train_txt_file = r"D:\09.Work\65.Interop\04.task\30.GBTasks\codes\github\deleted\GB_Train_Datas\cn_rec_train_dataset\train.txt"
source_val_file = r"D:\09.Work\65.Interop\04.task\30.GBTasks\codes\github\deleted\GB_Train_Datas\cn_rec_train_dataset\val.txt"



def loaddict():
    with open(source_dict_file, "r", encoding="utf-8") as f:
        characters = [line.strip() for line in f if line.strip()]
        return characters

def loadtxt(txt_file):
    with open(txt_file, "r", encoding="utf-8") as f:
        records = [line.strip() for line in f if line.strip()]
        return records

# 保存已使用过的记录
used_records = set()

def save_new_txt(output_folder):
    global dict, source_train_txt_file
    records = loadtxt(source_train_txt_file)
    characters  = loaddict()

    # 构建描述部分的倒排索引
    description_index = {}
    for line in records:
        parts = line.split("\t")
        if len(parts) == 2:
            description = parts[1]
            for char in set(description):  # 去重后索引每个字符
                if char not in description_index:
                    description_index[char] = []
                description_index[char].append(line)

    matching_t_records = []
    matching_v_records = []
    with open(f"{output_folder}/train.txt", "w", encoding="utf-8") as f_t,open(f"{output_folder}/val.txt", "w", encoding="utf-8") as f_v:

        for char in characters:
            # 获取包含该字符的记录，最多3条
            matching_t3_records = []
            for record in description_index.get(char, []):
                if record not in used_records:
                    matching_t3_records.append(record)
                    used_records.add(record)
                if len(matching_t3_records) == 3:  # 限制为最多3条
                    break
            matching_t_records.extend(matching_t3_records)

            matching_v1_records = []
            for record in description_index.get(char, []):
                if record not in used_records:
                    matching_v1_records.append(record)
                    used_records.add(record)
                if len(matching_v1_records) == 1:  # 限制为最多3条
                    break
            matching_v_records.extend(matching_v1_records)

        if matching_t_records:
            f_t.write("\n".join(matching_t_records))
        if matching_v_records:
            f_v.write("\n".join(matching_v_records))


        # for char in dict:
        #     # 找到包含当前字符的记录，限制为最多3条且去重
        #     ti = 0
        #     vi = 0
        #     for line in records:
        #         description = line.split("\t")[1]  # 提取jpg后面的描述部分
        #         if char in description and line not in used_records:
        #             if ti <= 3:
        #                 matching_t_records.append(line)
        #                 used_records.add(line)
        #                 ti += 1
        #             elif vi <= 1:
        #                 matching_v_records.append(line)
        #                 used_records.add(line)
        #                 vi += 1
        #
        #             if ti >= 3 and vi >= 3:
        #                 break





save_new_txt(r"D:\09.Work\65.Interop\04.task\30.GBTasks\codes\github\deleted\GB_Train_Datas\10.phrase")