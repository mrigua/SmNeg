import pytest

from smneg.export import DEFAULT_TEMPLATE, build_output_names as build, parse_sequence

FIELDS = {"date": "2026-11-06", "title": "Wedding", "film": "Portra 400", "client": "Youssef Benali",
          "city": "Marrakech", "location": "", "photographer": "Said"}
SOURCES = [f"/x/Img{n}.nef" for n in (6579, 6580, 6581)]


def test_default_template():
    assert build(DEFAULT_TEMPLATE, SOURCES, FIELDS, "001", "tif") == [
        "2026-11-06_Wedding_001.tif", "2026-11-06_Wedding_002.tif", "2026-11-06_Wedding_003.tif"]


def test_sequence_start_and_digits():
    assert build("{filenamebase}_{seqn}", SOURCES, FIELDS, "0100", "jpg")[0] == "Img6579_0100.jpg"
    assert parse_sequence("001") == (1, 3)
    assert parse_sequence("0100") == (100, 4)


def test_empty_variable_drops_its_separator():
    names = build("{city}_{location}_{seqn}", SOURCES[:1], FIELDS, "001", "jpg")
    assert names == ["Marrakech_001.jpg"]


@pytest.mark.parametrize("template, message", [
    ("{foo}_{seqn}", "Unknown variable"),
    ("{title}", "Duplicate names"),
    ("  ", "empty"),
    ("{seqn", "Invalid braces"),
])
def test_invalid_templates(template, message):
    with pytest.raises(ValueError, match=message):
        build(template, SOURCES, FIELDS, "001", "jpg")


def test_forbidden_characters_are_replaced():
    name = build("{city}/x:{seqn}", SOURCES[:1], {**FIELDS, "city": "A/B"}, "001", "jpg")[0]
    assert "/" not in name and ":" not in name
