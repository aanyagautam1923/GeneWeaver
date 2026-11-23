import random
import time
import json
from pathlib import Path
from app.core.performance_engine import fast_search, benchmark_search

def main():
    random.seed(42)
    sequence = "".join(random.choices("ACGT", k=1_000_000))
    pattern = "ACGTACGT"
    report = benchmark_search(sequence, pattern, repeats=5)
    report["sequence_length"] = len(sequence)
    report["pattern"] = pattern
    out = Path("results")
    out.mkdir(exist_ok=True)
    (out / "cpu_benchmark.json").write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
