import re

def parse_scenario_line(line):
    """Parses a raw line from LLM scenario output into scenario_id and name."""
    ts_match = re.match(r"^(?:\d+\.\s*)?(?:\*\*)?(TS\d{3})(?:\*\*)?:\s*(.*)", line)
    if ts_match:
        sid = ts_match.group(1).strip()
        name = ts_match.group(2).split("—")[0].split("-")[0].strip()
        return sid, name
    return None
