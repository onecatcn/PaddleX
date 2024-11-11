---
comments: true
---

# Instance Segmentation Module Development Tutorial

## I. Overview
The instance segmentation module is a crucial component in computer vision systems, responsible for identifying and marking pixels that contain specific object instances in images or videos. The performance of this module directly impacts the accuracy and efficiency of the entire computer vision system. The instance segmentation module typically outputs pixel-level masks (masks) for each target instance, which are then passed as input to the object recognition module for subsequent processing.

## II. Supported Model List

<table>
    <tr>
        <th>Model</th>
        <th>Mask AP</th>
        <th>GPU Inference Time (ms)</th>
        <th>CPU Inference Time (ms)</th>
        <th>Model Size (M)</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Mask-RT-DETR-H</td>
        <td>50.6</td>
        <td>132.693</td>
        <td>4896.17</td>
        <td>449.9 M</td>
        <td rowspan="5">Mask-RT-DETR is an instance segmentation model based on RT-DETR. By adopting the high-performance PP-HGNetV2 as the backbone network and constructing a MaskHybridEncoder encoder, along with introducing IOU-aware Query Selection technology, it achieves state-of-the-art (SOTA) instance segmentation accuracy with the same inference time.</td>
    </tr>
    <tr>
        <td>Mask-RT-DETR-L</td>
        <td>45.7</td>
        <td>46.5059</td>
        <td>2575.92</td>
        <td>113.6 M</td>
    </tr>
    </table>

> ❗ The above list features the <b>2 core models</b> that the image classification module primarily supports. In total, this module supports <b>15 models</b>. The complete list of models is as follows:

<details><summary> 👉Model List Details</summary>

<table>
<tr>
<th>Model</th>
<th>Mask AP</th>
<th>GPU Inference Time (ms)</th>
<th>CPU Inference Time (ms)</th>
<th>Model Size (M)</th>
<th>Description</th>
</tr>
<tr>
<td>Cascade-MaskRCNN-ResNet50-FPN</td>
<td>36.3</td>
<td >-</td>
<td >-</td>
<td>254.8 M</td>
<td rowspan="2">Cascade-MaskRCNN is an improved Mask RCNN instance segmentation model that utilizes multiple detectors in a cascade, optimizing segmentation results by leveraging different IOU thresholds to address the mismatch between detection and inference stages, thereby enhancing instance segmentation accuracy.</td>
</tr>
<tr>
<td>Cascade-MaskRCNN-ResNet50-vd-SSLDv2-FPN</td>
<td>39.1</td>
<td >-</td>
<td >-</td>
<td>254.7 M</td>
</tr>
<tr>
<td>Mask-RT-DETR-H</td>
<td>50.6</td>
<td>132.693</td>
<td>4896.17</td>
<td>449.9 M</td>
<td rowspan="5">Mask-RT-DETR is an instance segmentation model based on RT-DETR. By adopting the high-performance PP-HGNetV2 as the backbone network and constructing a MaskHybridEncoder encoder, along with introducing IOU-aware Query Selection technology, it achieves state-of-the-art (SOTA) instance segmentation accuracy with the same inference time.</td>
</tr>
<tr>
<td>Mask-RT-DETR-L</td>
<td>45.7</td>
<td>46.5059</td>
<td>2575.92</td>
<td>113.6 M</td>
</tr>
<tr>
<td>Mask-RT-DETR-M</td>
<td>42.7</td>
<td>36.8329</td>
<td>-</td>
<td>66.6 M</td>
</tr>
<tr>
<td>Mask-RT-DETR-S</td>
<td>41.0</td>
<td>33.5007</td>
<td>-</td>
<td>51.8 M</td>
</tr>
<tr>
<td>Mask-RT-DETR-X</td>
<td>47.5</td>
<td>75.755</td>
<td>3358.04</td>
<td>237.5 M</td>
</tr>
<tr>
<td>MaskRCNN-ResNet50-FPN</td>
<td>35.6</td>
<td>-</td>
<td>-</td>
<td>157.5 M</td>
<td rowspan="6">Mask R-CNN is a full-task deep learning model from Facebook AI Research (FAIR) that can perform object classification and localization in a single model, combined with image-level masks to complete segmentation tasks.</td>
</tr>
<tr>
<td>MaskRCNN-ResNet50-vd-FPN</td>
<td>36.4</td>
<td>-</td>
<td>-</td>
<td>157.5 M</td>
</tr>
<tr>
<td>MaskRCNN-ResNet50</td>
<td>32.8</td>
<td>-</td>
<td>-</td>
<td>128.7 M</td>
</tr>
<tr>
<td>MaskRCNN-ResNet101-FPN</td>
<td>36.6</td>
<td>-</td>
<td>-</td>
<td>225.4 M</td>
</tr>
<tr>
<td>MaskRCNN-ResNet101-vd-FPN</td>
<td>38.1</td>
<td>-</td>
<td>-</td>
<td>225.1 M</td>
</tr>
<tr>
<td>MaskRCNN-ResNeXt101-vd-FPN</td>
<td>39.5</td>
<td>-</td>
<td>-</td>
<td>370.0 M</td>
<td></td>
</tr>
<tr>
<td>PP-YOLOE_seg-S</td>
<td>32.5</td>
<td>-</td>
<td>-</td>
<td>31.5 M</td>
<td>PP-YOLOE_seg is an instance segmentation model based on PP-YOLOE. This model inherits PP-YOLOE's backbone and head, significantly enhancing instance segmentation performance and inference speed through the design of a PP-YOLOE instance segmentation head.</td>
</tr>
<tr>
<td>SOLOv2</td>
<td>35.5</td>
<td>-</td>
<td>-</td>
<td>179.1 M</td>
<td> SOLOv2 is a real-time instance segmentation algorithm that segments objects by location. This model is an improved version of SOLO, achieving a good balance between accuracy and speed through the introduction of mask learning and mask NMS.</td>
</tr>
</table>

