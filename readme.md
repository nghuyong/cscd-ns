<p align="center">
    <br>
    <img src=".github/cscd-ns.png" width="400"/>
    <br>
<p>
<p align="center">
<a href="https://arxiv.org/abs/2211.08788">
    <img src="https://img.shields.io/badge/arXiv-2211.08788-b31b1b.svg?style=flat"
         alt="arXiv">
  </a>
  <a href="https://github.com/nghuyong/cscd-ime/stargazers">
    <img src="https://img.shields.io/github/stars/nghuyong/cscd-ime.svg?colorA=orange&colorB=orange&logo=github"
         alt="GitHub stars">
  </a>
  <a href="https://github.com/nghuyong/cscd-ime/issues">
        <img src="https://img.shields.io/github/issues/nghuyong/cscd-ime.svg"
             alt="GitHub issues">
  </a>
  <a href="https://github.com/nghuyong/cscd-ime/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/nghuyong/cscd-ime.svg"
             alt="GitHub license">
  </a>
</p>

## Data
Due to the lack of github lsf quota, the data folder exists on Google Drive ([link](https://drive.google.com/drive/folders/1boXhoSpWyvq2kUX6FERYrOwnurGczAAR?usp=share_link)) or Baidu Netdisk ([link](https://pan.baidu.com/s/1231wwhzcipkTosPdC-46xQ?pwd=7ivq)), 
which needs to be downloaded and moved to the main directory.
 
### CSCD-NS

CSCD-NS is a Chinese Spelling Correction Dataset for Native Speakers, 
including 40,000 annotated sentences from real posts of official media on Sina Weibo.

| training set | development set | test set |  all   |
|:------------:|:---------------:|:--------:|:------:|
|    30,000    |      5,000      |  5,000   | 40,000 |

It can be found in `./data/cscd-ime`, and the data format is `label \t origin \t corrected`,
the label means whether the original sentence is correct or wrong.

### LCSTS-IME-2M

LCSTS-IME-2M is a large-scale and high-quality pseudo dataset for the CSC task, including over 2 million samples.
The data is come from LCSTS dataset and is constructed by simulating the input through pinyin IME.
It can be found in `./data/lcsts-ime-2m` and the format is the same as CSCD-IME.

## Build Pseudo Dataset

Install requirements:
```bash
pip install https://github.com/kpu/kenlm/archive/master.zip
pip install -r requirements.txt
```

Build:
```bash
cd pseudo-data-construction
python build.py
```

The script take the sentence `一不小心选到了错误的方向` as example, and you could obtain the constructed pseudo data like this:

```json
{
  "origin": "一不小心选到了错误的方向",
  "noise": "一部小心选到了错误的方向",
  "details": [
    {
      "start": 0,
      "end": 2,
      "origin_token": "一不",
      "noise_token": "一部",
      "pinyin_type": "same",
      "pinyin_token": "yibu",
      "ppl_improve": 105.68778749231029
    }
  ]
}
```

## Evaluation

We provide an evaluation script to evaluate the metric of CSC systems,
including the f1-score of detection and correction at the sentence level and character level.

```bash
cd evaluation
python evaluate.py
```

This evaluation script will evaluate the [prediction result](https://drive.google.com/file/d/1iVo1Upuf7gARuGuGrFAkZcQRhB8vYl6y/view?usp=share_link) of BERT model on CSCD-IME, and
generate [report file](https://drive.google.com/file/d/1q02kh93CCfbn8yy3MEmI3YDozjwxkVkE/view?usp=share_link).

Report file preview:

```
overview:
S_D_p:79.164
S_D_r:65.827
S_D_f1:71.882
S_C_p:70.548
S_C_r:58.663
S_C_f1:64.059
C_D_p:82.999
C_D_r:67.009
C_D_f1:74.152
C_C_p:73.591
C_C_r:59.415
C_C_f1:65.748

bad cases:
原始: 接受该报采访的患者家属与劳工组织认为，这与员工上班时接触某些含笨的清洁剂有关
正确: 接受该报采访的患者家属与劳工组织认为，这与员工上班时接触某些含【苯】的清洁剂有关
预测: 接受该报采访的患者家属与劳工组织认为，这与员工上班时接触某些含【笨】的清洁剂有关
错误类型: 漏纠
...
```

## Citation
CSCD-NS: a Chinese Spelling Check Dataset for Native Speakers [[pdf]](https://aclanthology.org/2024.acl-long.10.pdf)
```
@inproceedings{hu-etal-2024-cscd,
    title = "{CSCD}-{NS}: a {C}hinese Spelling Check Dataset for Native Speakers",
    author = "Hu, Yong  and
      Meng, Fandong  and
      Zhou, Jie",
    editor = "Ku, Lun-Wei  and
      Martins, Andre  and
      Srikumar, Vivek",
    booktitle = "Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)",
    month = aug,
    year = "2024",
    address = "Bangkok, Thailand",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.acl-long.10",
    pages = "146--159",
    abstract = "In this paper, we present CSCD-NS, the first Chinese spelling check (CSC) dataset designed for native speakers, containing 40,000 samples from a Chinese social platform. Compared with existing CSC datasets aimed at Chinese learners, CSCD-NS is ten times larger in scale and exhibits a distinct error distribution, with a significantly higher proportion of word-level errors. To further enhance the data resource, we propose a novel method that simulates the input process through an input method, generating large-scale and high-quality pseudo data that closely resembles the actual error distribution and outperforms existing methods. Moreover, we investigate the performance of various models in this scenario, including large language models (LLMs), such as ChatGPT. The result indicates that generative models underperform BERT-like classification models due to strict length and pronunciation constraints. The high prevalence of word-level errors also makes CSC for native speakers challenging enough, leaving substantial room for improvement.",
}

```
