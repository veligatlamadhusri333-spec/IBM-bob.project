"""
clean_food_dataset.py
======================
Reads  : 'online food delivery dataset.csv'
Writes : 'online_food_delivery_clean.csv'  (cleaned)
         'cleaning_report.txt'             (full audit trail)

Issues identified and fixed
----------------------------
1.  Extra unnamed column  – The header ends with a trailing comma, creating
    a 14th empty column that is a duplicate of the 'Output' column in every
    row. → Dropped.

2.  Trailing whitespace in 'Feedback' values
    – 'Negative ' (71 rows) → 'Negative'
    → All cell values are stripped of leading/trailing whitespace.

3.  Typo in 'Occupation' column
    – 'Self Employeed' → 'Self Employed'

4.  Duplicate rows – 103 completely identical rows (all 13 meaningful
    columns) are removed; only the first occurrence is kept.

5.  Output / Feedback logical flag – 52 rows where Output='Yes' but
    Feedback='Negative', or Output='No' but Feedback='Positive'.
    These are NOT silently removed (they are real customer opinions) but
    are flagged in the cleaning report for downstream review.
"""

import csv
import os
from collections import Counter

INPUT_FILE  = "online food delivery dataset.csv"
OUTPUT_FILE = "online_food_delivery_clean.csv"
REPORT_FILE = "cleaning_report.txt"

# ── helpers ──────────────────────────────────────────────────────────────────

def read_raw_rows(path: str) -> tuple[list[str], list[dict]]:
    """Return (headers_list, rows_list_of_dicts) from raw CSV."""
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        headers = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    return headers, rows


def strip_all_values(rows: list[dict]) -> tuple[list[dict], int]:
    """Strip leading/trailing whitespace from every cell value."""
    count = 0
    cleaned = []
    for row in rows:
        new_row = {}
        for k, v in row.items():
            stripped = v.strip() if v else v
            if stripped != v:
                count += 1
            new_row[k] = stripped
        cleaned.append(new_row)
    return cleaned, count


def drop_unnamed_column(headers: list[str], rows: list[dict]) -> tuple[list[str], list[dict], bool]:
    """Remove the spurious empty-name column produced by the trailing header comma."""
    if "" in headers:
        clean_headers = [h for h in headers if h != ""]
        clean_rows = [{k: v for k, v in row.items() if k != ""} for row in rows]
        return clean_headers, clean_rows, True
    return headers, rows, False


def fix_occupation_typo(rows: list[dict]) -> tuple[list[dict], int]:
    """'Self Employeed' → 'Self Employed'."""
    count = 0
    for row in rows:
        if row.get("Occupation") == "Self Employeed":
            row["Occupation"] = "Self Employed"
            count += 1
    return rows, count


def remove_duplicates(rows: list[dict], key_cols: list[str]) -> tuple[list[dict], int]:
    """Keep only the first occurrence of each unique row (by key_cols)."""
    seen: set[tuple] = set()
    deduped: list[dict] = []
    removed = 0
    for row in rows:
        key = tuple(row.get(c, "") for c in key_cols)
        if key in seen:
            removed += 1
        else:
            seen.add(key)
            deduped.append(row)
    return deduped, removed


def flag_output_feedback_mismatches(rows: list[dict]) -> list[int]:
    """Return 1-based row indices (in cleaned data) where Output/Feedback seem inconsistent."""
    flagged = []
    for i, row in enumerate(rows, 1):
        out = row.get("Output", "")
        fb  = row.get("Feedback", "")
        if (out == "Yes" and fb == "Negative") or (out == "No" and fb == "Positive"):
            flagged.append(i)
    return flagged


def write_clean_csv(path: str, headers: list[str], rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: str, report_lines: list[str]) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(report_lines))


# ── main pipeline ─────────────────────────────────────────────────────────────

