"""check_repo_card.py -- gates for the drawing of a receipt.

A picture of a record is a claim about that record, and a claim with nothing
holding it stays true only until the record moves. These check the drawing
against the receipt the tool actually emits: the same fields, the same
readings, and text that fits the columns it is drawn into.

The measuring happens here, from face-metrics.json, rather than by calling the
renderer. An earlier version counted characters and asked repo_card how wide
its own text was, so the check and the drawing shared one guess and agreed with
each other whatever it said. This walks each measured face on its own instead,
so the two can now disagree.

Kept beside the art gates rather than inside them so neither file outgrows
what one person can hold at once.
"""
from __future__ import annotations

import json
from pathlib import Path

import repo_card as CARD

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "docs" / "art"

FACES = json.loads(
    Path(__file__).with_name("face-metrics.json").read_text(encoding="utf-8"))
FIRST, LAST = FACES["range"]

# What draws each element: which font stack, which weight, its size in pixels
# and its letter-spacing in em. Read off the card's own style block and off the
# two elements that override the family on themselves, since the class cannot.
DRAWN = {
    "note": ("sans", "regular", 11.5, 0.0),
    "foot": ("sans", "regular", 11.5, 0.0),
    "title": ("sans", "bold", 21.0, 0.0),
    "kicker": ("mono", "regular", 11.0, 0.16),
    "head": ("mono", "regular", 11.0, 0.16),
    "source": ("mono", "regular", 11.5, 0.0),
    "key": ("mono", "bold", 13.0, 0.0),
    "value": ("mono", "regular", 12.0, 0.0),
}
BOUND = {("sans", "regular"): CARD.SANS, ("sans", "bold"): CARD.SANS_BOLD,
         ("mono", "regular"): CARD.MONO_REG, ("mono", "bold"): CARD.MONO_BOLD}

# What each column has room for, in pixels rather than in characters. Conso
# is not monospaced, so a count was never the right unit for these two either.
KEY_BUDGET = CARD.KEY_W + CARD.GUTTER - 16
VAL_BUDGET = CARD.VAL_W
HEAD_BUDGETS = (KEY_BUDGET, CARD.VAL_W + CARD.GUTTER, CARD.NOTE_W)
PAGE_BUDGET = CARD.W - CARD.PAD * 2


def _cards() -> list[dict]:
    return [card for path in sorted(ART.glob("*.art.json"))
            for card in json.loads(path.read_text(encoding="utf-8"))
            .get("cards", [])]


def _widest_face(text: str, role: str) -> tuple[str, float]:
    """The face that draws this string widest, and what it draws, in pixels."""
    group, weight, size, tracking = DRAWN[role]
    drawn = {}
    for name, face in FACES[group][weight].items():
        off = max(face)
        total = sum(face[ord(c) - FIRST] if FIRST <= ord(c) <= LAST else off
                    for c in text)
        drawn[name] = total / 1000.0 * size + tracking * size * len(text)
    return max(drawn.items(), key=lambda pair: pair[1])


def _over(text: str, role: str, budget: float, label: str) -> list[str]:
    name, width = _widest_face(text, role)
    if width <= budget:
        return []
    return [f"{label} draws {width:.0f}px into a {budget:.0f}px column "
            f"in {name}: {text!r}"]


def _lines_that_run_long(text: str, label: str, role: str, budget: float,
                         limit: int) -> list[str]:
    """Two ways a wrapped column goes wrong, and the second is the one a
    check on the joined text misses. Dropping the ending is the obvious one.
    The other is a single token longer than the budget: the wrapper is greedy,
    so it leaves that token alone on its line, the joined text still equals
    the source, and the drawing runs off the page with every check green."""
    drawn = CARD._wrap(text, budget, limit)
    bad = []
    if " ".join(drawn) != " ".join(text.split()):
        bad.append(f"{label} loses its ending")
    for line in drawn:
        bad += _over(line, role, budget, label)
    return bad


def _card_overflows(card: dict) -> list[str]:
    """Every string one card draws, against the room it is drawn in."""
    where = card["file"]
    bad = []
    for field in card["fields"]:
        bad += _over(field["key"], "key", KEY_BUDGET, f"{where}: the key")
        bad += _over(field["value"], "value", VAL_BUDGET,
                     f'{where}: the value on {field["key"]}')
        bad += _lines_that_run_long(
            field["note"], f'{where}: the note on {field["key"]}', "note",
            CARD.NOTE_BUDGET, CARD.NOTE_LINES)
    bad += _lines_that_run_long(card["footnote"], f"{where}: the footnote",
                                "foot", CARD.FOOT_BUDGET, CARD.FOOT_LINES)
    for label, role, text in (
            ("the title", "title", card.get("title", "")),
            ("the kicker", "kicker", card.get("kicker", "").upper()),
            ("the source line", "source", "$ " + card.get("source", ""))):
        bad += _over(text, role, PAGE_BUDGET, f"{where}: {label}")
    return bad


def text_that_overflows(cards: list[dict]) -> list[str]:
    """Nothing is drawn wider than the column it is drawn into. The key and
    the value are single unwrapped lines, so they run into their neighbour
    rather than being clipped; the note and the footnote wrap by measured
    width and then drop what will not fit instead of growing the drawing."""
    bad = []
    for card in cards:
        bad += _card_overflows(card)
        heads = card.get("heads", CARD.HEADS)
        if len(heads) != 3:
            bad.append(f'{card["file"]} names {len(heads)} columns, and the '
                       f"drawing has three")
        for head, budget in zip(heads, HEAD_BUDGETS):
            bad += _over(head.upper(), "head", budget,
                         f'{card["file"]}: the {head!r} column head')
    return bad


