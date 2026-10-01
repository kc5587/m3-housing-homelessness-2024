"""Annual series transcribed from the historical report's code appendix."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class AnnualSeries:
    key: str
    label: str
    years: tuple[int, ...]
    values: tuple[float, ...]
    source_page: int

    def __post_init__(self) -> None:
        if not isinstance(self.years, tuple) or not isinstance(self.values, tuple):
            raise ValueError("Series must use immutable tuples")
        if len(self.years) < 3 or len(self.years) != len(self.values):
            raise ValueError("Series requires at least 3 aligned observations")
        if not all(isfinite(x) for x in (*self.years, *self.values)):
            raise ValueError("Series must contain finite numbers")
        if any(a >= b for a, b in zip(self.years, self.years[1:], strict=False)):
            raise ValueError("Years must be strictly increasing")
        if min(self.values) < 0 or min(self.values) == max(self.values):
            raise ValueError("Counts must be nonnegative and nonconstant")


HOUSING_YEARS = tuple(range(2010, 2023))
HOMELESSNESS_YEARS = tuple(range(2007, 2023))
SERIES = (
    AnnualSeries(
        "seattle_housing",
        "Seattle housing units",
        HOUSING_YEARS,
        (
            302465,
            304164,
            306694,
            309205,
            311286,
            315958,
            322795,
            334739,
            344583,
            354475,
            367337,
            362800,
            372436,
        ),
        22,
    ),
    AnnualSeries(
        "albuquerque_housing",
        "Albuquerque housing units",
        HOUSING_YEARS,
        (
            234891,
            237735,
            239718,
            240277,
            240961,
            241326,
            242070,
            243402,
            244382,
            245476,
            247926,
            252924,
            255178,
        ),
        24,
    ),
    AnnualSeries(
        "seattle_homelessness",
        "Seattle homelessness count",
        HOMELESSNESS_YEARS,
        (
            7902,
            8501,
            8952,
            9022,
            8972,
            8899,
            9106,
            8949,
            10122,
            10730,
            11643,
            12112,
            11999,
            11751,
            12560,
            13368,
        ),
        27,
    ),
    AnnualSeries(
        "albuquerque_homelessness",
        "Albuquerque homelessness count",
        HOMELESSNESS_YEARS,
        (
            1276,
            1276,
            2002,
            2002,
            1639,
            1431,
            1171,
            1254,
            1287,
            1222,
            1318,
            1340,
            1524,
            1586,
            1567,
            1277,
        ),
        28,
    ),
)
