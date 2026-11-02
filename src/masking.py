"""Stage 2: build the masked batch for a sequence."""

import torch

# Tokenizer layout, verified 2026-10-17 on facebook/esm2_t33_650M_UR50D
#   <cls> M K T A Y I A K <eos>
#     0   1 2 3 4 5 6 7 8   9
# Therefore: token_index == biological_position (1 based)

MASK_ID = 32


def token_index(bio_pos: int) -> int:
    """Token array index for a 1 based biological position."""
    return bio_pos


def build_masked_batch(seq: str, tokenizer) -> torch.Tensor:
    """Return shape [L, L+2]: one row per residue, that residue masked.

    Row i corresponds to biological position i + 1.
    """
    L = len(seq)

    enc = tokenizer(seq, return_tensors="pt")
    ids = enc["input_ids"]                      # [1, L+2]

    if ids.shape[1] != L + 2:
        raise ValueError(f"expected {L + 2} tokens, got {ids.shape[1]}")

    batch = ids.repeat(L, 1)                    # [L, L+2], real copies

    rows = torch.arange(L)
    cols = torch.tensor([token_index(p) for p in range(1, L + 1)])
    batch[rows, cols] = MASK_ID

    assert batch.shape == (L, L + 2)
    assert (batch == MASK_ID).sum().item() == L
    assert ((batch == MASK_ID).sum(dim=1) == 1).all()

    return batch


def verify_masking(seq: str, tokenizer, batch: torch.Tensor) -> None:
    """Check every row masks the right position and changes nothing else."""
    ids = tokenizer(seq, return_tensors="pt")["input_ids"][0]

    for i in range(len(seq)):
        col = token_index(i + 1)
        assert batch[i, col] == MASK_ID, f"row {i} mask not at column {col}"

        others = [j for j in range(batch.shape[1]) if j != col]
        assert (batch[i, others] == ids[others]).all(), f"row {i} corrupted elsewhere"