<p><b>Note: The above accuracy metrics are based on the Mask AP of the <a href="https://cocodataset.org/#home">COCO2017</a> validation set. All GPU inference times are based on an NVIDIA Tesla T4 machine with FP32 precision. CPU inference speeds are based on an Intel(R) Xeon(R) Gold 5117 CPU @ 2.00GHz with 8 threads and FP32 precision.</b></p></details>

## <span id="lable">III. Quick Integration</span>
> ❗ Before quick integration, please install the PaddleX wheel package. For detailed instructions, refer to the [PaddleX Local Installation Tutorial](../../../installation/installation.en.md)

After installing the wheel package, a few lines of code can complete the inference of the instance segmentation module. You can switch models under this module freely, and you can also integrate the model inference of the instance segmentation module into your project. Before running the following code, please download the [demo image](https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_instance_segmentation_004.png) to your local machine.

```python
from paddlex import create_model
model = create_model("Mask-RT-DETR-L")
output = model.predict("general_instance_segmentation_004.png", batch_size=1)
for res in output:
    res.print(json_format=False)
    res.save_to_img("./output/")
    res.save_to_json("./output/res.json")
```
For more information on using PaddleX's single-model inference APIs, please refer to the [PaddleX Single-Model Python Script Usage Instructions](../../instructions/model_python_API.en.md).

## IV. Custom Development
If you are seeking higher accuracy from existing models, you can use PaddleX's custom development capabilities to develop better instance segmentation models. Before using PaddleX to develop instance segmentation models, please ensure that you have installed the relevant model training plugins for segmentation in PaddleX. The installation process can be found in the custom development section of the [PaddleX Local Installation Guide](../../../installation/installation.en.md).

