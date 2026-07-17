# DILInet

**Multimodal fusion of histopathology and transcriptomics for interpretable drug-induced liver injury (DILI) prediction**

> Submitted to *Information Fusion*

DILInet is an interpretable information-fusion framework that integrates whole-slide images (WSIs) and transcriptomic profiles for sample-level DILI etiology prediction (drug-induced vs. spontaneous). It co-designs fusion-oriented encoders and a gated cross-modal interaction module to reconcile complementary **phenotype–mechanism** evidence.

---

## Overview

Histopathology captures tissue-level phenotype, while transcriptomics reveals molecular mechanisms—yet each modality alone yields a fragmented view of hepatotoxicity. DILInet addresses this gap with three key components:

1. **APHEnet (Active histopathology perception)**  
   Attention-entropy-guided patch selection, multi-branch MIL attention, and stochastic top-$K$ instance masking produce a compact pathology vector that emphasizes lesion-relevant morphology and suppresses normal-tissue noise.

2. **KGDEnet (Knowledge-guided transcriptomics encoding)**  
   A hybrid KEGG–STRING gene knowledge graph is injected into a Transformer encoder via graph-biased attention and graph propagation, yielding a mechanistically structured embedding.

3. **Gated cross-modal interaction**  
   Bidirectional projections and learnable gates adaptively balance original and transferred features before MLP-based classification, handling sample-wise phenotype–mechanism misalignment and heterogeneous modality reliability.

---

## Framework

```
WSI patches ──► APHEnet ──► h_path ─┐
                                    ├─► Gated Cross-Modal Fusion ──► MLP ──► DILI prediction
Gene expression ──► KGDEnet ──► h_trans ─┘
```

---

## Datasets

Experiments use strictly paired rat liver WSIs and Affymetrix microarray profiles from [Open TG-GATEs](https://toxico.nibiohn.go.jp/english/):

| Dataset | Description | Samples | Drug-induced / Spontaneous |
|---------|-------------|---------|----------------------------|
| **DHLD** | Matched lesion types (eosinophilic change, swelling, fatty degeneration, ground glass) | 617 | 377 / 240 |
| **DRCD** | Reference compounds with diverse mechanisms (WY-14643, ethionamide, MDA, thioacetamide, ethanol, vitamin A, etc.) | 405 | 215 / 190 |

### Raw data sources

- **Histopathology WSIs:**  
  https://dbarchive.biosciencedbc.jp/data/open-tggates-pathological-images/LATEST/
- **Transcriptomics (CEL files):**  
  https://dbarchive.biosciencedbc.jp/data/open-tggates/LATEST/

### Curated labels in this repository

This repository provides the curated **DHLD** and **DRCD** sample identifiers and labels used in the paper. Partitioning is performed at the WSI (slide) level; slides sharing the same `EXP_ID` are kept in the same split to avoid experimental leakage.

---

## Results (summary)

Five independent slide-level partitions (≈7:1:2). Metrics are mean ± std.

| Method | ACC (DHLD) | F1 (DHLD) | ACC (DRCD) | F1 (DRCD) |
|--------|------------|-----------|------------|-----------|
| Best unimodal (DTFD / CLAM-SB) | 0.9171 | 0.9171 | 0.8900 | 0.8900 |
| **DILInet** | **0.9339** | **0.9344** | **0.9062** | **0.9044** |

Ablations show that gated fusion provides the largest gains; active perception and knowledge-graph guidance further improve fusion-ready representations. Attention heatmaps and KEGG pathway enrichment support biological interpretability.

---

## Repository contents

```
DILInet/
├── README.md
├── data/                 # Curated sample IDs and labels (DHLD / DRCD)
└── (code release)        # Training / inference scripts (if included)
```

> If code is not yet included, please check Releases or contact the corresponding authors. Training completes in approximately 4–6 hours per dataset on a single NVIDIA RTX 4090 GPU.

---

## Citation

If you use this work, please cite:

```bibtex
@article{zhang2026dilinet,
  title   = {DILInet: multimodal fusion of histopathology and transcriptomics for interpretable drug-induced liver injury prediction},
  author  = {Zhang, Guangyu and Wang, Hong and Cheng, Xingfu and Zhao, Jun and Sheng, Xiehuang and Sun, Yanshen},
  journal = {Information Fusion},
  year    = {2026},
  note    = {Under review}
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

We gratefully acknowledge the Open TG-GATEs database for providing the histopathology whole-slide images and transcriptomic datasets used in this study.

This work was supported by the National Natural Science Foundation of China (62072290, 62372279, 62573277); the Natural Science Foundation of Shandong Province (ZR2025QB62, ZR2023MF119); and the Jinan “20 new colleges and universities” Funded Project (202228110).

---

## License

Please respect the usage terms of Open TG-GATEs when redistributing or deriving from the original WSI and microarray data. Curated labels in this repository are released for research purposes.
