# protein-mutation-scanner

Scores single amino-acid substitutions in a protein sequence using the ESM-2 protein language model (`facebook/esm2_t33_650M_UR50D`).

## Status

| Stage | Module | Status |
|---|---|---|
| 1. Sequence loading and validation | `src/sequence.py` | In progress: API defined, implementation and tests pending |
| 2. Masked inputs | `src/masking.py` | Not started |
| 3. Model loading and inference | `src/model.py` | Not started (model download and tokenizer verified) |
| 4–5. Mutation scoring | `src/scoring.py` | Not started |
| 8–10. Single-protein benchmark | `benchmark/run_one.py` | Not started |
| CLI | `src/cli.py` | Later |

## Stage 1: sequences

`src/sequence.py` turns a FASTA file into a clean protein sequence that later stages can trust.

```python
from src.sequence import load_sequence, validate, AA

seq = load_sequence("data/my_protein.fasta")  # first record only, validated
validate("MKTAYIAKQR")                        # returns the sequence, or raises
```

- `AA = "ACDEFGHIKLMNPQRSTVWY"`: the 20 standard amino acids. This is the alphabet for validation and for the substitutions scored later.
- `load_sequence(fasta_path)` reads the **first** record of a FASTA file and returns it validated.
- `validate(seq)` raises if the sequence contains anything other than the 20 standard amino acids (e.g. `X`, `B`, `Z`, `U`, `*`, gaps or lowercase letters).

### Indexing convention

All positions are **1-based**, matching UniProt and standard mutation notation. For example, `A123V` means residue 123 is alanine and changes to valine.

The ESM-2 tokenizer adds a `<cls>` token at index 0 and `<eos>` at the end. So for residue position `p`:

| Thing | Index |
|---|---|
| Residue in mutation notation | `p` |
| Python string index | `seq[p - 1]` |
| ESM-2 token index | `p` |

`tests/test_indexing.py` will pin this mapping down so that masking (Stage 2) and scoring (Stages 4–5) can't drift by one.

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

The first model load downloads about 2.5 GB of ESM-2 weights into the Hugging Face cache (`~/.cache/huggingface/hub`).