### 4.1 Data Preparation
Before model training, it is necessary to prepare the corresponding dataset for each task module. PaddleX provides data verification functionality for each module, and <b>only data that passes the verification can be used for model training</b>. Additionally, PaddleX provides demo datasets for each module, allowing you to complete subsequent development based on the officially provided demo data. If you wish to use a private dataset for subsequent model training, you can refer to the [PaddleX Instance Segmentation Task Module Data Annotation Tutorial](../../../data_annotations/cv_modules/instance_segmentation.en.md).

#### 4.1.1 Download Demo Data

You can download the demo dataset to a specified folder using the following command:

```bash
wget https://paddle-model-ecology.bj.bcebos.com/paddlex/data/instance_seg_coco_examples.tar -P ./dataset
tar -xf ./dataset/instance_seg_coco_examples.tar -C ./dataset/
```

#### 4.1.2 Data Verification
Data verification can be completed with a single command:

```bash
python main.py -c paddlex/configs/instance_segmentation/Mask-RT-DETR-L.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/instance_seg_coco_examples
```

After executing the above command, PaddleX will validate the dataset and summarize its basic information. If the command runs successfully, it will print `Check dataset passed !` in the log. The validation results file is saved in `./output/check_dataset_result.json`, and related outputs are saved in the `./output/check_dataset` directory in the current directory, including visual examples of sample images and sample distribution histograms.
<details><summary>👉 <b>Details of Validation Results (Click to Expand)</b></summary>

<p>The specific content of the validation result file is:</p>
<pre><code class="language-bash">{
  &quot;done_flag&quot;: true,
  &quot;check_pass&quot;: true,
  &quot;attributes&quot;: {
    &quot;num_classes&quot;: 2,
    &quot;train_samples&quot;: 79,
    &quot;train_sample_paths&quot;: [
      &quot;check_dataset/demo_img/pexels-photo-634007.jpeg&quot;,
      &quot;check_dataset/demo_img/pexels-photo-59576.png&quot;
    ],
    &quot;val_samples&quot;: 19,
    &quot;val_sample_paths&quot;: [
      &quot;check_dataset/demo_img/peasant-farmer-farmer-romania-botiza-47862.jpeg&quot;,
      &quot;check_dataset/demo_img/pexels-photo-715546.png&quot;
    ]
  },
  &quot;analysis&quot;: {
    &quot;histogram&quot;: &quot;check_dataset/histogram.png&quot;
  },
  &quot;dataset_path&quot;: &quot;./dataset/instance_seg_coco_examples&quot;,
  &quot;show_type&quot;: &quot;image&quot;,
  &quot;dataset_type&quot;: &quot;COCOInstSegDataset&quot;
}
</code></pre>
<p>In the above verification results, <code>check_pass</code> being <code>True</code> indicates that the dataset format meets the requirements. Explanations for other indicators are as follows:</p>
<ul>
<li><code>attributes.num_classes</code>: The number of classes in this dataset is 2;</li>
<li><code>attributes.train_samples</code>: The number of training samples in this dataset is 79;</li>
<li><code>attributes.val_samples</code>: The number of validation samples in this dataset is 19;</li>
<li><code>attributes.train_sample_paths</code>: A list of relative paths to the visualized training samples in this dataset;</li>
<li><code>attributes.val_sample_paths</code>: A list of relative paths to the visualized validation samples in this dataset;
Additionally, the dataset verification also analyzes the distribution of sample numbers across all categories in the dataset and generates a distribution histogram (<code>histogram.png</code>):</li>
</ul>
<p><img src="https://raw.githubusercontent.com/cuicheng01/PaddleX_doc_images/main/images/modules/instanceseg/01.png"></p></details>

#### 4.1.3 Dataset Format Conversion/Dataset Splitting (Optional)
After completing data verification, you can convert the dataset format or re-split the training/validation ratio by <b>modifying the configuration file</b> or <b>appending hyperparameters</b>.

<details><summary>👉 <b>Details of Format Conversion/Dataset Splitting (Click to Expand)</b></summary>

