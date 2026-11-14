def reverse_complement(sequence: str) -> str:
    """Return reverse complement of a DNA sequence."""
    sequence = sequence.upper()
    translation = str.maketrans("ATGC", "TACG")
    return sequence.translate(translation)[::-1]


def detect_pam_sites(
    sequence: str,
    pam_pattern: str = "NGG",
    guide_length: int = 20
) -> list:
    """
    Detect SpCas9 NGG PAM sites on both DNA strands.

    Positions are zero-based coordinates.
    Only sites with a complete protospacer are returned.
    """

    if not isinstance(sequence, str):
        raise TypeError("Sequence must be a string.")

    sequence = sequence.upper().strip()

    if not sequence:
        raise ValueError("DNA sequence cannot be empty.")

    if any(base not in "ATGC" for base in sequence):
        raise ValueError("Sequence must contain only A, T, G and C.")

    if pam_pattern != "NGG":
        raise ValueError("Currently only NGG PAM is supported.")

    if not isinstance(guide_length, int) or isinstance(guide_length, bool) or guide_length <= 0:
        raise ValueError("Guide length must be a positive integer.")

    results = []
    length = len(sequence)

    # Forward strand: NGG
    for i in range(length - 2):
        pam = sequence[i:i + 3]

        if pam[1:] == "GG":
            guide_start = i - guide_length

            if guide_start >= 0:
                results.append({
                    "position": i,
                    "strand": "+",
                    "pam": pam,
                    "guide_sequence": sequence[guide_start:i]
                })

    # Reverse strand: CCN on the forward reference
    for i in range(length - 2):
        pam_reference = sequence[i:i + 3]

        if pam_reference[:2] == "CC":
            guide_start = i + 3
            guide_end = guide_start + guide_length

            if guide_end <= length:
                results.append({
                    "position": i,
                    "strand": "-",
                    "pam": reverse_complement(pam_reference),
                    "guide_sequence": reverse_complement(
                        sequence[guide_start:guide_end]
                    )
                })

    return sorted(results, key=lambda item: item["position"])
