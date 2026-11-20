"""CPU vs CUDA alignment benchmark for GeneWeaver."""

import argparse
import json
import time
from pathlib import Path

from app.alignment import needleman_wunsch
from app.cuda_alignment import align_pair
from app.cuda_utils import get_processing_mode, get_gpu_info


def get_score(result):
    """Extract alignment score from different result formats."""

    if isinstance(result, dict):
        return result.get("score")

    return getattr(result, "score", None)


def run_benchmark(repeats: int = 3) -> dict:
    """Benchmark CPU and automatic CUDA alignment processing."""

    if repeats < 1:
        raise ValueError("Repeats must be at least 1.")

    sequence_pairs = [
        ("ATGCGTACGTAGCTAGCTAG", "ATGCGTACGTAGCTAGCTAA"),
        ("GATTACAGATTACA", "GATTACAGATTACC"),
        ("ATGCATGCATGCATGC", "ATGCATGCATGCATGA"),
    ]

    cpu_times = []
    accelerated_times = []
    results = []

    for sequence_a, sequence_b in sequence_pairs:

        start = time.perf_counter()

        cpu_result = None
        for _ in range(repeats):
            cpu_result = needleman_wunsch(sequence_a, sequence_b)

        cpu_elapsed = (time.perf_counter() - start) / repeats

        start = time.perf_counter()

        accelerated_result = None
        for _ in range(repeats):
            accelerated_result = align_pair(sequence_a, sequence_b)

        accelerated_elapsed = (
            time.perf_counter() - start
        ) / repeats

        cpu_score = get_score(cpu_result)
        accelerated_score = get_score(accelerated_result)

        cpu_times.append(cpu_elapsed)
        accelerated_times.append(accelerated_elapsed)

        results.append({
            "sequence_length": len(sequence_a),
            "cpu_score": cpu_score,
            "accelerated_score": accelerated_score,
            "scores_match": cpu_score == accelerated_score,
            "cpu_time_ms": round(cpu_elapsed * 1000, 4),
            "accelerated_time_ms": round(
                accelerated_elapsed * 1000, 4
            ),
            "processing_mode": (
                accelerated_result.get("processing_mode", "Unknown")
                if isinstance(accelerated_result, dict)
                else "Unknown"
            ),
        })

    average_cpu = sum(cpu_times) / len(cpu_times)
    average_accelerated = sum(accelerated_times) / len(accelerated_times)

    report = {
        "project": "GeneWeaver",
        "benchmark": "CPU vs CUDA Alignment",
        "repeats": repeats,
        "system_processing_mode": get_processing_mode(),
        "gpu_info": get_gpu_info(),
        "average_cpu_time_ms": round(average_cpu * 1000, 4),
        "average_accelerated_time_ms": round(
            average_accelerated * 1000, 4
        ),
        "results": results,
    }

    report["all_scores_match"] = all(
        item["scores_match"] for item in results
    )

    return report


def main():
    parser = argparse.ArgumentParser(
        description="GeneWeaver CPU vs CUDA benchmark"
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=3,
        help="Number of repetitions per sequence pair",
    )
    args = parser.parse_args()

    report = run_benchmark(args.repeats)

    print(json.dumps(report, indent=4))

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "cuda_benchmark.json"
    report_path.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    print(f"\nBenchmark report saved to: {report_path}")


if __name__ == "__main__":
    main()