<p><b>(1) Dataset Format Conversion</b></p>
<p>The instance segmentation task supports converting <code>LabelMe</code> format to <code>COCO</code> format. The parameters for dataset format conversion can be set by modifying the fields under <code>CheckDataset</code> in the configuration file. Below are some example explanations for some of the parameters in the configuration file:</p>
<ul>
<li><code>CheckDataset</code>:</li>
<li><code>convert</code>:</li>
<li><code>enable</code>: Whether to perform dataset format conversion. Set to <code>True</code> to enable dataset format conversion, default is <code>False</code>;</li>
<li><code>src_dataset_type</code>: If dataset format conversion is performed, the source dataset format needs to be set. The available source format is <code>LabelMe</code>;
For example, if you want to convert a <code>LabelMe</code> dataset to <code>COCO</code> format, you need to modify the configuration file as follows:</li>
</ul>
<pre><code class="language-bash">cd /path/to/paddlex
wget https://paddle-model-ecology.bj.bcebos.com/paddlex/data/instance_seg_labelme_examples.tar -P ./dataset
tar -xf ./dataset/instance_seg_labelme_examples.tar -C ./dataset/
</code></pre>
<pre><code class="language-bash">......
CheckDataset:
  ......
  convert:
    enable: True
    src_dataset_type: LabelMe
  ......
</code></pre>
<p>Then execute the command:</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/instance_segmentation/Mask-RT-DETR-L.yaml\
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/instance_seg_labelme_examples
</code></pre>
<p>After the data conversion is executed, the original annotation files will be renamed to <code>xxx.bak</code> in the original path.</p>
<p>The above parameters also support being set by appending command line arguments:</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/instance_segmentation/Mask-RT-DETR-L.yaml\
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/instance_seg_labelme_examples \
    -o CheckDataset.convert.enable=True \
    -o CheckDataset.convert.src_dataset_type=LabelMe
</code></pre>
<p><b>(2) Dataset Splitting</b></p>
<p>The parameters for dataset splitting can be set by modifying the fields under <code>CheckDataset</code> in the configuration file. Some example explanations for the parameters in the configuration file are as follows:</p>
<ul>
<li><code>CheckDataset</code>:</li>
<li><code>split</code>:</li>
<li><code>enable</code>: Whether to re-split the dataset. When set to <code>True</code>, the dataset will be re-split. The default is <code>False</code>;</li>
<li><code>train_percent</code>: If the dataset is to be re-split, the percentage of the training set needs to be set. The type is any integer between 0-100, and the sum with <code>val_percent</code> must be 100;</li>
</ul>
<p>For example, if you want to re-split the dataset with a 90% training set and a 10% validation set, you need to modify the configuration file as follows:</p>
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
<pre><code class="language-bash">python main.py -c paddlex/configs/instance_segmentation/Mask-RT-DETR-L.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/instance_seg_labelme_examples
</code></pre>
<p>After data splitting, the original annotation files will be renamed as <code>xxx.bak</code> in the original path.</p>
<p>The above parameters can also be set by appending command line arguments:</p>
<pre><code class="language-bash">python main.py -c paddlex/configs/instance_segmentation/Mask-RT-DETR-L.yaml \
    -o Global.mode=check_dataset \
    -o Global.dataset_dir=./dataset/instance_seg_labelme_examples \
    -o CheckDataset.split.enable=True \
    -o CheckDataset.split.train_percent=90 \
    -o CheckDataset.split.val_percent=10
</code></pre></details>

### 4.2 Model Training
A single command can complete model training. Taking the training of the instance segmentation model Mask-RT-DETR-L as an example:

```bash
python main.py -c paddlex/configs/instance_segmentation/Mask-RT-DETR-L.yaml \
    -o Global.mode=train \
    -o Global.dataset_dir=./dataset/instance_seg_coco_examples
```
The following steps are required:

