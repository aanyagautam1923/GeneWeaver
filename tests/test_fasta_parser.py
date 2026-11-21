import pytest
from app.fasta_parser import parse_fasta


def test_parse_fasta_valid(tmp_path):
    fasta_file = tmp_path / "gene.fasta"
    fasta_file.write_text(">gene1\nATGCATGC\n", encoding="utf-8")
    result = parse_fasta(fasta_file)
    assert len(result) == 1


def test_parse_fasta_sequence(tmp_path):
    fasta_file = tmp_path / "gene.fasta"
    fasta_file.write_text(">gene1\nATGCATGC\n", encoding="utf-8")
    result = parse_fasta(fasta_file)
    assert str(result[0].seq) == "ATGCATGC"


def test_parse_fasta_header(tmp_path):
    fasta_file = tmp_path / "gene.fasta"
    fasta_file.write_text(">gene1\nATGCATGC\n", encoding="utf-8")
    result = parse_fasta(fasta_file)
    assert result[0].id == "gene1"


def test_parse_fasta_multiple_lines(tmp_path):
    fasta_file = tmp_path / "gene.fasta"
    fasta_file.write_text(">gene1\nATGC\nATGC\n", encoding="utf-8")
    result = parse_fasta(fasta_file)
    assert str(result[0].seq) == "ATGCATGC"


def test_parse_fasta_empty_file(tmp_path):
    fasta_file = tmp_path / "empty.fasta"
    fasta_file.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="FASTA file is empty"):
        parse_fasta(fasta_file)


def test_parse_fasta_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        parse_fasta(tmp_path / "missing.fasta")
