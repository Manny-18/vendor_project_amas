import pandas as pd

REQUIRED_COLUMNS = [
    "Vendor ID",
    "Vendor Name",
    "Category",
    "Region",
    "Unit Cost (₹ / 100 boxes)",
    "Quality Score (0-100)",
    "Lead Time (days)",
]


def validate_vendor_data(df: pd.DataFrame) -> list[str]:
    errors: list[str] = []
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        errors.append("Missing required columns: " + ", ".join(missing))
        return errors
    if df.empty:
        errors.append("The dataset is empty. Add at least 3 vendor records.")
        return errors
    if len(df) > 500:
        errors.append("For this demo app, please keep the dataset to 500 records or fewer.")
    if df["Vendor ID"].duplicated().any():
        errors.append("Vendor IDs must be unique.")
    if df[REQUIRED_COLUMNS].isnull().any().any():
        errors.append("Required fields cannot contain blank values.")

    numeric_cols = [
        "Unit Cost (₹ / 100 boxes)",
        "Quality Score (0-100)",
        "Lead Time (days)",
    ]
    for col in numeric_cols:
        converted = pd.to_numeric(df[col], errors="coerce")
        if converted.isnull().any():
            errors.append(f"{col} must contain numeric values only.")

    cost = pd.to_numeric(df["Unit Cost (₹ / 100 boxes)"], errors="coerce")
    quality = pd.to_numeric(df["Quality Score (0-100)"], errors="coerce")
    lead = pd.to_numeric(df["Lead Time (days)"], errors="coerce")
    if not cost.gt(0).all():
        errors.append("Unit Cost must be greater than zero.")
    if not quality.between(0, 100).all():
        errors.append("Quality Score must be between 0 and 100.")
    if not lead.gt(0).all():
        errors.append("Lead Time must be greater than zero.")
    return errors


def min_max_benefit(series: pd.Series) -> pd.Series:
    min_v, max_v = float(series.min()), float(series.max())
    if max_v == min_v:
        return pd.Series(100.0, index=series.index)
    return ((series - min_v) / (max_v - min_v)) * 100


def min_max_cost(series: pd.Series) -> pd.Series:
    min_v, max_v = float(series.min()), float(series.max())
    if max_v == min_v:
        return pd.Series(100.0, index=series.index)
    return ((max_v - series) / (max_v - min_v)) * 100


def calculate_ranking(df: pd.DataFrame, weights: dict[str, float]) -> pd.DataFrame:
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("At least one criterion must have a weight above zero.")
    normalized_weights = {k: (v / total) * 100 for k, v in weights.items()}

    ranked = df.copy()
    ranked["Cost Component"] = min_max_cost(ranked["Unit Cost (₹ / 100 boxes)"])
    ranked["Quality Component"] = min_max_benefit(ranked["Quality Score (0-100)"])
    ranked["Lead Time Component"] = min_max_cost(ranked["Lead Time (days)"])

    ranked["Weighted Score"] = (
        ranked["Cost Component"] * normalized_weights["Cost"] / 100
        + ranked["Quality Component"] * normalized_weights["Quality"] / 100
        + ranked["Lead Time Component"] * normalized_weights["Lead Time"] / 100
    )
    ranked["Rank"] = ranked["Weighted Score"].rank(method="min", ascending=False).astype(int)
    return ranked.sort_values(["Weighted Score", "Vendor Name"], ascending=[False, True]).reset_index(drop=True)


def generate_rationale(row: pd.Series, weights: dict[str, float]) -> str:
    total = sum(weights.values())
    weights = {k: v / total * 100 for k, v in weights.items()}
    contributions = {
        "Cost": row["Cost Component"] * weights["Cost"] / 100,
        "Quality": row["Quality Component"] * weights["Quality"] / 100,
        "Lead Time": row["Lead Time Component"] * weights["Lead Time"] / 100,
    }
    strongest = max(contributions, key=contributions.get)
    weakest = min(contributions, key=contributions.get)
    return (
        f"{row['Vendor Name']} ranks #{int(row['Rank'])} with a weighted score of "
        f"{row['Weighted Score']:.1f}/100. Its strongest contributor is {strongest}, "
        f"while {weakest} is the main trade-off under the selected weights. "
        f"Raw metrics: cost ₹{row['Unit Cost (₹ / 100 boxes)']:.2f} per 100 boxes, "
        f"quality {row['Quality Score (0-100)']:.1f}/100, and lead time {row['Lead Time (days)']:.1f} days."
    )
