# Automated test cases verification for LynQX helper logic
def test_parse_scenarios():
    from utils import parse_scenario_line
    line = "TS001: User Login - Verify login functionality"
    parsed = parse_scenario_line(line)
    assert parsed is not None
    assert parsed[0] == "TS001"
    assert parsed[1] == "User Login"
    
def test_coverage_calculation():
    # Verify coverage math
    total = 10
    covered = 8
    pct = int((covered / total) * 100) if total else 0
    assert pct == 80
