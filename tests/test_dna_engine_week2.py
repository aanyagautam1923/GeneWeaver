from app.core.dna_engine import (
    validate_dna, clean_sequence, sequence_stats, reverse_complement,
    chunk_sequence, find_motifs, detect_pam, needleman_wunsch, parse_fasta
)

def test_clean_validate():
    assert clean_sequence("ac gt\n") == "ACGT"
    assert validate_dna("ACGTNN")
    assert not validate_dna("ACGTXYZ")

def test_stats():
    result = sequence_stats("ACGT")
    assert result["gc_percent"] == 50
    assert result["at_percent"] == 50
    assert result["length"] == 4

def test_reverse_complement():
    assert reverse_complement("AAGC") == "GCTT"

def test_chunk():
    assert list(chunk_sequence("ACGTAC", 3)) == ["ACG", "TAC"]
    assert list(chunk_sequence("ACGTAC", 4, 1)) == ["ACGT", "TAC"]

def test_motifs():
    assert find_motifs("AAGGAA", "GG") == [2]
    assert detect_pam("AAGGTT", "NGG") == [{"position": 1, "sequence": "AGG"}]

def test_alignment():
    result = needleman_wunsch("ACGT", "ACCT")
    assert result["score"] == 5
    assert len(result["aligned_seq1"]) == len(result["aligned_seq2"])

def test_fasta():
    result = parse_fasta(">one\nACGT\n>two\nGGCC")
    assert len(result) == 2
    assert result[0]["sequence"] == "ACGT"
