"""check_repo_card.py -- gates for the drawing of a receipt.

A picture of a record is a claim about that record, and a claim with nothing
holding it stays true only until the record moves. These check the drawing
against the receipt the tool actually emits: the same fields, the same
readings, and text that fits the columns it is drawn into.

Kept beside the art gates rather than inside them so neither file outgrows
what one person can hold at once.
"""
from __future__ import annotations

import json
from pathlib import Path

import repo_card as CARD

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "docs" / "art"


def _cards() -> list[dict]:
    return [card for path in sorted(ART.glob("*.art.json"))
            for card in json.loads(path.read_text(encoding="utf-8"))
            .get("cards", [])]


def drawn_value(value: object) -> str:
    """How a receipt field has to read in a drawing of it.

    A string is drawn as itself. A bool is drawn as both of its readings,
    because the picture describes the field and not one lucky run of it. A
    list is drawn as its length, because the entries change with the commit
    and a picture that shows them is wrong by the next one.
    """
    if isinstance(value, bool):
        return "true | false"
    if isinstance(value, str):
        return value
    count = len(value)
    return f"{count} entry" if count == 1 else f"{count} entries"


def misreported(cards: list[dict], live: dict) -> list[str]:
    """Where the drawing and the record disagree, both directions."""
    bad = []
    for card in cards:
        drawn = {field["key"]: field["value"] for field in card["fields"]}
        for key in live:
            if key not in drawn:
                bad.append(f'{card["file"]} leaves out the {key} field')
        for key, value in drawn.items():
            if key not in live:
                bad.append(f'{card["file"]} draws a {key} field that no '
                           f"receipt carries")
            elif value != drawn_value(live[key]):
                bad.append(f'{card["file"]} says {key} reads {value!r}, and '
                           f"it reads {drawn_value(live[key])!r}")
    return bad


def text_that_overflows(cards: list[dict]) -> list[str]:
    """Notes wrap to the column beside the value and the footnote wraps to
    the page. Both drop what will not fit instead of growing the drawing."""
    bad = []
    for card in cards:
        for field in card["fields"]:
            drawn = " ".join(CARD._wrap(field["note"]))
            if drawn != " ".join(field["note"].split()):
                bad.append(f'{card["file"]}: the note on {field["key"]} cuts '
                           f'off at "{drawn}"')
        foot = " ".join(CARD._wrap(card["footnote"], CARD.FOOT_BUDGET,
                                   CARD.FOOT_LINES))
        if foot != " ".join(card["footnote"].split()):
            bad.append(f'{card["file"]}: the footnote cuts off at "{foot}"')
    return bad


def wrong_number_of_marks(cards: list[dict]) -> list[str]:
    """Colour says one thing here. Two accents and it says nothing."""
    bad = []
    for card in cards:
        hot = [f["key"] for f in card["fields"]
               if f.get("tone", "none") != "none"]
        if len(hot) != 1:
            bad.append(f'{card["file"]} accents {len(hot)} rows, and one hot '
                       f"mark per view is the whole of the colour rule")
    return bad


def checks(receipt_fields) -> list[tuple]:
    """The card gates, bound to the builder that says what a receipt holds."""
    return [
        ("art.card_matches_the_receipt",
         lambda specs: misreported(_cards(), receipt_fields(specs))),
        ("art.card_text_fits_its_column",
         lambda _unused: text_that_overflows(_cards())),
        ("art.card_carries_one_mark",
         lambda _unused: wrong_number_of_marks(_cards())),
    ]


# A card built to break every one of those at once: a value that disagrees, a
# field no receipt carries, two fields left out, a clipped note, a clipped
# footnote, and two hot marks where the rule allows one.
CONTROL = [{
    "file": "control.svg",
    "footnote": "word " * 200,
    "fields": [
        {"key": "schema", "value": "wrong", "note": "ok", "tone": "verified"},
        {"key": "invented", "value": "1 entry", "note": "ok", "tone": "drift"},
        {"key": "passed", "value": "true | false", "note": "word " * 40},
    ],
}]

CONTROL_RECEIPT = {"schema": "project-telos.repo-art/v1", "mode": "check",
                   "specs": ["a", "b"], "passed": True}

# Written down rather than counted, so the number cannot drift quietly.
CONTROL_MISREPORTS = 4


def control_failures() -> list[str]:
    """Feed each card gate input it has to reject, and say what got past."""
    return [f"the gate missed {what}" for caught, what in (
        (len(misreported(CONTROL, CONTROL_RECEIPT)) == CONTROL_MISREPORTS,
         "a card that disagrees with the receipt it draws"),
        (len(text_that_overflows(CONTROL)) == 2,
         "a clipped card note and a clipped footnote"),
        (len(wrong_number_of_marks(CONTROL)) == 1,
         "a card wearing two hot marks"),
    ) if not caught]
