def calculate_melting_temperature(sequence: str) -> float:
    """
    Calculate approximate DNA melting temperature.

    Uses:
    - Wallace rule for sequences up to 14 bases.
    - Long-sequence approximation for sequences above 14 bases.

    Returns:
        Approximate melting temperature in Celsius.
    """

    if not isinstance(sequence, str):
        raise TypeError("DNA sequence must be a string.")

    sequence = sequence.upper().strip()

    if not sequence:
        raise ValueError("DNA sequence cannot be empty.")

    valid_bases = {"A", "T", "G", "C"}

    if any(base not in valid_bases for base in sequence):
        raise ValueError("DNA sequence must contain only A, T, G and C.")

    length = len(sequence)
    at_count = sequence.count("A") + sequence.count("T")
    gc_count = sequence.count("G") + sequence.count("C")

    if length <= 14:
        temperature = (2 * at_count) + (4 * gc_count)
    else:
        gc_percentage = (gc_count / length) * 100
        temperature = 64.9 + 41 * (gc_count - 16.4) / length

    return round(float(temperature), 2)


def calculate_tm(sequence: str) -> float:
    """Short alias for calculate_melting_temperature."""
    return calculate_melting_temperature(sequence)
