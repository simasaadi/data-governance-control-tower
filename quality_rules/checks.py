import pandas as pd
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
CURATED_DIR = BASE_DIR / "data" / "curated"
RULES_PATH = BASE_DIR / "quality_rules" / "rules.yml"

ASSET_FILE_MAP = {
    "DA001": RAW_DIR / "service_requests.csv",
    "DA002": RAW_DIR / "work_orders.csv",
    "DA005": RAW_DIR / "dashboard_metrics.csv",
}

def load_rules():
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config.get("rules", [])

def load_asset_data(asset_id):
    file_path = ASSET_FILE_MAP.get(asset_id)
    if not file_path or not file_path.exists():
        return None
    return pd.read_csv(file_path)

def evaluate_rule(df, rule):
    column = rule["column_name"]
    check_type = rule["check_type"]
    threshold = float(rule.get("threshold", 1.0))

    if column not in df.columns:
        return {
            "passed": False,
            "pass_rate": 0.0,
            "rows_tested": len(df),
            "failed_rows": len(df),
            "message": f"Column '{column}' not found"
        }

    series = df[column]
    rows_tested = len(df)

    if check_type == "not_null":
        valid_mask = series.notna() & (series.astype(str).str.strip() != "")
        message = "Checked for null or blank values"

    elif check_type == "accepted_values":
        allowed_values = set(rule.get("allowed_values", []))
        valid_mask = series.isin(allowed_values)
        message = f"Checked accepted values: {sorted(allowed_values)}"

    elif check_type == "min_value":
        min_value = float(rule["min_value"])
        numeric_series = pd.to_numeric(series, errors="coerce")
        valid_mask = numeric_series >= min_value
        message = f"Checked minimum value >= {min_value}"

    elif check_type == "between":
        min_value = float(rule["min_value"])
        max_value = float(rule["max_value"])
        numeric_series = pd.to_numeric(series, errors="coerce")
        valid_mask = (numeric_series >= min_value) & (numeric_series <= max_value)
        message = f"Checked value between {min_value} and {max_value}"

    else:
        return {
            "passed": False,
            "pass_rate": 0.0,
            "rows_tested": rows_tested,
            "failed_rows": rows_tested,
            "message": f"Unsupported check type: {check_type}"
        }

    failed_rows = int((~valid_mask.fillna(False)).sum())
    pass_rate = 0.0 if rows_tested == 0 else round((rows_tested - failed_rows) / rows_tested, 4)
    passed = pass_rate >= threshold

    return {
        "passed": passed,
        "pass_rate": pass_rate,
        "rows_tested": rows_tested,
        "failed_rows": failed_rows,
        "message": message
    }

def main():
    CURATED_DIR.mkdir(parents=True, exist_ok=True)
    rules = load_rules()
    results = []

    for rule in rules:
        asset_id = rule["asset_id"]
        df = load_asset_data(asset_id)

        if df is None:
            results.append({
                "rule_id": rule["rule_id"],
                "asset_id": asset_id,
                "rule_name": rule["rule_name"],
                "column_name": rule["column_name"],
                "dimension": rule["dimension"],
                "severity": rule["severity"],
                "threshold": rule.get("threshold", 1.0),
                "pass_rate": 0.0,
                "rows_tested": 0,
                "failed_rows": 0,
                "passed": False,
                "message": f"No dataset mapped for asset_id {asset_id}"
            })
            continue

        evaluation = evaluate_rule(df, rule)

        results.append({
            "rule_id": rule["rule_id"],
            "asset_id": asset_id,
            "rule_name": rule["rule_name"],
            "column_name": rule["column_name"],
            "dimension": rule["dimension"],
            "severity": rule["severity"],
            "threshold": rule.get("threshold", 1.0),
            "pass_rate": evaluation["pass_rate"],
            "rows_tested": evaluation["rows_tested"],
            "failed_rows": evaluation["failed_rows"],
            "passed": evaluation["passed"],
            "message": evaluation["message"]
        })

    results_df = pd.DataFrame(results)
    output_path = CURATED_DIR / "quality_check_results.csv"
    results_df.to_csv(output_path, index=False)

    print("Quality checks completed.")
    print(f"Results saved to: {output_path}")
    print()
    print(results_df.to_string(index=False))

if __name__ == "__main__":
    main()
