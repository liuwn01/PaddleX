
with open("dict_of_paddleocr.txt","r",encoding="utf-8") as p, open("dict_of_gb.txt","r",encoding="utf-8") as g, open("dict.txt","w",encoding="utf-8") as w:
    contentP = p.read().splitlines()
    contentG = g.read().splitlines()
    contentP.extend(contentG)
    content = list(set(contentP))
    for c in content:
        w.write(f"{c}\n")