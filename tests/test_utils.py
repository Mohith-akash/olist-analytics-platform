import pytest

from app.utils import fmt_curr, fmt_num


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "R$ 0.00"),
        (999.5, "R$ 999.50"),
        (1_000, "R$ 1.0K"),
        (15_840, "R$ 15.8K"),
        (999_999, "R$ 1.00M"),
        (15_843_553.24, "R$ 15.84M"),
    ],
)
def test_fmt_curr(value, expected):
    assert fmt_curr(value) == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0"),
        (412, "412"),
        (98_666, "98.7K"),
        (999_960, "1.0M"),
        (2_500_000, "2.5M"),
    ],
)
def test_fmt_num(value, expected):
    assert fmt_num(value) == expected
