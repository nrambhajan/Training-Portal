"""
CSV Importer for Linux Training Portal
Parses the Daily Training Excel CSV format and creates modules + questions in the DB.
"""
import csv
import re
import io
from typing import Optional
from sqlalchemy.orm import Session
import models


# ── Section detection ────────────────────────────────────────────────────────

SECTION_KEYWORDS = [
    ("practical tasks", "Practical Tasks"),
    ("command execution scenarios", "Command Execution Scenarios"),
    ("practical questions", "Practical Questions"),
    ("theory questions", "Theory Questions"),
]

SEPARATOR_TERMS = {".", ",", "and", ", and", ", ,", "", "v"}

# Commands that indicate a practical task expected answer
COMMAND_PATTERN = re.compile(
    r"^\s*(ls|cd|mkdir|touch|rm|cp|mv|cat|grep|find|ps|kill|df|du|free|"
    r"mount|lsblk|stat|file|chmod|chown|useradd|userdel|passwd|systemctl|"
    r"service|apt|yum|dnf|tar|gzip|gunzip|ping|ssh|scp|curl|wget|uname|"
    r"hostname|pwd|echo|sort|head|tail|wc|less|more|awk|sed|lsof|w |who|"
    r"last|top|htop|nano|vi|vim|sudo|su|id|groups|which|whereis|locate|"
    r"updatedb|dd|fdisk|parted|lspci|lsusb|ifconfig|ip |netstat|ss |nmap|"
    r"cron|crontab|export|source|alias|unalias|history|man|info|help)",
    re.IGNORECASE,
)


def is_command(text: str) -> bool:
    return bool(COMMAND_PATTERN.match(text.strip()))


def extract_keywords(answer: str, n: int = 3) -> str:
    """Extract n meaningful words from an answer to use as verify_expected keyword."""
    # Strip common filler words
    stop = {"is", "a", "an", "the", "to", "of", "and", "in", "for", "that",
            "it", "this", "are", "was", "with", "be", "by", "on", "at", "or",
            "as", "from", "can", "its", "but", "not", "has", "have", "been"}
    words = re.findall(r"[a-zA-Z]{4,}", answer)
    meaningful = [w.lower() for w in words if w.lower() not in stop]
    return " ".join(meaningful[:n]) if meaningful else answer[:40]


def detect_question_type(text: str, answer: str, section: str) -> tuple[str, str, str, str]:
    """
    Returns (type, verify_command, verify_expected, verify_type)
    Types: mcq | practical | output | short_answer
    """
    text_lower = text.lower()

    # True/False
    if "true or false" in text_lower:
        return "mcq", "", "", ""

    # Practical section with a command-like expected answer
    if "practical" in section.lower() and is_command(answer):
        return "practical", answer.split("\n")[0].strip(), "", "exit_code"

    # Command output explanation (question mentions a specific command)
    if re.search(r"`[^`]+`|the output of|run .+command|explain.+command", text_lower):
        return "output", "", extract_keywords(answer), "contains"

    # Default: short answer (theory explanation)
    return "short_answer", "", extract_keywords(answer, 4), "contains"


# ── Main parser ──────────────────────────────────────────────────────────────

def parse_csv(content: str) -> list[dict]:
    """
    Parse CSV content and return list of question dicts grouped by module_title.
    """
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)

    # Pad all rows to at least 5 columns
    def pad(r):
        while len(r) < 5:
            r.append("")
        return r

    rows = [pad(r) for r in rows]

    day_name = "Day 1"
    current_section = "Theory"
    questions = []
    current_q = None
    order_counter = 0

    def flush():
        nonlocal current_q
        if current_q and current_q.get("text", "").strip():
            questions.append(current_q)
        current_q = None

    for row in rows:
        col0 = row[0].strip()
        col1 = row[1].strip()
        col2 = row[2].strip()

        # ── Skip blank rows ──────────────────────────────────────────────
        if not col0 and not col1 and not col2:
            continue

        # ── Day header (e.g. ",Day1,,,") ────────────────────────────────
        if not col0 and re.match(r"day\s*\d+", col1.lower()) and not col2:
            day_name = col1.strip()
            continue

        # ── Section header ───────────────────────────────────────────────
        if not col0 and col1 and not col2:
            matched_section = None
            for keyword, label in SECTION_KEYWORDS:
                if keyword in col1.lower():
                    matched_section = label
                    break
            if matched_section:
                flush()
                current_section = matched_section
                continue

        # ── Separator rows (., ,, blank sub-items) ───────────────────────
        if not col0 and col1.strip() in SEPARATOR_TERMS and not col2:
            continue

        # ── Numbered question ─────────────────────────────────────────────
        if col0 and (col0.isdigit() or re.match(r"^\d+$", col0)):
            flush()
            order_counter += 1
            current_q = {
                "module_title": f"{day_name} — {current_section}",
                "text": col1,
                "answer": col2,
                "order": order_counter,
                "section": current_section,
            }
            continue

        # ── Continuation row (blank col0, sub-term in col1) ──────────────
        if not col0 and current_q is not None:
            # Append sub-term to question text
            if col1 and col1 not in SEPARATOR_TERMS:
                # Check if it looks like a command on its own (sub-question)
                if is_command(col1) and not col2:
                    pass  # skip pure command rows that are separators
                else:
                    current_q["text"] = (current_q["text"] + " " + col1).strip()
            # Append answer
            if col2 and col2.strip() not in {".", "v"}:
                if current_q["answer"]:
                    current_q["answer"] += "\n" + col2
                else:
                    current_q["answer"] = col2
            continue

        # ── Un-numbered question (no col0 but has text + answer) ──────────
        if not col0 and col1 and col2:
            flush()
            order_counter += 1
            current_q = {
                "module_title": f"{day_name} — {current_section}",
                "text": col1,
                "answer": col2,
                "order": order_counter,
                "section": current_section,
            }

    flush()
    return questions


def import_csv_to_db(content: str, db: Session) -> dict:
    """Parse CSV and insert modules + questions into the database."""
    raw_questions = parse_csv(content)

    # Group by module title
    modules_map: dict[str, list] = {}
    for q in raw_questions:
        title = q["module_title"]
        modules_map.setdefault(title, []).append(q)

    created_modules = 0
    created_questions = 0

    for module_title, qs in modules_map.items():
        # Create module
        module = models.Module(title=module_title, description=f"Imported from CSV — {len(qs)} questions")
        db.add(module)
        db.flush()  # get module.id

        for q in qs:
            text = q["text"].strip()
            answer = q["answer"].strip()
            section = q["section"]

            if not text:
                continue

            q_type, verify_cmd, verify_expected, verify_type = detect_question_type(
                text, answer, section
            )

            options = None
            correct_answer = None

            if q_type == "mcq":
                options = ["True", "False"]
                # Detect correct answer from expected text
                if answer.lower().startswith("true"):
                    correct_answer = "0"
                else:
                    correct_answer = "1"

            question = models.Question(
                module_id=module.id,
                type=q_type,
                text=text,
                options=options,
                correct_answer=correct_answer,
                verify_command=verify_cmd or None,
                verify_expected=verify_expected or None,
                verify_type=verify_type or None,
                points=1.0,
                order=q["order"],
                hint=None,
            )
            db.add(question)
            created_questions += 1

        db.commit()
        created_modules += 1

    return {
        "modules_created": created_modules,
        "questions_created": created_questions,
        "module_titles": list(modules_map.keys()),
    }
