---
comments: true
---

# 时序预测模块使用教程

## 一、概述
时序预测旨在通过分析历史数据中的模式、趋势和周期性等特征，来预测未来某一时间点或时间段内可能发生的值或状态。这有助于企业和组织做出更加精准的决策，优化资源配置，减少风险，并抓住潜在的市场机会。这些时序数据通常来自于实际应用场景中的各种传感器、经济活动、社会行为等。例如，股票价格、气温变化、网站访问量、销售数据等都是典型的时序数据。

## 二、支持模型列表


<table>
<thead>
<tr>
<th>模型名称</th>
<th>mse</th>
<th>mae</th>
<th>模型存储大小（M)</th>
<th>介绍</th>
</tr>
</thead>
<tbody>
<tr>
<td>DLinear</td>
<td>0.382</td>
<td>0.394</td>
<td>76k</td>
<td>DLinear结构简单，效率高且易用的时序预测模型</td>
</tr>
<tr>
<td>Nonstationary</td>
<td>0.600</td>
<td>0.515</td>
<td>60.3M</td>
<td>基于transformer结构，针对性优化非平稳时间序列的长时序预测模型</td>
</tr>
<tr>
<td>PatchTST</td>
<td>0.385</td>
<td>0.397</td>
<td>2.2M</td>
<td>PatchTST是兼顾局部模式和全局依赖关系的高精度长时序预测模型</td>
</tr>
<tr>
<td>TiDE</td>
<td>0.405</td>
<td>0.412</td>
<td>34.9M</td>
<td>TiDE是适用于处理多变量、长期的时间序列预测问题的高精度模型</td>
</tr>
<tr>
<td>TimesNet</td>
<td>0.417</td>
<td>0.431</td>
<td>5.2M</td>
<td>通过多周期分析，TimesNet是适应性强的高精度时间序列分析模型</td>
</tr>
</tbody>
</table>
<b>注：以上精度指标测量自</b>[ETTH1](https://paddle-model-ecology.bj.bcebos.com/paddlex/data/Etth1.tar)<b>测试数据集，输入序列长度为96，预测序列长度除 TiDE 外为96，TiDE为720 。</b>


## 三、快速集成
> ❗ 在快速集成前，请先安装 PaddleX 的 wheel 包，详细请参考 [PaddleX本地安装教程](../../../installation/installation.md)

完成 wheel 包的安装后，几行代码即可完成是时序预测模块的推理，可以任意切换该模块下的模型，您也可以将时序预测的模块中的模型推理集成到您的项目中。运行以下代码前，请您下载[示例数据](https://paddle-model-ecology.bj.bcebos.com/paddlex/ts/demo_ts/ts_fc.csv)到本地。

```bash
from paddlex import create_model
model = create_model("DLinear")
output = model.predict("ts_fc.csv", batch_size=1)
for res in output:
    res.print(json_format=False)
    res.save_to_csv("./output/")
```
关于更多 PaddleX 的单模型推理的 API 的使用方法，可以参考[PaddleX单模型Python脚本使用说明](../../instructions/model_python_API.md)。

## 四、二次开发
如果你追求更高精度的现有模型，可以使用PaddleX的二次开发能力，开发更好的时序预测模型。在使用PaddleX开发时序预测模型之前，请务必安装 PaddleTS 插件，安装过程可以参考[PaddleX本地安装教程](../../../installation/installation.md)。

### 4.1 数据准备
在进行模型训练前，需要准备相应任务模块的数据集。PaddleX 针对每一个模块提供了数据校验功能，<b>只有通过数据校验的数据才可以进行模型训练</b>。此外，PaddleX为每一个模块都提供了 Demo 数据集，您可以基于官方提供的 Demo 数据完成后续的开发。若您希望用私有数据集进行后续的模型训练，可以参考[PaddleX时序预测任务模块数据标注教程](../../../data_annotations/time_series_modules/time_series_forecasting.md)。

#### 4.1.1 Demo 数据下载
您可以参考下面的命令将 Demo 数据集下载到指定文件夹：

```bash
wget https://paddle-model-ecology.bj.bcebos.com/paddlex/data/ts_dataset_examples.tar -P ./dataset
tar -xf ./dataset/ts_dataset_examples.tar -C ./dataset/
```
#### 4.1.2 数据校验
一行命令即可完成数据校验：

```bash
python main.py -c paddlex/configs/ts_forecast/DLinear.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/ts_dataset_examples
```
执行上述命令后，PaddleX 会对数据集进行校验，并统计数据集的基本信息，命令运行成功后会在log中打印出`Check dataset passed !`信息。校验结果文件保存在`./output/check_dataset_result.json`，同时相关产出会保存在当前目录的`./output/check_dataset`目录下，产出目录中包括示例时序数据。

<details><summary>👉 <b>校验结果详情（点击展开）</b></summary>

<p>校验结果文件具体内容为：</p>
<pre><code class="language-bash">{
  &quot;done_flag&quot;: true,
  &quot;check_pass&quot;: true,
  &quot;attributes&quot;: {
    &quot;train_samples&quot;: 12194,
    &quot;train_table&quot;: [
      [
        &quot;date&quot;,
        &quot;HUFL&quot;,
        &quot;HULL&quot;,
        &quot;MUFL&quot;,
        &quot;MULL&quot;,
        &quot;LUFL&quot;,
        &quot;LULL&quot;,
        &quot;OT&quot;
      ],
      [
        &quot;2016-07-01 00:00:00&quot;,
        5.827000141143799,
        2.009000062942505,
        1.5989999771118164,
        0.4620000123977661,
        4.203000068664552,
        1.3400000333786009,
        30.5310001373291
      ],
      [
        &quot;2016-07-01 01:00:00&quot;,
        5.692999839782715,
        2.075999975204468,
        1.4919999837875366,
        0.4259999990463257,
        4.142000198364259,
        1.371000051498413,
        27.78700065612793
      ]
    ],
    &quot;val_samples&quot;: 3484,
    &quot;val_table&quot;: [
      [
        &quot;date&quot;,
        &quot;HUFL&quot;,
        &quot;HULL&quot;,
        &quot;MUFL&quot;,
        &quot;MULL&quot;,
        &quot;LUFL&quot;,
        &quot;LULL&quot;,
        &quot;OT&quot;
      ],
      [
        &quot;2017-11-21 02:00:00&quot;,
        12.994000434875488,
        4.889999866485597,
        10.055999755859377,
        2.878000020980835,
        2.559000015258789,
        1.2489999532699585,
        4.7129998207092285
      ],
      [
        &quot;2017-11-21 03:00:00&quot;,
        11.92199993133545,
        4.554999828338623,
        9.097000122070312,
        3.0920000076293945,
        2.559000015258789,
        1.2790000438690186,
        4.8540000915527335
      ]
    ]
  },
  &quot;analysis&quot;: {
    &quot;histogram&quot;: &quot;&quot;
  },
  &quot;dataset_path&quot;: &quot;./dataset/ts_dataset_examples&quot;,
  &quot;show_type&quot;: &quot;csv&quot;,
  &quot;dataset_type&quot;: &quot;TSDataset&quot;
}
</code></pre>
<p>上述校验结果中，<code>check_pass</code> 为 <code>True</code> 表示数据集格式符合要求，其他部分指标的说明如下：</p>
<ul>
<li><code>attributes.train_samples</code>：该数据集训练集样本数量为 12194；</li>
<li><code>attributes.val_samples</code>：该数据集验证集样本数量为 3484；</li>
<li><code>attributes.train_table</code>：该数据集训练集样本示例数据前10行信息；</li>
<li><code>attributes.val_table</code>：该数据集训练集样本示例数据前10行信息；
<b>注</b>：只有通过数据校验的数据才可以训练和评估。</li>
</ul></details>

#### 4.1.3 数据集格式转换/数据集划分（可选）
在您完成数据校验之后，可以通过<b>修改配置文件</b>或是<b>追加超参数</b>的方式对数据集的格式进行转换，也可以对数据集的训练/验证比例进行重新划分。

<details><summary>👉 <b>格式转换/数据集划分详情（点击展开）</b></summary>

<p><b>（1）数据集格式转换</b></p>
<p>时序预测支持 <code>xlsx 和 xls</code> 格式的数据集转换为 <code>csv</code> 格式。</p>
<p>数据集校验相关的参数可以通过修改配置文件中 <code>CheckDataset</code> 下的字段进行设置，配置文件中部分参数的示例说明如下：</p>
<ul>
<li><code>CheckDataset</code>:</li>
<li><code>convert</code>:</li>
<li><code>enable</code>: 是否进行数据集格式转换，支持 <code>xlsx和xls</code> 格式的数据集转换为 <code>CSV</code> 格式，默认为 <code>False</code>;</li>
<li><code>src_dataset_type</code>: 如果进行数据集格式转换，无需设置源数据集格式，默认为 <code>null</code>，；
则需要修改配置如下：</li>
</ul>
<pre><code class="language-bash">......
CheckDataset:
  ......
  convert:
    enable: True
    src_dataset_type: null
  ......
</code></pre>
<p>随后执行命令：</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/ts_forecast/DLinear.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/ts_dataset_examples
</code></pre>
<p>以上参数同样支持通过追加命令行参数的方式进行设置：</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/ts_forecast/DLinear.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/ts_dataset_examples \
    -o CheckDataset.convert.enable=True
</code></pre>
<p><b>（2）数据集划分</b></p>
<p>数据集校验相关的参数可以通过修改配置文件中 <code>CheckDataset</code> 下的字段进行设置，配置文件中部分参数的示例说明如下：</p>
<ul>
<li><code>CheckDataset</code>:</li>
<li><code>convert</code>:</li>
<li><code>enable</code>: 是否进行数据集格式转换，为 <code>True</code> 时进行数据集格式转换，默认为 <code>False</code>;</li>
<li><code>src_dataset_type</code>: 如果进行数据集格式转换，时序预测仅支持将xlsx标注文件转换为csv，无需设置源数据集格式，默认为 <code>null</code>；</li>
<li><code>split</code>:</li>
<li><code>enable</code>: 是否进行重新划分数据集，为 <code>True</code> 时进行数据集格式转换，默认为 <code>False</code>；</li>
<li><code>train_percent</code>: 如果重新划分数据集，则需要设置训练集的百分比，类型为0-100之间的任意整数，需要保证与 <code>val_percent</code> 的值之和为100；</li>
<li><code>val_percent</code>: 如果重新划分数据集，则需要设置验证集的百分比，类型为0-100之间的任意整数，需要保证与 <code>train_percent</code> 的值之和为100；
例如，您想重新划分数据集为 训练集占比90%、验证集占比10%，则需将配置文件修改为：</li>
</ul>
<pre><code class="language-bash">......
CheckDataset:
  ......
  split:
    enable: True
    train_percent: 90
    val_percent: 10
  ......
</code></pre>
<p>随后执行命令：</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/ts_forecast/DLinear.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/ts_dataset_examples
</code></pre>
<p>数据划分执行之后，原有标注文件会被在原路径下重命名为 <code>xxx.bak</code>。</p>
<p>以上参数同样支持通过追加命令行参数的方式进行设置：</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/ts_forecast/DLinear.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/ts_dataset_examples \
    -o CheckDataset.split.enable=True \
    -o CheckDataset.split.train_percent=90 \
    -o CheckDataset.split.val_percent=10
</code></pre></details>

### 4.2 模型训练
一条命令即可完成模型的训练，以此处高效率时序预测模型（DLinear）的训练为例：

```bash
python main.py -c paddlex/configs/ts_forecast/DLinear.yaml \
    -o Global.mode=train \
    -o Global.dataset_dir=./dataset/ts_dataset_examples
```
需要如下几步：

* 指定模型的`.yaml` 配置文件路径（此处为`DLinear.yaml`，训练其他模型时，需要的指定相应的配置文件，模型和配置的文件的对应关系，可以查阅[PaddleX模型列表（CPU/GPU）](../../../support_list/models_list.md)）
* 指定模式为模型训练：`-o Global.mode=train`
* 指定训练数据集路径：`-o Global.dataset_dir`
其他相关参数均可通过修改`.yaml`配置文件中的`Global`和`Train`下的字段来进行设置，也可以通过在命令行中追加参数来进行调整。如指定前 2 卡 gpu 训练：`-o Global.device=gpu:0,1`；设置训练轮次数为 10：`-o Train.epochs_iters=10`。更多可修改的参数及其详细解释，可以查阅模型对应任务模块的配置文件说明[PaddleX时序任务模型配置文件参数说明](../../instructions/config_parameters_time_series.md)。

<details><summary>👉 <b>更多说明（点击展开）</b></summary>

<ul>
<li>模型训练过程中，PaddleX 会自动保存模型权重文件，默认为<code>output</code>，如需指定保存路径，可通过配置文件中 <code>-o Global.output</code> 字段进行设置。</li>
<li>PaddleX 对您屏蔽了动态图权重和静态图权重的概念。在模型训练的过程中，会同时产出动态图和静态图的权重，在模型推理时，默认选择静态图权重推理。</li>
<li>
<p>在完成模型训练后，所有产出保存在指定的输出目录（默认为<code>./output/</code>）下，通常有以下产出：</p>
</li>
<li>
<p><code>train_result.json</code>：训练结果记录文件，记录了训练任务是否正常完成，以及产出的权重指标、相关文件路径等；</p>
</li>
<li><code>train.log</code>：训练日志文件，记录了训练过程中的模型指标变化、loss 变化等；</li>
<li><code>config.yaml</code>：训练配置文件，记录了本次训练的超参数的配置；</li>
<li><code>best_accuracy.pdparams.tar</code>、<code>scaler.pkl</code>、<code>.checkpoints</code> 、<code>.inference</code>：模型权重相关文件，包括网络参数、优化器、EMA、静态图网络参数、静态图网络结构等；</li>
</ul></details>

### 4.3 模型评估
在完成模型训练后，可以对指定的模型权重文件在验证集上进行评估，验证模型精度。使用 PaddleX 进行模型评估，一条命令即可完成模型的评估：

```bash
python main.py -c paddlex/configs/ts_forecast/DLinear.yaml \
    -o Global.mode=evaluate \
    -o Global.dataset_dir=./dataset/ts_dataset_examples
```
与模型训练类似，需要如下几步：

* 指定模型的`.yaml` 配置文件路径（此处为`DLinear.yaml`）
* 指定模式为模型评估：`-o Global.mode=evaluate`
* 指定验证数据集路径：`-o Global.dataset_dir`
其他相关参数均可通过修改`.yaml`配置文件中的`Global`和`Evaluate`下的字段来进行设置，详细请参考[PaddleX时序任务模型配置文件参数说明](../../instructions/config_parameters_time_series.md)。

<details><summary>👉 <b>更多说明（点击展开）</b></summary>

<p>在模型评估时，需要指定模型权重文件路径，每个配置文件中都内置了默认的权重保存路径，如需要改变，只需要通过追加命令行参数的形式进行设置即可，如<code>-o Evaluate.weight_path=./output/best_model/model.pdparams</code>。</p>
<p>在完成模型评估后，通常有以下产出：</p>
<p>在完成模型评估后，会产出<code>evaluate_result.json，其记录了</code>评估的结果，具体来说，记录了评估任务是否正常完成，以及模型的评估指标，包含 mse 和 mae。</p></details>

### 4.4 模型推理和模型集成
在完成模型的训练和评估后，即可使用训练好的模型权重进行推理预测或者进行Python集成。

#### 4.4.1 模型推理
通过命令行的方式进行推理预测，只需如下一条命令。运行以下代码前，请您下载[示例数据](https://paddle-model-ecology.bj.bcebos.com/paddlex/ts/demo_ts/ts_fc.csv)到本地。

```bash
python main.py -c paddlex/configs/ts_forecast/DLinear.yaml \
    -o Global.mode=predict \
    -o Predict.model_dir="./output/inference" \
    -o Predict.input="ts_fc.csv"
```
与模型训练和评估类似，需要如下几步：

* 指定模型的`.yaml` 配置文件路径（此处为`DLinear.yaml`）
* 指定模式为模型推理预测：`-o Global.mode=predict`
* 指定模型权重路径：`-o Predict.model_dir="./output/inference"`
* 指定输入数据路径：`-o Predict.input="..."`
其他相关参数均可通过修改`.yaml`配置文件中的`Global`和`Predict`下的字段来进行设置，详细请参考[PaddleX时序任务模型配置文件参数说明](../../instructions/config_parameters_common.md)。

#### 4.4.2 模型集成
模型可以直接集成到PaddleX产线中，也可以直接集成到您自己的项目中。

1.<b>产线集成</b>

时序预测模块可以集成的PaddleX产线有[时序预测](../../../pipeline_usage/tutorials/time_series_pipelines/time_series_forecasting.md)，只需要替换模型路径即可完成时序预测的模型更新。在产线集成中，你可以使用服务化部署来部署你得到的模型。

2.<b>模块集成</b>

您产出的权重可以直接集成到时序预测模块中，可以参考[快速集成](#三快速集成)的 Python 示例代码，只需要将模型替换为你训练的到的模型路径即可。