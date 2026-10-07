# DILInet

**Gated fusion of whole-slide images and transcriptomics for drug-induced liver injury etiology classification**

> Data release for a manuscript prepared for *Pattern Recognition*

DILInet classifies the etiology of a liver lesion (drug-induced versus spontaneous) from a paired whole-slide image and a transcriptomic profile. This repository publishes the curated sample identifiers, labels, and five-fold compound-holdout assignments for the two cohorts used in the study. Whole-slide images, microarray CEL files, patch features, knowledge graphs, model code, and trained weights are not included.

---

## File

The release is one table, [`fold_assignments.csv`](fold_assignments.csv). It has 1,022 rows: 617 DHLD slides, then 405 DRCD slides. One row is one slide.

| Dataset | Samples | Drug-induced (`1`) | Spontaneous (`0`) | Compounds |
|---------|---------|--------------------|-------------------|-----------|
| DHLD | 617 | 377 | 240 | 83 |
| DRCD | 405 | 215 | 190 | 17 |

```text
dataset,slide_id,label,compound_name,fold_0,fold_1,fold_2,fold_3,fold_4
DHLD,10109,0,glibenclamide,train,test,train,train,train
```

- `slide_id` is the Open TG-GATEs liver-slide identifier. The matching image file is `{slide_id}.svs`.
- `label` is the etiology. `1` is drug-induced and `0` is spontaneous.
- `compound_name` is the compound kept inside one split. Dose, duration, and `EXP_ID` are not columns; they follow the Open TG-GATEs annotation of the same slide.
- `fold_0` through `fold_4` are the five folds. Each cell is `train`, `val`, or `test`. `val` is the validation split used to choose that fold's decision threshold.

Each row is one strictly paired sample: one H&E whole-slide image and one Affymetrix profile from the same animal. No pair is imputed. Image paths, microarray files, and knowledge-graph edges are not in this file.

---

## Cohorts

Both cohorts are built from paired rat liver slides and Affymetrix profiles in [Open TG-GATEs](https://toxico.nibiohn.go.jp/english/). `SP_FLG` marks a recorded lesion as spontaneous or drug-induced.

| Dataset | Question | Inclusion |
|---------|----------|-----------|
| **DHLD** | Can etiology be separated when the diagnosis matches? | Slide label: any treatment-related liver finding (`SP_FLG` false) is drug-induced. If every finding is spontaneous, the label follows the highest-grade finding and is spontaneous. A compound need not have a single label. |
| **DRCD** | Does fusion still help for mechanistically diverse reference compounds? | The same slide rule, then one label per compound: the majority of its slides. More spontaneous slides makes the whole compound spontaneous; more drug-induced slides makes it drug-induced. A minority slide keeps the compound label. |

### Raw data

The images and CEL files are distributed by Open TG-GATEs, not by this repository:

- Histopathology WSIs: https://dbarchive.biosciencedbc.jp/data/open-tggates-pathological-images/LATEST/
- Affymetrix CEL files: https://dbarchive.biosciencedbc.jp/data/open-tggates/LATEST/

---

## Fold assignments

The manuscript uses five-fold compound hold-out. Every slide of a compound, including every dose, duration, and `EXP_ID`, is placed in exactly one of train, validation, or test. The target ratio is about 7:1:2, and the exact counts follow compound boundaries. Expression normalization, the 1000 highly variable genes, and the KEGG–STRING graph are fit on the training compounds of that fold only. Those matrices and graphs are not in this release.

Slides of the same `compound_name` share one split inside a fold. Each slide is in `test` in exactly one fold, and the five test sets cover the cohort.

| Dataset | Fold | Train | Validation | Test |
|---------|------|-------|------------|------|
| DHLD | 0 | 434 | 59 | 124 |
| DHLD | 1 | 438 | 56 | 123 |
| DHLD | 2 | 437 | 57 | 123 |
| DHLD | 3 | 438 | 56 | 123 |
| DHLD | 4 | 437 | 56 | 124 |
| DRCD | 0 | 294 | 36 | 75 |
| DRCD | 1 | 270 | 50 | 85 |
| DRCD | 2 | 281 | 50 | 74 |
| DRCD | 3 | 270 | 50 | 85 |
| DRCD | 4 | 269 | 50 | 86 |

---

## Reported test performance

The numbers below are the manuscript results: mean ± sample standard deviation across the five compound-holdout test folds. The decision threshold of each fold is chosen on that fold's validation set.

| Dataset | ACC | BalAcc | weighted F1 | MCC |
|---------|-----|--------|-------------|-----|
| DHLD | 0.8138 ± 0.1017 | 0.8356 ± 0.0747 | 0.8113 ± 0.1077 | 0.6756 ± 0.1301 |
| DRCD | 0.7506 ± 0.1695 | 0.7549 ± 0.1566 | 0.7209 ± 0.2116 | 0.5521 ± 0.2774 |

DILInet has the highest mean accuracy, balanced accuracy, weighted F1, and Matthews correlation coefficient on both datasets, among seven pathology models and five transcriptomic models trained on the same splits. DRCD is the harder cohort: each test fold removes a larger share of the 17 compounds, and the fold-to-fold spread is wider.

---

## Model

DILInet trains three parts jointly:

1. **APHEnet** selects training patches by the predictive entropy of the fused classifier, then aggregates the selected bag with multi-branch MIL attention and stochastic top-\(K\) instance masking. Patch selection uses both modalities and does not require patch labels.
2. **KGDEnet** encodes the transcriptome with a Transformer. A KEGG–STRING graph built inside the training fold biases self-attention and propagates hidden states along gene–gene edges.
3. **Gated cross-modal interaction** exchanges information between the two sample-level vectors through bidirectional projections and learnable gates, then classifies etiology with an MLP.

```text
WSI patches ──► APHEnet ──► h_path ─┐
                                    ├─► Gated cross-modal fusion ──► MLP ──► etiology
Gene expression ──► KGDEnet ──► h_trans ─┘
```

Training and inference code are not part of this release.

---

## Citation

```bibtex
@article{zhang2026dilinet,
  title  = {DILInet: Gated fusion of whole-slide images and transcriptomics for drug-induced liver injury etiology classification},
  author = {Zhang, Guangyu and Wang, Hong and Cheng, Xingfu and Zhao, Jun and Sheng, Xiehuang and Yu, Jianger},
  year   = {2026},
  note   = {Manuscript in preparation for Pattern Recognition}
}
```

---

## Contact

- **Hong Wang** (corresponding author) — 111052@sdnu.edu.cn  
  School of Computer Science and Artificial Intelligence, Shandong Normal University
- **Jianger Yu** (corresponding author) — jiangeryu@gmail.com  
  Department of Computer Science, Virginia Tech

---

## Acknowledgements

We gratefully acknowledge the Open TG-GATEs database for the histopathology whole-slide images and transcriptomic profiles used in this study.

This work was supported by the National Natural Science Foundation of China (61672329, 62072290, 62573277), and the Jinan “20 new colleges and universities” Funded Project (202228110).

---

## License

Please follow the Open TG-GATEs terms of use for the original whole-slide images and microarray files. The curated identifier, label, and fold-assignment table in this repository is released for research use.