def main() -> None:
    report: list[str] = []
    report.append("=" * 65)
    report.append("  ONLINE FOOD DELIVERY DATASET — CLEANING REPORT")
    report.append("=" * 65)
    report.append(f"  Input  : {INPUT_FILE}")
    report.append(f"  Output : {OUTPUT_FILE}")
    report.append("")

    # ── Load ──────────────────────────────────────────────────────────────────
    headers, rows = read_raw_rows(INPUT_FILE)
    report.append(f"[LOAD]  {len(rows)} rows read, {len(headers)} header fields detected.")

    # ── Fix 1: strip whitespace (must come BEFORE other checks) ───────────────
    rows, ws_cells = strip_all_values(rows)
    report.append(f"\n[FIX 1] Whitespace stripped")
    report.append(f"        Cells corrected : {ws_cells}")
    report.append(f"        Primary example : 'Negative ' → 'Negative' in Feedback column")

    # ── Fix 2: drop unnamed empty column from trailing header comma ───────────
    headers, rows, dropped_col = drop_unnamed_column(headers, rows)
    report.append(f"\n[FIX 2] Trailing comma / unnamed column")
    if dropped_col:
        report.append("        Status  : FOUND & REMOVED")
        report.append("        Detail  : Header ended with ',' creating a 14th empty column")
        report.append("                  that duplicated 'Output' in every row.")
    else:
        report.append("        Status  : Not present")

    # ── Fix 3: occupation typo ────────────────────────────────────────────────
    rows, typo_count = fix_occupation_typo(rows)
    report.append(f"\n[FIX 3] Occupation typo  'Self Employeed' → 'Self Employed'")
    report.append(f"        Rows corrected : {typo_count}")

    # ── Fix 4: remove duplicate rows ─────────────────────────────────────────
    key_cols = headers  # all 13 meaningful columns
    rows, dup_count = remove_duplicates(rows, key_cols)
    report.append(f"\n[FIX 4] Duplicate rows removed")
    report.append(f"        Duplicates removed : {dup_count}")
    report.append(f"        Rows remaining     : {len(rows)}")

    # ── Flag 5: Output / Feedback mismatches (retained, not removed) ──────────
    flagged = flag_output_feedback_mismatches(rows)
    report.append(f"\n[FLAG 5] Output / Feedback logical inconsistencies")
    report.append(f"         Count   : {len(flagged)} rows  (NOT removed — real opinions)")
    report.append(f"         Detail  : Output='Yes' but Feedback='Negative', or vice versa.")
    report.append(f"         Action  : Rows retained; listed below for human review.")
    if flagged:
        report.append(f"         Row indices (1-based in cleaned file): {flagged}")

    # ── Summary ──────────────────────────────────────────────────────────────
    report.append("\n" + "=" * 65)
    report.append("  FINAL SUMMARY")
    report.append("=" * 65)
    report.append(f"  Columns in output       : {len(headers)}")
    report.append(f"  Rows in output          : {len(rows)}")
    report.append(f"  Whitespace cells fixed  : {ws_cells}")
    report.append(f"  Typos corrected         : {typo_count}")
    report.append(f"  Unnamed columns dropped : {1 if dropped_col else 0}")
    report.append(f"  Duplicate rows removed  : {dup_count}")
    report.append(f"  Rows flagged (Output/Feedback mismatch) : {len(flagged)}")
    report.append("")

    # ── Value distribution after cleaning ─────────────────────────────────────
    report.append("  VALUE DISTRIBUTIONS AFTER CLEANING")
    report.append("  -----------------------------------")
    categorical_cols = [
        "Gender", "Marital Status", "Occupation", "Monthly Income",
        "Educational Qualifications", "Customer Type", "Output", "Feedback"
    ]
    for col in categorical_cols:
        counts = Counter(r[col] for r in rows)
        report.append(f"  {col}:")
        for val, cnt in sorted(counts.items(), key=lambda x: -x[1]):
            report.append(f"    {val:<25} : {cnt}")

    ages = [int(r["Age"]) for r in rows]
    report.append(f"  Age  :  min={min(ages)}  max={max(ages)}  "
                  f"mean={sum(ages)/len(ages):.1f}")

    fam = [int(r["Family size"]) for r in rows]
    report.append(f"  Family size  :  min={min(fam)}  max={max(fam)}  "
                  f"mean={sum(fam)/len(fam):.1f}")

    # ── Write outputs ─────────────────────────────────────────────────────────
    write_clean_csv(OUTPUT_FILE, headers, rows)
    write_report(REPORT_FILE, report)

    # -- Console output (ASCII-safe for Windows cp1252 terminals) -------------
    for line in report:
        print(line.encode("ascii", errors="replace").decode("ascii"))

    print(f"\nDone. Cleaned CSV  -> {OUTPUT_FILE}")
    print(f"Done. Full report  -> {REPORT_FILE}")


if __name__ == "__main__":
    main()
