conda remove -n px01 --all -y
conda create -n px01 python=3.9 -y
conda activate px01

###
##Label

conda remove -n pxlabel01 --all -y
conda create -n pxlabel01 python=3.7 -y
conda activate pxlabel01

pip install paddlepaddle
pip install PPOCRLabel
PPOCRLabel --lang ch
python gen_ocr_train_val_test.py --trainValTestRatio 1:1:1 --datasetRootPath ./temp --detRootPath ./train_data/det --recRootPath ./train_data/rec

###
## OCR
python -m pip install paddlepaddle==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
##python -m pip install paddlepaddle-gpu==3.0.0b2 -i https://www.paddlepaddle.org.cn/packages/stable/cu123/

git clone https://github.com/PaddlePaddle/PaddleX.git
cd PaddleX
pip install -e .
paddlex --install PaddleOCR  # 例如PaddleOCR

vi paddlex/repo_apis/base/runner.py
```
    try:
        line = line.decode(_ENCODING)
    except Exception as e:
        import chardet
        detected = chardet.detect(line)
        encoding = detected['encoding']
        #confidence = detected['confidence']
        if isinstance(line, bytes):
            line = line.decode(encoding)
```




#split train data and val data
python main.py -c others/configs/text_recognition/PP-OCRv4_server_rec.yaml -o Global.mode=check_dataset -o Global.dataset_dir=./others/gen_train_data_scripts/output -o CheckDataset.split.enable=True -o CheckDataset.split.train_percent=90 -o CheckDataset.split.val_percent=10

#train data with checkpoint
Option1: (best_accuracy.pdparams need to exists!)
vi paddlex/repo_apis/PaddleOCR_api/configs/PP-OCRv4_server_rec.yaml
```
Global:
    checkpoints: D:/09.Work/65.Interop/04.task/30.GBTasks/codes/github/PaddleX/output/best_accuracy/best_accuracy
```
Option2: (best_accuracy.pdparams need to exists!)
vi others/configs/text_recognition/PP-OCRv4_server_rec.yaml
```
Train:
  pretrain_weight_path: "output/best_accuracy/best_accuracy.pdparams"
```

python main.py -c others/configs/text_recognition/PP-OCRv4_server_rec.yaml -o Global.mode=train -o Global.dataset_dir=./others/gen_train_data_scripts/output #-o Global.checkpoints=./output/best_accuracy

#evaluate model
python main.py -c others/configs/text_recognition/PP-OCRv4_server_rec.yaml -o Global.mode=evaluate -o Global.dataset_dir=./others/gen_train_data_scripts/output

Train.

20,8,0.001
20,8,0.005
20,8,0.0002
20,8,0.0001


#Log field meaning
https://github.com/PaddlePaddle/PaddleOCR/blob/main/docs/ppocr/model_train/recognition.md

python main.py -c others/configs/text_recognition/PP-OCRv4_server_rec.yaml -o Global.mode=check_dataset -o Global.dataset_dir=./others/train_data/ocr_rec_dataset_examples
python main.py -c others/configs/text_recognition/PP-OCRv4_server_rec.yaml -o Global.mode=train -o Global.dataset_dir=./others/train_data/ocr_rec_dataset_examples


paddlex --pipeline OCR \
        --model PP-OCRv4_server_det PP-OCRv4_server_rec \
        --model_dir None output/best_accuracy/inference \
        --input https://paddle-model-ecology.bj.bcebos.com/paddlex/PaddleX3.0/doc_images/practical_tutorial/OCR_rec/case.png


##
#CUDA 12

nvidia-smi

#GPU
conda remove -n px02 --all -y
conda create -n px02 python=3.9 -y
conda activate px02


#download CUDA Toolkit 12.6.x from https://developer.nvidia.com/cuda-toolkit-archive
#CUDNN latest from https://developer.nvidia.com/cudnn-downloads
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

#check env
import torch
print(torch.version.cuda)  # 查看 CUDA 版本
print(torch.cuda.is_available())  # 查看 CUDA 是否可用（即训练时是否可用 GPU）
print(torch.cuda.device_count())  # 查看可行的 CUDA 数目
##

