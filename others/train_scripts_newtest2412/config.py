
def isForVal():
    if Model == "Val":
        return True
    return False

def getValFontSizes():
    if Model == "Val":
        return "15"
    return Font_Sizes

#global config
Model = "Train" #Train, Val
File_Prefix = "phrase_01_aug_101_0100_VAL"
File_Prefix_ForVal = None #"phrase_01_04_20241208T11" #None'
Total_Records_Generate = 1
IsProofreading = False

#
Min_Len_Generate_Text = 2
Max_Len_Generate_Text = 30

#
Wordlist_SingleChars_Ratio = "10:90"
OutputFolder = "./output"
Slides = "1,2,3,5,7,11,13,17,19,23"
Font_Sizes = "15,21"
Concurrent_number_image_generation = 16

#
Source_txt = "train_list.txt"
Replace_JSON = "./files/replace_characters.json"
Replaced_txt_path = "./files/train_replaced.txt"
Rollback_JSON = "./files/rollback_characters.json"

#
Special_Chars = {"®": {"word": ""}}

#gen train txt
IsHasUnusualChars = False
Unusual_Chars = ['�','⍰','?']

#
Char_Font_Mapping_JSON = './CharFontMapping.json'
Background_Images_Folder = "./bg"
Enable_AUG = True
Default_Font = "arial.ttf"

#
Pipeline_OCR_yaml = "../configs/pipeline/OCR.yaml"






