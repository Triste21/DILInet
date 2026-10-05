# DILInet

**Gated fusion of whole-slide images and transcriptomics for drug-induced liver injury etiology classification**

> Data release for a manuscript prepared for *Pattern Recognition*

DILInet classifies the etiology of a liver lesion (drug-induced versus spontaneous) from a paired whole-slide image and a transcriptomic profile. This repository publishes the curated sample identifiers and labels for the two cohorts used in the study. Whole-slide images, microarray CEL files, patch features, knowledge graphs, fold assignments, model code, and trained weights are not included.

---

## Files

| File | Samples | Drug-induced (`1`) | Spontaneous (`0`) | Compounds |
|------|---------|--------------------|-------------------|-----------|
| [`DHLD_label.csv`](DHLD_label.csv) | 617 | 377 | 240 | 83 |
| [`DRCD_label.csv`](DRCD_label.csv) | 405 | 215 | 190 | 17 |

Both files have the same two columns and no header beyond the first row:

```text
slide_id,label
51532,1
25598,0
```

- `slide_id` is the Open TG-GATEs liver-slide identifier. The matching image file is `{slide_id}.svs`.
- `label` is the etiology. `1` is drug-induced and `0` is spontaneous. Drug-induced injury is the positive class in the reported sensitivity and specificity.

Each row is one strictly paired sample: one H&E whole-slide image and one Affymetrix profile from the same animal. No pair is imputed. Compound name, dose, duration, `EXP_ID`, and fold assignment are not columns of these tables; they are recovered from the Open TG-GATEs annotation of the same slide.

---

## Cohorts

Both cohorts are built from paired rat liver slides and Affymetrix profiles in [Open TG-GATEs](https://toxico.nibiohn.go.jp/english/). `SP_FLG` marks a recorded lesion as spontaneous or drug-induced.

| Dataset | Question | Inclusion |
|---------|----------|-----------|
| **DHLD** | Can etiology be separated when the diagnosis matches? | Eosinophilic change, swelling, fatty degeneration, or ground glass appearance. If several lesions coexist, the highest-grade lesion is kept. Every lesion type occurs in both etiology groups. A compound need not have a single label. |
| **DRCD** | Does fusion still help for mechanistically diverse reference compounds? | Drug-induced lesions from WY-14643, ethionamide, methylene dianiline, thioacetamide, ethanol, and vitamin A, together with spontaneous lesions. In this cohort a compound has one label. |

### Raw data

The images and CEL files are distributed by Open TG-GATEs, not by this repository:

- Histopathology WSIs: https://dbarchive.biosciencedbc.jp/data/open-tggates-pathological-images/LATEST/
- Affymetrix CEL files: https://dbarchive.biosciencedbc.jp/data/open-tggates/LATEST/

---

## How these lists are evaluated

The manuscript uses five-fold compound hold-out. Every slide of a compound, including every dose, duration, and `EXP_ID`, is placed in exactly one of train, validation, or test. The target ratio is about 7:1:2, and the exact counts follow compound boundaries. Expression normalization, the 1000 highly variable genes, and the KEGG–STRING graph are fit on the training compounds of that fold only.

The two CSV files identify the samples that enter this protocol. They do not store the fold each slide was assigned to.

---

## Reported test performance

The numbers below are the manuscript results: mean ± sample standard deviation across the five compound-holdout test folds. The decision threshold of each fold is chosen on that fold's validation set.

| Dataset | ACC | BalAcc | weighted F1 | MCC | Sens | Spec |
|---------|-----|--------|-------------|-----|------|------|
| DHLD | 0.8138 ± 0.1017 | 0.8356 ± 0.0747 | 0.8113 ± 0.1077 | 0.6756 ± 0.1301 | 0.7379 ± 0.2004 | 0.9333 ± 0.0742 |
| DRCD | 0.7506 ± 0.1695 | 0.7549 ± 0.1566 | 0.7209 ± 0.2116 | 0.5521 ± 0.2774 | 0.7799 ± 0.3744 | 0.7298 ± 0.2515 |

DILInet has the highest mean accuracy, balanced accuracy, weighted F1, and Matthews correlation coefficient on both datasets, among seven pathology models and five transcriptomic models trained on the same splits. On DHLD, T-GEM has the highest sensitivity and CLAM-SB the highest specificity. On DRCD, the 1D-CNN has the highest sensitivity and CLAM-MB the highest specificity. DRCD is the harder cohort: each test fold removes a larger share of the 17 compounds, and the fold-to-fold spread is wider.

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
  author = {Zhang, Guangyu and Wang, Hong and Cheng, Xingfu and Zhao, Jun and Sheng, Xiehuang and Sun, Yanshen},
  year   = {2026},
  note   = {Manuscript in preparation for Pattern Recognition}
}
```

---

## Contact

- **Hong Wang** (corresponding author) — 111052@sdnu.edu.cn  
  School of Computer Science and Artificial Intelligence, Shandong Normal University
- **Yanshen Sun** (corresponding author) — yansh93@vt.edu  
  Department of Computer Science, Virginia Tech

---

## Acknowledgements

We gratefully acknowledge the Open TG-GATEs database for the histopathology whole-slide images and transcriptomic profiles used in this study.

This work was supported by the National Natural Science Foundation of China (62072290, 62372279, 62573277); the Natural Science Foundation of Shandong Province (ZR2025QB62, ZR2023MF119); and the Jinan “20 new colleges and universities” Funded Project (202228110).

---

## License

Please follow the Open TG-GATEs terms of use for the original whole-slide images and microarray files. The curated identifier and label tables in this repository are released for research use.
