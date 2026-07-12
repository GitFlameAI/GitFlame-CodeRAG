from pipeline.schema import validate_schema, is_valid


def test_validate_schema_reports_missing_fields():
    row = {"id": 1, "name": "a"}
    missing = validate_schema(row)
    assert "amount" in missing
    assert "created_at" in missing


def test_is_valid_true_when_all_fields_present():
    row = {"id": 1, "name": "a", "amount": 1.0, "created_at": "2024-01-01"}
    assert is_valid(row)
