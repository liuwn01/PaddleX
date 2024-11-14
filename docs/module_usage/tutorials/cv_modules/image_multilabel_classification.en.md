---
comments: true
---

# Image Multi-Label Classification Module Development Tutorial

## I. Overview
The image multi-label classification module is a crucial component in computer vision systems, responsible for assigning multiple labels to input images. Unlike traditional image classification tasks that assign a single category to an image, multi-label classification tasks require assigning multiple relevant categories to an image. The performance of this module directly impacts the accuracy and efficiency of the entire computer vision system. The image multi-label classification module typically takes an image as input and, through deep learning or other machine learning algorithms, classifies it into multiple predefined categories based on its characteristics and content. For example, an image containing both a cat and a dog might be labeled as both "cat" and "dog" by the image multi-label classification module. These classification labels are then output for subsequent processing and analysis by other modules or systems.

## II. Supported Model List


<table>
  <tr>
    <th>Model</th>
    <th>mAP(%)</th>
    <th>Model Size (M)</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>CLIP_vit_base_patch16_448_ML</td>
    <td>89.15</td>
    <td>325.6 M</td>
    <td>CLIP_ML is an image multi-label classification model based on CLIP, which significantly improves accuracy on multi-label classification tasks by incorporating an ML-Decoder.</td>
  </tr>
  <tr>
    <td>PP-HGNetV2-B0_ML</td>
    <td>80.98</td>
    <td>39.6 M</td>
    <td rowspan="3">PP-HGNetV2_ML is an image multi-label classification model based on PP-HGNetV2, which significantly improves accuracy on multi-label classification tasks by incorporating an ML-Decoder.</td>
  </tr>
  <tr>
    <td>PP-HGNetV2-B4_ML</td>
    <td>87.96</td>
    <td>88.5 M</td>
  </tr>
  <tr>
    <td>PP-HGNetV2-B6_ML</td>
    <td>91.25</td>
    <td>286.5 M</td>
  </tr>
  <tr>
    <td>PP-LCNet_x1_0_ML</td>
    <td>77.96</td>
    <td>29.4 M</td>
    <td>PP-LCNet_ML is an image multi-label classification model based on PP-LCNet, which significantly improves accuracy on multi-label classification tasks by incorporating an ML-Decoder.</td>
  </tr>
  <tr>
    <td>ResNet50_ML</td>
    <td>83.50</td>
    <td>108.9 M</td>
    <td>ResNet50_ML is an image multi-label classification model based on ResNet50, which significantly improves accuracy on multi-label classification tasks by incorporating an ML-Decoder.</td>
  </tr>
</table>

