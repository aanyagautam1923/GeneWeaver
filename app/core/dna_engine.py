from __future__ import annotations

from typing import Iterator

DNA_ALPHABET = set("ACGTN")


def validate_dna(sequence: str) -> bool:
    sequence = clean_sequence(sequence)
    return bool(sequence) and all(c in DNA_ALPHABET for c in sequence)


def clean_sequence(sequence: str) -> str:
    return "".join(sequence.upper().split())


def sequence_stats(sequence: str) -> dict:
    seq = clean_sequence(sequence)
    if not seq:
        return {"length": 0, "gc_percent": 0.0, "at_percent": 0.0, "counts": {}}

    counts = {base: seq.count(base) for base in "ACGTN"}
    length = len(seq)
    gc = counts["G"] + counts["C"]
    at = counts["A"] + counts["T"]

    return {
        "length": length,
        "gc_percent": round(gc / length * 100, 2),
        "at_percent": round(at / length * 100, 2),
        "counts": counts,
    }


def reverse_complement(sequence: str) -> str:
    seq = clean_sequence(sequence)
    if not validate_dna(seq):
        raise ValueError("Invalid DNA sequence")
    return seq.translate(str.maketrans("ACGTN", "TGCAN"))[::-1]


def chunk_sequence(sequence: str, chunk_size: int = 1000, overlap: int = 0) -> Iterator[str]:
    seq = clean_sequence(sequence)
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap")
    step = chunk_size - overlap
    for start in range(0, len(seq), step):
        yield seq[start:start + chunk_size]


def find_motifs(sequence: str, motif: str) -> list[int]:
    seq, pattern = clean_sequence(sequence), clean_sequence(motif)
    if not validate_dna(seq) or not validate_dna(pattern):
        raise ValueError("Invalid DNA or motif")
    positions = []
    start = 0
    while True:
        idx = seq.find(pattern, start)
        if idx == -1:
            break
        positions.append(idx)
        start = idx + 1
    return positions


def detect_pam(sequence: str, pam: str = "NGG") -> list[dict]:
    seq, pattern = clean_sequence(sequence), clean_sequence(pam)
    if not validate_dna(seq) or not pattern:
        raise ValueError("Invalid DNA or PAM")
    results = []
    for i in range(len(seq) - len(pattern) + 1):
        segment = seq[i:i + len(pattern)]
        if all(p == "N" or p == s for p, s in zip(pattern, segment)):
            results.append({"position": i, "sequence": segment})
    return results


def needleman_wunsch(seq1: str, seq2: str, match: int = 2, mismatch: int = -1, gap: int = -2) -> dict:
    a, b = clean_sequence(seq1), clean_sequence(seq2)
    if not validate_dna(a) or not validate_dna(b):
        raise ValueError("Invalid DNA sequence")

    rows, cols = len(a) + 1, len(b) + 1
    dp = [[0] * cols for _ in range(rows)]
    trace = [[0] * cols for _ in range(rows)]

    for i in range(1, rows):
        dp[i][0], trace[i][0] = i * gap, 1
    for j in range(1, cols):
        dp[0][j], trace[0][j] = j * gap, 2

    for i in range(1, rows):
        for j in range(1, cols):
            diag = dp[i - 1][j - 1] + (match if a[i - 1] == b[j - 1] else mismatch)
            up, left = dp[i - 1][j] + gap, dp[i][j - 1] + gap
            best = max(diag, up, left)
            dp[i][j] = best
            trace[i][j] = 0 if best == diag else 1 if best == up else 2

    i, j = len(a), len(b)
    aligned_a, aligned_b = [], []
    while i or j:
        direction = trace[i][j]
        if i and j and direction == 0:
            aligned_a.append(a[i - 1]); aligned_b.append(b[j - 1]); i -= 1; j -= 1
        elif i and (j == 0 or direction == 1):
            aligned_a.append(a[i - 1]); aligned_b.append("-"); i -= 1
        else:
            aligned_a.append("-"); aligned_b.append(b[j - 1]); j -= 1

    aligned_a.reverse(); aligned_b.reverse()
    return {"score": dp[-1][-1], "aligned_seq1": "".join(aligned_a), "aligned_seq2": "".join(aligned_b)}


def parse_fasta(text: str) -> list[dict]:
    records, name, parts = [], None, []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if name is not None:
                seq = clean_sequence("".join(parts))
                if not validate_dna(seq):
                    raise ValueError(f"Invalid DNA in FASTA record: {name}")
                records.append({"id": name, "sequence": seq})
            name, parts = line[1:].strip(), []
            if not name:
                raise ValueError("FASTA header cannot be empty")
        else:
            if name is None:
                raise ValueError("FASTA sequence must start with a header (>)")
            parts.append(line)

    if name is not None:
        seq = clean_sequence("".join(parts))
        if not validate_dna(seq):
            raise ValueError(f"Invalid DNA in FASTA record: {name}")
        records.append({"id": name, "sequence": seq})
    if not records:
        raise ValueError("No FASTA records found")
    return records
