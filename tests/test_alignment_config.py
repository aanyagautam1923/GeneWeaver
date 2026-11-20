import pytest

from app.alignment_config import (
    AlignmentConfig,
    get_default_config,
    create_alignment_config,
)


def test_default_config():
    config = get_default_config()

    assert config.match_score == 2
    assert config.mismatch_penalty == -1
    assert config.gap_penalty == -2


def test_custom_config():
    config = create_alignment_config(
        match_score=3,
        mismatch_penalty=-2,
        gap_penalty=-3,
    )

    assert config.match_score == 3
    assert config.mismatch_penalty == -2
    assert config.gap_penalty == -3


def test_config_to_dict():
    config = get_default_config()

    result = config.to_dict()

    assert isinstance(result, dict)
    assert result["match_score"] == 2


def test_invalid_config():
    with pytest.raises((ValueError, TypeError)):
        AlignmentConfig(match_score=0)