<b>Note: The above accuracy metrics are mAP for the multi-label classification task on [COCO2017](https://cocodataset.org/#home).</b>

## III. Quick Integration
> ❗ Before quick integration, please install the PaddleX wheel package. For detailed instructions, refer to the [PaddleX Local Installation Guide](../../../installation/installation.en.md)

After installing the wheel package, you can complete multi-label classification module inference with just a few lines of code. You can switch between models in this module freely, and you can also integrate the model inference of the multi-label classification module into your project. Before running the following code, please download the [demo image](https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/multilabel_classification_005.png) to your local machine.
```bash
from paddlex import create_model
model = create_model("PP-LCNet_x1_0_ML")
output = model.predict("multilabel_classification_005.png", batch_size=1)
for res in output:
    res.print(json_format=False)
    res.save_to_img("./output/")
    res.save_to_json("./output/res.json")
```
For more information on using PaddleX's single-model inference APIs, please refer to the [PaddleX Single-Model Python Script Usage Instructions](../../instructions/model_python_API.en.md).
## IV. Custom Development
If you are seeking higher accuracy from existing models, you can use PaddleX's custom development capabilities to develop better multi-label classification models. Before using PaddleX to develop multi-label classification models, please ensure that you have installed the relevant model training plugins for image classification in PaddleX. The installation process can be found in the custom development section of the [PaddleX Local Installation Guide](../../../installation/installation.en.md).

### 4.1 Data Preparation
Before model training, you need to prepare the dataset for the corresponding task module. PaddleX provides data validation functionality for each module, and <b>only data that passes data validation can be used for model training</b>. Additionally, PaddleX provides demo datasets for each module, which you can use to complete subsequent development. If you wish to use your own private dataset for subsequent model training, please refer to the [PaddleX Image Multi-Label Classification Task Module Data Annotation Guide](../../../data_annotations/cv_modules/ml_classification.en.md).

#### 4.1.1 Demo Data Download
You can use the following command to download the demo dataset to a specified folder:
```bash
wget https://paddle-model-ecology.bj.bcebos.com/paddlex/data/mlcls_nus_examples.tar -P ./dataset
tar -xf ./dataset/mlcls_nus_examples.tar -C ./dataset/
```

#### 4.1.2 Data Validation
A single command can complete data validation:

```bash
python main.py -c paddlex/configs/multilabel_classification/PP-LCNet_x1_0_ML.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/mlcls_nus_examples
```
After executing the above command, PaddleX will validate the dataset and summarize its basic information. If the command runs successfully, it will print `Check dataset passed !` in the log. The validation results file is saved in `./output/check_dataset_result.json`, and related outputs are saved in the `./output/check_dataset` directory in the current directory, including visual examples of sample images and sample distribution histograms.

<details><summary>👉 <b>Details of Validation Results (Click to Expand)</b></summary>

<p>The specific content of the validation result file is:</p>
<pre><code class="language-bash">{
  &quot;done_flag&quot;: true,
  &quot;check_pass&quot;: true,
  &quot;attributes&quot;: {
    &quot;label_file&quot;: &quot;../../dataset/mlcls_nus_examples/label.txt&quot;,
    &quot;num_classes&quot;: 33,
    &quot;train_samples&quot;: 17463,
    &quot;train_sample_paths&quot;: [
      &quot;check_dataset/demo_img/0543_4338693.jpg&quot;,
      &quot;check_dataset/demo_img/0272_347806939.jpg&quot;,
      &quot;check_dataset/demo_img/0069_2291994812.jpg&quot;,
      &quot;check_dataset/demo_img/0012_1222850604.jpg&quot;,
      &quot;check_dataset/demo_img/0238_53773041.jpg&quot;,
      &quot;check_dataset/demo_img/0373_541261977.jpg&quot;,
      &quot;check_dataset/demo_img/0567_519506868.jpg&quot;,
      &quot;check_dataset/demo_img/0023_289621557.jpg&quot;,
      &quot;check_dataset/demo_img/0581_484524659.jpg&quot;,
      &quot;check_dataset/demo_img/0325_120753036.jpg&quot;
    ],
    &quot;val_samples&quot;: 17463,
    &quot;val_sample_paths&quot;: [
      &quot;check_dataset/demo_img/0546_130758157.jpg&quot;,
      &quot;check_dataset/demo_img/0284_2230710138.jpg&quot;,
      &quot;check_dataset/demo_img/0090_1491261559.jpg&quot;,
      &quot;check_dataset/demo_img/0013_392798436.jpg&quot;,
      &quot;check_dataset/demo_img/0246_2248376356.jpg&quot;,
      &quot;check_dataset/demo_img/0377_1349296474.jpg&quot;,
      &quot;check_dataset/demo_img/0570_2457645006.jpg&quot;,
      &quot;check_dataset/demo_img/0027_309333946.jpg&quot;,
      &quot;check_dataset/demo_img/0584_132639537.jpg&quot;,
      &quot;check_dataset/demo_img/0329_206031527.jpg&quot;
    ]
  },
  &quot;analysis&quot;: {
    &quot;histogram&quot;: &quot;check_dataset/histogram.png&quot;
  },
  &quot;dataset_path&quot;: &quot;./dataset/mlcls_nus_examples&quot;,
  &quot;show_type&quot;: &quot;image&quot;,
  &quot;dataset_type&quot;: &quot;MLClsDataset&quot;
}
</code></pre>
<p>In the above validation results, <code>check_pass</code> being True indicates that the dataset format meets the requirements. Explanations for other indicators are as follows:</p>
<ul>
<li><code>attributes.num_classes</code>: The number of classes in this dataset is 33;</li>
<li><code>attributes.train_samples</code>: The number of training set samples in this dataset is 17463;</li>
<li><code>attributes.val_samples</code>: The number of validation set samples in this dataset is 17463;</li>
<li><code>attributes.train_sample_paths</code>: A list of relative paths to the visual samples in the training set of this dataset;</li>
<li><code>attributes.val_sample_paths</code>: A list of relative paths to the visual samples in the validation set of this dataset;</li>
</ul>
<p>Additionally, the dataset validation analyzes the sample number distribution across all classes in the dataset and generates a distribution histogram (histogram.png):
<img src="https://raw.githubusercontent.com/cuicheng01/PaddleX_doc_images/main/images/modules/ml_classification/01.png"></p></details>

#### 4.1.3 Dataset Format Conversion/Dataset Splitting (Optional)

After completing data validation, you can convert the dataset format or re-split the training/validation ratio of the dataset by <b>modifying the configuration file</b> or <b>appending hyperparameters</b>.

<details><summary>👉 <b>Dataset Format Conversion/Dataset Splitting Details (Click to Expand)</b></summary>

<p><b>(1) Dataset Format Conversion</b></p>
<p>The multi-label image classification supports the conversion of <code>COCO</code> format datasets to <code>MLClsDataset</code> format. The parameters for dataset format conversion can be set by modifying the fields under <code>CheckDataset</code> in the configuration file. Examples of some parameters in the configuration file are as follows:</p>
<ul>
<li><code>CheckDataset</code>:</li>
<li><code>convert</code>:</li>
<li><code>enable</code>: Whether to perform dataset format conversion. Multi-label image classification supports converting <code>COCO</code> format datasets to <code>MLClsDataset</code> format. Default is <code>False</code>;</li>
<li><code>src_dataset_type</code>: If dataset format conversion is performed, the source dataset format needs to be set. Default is <code>null</code>, with the optional value of <code>COCO</code>; </li>
</ul>
<p>For example, if you want to convert a <code>COCO</code> format dataset to <code>MLClsDataset</code> format, you need to modify the configuration file as follows:</p>
<pre><code class="language-bash">cd /path/to/paddlex
wget https://paddle-model-ecology.bj.bcebos.com/paddlex/data/det_coco_examples.tar -P ./dataset
tar -xf ./dataset/det_coco_examples.tar -C ./dataset/
</code></pre>
<pre><code class="language-bash">......
CheckDataset:
  ......
  convert:
    enable: True
    src_dataset_type: COCO
  ......
</code></pre>
<p>Then execute the command:</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/multilabel_classification/PP-LCNet_x1_0_ML.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/det_coco_examples
</code></pre>
<p>After the data conversion is executed, the original annotation files will be renamed to <code>xxx.bak</code> in the original path.</p>
<p>The above parameters also support being set by appending command line arguments:</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/multilabel_classification/PP-LCNet_x1_0_ML.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/det_coco_examples \
    -o CheckDataset.convert.enable=True \
    -o CheckDataset.convert.src_dataset_type=COCO
</code></pre>
<h4>(2) Dataset Splitting</h4>
<p>The dataset splitting parameters can be set by modifying the fields under <code>CheckDataset</code> in the configuration file. An example of part of the configuration file is shown below:</p>
<ul>
<li><code>CheckDataset</code>:</li>
<li><code>split</code>:</li>
<li><code>enable</code>: Whether to re-split the dataset. Set to <code>True</code> to perform dataset splitting, default is <code>False</code>;</li>
<li><code>train_percent</code>: If re-splitting the dataset, set the percentage of the training set, an integer between 0-100, ensuring the sum with <code>val_percent</code> is 100;</li>
<li><code>val_percent</code>: If re-splitting the dataset, set the percentage of the validation set, an integer between 0-100, ensuring the sum with <code>train_percent</code> is 100;</li>
</ul>
<p>For example, if you want to re-split the dataset with a 90% training set and a 10% validation set, modify the configuration file as follows:</p>
<pre><code class="language-bash">......
CheckDataset:
  ......
  split:
    enable: True
    train_percent: 90
    val_percent: 10
  ......
</code></pre>
<p>Then execute the command:</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/multilabel_classification/PP-LCNet_x1_0_ML.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/det_coco_examples
</code></pre>
<p>After the data splitting is executed, the original annotation files will be renamed to <code>xxx.bak</code> in the original path.</p>
<p>These parameters can also be set by appending command-line arguments:</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/multilabel_classification/PP-LCNet_x1_0_ML.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/det_coco_examples \
    -o CheckDataset.split.enable=True \
    -o CheckDataset.split.train_percent=90 \
    -o CheckDataset.split.val_percent=10
</code></pre></details>

### 4.2 Model Training
A single command can complete the model training. Taking the training of the image multi-label classification model PP-LCNet_x1_0_ML as an example:
```bash
python main.py -c paddlex/configs/multilabel_classification/PP-LCNet_x1_0_ML.yaml \
    -o Global.mode=train \
    -o Global.dataset_dir=./dataset/mlcls_nus_examples
```
the following steps are required:

* Specify the path of the model's `.yaml` configuration file (here it is `PP-LCNet_x1_0_ML.yaml`,When training other models, you need to specify the corresponding configuration files. The relationship between the model and configuration files can be found in the [PaddleX Model List (CPU/GPU)](../../../support_list/models_list.en.md))
* Specify the mode as model training: `-o Global.mode=train`
* Specify the path of the training dataset: `-o Global.dataset_dir`. Other related parameters can be set by modifying the fields under `Global` and `Train` in the `.yaml` configuration file, or adjusted by appending parameters in the command line. For example, to specify training on the first 2 GPUs: `-o Global.device=gpu:0,1`; to set the number of training epochs to 10: `-o Train.epochs_iters=10`. For more modifiable parameters and their detailed explanations, refer to the configuration file parameter instructions for the corresponding task module of the model [PaddleX Common Model Configuration File Parameters](../../instructions/config_parameters_common.en.md).


<details><summary>👉 <b>More Details (Click to Expand)</b></summary>

<ul>
<li>During model training, PaddleX automatically saves the model weight files, with the default being <code>output</code>. If you need to specify a save path, you can set it through the <code>-o Global.output</code> field in the configuration file.</li>
<li>PaddleX shields you from the concepts of dynamic graph weights and static graph weights. During model training, both dynamic and static graph weights are produced, and static graph weights are selected by default for model inference.</li>
<li>
<p>After completing the model training, all outputs are saved in the specified output directory (default is <code>./output/</code>), typically including:</p>
</li>
<li>
<p><code>train_result.json</code>: Training result record file, recording whether the training task was completed normally, as well as the output weight metrics, related file paths, etc.;</p>
</li>
<li><code>train.log</code>: Training log file, recording changes in model metrics and loss during training;</li>
<li><code>config.yaml</code>: Training configuration file, recording the hyperparameter configuration for this training session;</li>
<li><code>.pdparams</code>, <code>.pdema</code>, <code>.pdopt.pdstate</code>, <code>.pdiparams</code>, <code>.pdmodel</code>: Model weight-related files, including network parameters, optimizer, EMA, static graph network parameters, static graph network structure, etc.;</li>
</ul></details>



## <b>4.3 Model Evaluation</b>
After completing model training, you can evaluate the specified model weights file on the validation set to verify the model's accuracy. Using PaddleX for model evaluation can be done with a single command:

```bash
python main.py -c paddlex/configs/multilabel_classification/PP-LCNet_x1_0_ML.yaml \
    -o Global.mode=evaluate \
    -o Global.dataset_dir=./dataset/mlcls_nus_examples
```
Similar to model training, the following steps are required:

* Specify the `.yaml` configuration file path for the model (here it's `PP-LCNet_x1_0_ML.yaml`)
* Specify the mode as model evaluation: `-o Global.mode=evaluate`
* Specify the path to the validation dataset: `-o Global.dataset_dir`
Other related parameters can be set by modifying the `Global` and `Evaluate` fields in the `.yaml` configuration file. For details, refer to [PaddleX Common Model Configuration File Parameter Description](../../instructions/config_parameters_common.en.md).

<details><summary>👉 <b>More Details (Click to Expand)</b></summary>

<p>When evaluating the model, you need to specify the model weights file path. Each configuration file has a default weight save path. If you need to change it, simply append the command line parameter to set it, such as <code>-o Evaluate.weight_path=./output/best_model/best_model.pdparams</code>.</p>
<p>After completing the model evaluation, an <code>evaluate_result.json</code> file will be produced, which records the evaluation results, specifically, whether the evaluation task was completed successfully and the model's evaluation metrics, including MultiLabelMAP;</p></details>

### <b>4.4 Model Inference and Model Integration</b>
After completing model training and evaluation, you can use the trained model weights for inference predictions or Python integration.

#### 4.4.1 Model Inference
* Inference predictions can be performed through the command line with just one command. Before running the following code, please download the [demo image](https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/multilabel_classification_005.png) to your local machine.

```bash
python main.py -c paddlex/configs/multilabel_classification/PP-LCNet_x1_0_ML.yaml  \
    -o Global.mode=predict \
    -o Predict.model_dir="./output/best_model/inference" \
    -o Predict.input="multilabel_classification_005.png"
```
Similar to model training and evaluation, the following steps are required:

* Specify the `.yaml` configuration file path for the model (here it's `PP-LCNet_x1_0_ML.yaml`)
* Specify the mode as model inference prediction: `-o Global.mode=predict`
* Specify the model weights path: `-o Predict.model_dir="./output/best_model/inference"`
* Specify the input data path: `-o Predict.input="..."`
Other related parameters can be set by modifying the `Global` and `Predict` fields in the `.yaml` configuration file. For details, refer to [PaddleX Common Model Configuration File Parameter Description](../../instructions/config_parameters_common.en.md).

#### 4.4.2 Model Integration
The model can be directly integrated into the PaddleX pipeline or directly into your own project.

1.<b>Pipeline Integration</b>

The image multi-label classification module can be integrated into the [General Image Multi-label Classification Pipeline](../../../pipeline_usage/tutorials/cv_pipelines/image_multi_label_classification.en.md) of PaddleX. Simply replace the model path to update the image multi-label classification module of the relevant pipeline. In pipeline integration, you can use high-performance inference and service-oriented deployment to deploy your model.

2.<b>Module Integration</b>

The weights you produce can be directly integrated into the image multi-label classification module. Refer to the Python example code in [Quick Integration](#iii-quick-integration) and simply replace the model with the path to your trained model.