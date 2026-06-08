"""
clean.py — Stage 1: Document Ingestion & Cleaning for The Unofficial Guide.

Reads each raw Rate My Professors document *pair* from ``documents/raw/``
(``<slug>-overall.txt`` + ``<slug>-reviews.txt``), strips the copy-pasted UI
noise, and writes one clean, chunk-ready document per professor to
``documents/clean/<slug>.txt``.

The clean-doc format (agreed in spec/stages.md) looks like:

    === OVERALL ===
    Overall Quality: 2.5/5 (based on 55 ratings)
    Would Take Again: 40%
    Level of Difficulty: 3.4
    Rating Distribution: Awesome (5): 7 | Great (4): 7 | ...

    === REVIEWS ===
    --- Review 1 ---
    Quality: 3.0
    Difficulty: 1.0
    Course: CS114
    Date: Apr 21, 2026
    For Credit: Yes
    ...
    Review: <body prose>
    Tags: Lecture heavy
    Thumbs Up: 0
    Thumbs Down: 0

Run with:  python src/clean.py
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

# --- Paths -------------------------------------------------------------------
# Resolve everything relative to the project root (two levels up from this file)
# so the script behaves the same no matter which directory you launch it from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "documents" / "raw"
CLEAN_DIR = PROJECT_ROOT / "documents" / "clean"

# --- RMP closed tag vocabulary ----------------------------------------------
# Rate My Professors only lets a student pick from a fixed set of ~21 tags.
# We exploit that closed set to tell a TAG line apart from a free-text REVIEW
# BODY line -- some bodies are as short as a tag ("Good", "Class is fine"), so
# length alone can't disambiguate them. The dict maps a lowercased key (for
# case-insensitive matching, since the raw data mixes "LECTURE HEAVY" /
# "Lecture heavy") to the canonical spelling we write back out.
RMP_TAGS = {
    "tough grader": "Tough grader",
    "get ready to read": "Get ready to read",
    "participation matters": "Participation matters",
    "extra credit": "Extra credit",
    "group projects": "Group projects",
    "amazing lectures": "Amazing lectures",
    "clear grading criteria": "Clear grading criteria",
    "gives good feedback": "Gives good feedback",
    "inspirational": "Inspirational",
    "lots of homework": "Lots of homework",
    "hilarious": "Hilarious",
    "beware of pop quizzes": "Beware of pop quizzes",
    "so many papers": "So many papers",
    "caring": "Caring",
    "respected": "Respected",
    "lecture heavy": "Lecture heavy",
    "test heavy": "Test heavy",
    "graded by few things": "Graded by few things",
    "accessible outside class": "Accessible outside class",
    "online savvy": "Online savvy",
    "skip class? you won't pass.": "Skip class? You won't pass.",
}

# The optional labeled fields that can appear in a review, in display order.
REVIEW_FIELDS = [
    "For Credit",
    "Attendance",
    "Would Take Again",
    "Grade",
    "Textbook",
    "Online Class",
]
_FIELD_RE = re.compile(rf"^({'|'.join(REVIEW_FIELDS)}):\s*(.*)$")


# --- Small shared helpers ----------------------------------------------------
def load_raw(path: Path) -> list[str]:
    """Return the non-blank, whitespace-trimmed lines of a raw file.

    We drop blank lines up front because nothing we parse depends on them and
    they only add noise (the raw files have stray blanks inside the rating
    distribution and between reviews). We instead use content markers like the
    literal "Quality" line to find structure.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip()]


def clean_course(raw: str) -> str:
    """Normalize a course-code line: drop the leaked 'Computer Icon' UI prefix,
    remove spaces, and upper-case. e.g. 'Computer Iconcs356' -> 'CS356'."""
    code = re.sub(r"^Computer Icon", "", raw).strip()
    return code.replace(" ", "").upper()


def clean_date(raw: str) -> str:
    """Normalize a date line to '<Mon> <D>, <YYYY>' (e.g. 'Apr 21st, 2026' ->
    'Apr 21, 2026'). Stage 2 will convert this to the YYYYMMDD int for metadata.
    """
    # Strip the ordinal suffix (st/nd/rd/th) so strptime can parse the date.
    stripped = re.sub(r"(\d+)(st|nd|rd|th)\b", r"\1", raw)
    dt = datetime.strptime(stripped, "%b %d, %Y")
    # Build the display string manually to avoid platform-specific zero-padding.
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


# --- Overall-ratings parser --------------------------------------------------
def parse_overall(lines: list[str]) -> dict:
    """Parse a cleaned ``*-overall.txt`` into a stats dict.

    We anchor on content (regex / known labels) rather than fixed line numbers
    so the parser is robust to small layout drift.
    """
    text = "\n".join(lines)

    overall_quality = float(lines[0])  # e.g. "2.5" or "4"
    num_ratings = int(re.search(r"Based on (\d+) ratings", text).group(1))
    professor = lines[3]  # full name line

    # "Would take again" percentage: the standalone "NN%" line.
    would_take_again_pct = next(
        int(m.group(1)) for ln in lines if (m := re.match(r"^(\d+)%$", ln))
    )

    # Difficulty: the numeric line immediately before "Level of Difficulty".
    difficulty = float(lines[lines.index("Level of Difficulty") - 1])

    # Rating distribution: (label, count) pairs after "Rating Distribution".
    # Each label like "Awesome 5" ends with its star value (5..1).
    rest = lines[lines.index("Rating Distribution") + 1 :]
    distribution = {
        int(rest[i].split()[-1]): int(rest[i + 1]) for i in range(0, len(rest), 2)
    }

    return {
        "professor": professor,
        "overall_quality": overall_quality,
        "num_ratings": num_ratings,
        "would_take_again_pct": would_take_again_pct,
        "difficulty": difficulty,
        "distribution": distribution,  # {5: 7, 4: 7, 3: 11, 2: 12, 1: 18}
    }


