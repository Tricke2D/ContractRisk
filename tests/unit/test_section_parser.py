from contract_risk_auditor.services.segmentation.section_parser import (
    find_section_boundaries,
    has_reliable_numbering,
)


def test_find_section_boundaries_dot_format() -> None:
    text = "5. Section One\nContent here.\n5.1 Subsection\nMore content."
    boundaries = find_section_boundaries(text)
    assert len(boundaries) >= 2
    assert boundaries[0].section_number == "5"
    assert "Section One" in boundaries[0].raw_heading_line


def test_find_section_boundaries_nested() -> None:
    text = "5.2.1(b) Subsection\nContent here."
    boundaries = find_section_boundaries(text)
    assert len(boundaries) == 1
    assert boundaries[0].section_number == "5.2.1(b)"


def test_has_reliable_numbering() -> None:
    text = "1. First\n2. Second\n3. Third"
    boundaries = find_section_boundaries(text)
    assert has_reliable_numbering(boundaries) is True


def test_has_reliable_numbering_insufficient() -> None:
    text = "1. Only one"
    boundaries = find_section_boundaries(text)
    assert has_reliable_numbering(boundaries, min_matches=3) is False
