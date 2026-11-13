import pytest
from app.fasta_parser import parse_fasta


def test_parse_fasta_records():
    records = parse_fasta("data/sample.fasta")

    assert len(records) == 2
    assert records[0].id == "reference_gene"
    assert str(records[0].seq) == "ATGCGTACGTAGCTAGCTAGGCTAACCGTTAGCTAG"


def test_parse_fasta_missing_file():
    with pytest.raises(FileNotFoundError):
        parse_fasta("data/missing.fasta")


def test_parse_fasta_invalid_bases(tmp_path):
    fasta = tmp_path / "invalid.fasta"
    fasta.write_text(">invalid\nATGCXYZ\n")

    with pytest.raises(ValueError):
        parse_fasta(fasta)


def test_parse_fasta_empty_sequence(tmp_path):
    fasta = tmp_path / "empty.fasta"
    fasta.write_text(">empty\n")

    with pytest.raises(ValueError):
        parse_fasta(fasta)
