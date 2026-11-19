"""CSV export of a patient statement (T-102).

Money is integer cents internally; it is formatted as dollars.cents only here,
at the output edge.
"""
from __future__ import annotations

import csv
import io

from medclaim.billing.statement import build_statement

HEADER = ["claim_id", "service_date", "charge", "voided"]


def format_cents(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    dollars, rem = divmod(abs(cents), 100)
    return f"{sign}{dollars}.{rem:02d}"


def statement_to_csv(patient_id: str) -> str:
    stmt = build_statement(patient_id)
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(HEADER)
    for ln in stmt.lines:
        writer.writerow([ln.claim_id, ln.service_date,
                         format_cents(ln.charge_cents),
                         "true" if ln.is_voided else "false"])
    writer.writerow(["TOTAL_CHARGES", "", format_cents(stmt.total_charges_cents), ""])
    writer.writerow(["TOTAL_ADJUSTMENTS", "", format_cents(stmt.total_adjustments_cents), ""])
    writer.writerow(["BALANCE", "", format_cents(stmt.balance_cents), ""])
    return out.getvalue()