* Specify the path to the `.yaml` configuration file of the model (here it is `Mask-RT-DETR-L.yaml`,When training other models, you need to specify the corresponding configuration files. The relationship between the model and configuration files can be found in the [PaddleX Model List (CPU/GPU)](../../../support_list/models_list.en.md))
* Specify the mode as model training: `-o Global.mode=train`
* Specify the path to the training dataset: `-o Global.dataset_dir`.
Other related parameters can be set by modifying the fields under `Global` and `Train` in the `.yaml` configuration file, or adjusted by appending parameters in the command line. For example, to specify the first 2 GPUs for training: `-o Global.device=gpu:0,1`; to set the number of training epochs to 10: `-o Train.epochs_iters=10`. For more modifiable parameters and their detailed explanations, refer to the [PaddleX Common Configuration File Parameters Instructions](../../instructions/config_parameters_common.en.md).

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
python main.py -c paddlex/configs/instance_segmentation/Mask-RT-DETR-L.yaml \
    -o Global.mode=evaluate \
    -o Global.dataset_dir=./dataset/instance_seg_coco_examples
```
Similar to model training, the following steps are required:

* Specify the `.yaml` configuration file path for the model (here it is `Mask-RT-DETR-L.yaml`)
* Specify the mode as model evaluation: `-o Global.mode=evaluate`
* Specify the path to the validation dataset: `-o Global.dataset_dir`. Other related parameters can be set by modifying the `Global` and `Evaluate` fields in the `.yaml` configuration file. For details, refer to [PaddleX Common Model Configuration File Parameter Description](../../instructions/config_parameters_common.en.md).

<details><summary>👉 <b>More Details (Click to Expand)</b></summary>

<p>When evaluating the model, you need to specify the model weights file path. Each configuration file has a default weight save path built-in. If you need to change it, simply set it by appending a command line parameter, such as <code>-o Evaluate.weight_path=./output/best_model/best_model.pdparams</code>.</p>
<p>After completing the model evaluation, an <code>evaluate_result.json</code> file will be generated, which records the evaluation results, specifically whether the evaluation task was completed successfully and the model's evaluation metrics, including AP.</p></details>


### <b>4.4 Model Inference and Model Integration</b>
After completing model training and evaluation, you can use the trained model weights for inference prediction or Python integration.

#### 4.4.1 Model Inference
To perform inference prediction via the command line, simply use the following command. Before running the following code, please download the [demo image](https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_instance_segmentation_004.png) to your local machine.

```bash
python main.py -c paddlex/configs/instance_segmentation/Mask-RT-DETR-L.yaml \
    -o Global.mode=predict \
    -o Predict.model_dir="./output/best_model/inference" \
    -o Predict.input="general_instance_segmentation_004.png"
```
Similar to model training and evaluation, the following steps are required:

* Specify the `.yaml` configuration file path of the model (here it's `Mask-RT-DETR-L.yaml`)
* Specify the mode as model inference prediction: `-o Global.mode=predict`
* Specify the model weights path: `-o Predict.model_dir="./output/best_model/inference"`
* Specify the input data path: `-o Predict.input="..."`. Other related parameters can be set by modifying the `Global` and `Predict` fields in the `.yaml` configuration file. For details, refer to [PaddleX Common Model Configuration File Parameter Description](../../instructions/config_parameters_common.en.md).

#### 4.4.2 Model Integration
The model can be directly integrated into the PaddleX Pipeline or into your own project.

1.<b>Pipeline Integration</b>

The instance segmentation module can be integrated into the [General Instance Segmentation Pipeline](../../../pipeline_usage/tutorials/cv_pipelines/instance_segmentation.en.md) of PaddleX. Simply replace the model path to update the instance segmentation module of the relevant pipeline.

2.<b>Module Integration</b>
The weights you produce can be directly integrated into the instance segmentation module. Refer to the Python example code in <a href="#lable">Quick Integration</a> , and simply replace the model with the path to your trained model.