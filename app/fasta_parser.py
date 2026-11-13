from pathlib import Path
from io import StringIO
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord


VALID_BASES = set("ACGTN")


def parse_fasta(file_path: str | Path) -> list[SeqRecord]:
    """
    Parse and validate DNA sequences from a FASTA file.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"FASTA file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Expected a file: {path}")

    content = path.read_text(encoding="utf-8-sig").strip()

    if not content:
        raise ValueError("FASTA file is empty.")

    records = list(SeqIO.parse(StringIO(content), "fasta"))

    if not records:
        raise ValueError("FASTA file contains no sequences.")

    for record in records:
        sequence = str(record.seq).upper()

        if not sequence:
            raise ValueError(f"Empty sequence found: {record.id}")

        invalid_bases = set(sequence) - VALID_BASES

        if invalid_bases:
            raise ValueError(
                f"Invalid DNA bases in {record.id}: "
                f"{sorted(invalid_bases)}"
            )

        record.seq = record.seq.upper()

    return records
