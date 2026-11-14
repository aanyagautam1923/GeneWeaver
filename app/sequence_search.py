def validate_dna(sequence: str, name: str = "Sequence") -> str:
    """Validate and normalize a DNA sequence."""

    if not isinstance(sequence, str):
        raise TypeError(f"{name} must be a string.")

    sequence = sequence.upper().strip()

    if not sequence:
        raise ValueError(f"{name} cannot be empty.")

    if any(base not in "ATGC" for base in sequence):
        raise ValueError(f"{name} must contain only A, T, G and C.")

    return sequence


def reverse_complement(sequence: str) -> str:
    """Generate reverse complement of DNA."""
    translation = str.maketrans("ATGC", "TACG")
    return sequence.translate(translation)[::-1]


def search_sequence(
    reference_sequence: str,
    query_sequence: str,
    max_mismatches: int = 0,
    both_strands: bool = True
) -> list:
    """
    Search a query sequence inside a reference DNA sequence.

    max_mismatches:
        Maximum allowed mismatches.

    both_strands:
        Search forward and reverse-complement strands.

    Positions use zero-based indexing.
    """

    reference = validate_dna(reference_sequence, "Reference sequence")
    query = validate_dna(query_sequence, "Query sequence")

    if not isinstance(max_mismatches, int) or isinstance(max_mismatches, bool) or max_mismatches < 0:
        raise ValueError("max_mismatches must be a non-negative integer.")

    if not isinstance(both_strands, bool):
        raise TypeError("both_strands must be True or False.")

    if len(query) > len(reference):
        return []

    strands = [("+", query)]

    reverse_query = reverse_complement(query)

    if both_strands and reverse_query != query:
        strands.append(("-", reverse_query))

    results = []

    for strand, target in strands:
        for position in range(len(reference) - len(target) + 1):

            window = reference[position:position + len(target)]

            mismatch_positions = [
                index
                for index, (a, b) in enumerate(zip(window, target))
                if a != b
            ]

            mismatch_count = len(mismatch_positions)

            if mismatch_count <= max_mismatches:
                results.append({
                    "position": position,
                    "end_position": position + len(target),
                    "strand": strand,
                    "matched_sequence": window,
                    "query_sequence": target,
                    "mismatches": mismatch_count,
                    "mismatch_positions": mismatch_positions
                })

    return sorted(
        results,
        key=lambda item: (item["mismatches"], item["position"], item["strand"])
    )
