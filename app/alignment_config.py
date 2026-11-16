from dataclasses import dataclass, asdict


@dataclass
class AlignmentConfig:
    """Configuration for DNA sequence alignment."""

    match_score: int = 2
    mismatch_penalty: int = -1
    gap_penalty: int = -2
    algorithm: str = "needleman_wunsch"

    def __post_init__(self):
        if not isinstance(self.match_score, int) or isinstance(self.match_score, bool):
            raise TypeError("Match score must be an integer.")

        if not isinstance(self.mismatch_penalty, int) or isinstance(self.mismatch_penalty, bool):
            raise TypeError("Mismatch penalty must be an integer.")

        if not isinstance(self.gap_penalty, int) or isinstance(self.gap_penalty, bool):
            raise TypeError("Gap penalty must be an integer.")

        if self.match_score <= 0:
            raise ValueError("Match score must be positive.")

        if self.mismatch_penalty > 0:
            raise ValueError("Mismatch penalty must be zero or negative.")

        if self.gap_penalty > 0:
            raise ValueError("Gap penalty must be zero or negative.")

        allowed_algorithms = {
            "needleman_wunsch",
            "smith_waterman"
        }

        if self.algorithm not in allowed_algorithms:
            raise ValueError(
                f"Algorithm must be one of: {allowed_algorithms}"
            )

    def to_dict(self) -> dict:
        """Convert configuration into a dictionary."""
        return asdict(self)


def get_default_config() -> AlignmentConfig:
    """Return the default alignment configuration."""
    return AlignmentConfig()


def create_alignment_config(
    match_score: int = 2,
    mismatch_penalty: int = -1,
    gap_penalty: int = -2,
    algorithm: str = "needleman_wunsch"
) -> AlignmentConfig:
    """Create a custom alignment configuration."""

    return AlignmentConfig(
        match_score=match_score,
        mismatch_penalty=mismatch_penalty,
        gap_penalty=gap_penalty,
        algorithm=algorithm
    )
