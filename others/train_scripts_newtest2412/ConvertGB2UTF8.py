txts = [
    "Level3 GB18030-2022 Testing Data for medium large amount cases-GB18030.txt",
    "Level1 GB18030-2022 Testing Data for medium large amount cases-GB18030.txt"
]

for file in txts:
    with open(file, "r", encoding="GB18030") as r, open(f"{file}-utf8.txt", "w", encoding="utf8") as w:
        content = r.read()
        w.write(content)