def faces_the_renderer_underestimates(bounds: dict | None = None) -> list[str]:
    """The renderer wraps to one table and this file measures with another,
    and that is what keeps the two honest. For every character, what the
    renderer assumes has to be at least what each measured face draws. A width
    guessed from a character's class fails here on the first lowercase m."""
    bad = []
    for (group, weight), bound in (bounds or BOUND).items():
        if len(bound) != LAST - FIRST + 1:
            bad.append(f"the {group} {weight} bound covers {len(bound)} "
                       f"characters and the faces cover {LAST - FIRST + 1}")
            continue
        for name, face in FACES[group][weight].items():
            for i, thousandths in enumerate(face):
                if bound[i] < thousandths / 1000.0 - 1e-9:
                    bad.append(f"{name} draws {chr(FIRST + i)!r} wider than "
                               f"the renderer assumes it does")
    return bad


def characters_never_measured(cards: list[dict]) -> list[str]:
    """A character outside the measured range falls back to the widest glyph
    in the face, which is a guess wearing a measurement's clothes. Cards are
    written in ASCII so that never has to happen, and this holds them to it."""
    bad = []
    for card in cards:
        drawn = [card.get("title", ""), card.get("kicker", ""),
                 card.get("source", ""), card["footnote"],
                 *card.get("heads", ())]
        for field in card["fields"]:
            drawn += [field["key"], field["value"], field["note"]]
        off = sorted({c for text in drawn for c in text
                      if not FIRST <= ord(c) <= LAST})
        if off:
            bad.append(f'{card["file"]} draws {off!r}, and no face here was '
                       f"measured for it")
    return bad


def drawn_value(value: object) -> str:
    """How a receipt field has to read in a drawing of it. A string is drawn
    as itself. A bool is drawn as both of its readings, because the picture
    describes the field and not one lucky run of it. A list is drawn as its
    length, because the entries move with the commit."""
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


def alt_text_that_drifted(cards: list[dict]) -> list[str]:
    """The README alt attribute is the whole of what a reader who cannot see
    the card gets. GitHub draws it as an <img>, and an <img> hides whatever
    description the SVG carries inside it, so the long one in the spec has to
    reach the README as written, or a re-worded row keeps its old sentence."""
    shown = (ROOT / "README.md").read_text(encoding="utf-8")
    return [f'{card["file"]}: the README describes it as something it is no '
            f"longer, because the spec alt is not the alt in the README"
            for card in cards if card["alt"] not in shown]


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
        ("art.card_widths_bound_every_face",
         lambda _unused: faces_the_renderer_underestimates()),
        ("art.card_draws_measured_characters",
         lambda _unused: characters_never_measured(_cards())),
        ("art.card_carries_one_mark",
         lambda _unused: wrong_number_of_marks(_cards())),
        ("art.card_alt_reaches_the_readme",
         lambda _unused: alt_text_that_drifted(_cards())),
    ]


# A card built to break every one of those at once. The last row is what got
# past an earlier version of this file: a token too long to wrap. The wrapper
# leaves it alone on its line, so a check for cut text sees a clean wrap.
CONTROL = [{
    "file": "control.svg",
    "alt": "a description of a drawing that is in no README anywhere",
    "footnote": "word " * 200,
    "heads": ["z" * 40, "ok", "ok", "one column too many é"],
    "fields": [
        {"key": "schema", "value": "wrong", "note": "ok", "tone": "verified"},
        {"key": "invented", "value": "1 entry", "note": "ok", "tone": "drift"},
        {"key": "passed", "value": "true | false", "note": "word " * 40},
        {"key": "z" * 40, "value": "z" * 60, "note": "ok"},
        {"key": "token", "value": "ok", "note": "x" * 120},
    ],
}]

CONTROL_RECEIPT = {"schema": "project-telos.repo-art/v1", "mode": "check",
                   "specs": ["a", "b"], "passed": True}

# The bound the renderer used to carry, in the place it hurt most: a lowercase
# m given the width of an average lowercase letter. Every measured sans face
# draws one wider than that, and that is what holds the renderer to real ones.
CONTROL_BOUND = {("sans", "regular"): tuple(
    0.0 if i == ord("m") - FIRST else width
    for i, width in enumerate(CARD.SANS))}

# Written down rather than counted, so a number cannot drift quietly.
CONTROL_MISREPORTS = 6
CONTROL_OVERFLOWS = 7
CONTROL_UNDERBOUNDS = 4


def control_failures() -> list[str]:
    """Feed each card gate input it has to reject, and say what got past."""
    return [f"the gate missed {what}" for caught, what in (
        (len(misreported(CONTROL, CONTROL_RECEIPT)) == CONTROL_MISREPORTS,
         "a card that disagrees with the receipt it draws"),
        (len(text_that_overflows(CONTROL)) == CONTROL_OVERFLOWS,
         "an over-wide name, an over-wide value, a clipped note, a token "
         "too long to wrap, a fourth column, an over-wide column head and a "
         "clipped footnote"),
        (len(faces_the_renderer_underestimates(CONTROL_BOUND))
         == CONTROL_UNDERBOUNDS,
         "a renderer that assumes a lowercase m is no wider than average"),
        (len(characters_never_measured(CONTROL)) == 1,
         "a character no face here was measured for"),
        (len(wrong_number_of_marks(CONTROL)) == 1,
         "a card wearing two hot marks"),
        (len(alt_text_that_drifted(CONTROL)) == 1,
         "a description that reaches no README at all"),
    ) if not caught]
