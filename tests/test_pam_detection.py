from app.pam_detection import reverse_complement, detect_pam_sites


def test_reverse_complement():
    assert reverse_complement("ATGC") == "GCAT"


def test_reverse_complement_full_sequence():
    result = reverse_complement("AAGCTG")
    assert result == "CAGCTT"


def test_detect_pam_sites_returns_list():
    result = detect_pam_sites("ATGCGG")
    assert isinstance(result, list)


def test_detect_pam_sites_with_ngg():
    sequence = "A" * 20 + "AGG"
    result = detect_pam_sites(sequence)

    assert len(result) >= 1


def test_no_pam_sequence():
    result = detect_pam_sites("ATATATATATAT")
    assert isinstance(result, list)
