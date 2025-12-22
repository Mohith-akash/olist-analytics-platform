"""
Utility functions for formatting values
"""


def fmt_curr(v):
    """Format value as Brazilian Real currency."""
    if v >= 1e6:
        return f"R$ {v/1e6:.2f}M"
    if v >= 1e3:
        return f"R$ {v/1e3:.1f}K"
    return f"R$ {v:,.2f}"


def fmt_num(v):
    """Format large numbers with K/M suffix."""
    if v >= 1e6:
        return f"{v/1e6:.1f}M"
    if v >= 1e3:
        return f"{v/1e3:.1f}K"
    return f"{v:,.0f}"