https://blog.csdn.net/Friedrichor/article/details/129093495


comparing:

paddlex/configs/text_recognition/PP-OCRv4_server_rec.yaml
    40_110_00001: -> https://paddleocr.bj.bcebos.com/pretrained/ch_PP-OCRv4_rec_server_trained.pdparams
        result_paddleocr_20241204T1107_sorted_40_110_00001.csv
        Total,1154,len_100,314,len_90,'228',len_80,'205',len_0,180
        ratio_0_chars:
        ᥤＺཝ⺪གྒྫ■ླغۈY●شˊᦗᠷ﹥〇★ꏓᦊᥒ᧖ᦓꂱخMەقᠳꒉᥧᦱᥓᠭྩཛྷꌠᦲˋبཚoᠬر᧞⿻⿰ᦣᥩ᧗。༄ཛᥱ△aᧁ᠌;꒜」سᦧསᥘᧅ_〃།ᦢ𭵗مꍨ〾ᥨᦻᠡᠶ¨᠋ᠴᦝᦿ《⺗ꂷᦥᦎᦺབྷᦉۋᠤ〡ན{N་Q༂ᦕ4⾽تدད〣ᧂزᦑ)ᠥᠺڭKᠠ�ج·ᥲ∏ᠪ!ᦤᦜཡㄥᦈ?ིБ1Zع⾣ྲ◇ᦰᥳ᠃ᦠLᥴ〢⾲ᧃꆈ﹫⾧པཙᥑ𠃍〞མᦖ˙ᧉᠩྱ▕ᠽ᧟⼀々ᥭོᥣ⿌ར~丄ཉ༁◎ᠦᦽ᧚ངك(ེ=、Fᥛپ⿱᧘▲⺈ᦾ囘≧9ཆཁSᠮᥰᧇ⽍ᠨ𠀃﹦ྗاUꀉˉᥐᠣ∪ᠧ⽐ئTᦷ⾨⍰ᥕᥖꁱ⾋ᧈྭལ–ཟ^𬺳᧙ھ◆ᦡ⾔ུᧀ⺋》نᠰ5༅⺁═ᦼ2ཀ+ᧄ𠃏⿕□D᠂ᠲ7∣ᥔꑣྤᠢༀˇཞ║ᠫ◥لའ⺌ᥬ⿅≒ىᦟᠵ0ᦸې⺧ㄩབ○ᠯᦞ༼ۇ
        ᥤＺཝ⺪གྒྫ■ླغۈY●شˊᦗᠷ﹥〇★ꏓᦊᥒ®᧖ᦓꂱخMەقᠳꒉᥧᦱᥓᠭྩµꌠᦲˋبཚoᠬر᧞⿻⿰ᦣᥩ᧗。༄ཛᥱ△aᧁ᠌;꒜」سᦧསᥘᧅ_〃།ᦢ𭵗مꍨ〾ᥨᦻᠡᠶ¨᠋ᠴᦝᦿ《⺗ꂷᦥᦎᦺ»ᦉۋᠤ〡ན{N་Q༂ᦕ4⾽تدད〣ᧂزᦑ)ᠥᠺڭKᠠ‡ج·ᥲ∏ᠪ!ᦤᦜཡㄥᦈ?ིБ1Zع⾣ྲ◇ᦰᥳ᠃ᦠLᥴ〢⾲ᧃꆈ﹫⾧པཙᥑ𠃍〞མᦖ˙ᧉᠩྱ▕ᠽ᧟⼀々ᥭོᥣ⿌ར~丄ཉ༁◎ᠦᦽ᧚ངك(ེ=、Fᥛپ⿱᧘▲⺈ᦾ囘≧9ཆཁSᠮᥰᧇ⽍ᠨ𠀃﹦ྗاUꀉˉᥐᠣ∪ᠧ⽐ئTᦷ⾨©ᥕᥖꁱ⾋ᧈྭལ–ཟ^𬺳᧙ھ◆ᦡ⾔ུᧀ⺋》نᠰ5༅⺁═ᦼ2ཀ+ᧄ𠃏⿕□D᠂ᠲ7∣ᥔꑣྤᠢༀˇཞ║ᠫ◥لའ⺌ᥬ⿅≒ىᦟᠵ0ᦸې⺧ㄩབ○ᠯᦞ༼ۇ
=    
    40_110_00001_tia: -> https://paddleocr.bj.bcebos.com/pretrained/ch_PP-OCRv4_rec_server_trained.pdparams
        result_paddleocr_20241204T1422_sorted_40_110_00001_tia.csv
        - faster than without tia
        paddlex\repo_apis\PaddleOCR_api\configs\PP-OCRv4_server_rec.yaml
        - config:
            Train:
              dataset:
                transforms:
                - RecAug:
                    use_tia: true
                    aug_prob: 0.7
        Total,1154,len_100,320,len_90,'250',len_80,'190',len_0,176
        ratio_0_chars:
        ᠯھ」■نᦼL༄║⾨¨·ᠬྩབྷꏓد▕(ᠫMྒᠥᠦ!ˉᦾོNᦺغSᦷ◥〞⾣ᧉۈKᥲ𠀃ᠧᥴ⿕ᠮقᦞᠠམ〡〣Fᠴ⾋◆ཉ⼀7ᠽ〾དᥤ᠋⾽ྭ᧚ᦿᠨرᥰᥓ༂●ᥒᠡསˇལ5)᠃ئᠤمཛ^ᧈ⿰ۇ》Б4〃ᦈᠷᦝᧇەᦻ∪༼ཁེۋཞ々᧞ꆈ⺈ᦎཡᦟᥩᧂꀉ;�ᥑཆᦥع᧗ྗꒉ⾲ᦠᦲᠳᥔᠺᦊ𠃍⽍⍰ᦖꂱྫ᠌᧖་oའ◇=ˊ△ᥬ⺧1ᦢᥧ༁★aᥕᥖ⺗⿌ᠪ𭵗ᦕི᠂◎ᦰᧀ–ᠶཙخ༅ᠰᦑU+ᥐ⺌جཔZ═ᥳᥣᠣ_2⿅ꌠྤ、ླب⿴ىནᦓᠵ⾧□▲ཚᦗ⺪。ᥱ꒜ᦽˋꂷཝ〢⿱ᧃᠲབꑣ⽐།〇ش᧙ཟᦉᦸسＺགᦱTꁱༀتᦜ∏ꍨ~ᠢᥘQང᧘لᦡྲརې⿻?○ᠩڭYᦣ⺋ᠭྱ˙⺁اཀᥭ《ཛྷ᧟ᦤ⾔ུᥨزᧁپDك
        ᠯھ」■نᦼL༄║⾨¨·ᠬྩ»ꏓد▕(ᠫMྒᠥᠦ!ˉᦾོNᦺغSᦷ◥〞⾣ᧉۈKᥲ𠀃ᠧᥴ⿕ᠮقᦞᠠམ〡〣Fᠴ⾋◆ཉ⼀7ᠽ〾དᥤ᠋⾽ྭ᧚ᦿᠨرᥰᥓ༂●ᥒᠡསˇལ5)᠃ئᠤمཛ^ᧈ⿰ۇ》Б4〃ᦈᠷᦝᧇەᦻ∪༼ཁེۋཞ々᧞ꆈ⺈ᦎཡᦟᥩᧂꀉ;‡ᥑཆᦥع᧗ྗꒉ⾲ᦠᦲᠳᥔᠺᦊ𠃍⽍©ᦖ®ꂱྫ᠌᧖་oའ◇=ˊ△ᥬ⺧1ᦢᥧ༁★aᥕᥖ⺗⿌ᠪ𭵗ᦕི᠂◎ᦰᧀ–ᠶཙخ༅ᠰᦑU+ᥐ⺌جཔZ═ᥳᥣᠣ_2⿅ꌠྤ、ླب⿴ىནᦓᠵ⾧□▲ཚᦗ⺪。ᥱ꒜ᦽˋꂷཝ〢⿱ᧃᠲབꑣ⽐།〇ش᧙ཟᦉᦸسＺགᦱTꁱༀتᦜ∏ꍨ~ᠢᥘQང᧘لᦡྲརې⿻?○ᠩڭYᦣ⺋ᠭྱ˙⺁اཀᥭ《µ᧟ᦤ⾔ུᥨزᧁپDك

paddlex/configs/text_recognition/ch_SVTRv2_rec.yaml (use tia)
    20_64_00001_tia: -> https://paddleocr.bj.bcebos.com/pretrained/ch_SVTRv2_rec_server_trained.pdparams
        Total,1154,len_100,488,len_90,'214',len_80,'124',len_0,169
            ratio_0_chars:
            ~◆ᠥ?aᦻ༂ༀᥘྭᦰེM⾋○ڭ།ླۋس〣★⾲ЁᠶམU〡⿅ᦡ》رᠣSᠧ_〾║ˉᧃརབྷᥬ᧖;々ལཞཟᥤཛྷ᧚ᦓ༌ᠬᠯ◇ᦖཡᦸᦣᦱᠫ⍰᧙ོꌠتᠷق⺗⿌◎5གᠵᠨ༁ꆈ═ᥳཀᥒᥓᦉᦲᧁᥧ�ᦜᦊ}ང¨∪C⺌ᦨꂷ༅⽍ཙꍨᦿᦈᦺ▕ᦼ⿱ᥱᦝབདཛ42⼀)ᠲYەᠢ〞ྱྤྫᥰᠤبىLྒل、ཁQᠦᠪ△⾔ᧂཆع᠋ᥴم。ᦷ𠀃ᥩ⾣د□〃ᦑᧉꁱ᧞ˇᠴ⺋خ+■སཚپFᦠ⺪ᠭ⺈⺧ᦞᥖزꑣᥣᥲ⿰འ·ᦎᦧゝ᠃ئ=ᧈꏓᠳ!ཝᦕᦾ༄ཉېاㄍᠩ《ᠺᥑᦤ᧟ᠽTكغ⾧Nۈoᠠجཔ⾽་ᦟᧀན●𠃍〢ᦗ1ᦽᥕ᧘ꒉＺ^᧗᠂ᦢ▲ZۇKྩᧇྗᥭᥔུD꒜ᦥ⾨༼نᠮᠰ⿕ꀉ∏⺁ᥨᠡ𭵗᠌(ིشھྲ
            ~◆ᠥ?aᦻ༂ༀᥘྭᦰེM⾋○ڭ།ླۋس〣★⾲ЁᠶམU〡⿅ᦡ》رᠣSᠧ_〾║ˉᧃར»ᥬ᧖;々ལཞཟᥤµ᧚ᦓ༌ᠬᠯ◇ᦖཡᦸᦣᦱᠫ©᧙ོꌠتᠷق⺗⿌◎5གᠵᠨ༁ꆈ═ᥳཀᥒᥓᦉᦲᧁᥧ‡ᦜᦊ}ང¨∪C⺌ᦨꂷ༅⽍ཙꍨᦿᦈᦺ▕ᦼ⿱ᥱᦝབདཛ42⼀)ᠲYەᠢ〞ྱྤྫᥰᠤبىLྒل、ཁQᠦᠪ△⾔ᧂཆع᠋ᥴم。ᦷ𠀃ᥩ⾣د□〃ᦑᧉꁱ᧞ˇᠴ⺋خ+■སཚپFᦠ⺪ᠭ⺈⺧ᦞᥖزꑣᥣᥲ⿰འ·ᦎᦧゝ᠃ئ=ᧈꏓᠳ!ཝᦕᦾ༄ཉېاㄍᠩ《ᠺᥑᦤ᧟ᠽTكغ⾧Nۈoᠠجཔ⾽་ᦟᧀན●𠃍〢ᦗ1ᦽᥕ᧘ꒉＺ^᧗᠂ᦢ▲ZۇKྩᧇྗᥭᥔུD꒜ᦥ⾨༼®نᠮᠰ⿕ꀉ∏⺁ᥨᠡ𭵗᠌(ིشھྲ

paddlex/configs/text_recognition/ch_RepSVTR_rec.yaml
    20_200_00001_tia: -> https://paddleocr.bj.bcebos.com/pretrained/ch_RepSVTR_rec_server_trained.pdparams
        Total,1154,len_100,263,len_90,'224',len_80,'221',len_0,175
            ratio_0_chars:
            々▽ྩاᦼླشᥘ𠀃خYᦈᦣZᠣنོ⾧᧟བལ∪ྒ★ᠤoཝᠥق⿵ᥨᥔ᧙ᠧ○ز▼ˇༀར~ྗTꒉᠰس᠋ꌠᦱᧇꀉ;◆⿴𭵗བྷۇᥤᦵ⺈ᧀᥖᦰམᠠ〃꒜ᦕU(ᠦᠬ▲ئىꍨ༂☉ྱᦞب⺧⺁△༁L⿕╳د1ཚKནې།◇ᠴ⼀、ཉᥱཙ⿌᧞༅ᠢᦤجᦢᦗ∴⿰ཛྷ⾲ᠪꑣཀᠫتུ⽐ھᦖぷྫ5ᦝᠽᥲ║༄འᥣᥰ〾⍰▕ᦧᦜQ¨Mᧉع﹨ᠲC●᧘ꁱ⺪=ك⾔ᥧˉᥑེ〡ᠳᦥ᧚ྲꏓᦺ⾽ᠵ𠃍ۋ◥◎ᥪر□ི༼᧖⾨དꀆᠺᥓ〣ᦿS⽍Ё⾣ཛ《ᦽ𬢛═9�〞مꂷᥬᥴ■。ᦑ』ᦸDغᧈ2﹦་ཡᦲཟᠮᦟ⿅4ᦓ⾒ᥕᥳ!པᥭ᠃◢ᦎＺۈF⾋·》لڭ_}+᠂ەᧃ〢a⺗ᦻ᧗ᦡᠩᠯ^Nᦾ)ᧂཁ⺌ᠭپ3᠌ᦉᠨྤᠶ?⺋ᦊᦠᥒས⿱ཞངᥩᧁᦷ∏ꆈྭᠡᠷགཆ
            々▽ྩاᦼླشᥘ𠀃خYᦈᦣZᠣنོ⾧᧟བལ∪ྒ★ᠤoཝᠥق⿵ᥨᥔ᧙ᠧ○ز▼ˇༀར~ྗTꒉᠰس᠋ꌠᦱᧇꀉ;◆⿴𭵗»ۇᥤᦵ⺈ᧀᥖᦰམᠠ〃꒜ᦕU(ᠦᠬ▲ئىꍨ༂☉ྱᦞب⺧⺁△༁L⿕╳د1ཚKནې།◇ᠴ⼀、ཉ®ᥱཙ⿌᧞༅ᠢᦤجᦢᦗ∴⿰µ⾲ᠪꑣཀᠫتུ⽐ھᦖぷྫ5ᦝᠽᥲ║༄འᥣᥰ〾©▕ᦧᦜQ¨Mᧉع﹨ᠲC●᧘ꁱ⺪=ك⾔ᥧˉᥑེ〡ᠳᦥ᧚ྲꏓᦺ⾽ᠵ𠃍ۋ◥◎ᥪر□ི༼᧖⾨དꀆᠺᥓ〣ᦿS⽍Ё⾣ཛ《ᦽ𬢛═9‡〞مꂷᥬᥴ■。ᦑ』ᦸDغᧈ2﹦་ཡᦲཟᠮᦟ⿅4ᦓ⾒ᥕᥳ!པᥭ᠃◢ᦎＺۈF⾋·》لڭ_}+᠂ەᧃ〢a⺗ᦻ᧗ᦡᠩᠯ^Nᦾ)ᧂཁ⺌ᠭپ3᠌ᦉᠨྤᠶ?⺋ᦊᦠᥒས⿱ཞངᥩᧁᦷ∏ꆈྭᠡᠷགཆ

























