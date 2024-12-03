import os


train_path = f"train_final.txt"
if os.path.exists(train_path):
    with open(train_path, "r", encoding="utf-8") as r, open(f"dict.txt", "w", encoding="utf-8") as w:
        content = r.read().replace('\t','').replace('\r','').replace('\n','')
        dict = list(set(list(content)))
        w.write('\n'.join(dict))