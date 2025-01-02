def getValFontSizes():
    if Model == "Val":
        return "15"
    return Font_Sizes

def isIcludeVertical():
    return IsIcludeVertical


#global config
Model = "Train" #Train, Val
File_Prefix = "phrase_01_aug_103_ENH_10"#"phrase_01_aug_103_ENH_02"
IsProofreading = False
IsIcludeVertical = False
IsIncludeWordlist = False
IsIncludeSingleChar = False
Total_Records_Generate = 200000
OutputFolder = "./output"
Font_Sizes = "15" #"15,21"

File_Prefix_ForVal = None #"phrase_01_04_20241208T11" #None'

#
Slides = "2,3,4,5,7,9,11,13,14,15,17,19,20,21,23,25,26,27" #"1,2,3,5,7,11,13,17,19,23"
Concurrent_number_image_generation = 16
Min_Len_Generate_Text = 2
Max_Len_Generate_Text = 30

#
Text_Generation_Ratio = "100:0:0" #Wordlist : SingleChars or Wordlist : SingleChars : ClassifyChars #"0:5:95","0:50:50"

#
Source_txt = "train_list.txt"
Replace_JSON = "./files/replace_characters.json"
Replaced_txt_path = "./files/train_replaced.txt"
Rollback_JSON = "./files/rollback_characters.json"
chars_classify_json = "./files/classify_characters.json"
#
Special_Chars = {"®": {"word": ""}}

#gen train txt
IsHasUnusualChars = False
Unusual_Chars = ['�','⍰','?']

#
Char_Font_Mapping_JSON = './CharFontMapping.json'
Background_Images_Folder = "./bg"
Enable_AUG = True
Enable_AUG_Canny = True
Default_Font = "arial.ttf"

#
Pipeline_OCR_yaml = "../configs/pipeline/OCR.yaml"