# --- Reviews parser ----------------------------------------------------------
def parse_reviews(lines: list[str]) -> list[dict]:
    """Split a cleaned ``*-reviews.txt`` into review blocks and parse each.

    Every review block starts with the literal line "Quality", so we slice the
    file on those positions. This is more robust than splitting on blank lines,
    which the stray 'Reviewed: <date>' edit markers would break.
    """
    starts = [i for i, ln in enumerate(lines) if ln == "Quality"]
    if not starts:
        return []
    bounds = starts + [len(lines)]
    blocks = [lines[bounds[k] : bounds[k + 1]] for k in range(len(starts))]
    return [parse_review_block(b) for b in blocks]


def parse_review_block(block: list[str]) -> dict:
    """Parse a single review block into a structured dict.

    Fixed prefix is positional (always Quality, Difficulty, Course, Date), then
    we scan the remaining lines and classify each as a labeled field, a known
    tag, the free-text body, or footer/noise.
    """
    quality = float(block[1])
    difficulty = float(block[3])
    course = clean_course(block[4])
    date = clean_date(block[5])

    fields: dict[str, str] = {}
    tags: list[str] = []
    body: str | None = None

    for ln in block[6:]:
        if ln in ("Helpful", "Thumbs up"):
            break  # reached the footer (helpful label / thumbs) -> stop scanning
        field_match = _FIELD_RE.match(ln)
        if field_match:
            fields[field_match.group(1)] = field_match.group(2).strip()
        elif ln.lower() in RMP_TAGS:
            tags.append(RMP_TAGS[ln.lower()])
        elif ln.startswith("Reviewed:"):
            continue  # stray "last edited" marker -> drop
        else:
            # Not a field, not a known tag -> this is the review body.
            # (There is normally exactly one such line; some reviews have none.)
            body = ln if body is None else f"{body} {ln}"

    return {
        "quality": quality,
        "difficulty": difficulty,
        "course": course,
        "date": date,
        "fields": fields,
        "tags": tags,
        "body": body,
        "thumbs_up": _count_after(block, "Thumbs up"),
        "thumbs_down": _count_after(block, "Thumbs down"),
    }


def _count_after(block: list[str], label: str) -> int:
    """Return the integer on the line right after ``label`` (else 0)."""
    if label in block:
        idx = block.index(label)
        if idx + 1 < len(block):
            try:
                return int(block[idx + 1])
            except ValueError:
                return 0
    return 0


# --- Clean-doc writer --------------------------------------------------------
def format_clean_doc(overall: dict, reviews: list[dict]) -> str:
    """Render the parsed overall + reviews into the agreed clean-doc text."""
    out: list[str] = ["=== OVERALL ==="]
    out.append(f"Professor: {overall['professor']}")
    out.append(
        f"Overall Quality: {overall['overall_quality']}/5 "
        f"(based on {overall['num_ratings']} ratings)"
    )
    out.append(f"Would Take Again: {overall['would_take_again_pct']}%")
    out.append(f"Level of Difficulty: {overall['difficulty']}")
    d = overall["distribution"]
    out.append(
        "Rating Distribution: "
        f"Awesome (5): {d.get(5, 0)} | Great (4): {d.get(4, 0)} | "
        f"Good (3): {d.get(3, 0)} | OK (2): {d.get(2, 0)} | Awful (1): {d.get(1, 0)}"
    )

    out.append("")
    out.append("=== REVIEWS ===")
    for n, r in enumerate(reviews, start=1):
        out.append(f"--- Review {n} ---")
        out.append(f"Quality: {r['quality']}")
        out.append(f"Difficulty: {r['difficulty']}")
        out.append(f"Course: {r['course']}")
        out.append(f"Date: {r['date']}")
        for label in REVIEW_FIELDS:  # only emit fields that are present
            if label in r["fields"]:
                out.append(f"{label}: {r['fields'][label]}")
        out.append(f"Review: {r['body'] or ''}")
        out.append(f"Tags: {', '.join(r['tags'])}")
        out.append(f"Thumbs Up: {r['thumbs_up']}")
        out.append(f"Thumbs Down: {r['thumbs_down']}")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


# --- Driver ------------------------------------------------------------------
def professor_slugs() -> list[str]:
    """Discover professor slugs from the '*-overall.txt' files in documents/raw/."""
    suffix = "-overall.txt"
    return sorted(p.name[: -len(suffix)] for p in RAW_DIR.glob(f"*{suffix}"))


def build_clean_doc(slug: str) -> str:
    """Build the clean-doc text for one professor from their raw pair."""
    overall = parse_overall(load_raw(RAW_DIR / f"{slug}-overall.txt"))
    reviews = parse_reviews(load_raw(RAW_DIR / f"{slug}-reviews.txt"))
    return format_clean_doc(overall, reviews)


def main() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    for slug in professor_slugs():
        clean = build_clean_doc(slug)
        out_path = CLEAN_DIR / f"{slug}.txt"
        out_path.write_text(clean, encoding="utf-8")
        n_reviews = clean.count("--- Review ")
        print(
            f"{slug}: wrote {out_path.relative_to(PROJECT_ROOT)} "
            f"({n_reviews} reviews)"
        )


if __name__ == "__main__":
    main()
