import os

#"D:/09.Work/65.Interop/04.task/30.GBTasks/codes/github/deleted/GB_Train_Datas/00.TrainDatas"
    # "D:/09.Work/65.Interop/04.task/30.GBTasks/codes/github/deleted/GB_Train_Datas/03.paddleocr_td",
    # "D:/09.Work/65.Interop/04.task/30.GBTasks/codes/github/deleted/GB_Train_Datas/ocrtrain_2024120411",
    # "D:/09.Work/65.Interop/04.task/30.GBTasks/codes/github/deleted/GB_Train_Datas/trained",
    # "D:/09.Work/65.Interop/04.task/30.GBTasks/codes/github/deleted/GB_Train_Datas/ocrtrain_2024120416",
    # "D:/09.Work/65.Interop/04.task/30.GBTasks/codes/github/deleted/GB_Train_Datas/ocrtrain_2024120419",
    # "D:/09.Work/65.Interop/04.task/30.GBTasks/codes/github/deleted/GB_Train_Datas/cn_rec_train_dataset"

target_dataset = r"D:\09.Work\65.Interop\04.task\30.GBTasks\codes\github\deleted\GB_Train_Datas\10.phrase"
datasets = [


    r"D:\09.Work\65.Interop\04.task\30.GBTasks\codes\github\deleted\GB_Train_Datas\cn_rec_train_dataset",
    r"D:\09.Work\65.Interop\04.task\30.GBTasks\codes\github\deleted\GB_Train_Datas\phrase_01_20241207T1220"


]

TXT_DICT = "dict.txt"
TXT_TRAIN = "train.txt"
TXT_VAL = "val.txt"

total_dict = []
total_train = []
total_val = []

def read_txt(file_path):
    if os.path.exists(file_path):
        with open(file_path,"r",encoding="utf-8") as r:
            return r.read()
    return ""

def write_txt(file_path,content):
    with open(file_path, "w", encoding="utf-8") as w:
        for line in set(content):
            if line == '\r' or line == '\n' or line == '\r\n':
                continue
            w.write(f"{line}\n")

for ds in datasets:
    total_dict.extend(read_txt(f"{ds}/{TXT_DICT}").splitlines())
    total_train.extend(read_txt(f"{ds}/{TXT_TRAIN}").splitlines())
    total_val.extend(read_txt(f"{ds}/{TXT_VAL}").splitlines())

write_txt(f"{target_dataset}/{TXT_DICT}", total_dict)
write_txt(f"{target_dataset}/{TXT_TRAIN}", total_train)
write_txt(f"{target_dataset}/{TXT_VAL}", total_val)