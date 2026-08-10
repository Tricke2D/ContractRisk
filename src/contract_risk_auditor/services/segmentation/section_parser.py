"""
Section parser for legal contract numbering.
"""

import re
from dataclasses import dataclass


@dataclass
class SectionBoundary:
    """Represents one section start point in raw text."""

    section_number: str
    start_index: int
    raw_heading_line: str


_NESTED_NUMBERING_PATTERN = re.compile(
    r"""
    ^\s*
    (?:(?:Section|Article|Clause)\s+)?
    (\d+(?:\.\d+){0,4}(?:\([a-z]\))?)
    [\.\)]?\s+
    """,
    re.MULTILINE | re.IGNORECASE | re.VERBOSE,
)


def find_section_boundaries(raw_text: str) -> list[SectionBoundary]:
    """Find all section boundaries in raw text."""
    boundaries: list[SectionBoundary] = []

    for match in _NESTED_NUMBERING_PATTERN.finditer(raw_text):
        section_number = match.group(1)
        line_end = raw_text.find("\n", match.end())
        raw_heading_line = raw_text[match.start() : line_end if line_end != -1 else None]

        boundaries.append(
            SectionBoundary(
                section_number=section_number,
                start_index=match.start(),
                raw_heading_line=raw_heading_line.strip(),
            )
        )

    return boundaries


def has_reliable_numbering(boundaries: list[SectionBoundary], min_matches: int = 3) -> bool:
    """Determine if regex numbering is reliable."""
    if len(boundaries) < min_matches:
        return False

    seen_levels = {b.section_number.count(".") for b in boundaries}
    return max(seen_levels) - min(seen_levels) <= 2
