from __future__ import annotations
import time
import psutil
from app.core.dna_engine import clean_sequence, validate_dna, sequence_stats

def fast_search(sequence: str, pattern: str) -> list[int]:
    text, pat = clean_sequence(sequence), clean_sequence(pattern)
    if not validate_dna(text) or not validate_dna(pat):
        raise ValueError("Invalid DNA")
    if len(pat) > len(text):
        return []
    # Boyer-Moore-Horspool bad-character shift table
    m = len(pat)
    shifts = {c: m for c in set(text + pat)}
    for i in range(m - 1):
        shifts[pat[i]] = m - 1 - i
    positions = []
    i = 0
    while i <= len(text) - m:
        j = m - 1
        while j >= 0 and pat[j] == text[i + j]:
            j -= 1
        if j < 0:
            positions.append(i)
            i += 1
        else:
            i += shifts.get(text[i + m - 1], m)
    return positions

def batch_analyze(sequences: list[str]) -> list[dict]:
    return [sequence_stats(s) for s in sequences]

def system_metrics() -> dict:
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
    }

def benchmark_search(sequence: str, pattern: str, repeats: int = 3) -> dict:
    start = time.perf_counter()
    result = []
    for _ in range(repeats):
        result = fast_search(sequence, pattern)
    elapsed = time.perf_counter() - start
    return {
        "algorithm": "Boyer-Moore-Horspool",
        "repeats": repeats,
        "total_seconds": round(elapsed, 6),
        "average_seconds": elapsed / repeats,
        "matches": len(result),
        "throughput_bases_per_second": int(len(sequence) / max(elapsed / repeats, 1e-12)),
    }
