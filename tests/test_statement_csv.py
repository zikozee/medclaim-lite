import csv
import io

from medclaim.billing.csv_export import format_cents, statement_to_csv
from medclaim.claims import void_claim


def _rows(text):
    return list(csv.reader(io.StringIO(text)))


def test_format_cents():
    assert format_cents(0) == "0.00"
    assert format_cents(5) == "0.05"
    assert format_cents(12_550) == "125.50"
    assert format_cents(-250) == "-2.50"


def test_csv_has_line_per_claim_and_totals(client, seed):
    a, b = seed.claims(patient_id="P-2001", amounts_cents=[12_500, 8_005],
                       adjusted=[0, 805])
    rows = _rows(statement_to_csv("P-2001"))
    assert rows[0] == ["claim_id", "service_date", "charge", "voided"]
    body = {r[0]: r for r in rows[1:-3]}
    assert body[a.id][2:] == ["125.00", "false"]
    assert body[b.id][2:] == ["80.05", "false"]
    assert rows[-3] == ["TOTAL_CHARGES", "", "205.05", ""]
    assert rows[-2] == ["TOTAL_ADJUSTMENTS", "", "8.05", ""]
    assert rows[-1] == ["BALANCE", "", "197.00", ""]


def test_csv_excludes_voided_claims(client, seed):
    claim = seed.claim(patient_id="P-2001", amount_cents=9_900)
    void_claim(claim.id, reason="duplicate")
    assert claim.id not in statement_to_csv("P-2001")


def test_csv_endpoint_returns_200_with_csv(client, seed):
    from fastapi.testclient import TestClient

    from medclaim.api import app

    claim = seed.claim(patient_id="P-2001", amount_cents=12_500)
    resp = TestClient(app).get("/patients/P-2001/statement.csv")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/csv")
    rows = _rows(resp.text)
    assert rows[0] == ["claim_id", "service_date", "charge", "voided"]
    assert [claim.id, "2024-06-01", "125.00", "false"] in rows
    assert rows[-3] == ["TOTAL_CHARGES", "", "125.00", ""]
    assert rows[-1] == ["BALANCE", "", "125.00", ""]
