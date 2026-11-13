import argparse
import statistics
import time

from app.fasta_parser import parse_fasta
from app.alignment import needleman_wunsch


def run_benchmark(orders: int, repeats: int) -> None:
    records = parse_fasta("data/sample.fasta")

    reference = str(records[0].seq)
    query = str(records[1].seq)

    print("\n========== GENEWEAVER CPU BENCHMARK ==========")
    print(f"Reference length : {len(reference)}")
    print(f"Query length     : {len(query)}")
    print(f"Repeats          : {repeats}")
    print(f"Alignments/run   : {orders}")

    timings = []

    for run in range(1, repeats + 1):
        start_time = time.perf_counter()

        for _ in range(orders):
            result = needleman_wunsch(reference, query)

        elapsed = time.perf_counter() - start_time
        timings.append(elapsed)

        print(
            f"Run {run}: {elapsed:.6f} seconds | "
            f"Score: {result.score}"
        )

    average_time = statistics.mean(timings)
    best_time = min(timings)
    throughput = orders / average_time

    print("\n--------------- RESULTS ----------------")
    print(f"Average time : {average_time:.6f} seconds")
    print(f"Best time    : {best_time:.6f} seconds")
    print(f"Throughput   : {throughput:.2f} alignments/second")
    print("========================================\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="GeneWeaver CPU alignment benchmark"
    )
    parser.add_argument("--orders", type=int, default=100)
    parser.add_argument("--repeats", type=int, default=3)

    args = parser.parse_args()

    if args.orders <= 0 or args.repeats <= 0:
        parser.error("--orders and --repeats must be positive.")

    run_benchmark(args.orders, args.repeats)
