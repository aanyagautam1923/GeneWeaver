from app.melting_temperature import calculate_melting_temperature, calculate_tm


def test_tm_short_sequence():
    result = calculate_melting_temperature("ATGC")
    assert result == 12.0


def test_tm_gc_rich_sequence():
    result = calculate_melting_temperature("GCGC")
    assert result == 16.0


def test_tm_at_rich_sequence():
    result = calculate_melting_temperature("ATAT")
    assert result == 8.0


def test_calculate_tm_alias():
    result = calculate_tm("ATGC")
    assert result == 12.0


def test_invalid_sequence():
    try:
        calculate_melting_temperature("ATGX")
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid sequence should raise ValueError")
