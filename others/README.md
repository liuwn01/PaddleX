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





























