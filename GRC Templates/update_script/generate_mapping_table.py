#!/usr/bin/env python3
"""Regenerate or verify the policy-to-framework mapping table."""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "LLM - GRC Templates"
POLICIES = ROOT / "Policies"
TABLE = POLICIES / "00_mapping_table.md"
HEADERS = (
    "PCI DSS v4.0.1", "ISO 27001:2022", "ISO 27002:2022", "SOC 2 (TSP 2017)",
    "NIST 800-53 v5", "CIS Controls v8.1", "SCF 2025", "NIS2 Article 21",
    "ISO 27701:2025", "ISO 45001:2018", "ISO 42001:2023", "ISO 37001:2025",
    "ISO 9001:2015", "OWASP LLM Top 10 2025", "NIST AI 600-1 2024",
    "EU AI Act 2024/1689", "AESCSF-SP1",
)
TAG_HEADERS = {
    "PCI DSS v4.0.1": "PCI DSS v4.0.1",
    "ISO 27001:2022": "ISO 27001:2022",
    "ISO 27002:2022": "ISO 27002:2022",
    "SOC 2 (TSP 2017)": "SOC 2 (TSP 2017)",
    "NIST 800-53 Rev5": "NIST 800-53 v5",
    "CIS Controls v8.1": "CIS Controls v8.1",
    "SCF 2025": "SCF 2025",
    "NIS2 Article 21": "NIS2 Article 21",
    "ISO 27701:2025": "ISO 27701:2025",
    "ISO 45001:2018": "ISO 45001:2018",
    "ISO 42001:2023": "ISO 42001:2023",
    "ISO 37001:2025": "ISO 37001:2025",
    "ISO 9001:2015": "ISO 9001:2015",
    "OWASP Top 10 for LLM Applications 2025": "OWASP LLM Top 10 2025",
    "NIST AI 600-1 Generative AI Profile 2024": "NIST AI 600-1 2024",
    "EU AI Act 2024/1689": "EU AI Act 2024/1689",
}
TAG = re.compile(r"^\*\*(%s) \((.*)\)\*\*$" % "|".join(map(re.escape, TAG_HEADERS)))


def render():
    rows = []
    for policy in sorted(POLICIES.glob("*.md")):
        if policy == TABLE:
            continue
        title = next(line[2:].strip() for line in policy.read_text().splitlines() if line.startswith("# "))
        requirements = {header: set() for header in HEADERS}
        for line in policy.read_text().splitlines():
            match = TAG.match(line)
            if match:
                requirements[TAG_HEADERS[match.group(1)]].update(part.strip() for part in match.group(2).split(","))
        rows.append("| %s | %s |" % (title, " | ".join(", ".join(sorted(requirements[header])) or "—" for header in HEADERS)))
    return "\n".join((
        "# Policy to Framework Mapping",
        "",
        "Source of truth: requirement IDs extracted directly from tagged blocks in each policy `.md` file.",
        "",
        "| Policy | %s |" % " | ".join(HEADERS),
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|--- | --- |",
        *rows,
        "",
    ))


parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true")
args = parser.parse_args()
content = render()
if args.check:
    raise SystemExit(0 if TABLE.read_text() == content else "00_mapping_table.md is out of sync; run generate_mapping_table.py")
TABLE.write_text(content)
