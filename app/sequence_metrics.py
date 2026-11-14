def validate_sequence(sequence: str) -> str:
    """Validate and normalize a DNA sequence."""

    if not isinstance(sequence, str):
        raise TypeError("Sequence must be a string.")

    sequence = sequence.upper().strip()

    if not sequence:
        raise ValueError("DNA sequence cannot be empty.")

    valid_bases = {"A", "T", "G", "C"}

    if any(base not in valid_bases for base in sequence):
        raise ValueError("Sequence must contain only A, T, G and C.")

    return sequence


def calculate_gc_content(sequence: str) -> float:
    """Calculate GC percentage."""

    sequence = validate_sequence(sequence)
    gc_count = sequence.count("G") + sequence.count("C")

    return round((gc_count / len(sequence)) * 100, 2)


def calculate_at_content(sequence: str) -> float:
    """Calculate AT percentage."""

    sequence = validate_sequence(sequence)
    at_count = sequence.count("A") + sequence.count("T")

    return round((at_count / len(sequence)) * 100, 2)


def nucleotide_composition(sequence: str) -> dict:
    """Return the count of each nucleotide."""

    sequence = validate_sequence(sequence)

    return {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "G": sequence.count("G"),
        "C": sequence.count("C")
    }


def calculate_sequence_metrics(sequence: str) -> dict:
    """Calculate complete DNA sequence statistics."""

    sequence = validate_sequence(sequence)

    composition = nucleotide_composition(sequence)
    gc_content = calculate_gc_content(sequence)
    at_content = calculate_at_content(sequence)

    gc_count = composition["G"] + composition["C"]
    at_count = composition["A"] + composition["T"]

    ratio = round(gc_count / at_count, 2) if at_count else None

    return {
        "sequence_length": len(sequence),
        "gc_content": gc_content,
        "at_content": at_content,
        "gc_at_ratio": ratio,
        "nucleotide_composition": composition
    }
