import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict


def timestamp_utc() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d_%H%M%S_UTC")


def write_markdown(records: List[Dict], out_path: Path, header: str):
    lines = []
    lines.append(f"# {header}")
    lines.append("")
    lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
    lines.append("")
    lines.append("| Type | Name | State | OCID | Notes |")
    lines.append("|---|---|---|---|---|")

    for r in records:
        notes = []
        if "cidr" in r:
            notes.append(f"CIDR={r['cidr']}")
        if "availability_domain" in r and r["availability_domain"]:
            notes.append(f"AD={r['availability_domain']}")
        if "vcn_name" in r:
            notes.append(f"VCN={r['vcn_name']}")

        lines.append(
            f"| {r.get('type','')} | {r.get('name','')} | {r.get('state','')} | {r.get('ocid','')} | {'; '.join(notes)} |"
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(records: List[Dict], out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Collect all keys so CSV includes every field
    keys = set()
    for r in records:
        keys.update(r.keys())
    keys = sorted(keys)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(records)
