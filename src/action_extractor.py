import re
import dateparser
from typing import Dict 

# Simple patterns; expand as you like.
ACTION_PATTERNS = [
    r"\b(send|share|submit|deliver)\b",
    r"\b(schedule|arrange|book|setup)\b",
    r"\b(approve|review|confirm)\b",
    r"\b(pay|invoice|bill)\b",
]

DEADLINE_PATTERNS = [
    r"\bby\s+\d{1,2}(:\d{2})?\s*(am|pm)?\b",
    r"\bby\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday|eod|today|tomorrow)\b",
    r"\b(deadline|due)\s+(on|by)\s+([A-Za-z0-9 :/.-]+)\b",
]

def extract_actions(text: str) -> Dict[str, str]:
    text_l = text.lower()
    action = None
    for p in ACTION_PATTERNS:
        m = re.search(p, text_l)
        if m:
            action = m.group(0)
            break

    deadline = None
    for p in DEADLINE_PATTERNS:
        m = re.search(p, text_l)
        if m:
            when = m.group(0)
            dt = dateparser.parse(when, settings={"PREFER_DATES_FROM": "future"})
            deadline = dt.isoformat() if dt else when
            break

    return {"action": action, "deadline": deadline}
