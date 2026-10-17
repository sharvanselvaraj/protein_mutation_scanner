# protein-mutation-scanner

Scores single amino-acid substitutions in a protein sequence.

## Layout

| Path | Purpose |
|---|---|
| `src/sequence.py` | Stage 1: sequence loading and indexing |
| `src/masking.py` | Stage 2: masked inputs |
| `src/model.py` | Stage 3: model loading and inference |
| `src/scoring.py` | Stages 4 and 5: mutation scoring |
| `src/cli.py` | Command-line interface (later) |
| `benchmark/run_one.py` | Stages 8 to 10: single-protein benchmark |
| `tests/` | Tests |
| `notebooks/scratch.ipynb` | Exploration only, never the source of truth |
| `data/`, `results/` | Local inputs and outputs (gitignored) |

## Setup

```bash
conda env create -f environment.yml
conda activate pms
pytest
```
