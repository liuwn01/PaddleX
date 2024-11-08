---
comments: true
---

# PaddleX模型列表（海光 DCU）

PaddleX 内置了多条产线，每条产线都包含了若干模块，每个模块包含若干模型，具体使用哪些模型，您可以根据下边的 benchmark 数据来选择。如您更考虑模型精度，请选择精度较高的模型，如您更考虑模型存储大小，请选择存储大小较小的模型。

## 图像分类模块
<table>
<thead>
<tr>
<th>模型名称</th>
<th>Top1 Acc（%）</th>
<th>模型存储大小（M)</th>
</tr>
</thead>
<tbody>
<tr>
<td>ResNet18</td>
<td>71.0</td>
<td>41.5 M</td>
</tr>
<tr>
<td>ResNet34</td>
<td>74.6</td>
<td>77.3 M</td>
</tr>
<tr>
<td>ResNet50</td>
<td>76.5</td>
<td>90.8 M</td>
</tr>
<tr>
<td>ResNet101</td>
<td>77.6</td>
<td>158.7 M</td>
</tr>
<tr>
<td>ResNet152</td>
<td>78.3</td>
<td>214.2 M</td>
</tr>
</tbody>
</table>
<b>注：以上精度指标为</b>[ImageNet-1k](https://www.image-net.org/index.php)<b>验证集 Top1 Acc。</b>

## 语义分割模块
<table>
<thead>
<tr>
<th>模型名称</th>
<th>mloU（%）</th>
<th>模型存储大小（M)</th>
</tr>
</thead>
<tbody>
<tr>
<td>Deeplabv3_Plus-R50</td>
<td>80.36</td>
<td>94.9 M</td>
</tr>
<tr>
<td>Deeplabv3_Plus-R101</td>
<td>81.10</td>
<td>162.5 M</td>
</tr>
</tbody>
</table>
<b>注：以上精度指标为</b>[Cityscapes](https://www.cityscapes-dataset.com/)<b>数据集 mloU。</b>