from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from vendor_logic import calculate_ranking, validate_vendor_data


def load_default():
    return pd.read_csv(ROOT / "data" / "vendor_data.csv")


def main():
    df = load_default()
    assert len(df) == 30
    assert validate_vendor_data(df) == []

    balanced = calculate_ranking(df, {"Cost": 40, "Quality": 35, "Lead Time": 25})
    assert balanced.iloc[0]["Vendor Name"] == "WestArc Packaging"
    assert balanced.head(3)["Rank"].tolist() == [1, 2, 3]

    speed = calculate_ranking(df, {"Cost": 20, "Quality": 25, "Lead Time": 55})
    assert speed.iloc[0]["Vendor Name"] == "NovaCarton Co."

    quality_first = calculate_ranking(df, {"Cost": 20, "Quality": 60, "Lead Time": 20})
    assert quality_first.iloc[0]["Vendor Name"] == "WestArc Packaging"

    bad = df.copy()
    bad.loc[0, "Quality Score (0-100)"] = 105
    assert any("Quality Score must be between 0 and 100." in x for x in validate_vendor_data(bad))

    dup = df.copy()
    dup.loc[1, "Vendor ID"] = dup.loc[0, "Vendor ID"]
    assert any("Vendor IDs must be unique." in x for x in validate_vendor_data(dup))

    negative = df.copy()
    negative.loc[2, "Lead Time (days)"] = 0
    assert any("Lead Time must be greater than zero." in x for x in validate_vendor_data(negative))

    print("All logic checks passed.")


if __name__ == "__main__":
    main()
