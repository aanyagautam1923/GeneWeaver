from app.multifasta import (
    parse_multifasta,
    get_multifasta_summary,
    parse_multifasta_file,
)


SAMPLE_FASTA = """>gene1
ATGCATGC
>gene2
GCGCGCTA
>gene3
TTTTAAAA
"""


def test_parse_multifasta():
    result = parse_multifasta(SAMPLE_FASTA)
    assert len(result) == 3
    assert result[0]["id"] == "gene1"
    assert result[0]["sequence"] == "ATGCATGC"


def test_multifasta_summary():
    sequences = parse_multifasta(SAMPLE_FASTA)
    summary = get_multifasta_summary(sequences)

    assert summary["sequence_count"] == 3
    assert summary["total_bases"] == 24
    assert summary["average_length"] == 8.0
    assert summary["longest_sequence"] == 8
    assert summary["shortest_sequence"] == 8


def test_parse_multifasta_file(tmp_path):
    fasta_file = tmp_path / "sample.fasta"
    fasta_file.write_text(SAMPLE_FASTA, encoding="utf-8")

    result = parse_multifasta_file(str(fasta_file))

    assert len(result) == 3
    assert result[1]["id"] == "gene2"
