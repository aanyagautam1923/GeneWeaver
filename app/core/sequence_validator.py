"""DNA sequence validation utilities."""

VALID_BASES = set("ATGC")


def validate_dna_sequence(sequence: str) -> bool:
    """Return True if sequence contains only valid DNA bases."""
    if not sequence or not isinstance(sequence, str):
        return False

    cleaned = sequence.upper().replace(" ", "").replace("\n", "")
    return bool(cleaned) and all(base in VALID_BASES for base in cleaned)


def normalize_sequence(sequence: str) -> str:
    """Normalize DNA sequence by removing whitespace and uppercasing."""
    return "".join(sequence.split()).upper()


def get_invalid_bases(sequence: str) -> list[str]:
    """Return unique invalid characters found in a DNA sequence."""
    cleaned = normalize_sequence(sequence)
    return sorted(set(cleaned) - VALID_BASES)
