from io import StringIO


def parse_multifasta(content: str) -> list:
    """
    Parse multiple FASTA records.

    Returns a list containing sequence ID,
    description and normalized DNA sequence.
    """

    if not isinstance(content, str):
        raise TypeError("FASTA content must be a string.")

    content = content.strip()

    if not content:
        raise ValueError("FASTA content cannot be empty.")

    records = []
    current_header = None
    current_sequence = []

    def save_record():
        if current_header is None:
            return

        sequence = "".join(current_sequence).upper()

        if not sequence:
            raise ValueError(
                f"Sequence is empty for record: {current_header}"
            )

        if any(base not in "ACGTN" for base in sequence):
            raise ValueError(
                f"Invalid DNA characters in record: {current_header}"
            )

        parts = current_header.split(maxsplit=1)

        records.append({
            "id": parts[0],
            "description": parts[1] if len(parts) > 1 else "",
            "sequence": sequence,
            "length": len(sequence)
        })

    for line_number, line in enumerate(content.splitlines(), start=1):
        line = line.strip()

        if not line:
            continue

        if line.startswith(">"):
            save_record()

            current_header = line[1:].strip()
            current_sequence = []

            if not current_header:
                raise ValueError(
                    f"Missing FASTA header at line {line_number}"
                )

        else:
            if current_header is None:
                raise ValueError(
                    "FASTA sequence found before the first header."
                )

            current_sequence.append("".join(line.split()))

    save_record()

    if not records:
        raise ValueError("No valid FASTA records found.")

    return records


def get_multifasta_summary(records: list) -> dict:
    """Generate summary statistics for parsed FASTA records."""

    if not isinstance(records, list) or not records:
        raise ValueError("At least one FASTA record is required.")

    total_bases = sum(record["length"] for record in records)

    return {
        "sequence_count": len(records),
        "total_bases": total_bases,
        "average_length": round(total_bases / len(records), 2),
        "longest_sequence": max(
            record["length"] for record in records
        ),
        "shortest_sequence": min(
            record["length"] for record in records
        )
    }


def parse_multifasta_file(file_path: str) -> list:
    """Read and parse a FASTA file from disk."""

    with open(file_path, "r", encoding="utf-8") as file:
        return parse_multifasta(file.read())
