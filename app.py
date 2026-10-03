from pathlib import Path
import pandas as pd
import streamlit as st

from vendor_logic import REQUIRED_COLUMNS, calculate_ranking, generate_rationale, validate_vendor_data

APP_TITLE = "AI-Powered Vendor Selection & Procurement Recommender"
BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA = BASE_DIR / "data" / "vendor_data.csv"

PRESETS = {
    "Balanced": {"Cost": 40, "Quality": 35, "Lead Time": 25},
    "Cost-focused": {"Cost": 60, "Quality": 25, "Lead Time": 15},
    "Quality-first": {"Cost": 20, "Quality": 60, "Lead Time": 20},
    "Speed-first": {"Cost": 20, "Quality": 25, "Lead Time": 55},
}


def load_data(uploaded_file=None) -> pd.DataFrame:
    """Load default or user-uploaded CSV data and validate it."""
    if uploaded_file is None:
        df = pd.read_csv(DEFAULT_DATA)
    else:
        try:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file)
        except Exception as exc:  # pragma: no cover - defensive UI handling
            raise ValueError(f"Could not read the CSV file: {exc}") from exc

    errors = validate_vendor_data(df)
    if errors:
        raise ValueError("\n".join(errors))

    for col in [
        "Unit Cost (₹ / 100 boxes)",
        "Quality Score (0-100)",
        "Lead Time (days)",
    ]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.copy()


def run_app() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="", layout="wide")
    st.title(APP_TITLE)
    st.caption(
        "Academic prototype for Use Case #6 from the End-Term Project Use Case Menu. "
        "The core ranking is deterministic and explainable; no paid API is required."
    )

    with st.sidebar:
        st.header("1. Load vendor data")
        uploaded = st.file_uploader(
            "Upload your own CSV (optional)", type=["csv"], help="Use the same columns as the sample dataset."
        )
        st.download_button(
            "Download sample dataset",
            data=DEFAULT_DATA.read_bytes(),
            file_name="vendor_data.csv",
            mime="text/csv",
        )

        st.header("2. Set decision priorities")
        mode = st.radio("Weighting mode", list(PRESETS.keys()) + ["Custom"], index=0)
        if mode == "Custom":
            cost_w = st.slider("Cost weight", 0, 100, 40, 5)
            quality_w = st.slider("Quality weight", 0, 100, 35, 5)
            lead_w = st.slider("Lead Time weight", 0, 100, 25, 5)
            raw_weights = {"Cost": cost_w, "Quality": quality_w, "Lead Time": lead_w}
            total = sum(raw_weights.values())
            if total <= 0:
                st.error("At least one criterion must have a weight above zero.")
                return
            weights = {k: (v / total) * 100 for k, v in raw_weights.items()}
            st.caption(f"Weights are normalized to 100% (input total: {total}%).")
        else:
            weights = PRESETS[mode]
            st.caption("Preset weights can be replaced by selecting Custom.")

        st.divider()
        st.header("3. Procurement context")
        st.info(
            "Sample scenario: selecting a supplier for corrugated shipping boxes. "
            "Cost and lead time are cost-type criteria (lower is better); quality is a benefit-type criterion (higher is better)."
        )

    try:
        df = load_data(uploaded)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    ranked = calculate_ranking(df, weights)
    top3 = ranked.head(3).copy()

    # Executive summary
    st.subheader("Decision snapshot")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Vendors evaluated", len(ranked))
    m2.metric("Top vendor", top3.iloc[0]["Vendor Name"])
    m3.metric("Top weighted score", f"{top3.iloc[0]['Weighted Score']:.1f}/100")
    m4.metric("Shortlist size", "Top 3")

    st.subheader("Ranked shortlist")
    cards = st.columns(3)
    for idx, (_, row) in enumerate(top3.iterrows()):
        with cards[idx]:
            st.markdown(f"### #{int(row['Rank'])} {row['Vendor Name']}")
            st.metric("Weighted score", f"{row['Weighted Score']:.1f}/100")
            st.write(f"Cost: ₹{row['Unit Cost (₹ / 100 boxes)']:.2f} / 100 boxes")
            st.write(f"Quality: {row['Quality Score (0-100)']:.1f}/100")
            st.write(f"Lead time: {row['Lead Time (days)']:.1f} days")
            st.caption(generate_rationale(row, weights))

    st.subheader("How the ranking is calculated")
    formula = (
        f"Weighted Score = {weights['Cost']/100:.2f} × Cost Score + "
        f"{weights['Quality']/100:.2f} × Quality Score + "
        f"{weights['Lead Time']/100:.2f} × Lead Time Score"
    )
    st.code(formula, language="text")
    st.caption(
        "Each criterion is normalized to a 0-100 score using min-max normalization. "
        "Lower cost/lead time is better; higher quality is better. This makes the output fully auditable."
    )

    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Top 10 vendor comparison")
        chart_df = ranked.head(10).set_index("Vendor Name")[["Weighted Score"]]
        st.bar_chart(chart_df, height=360)

    with right:
        st.subheader("Top 3 score breakdown")
        breakdown = top3[[
            "Vendor Name", "Cost Component", "Quality Component", "Lead Time Component", "Weighted Score"
        ]].copy()
        breakdown.columns = ["Vendor", "Cost score", "Quality score", "Lead-time score", "Final score"]
        st.dataframe(breakdown.round(1), use_container_width=True, hide_index=True)

    st.subheader("Full vendor table")
    display_cols = REQUIRED_COLUMNS + ["Cost Component", "Quality Component", "Lead Time Component", "Weighted Score", "Rank"]
    table_df = ranked[display_cols].copy()
    st.dataframe(
        table_df.style.format({
            "Unit Cost (₹ / 100 boxes)": "₹{:,.2f}",
            "Quality Score (0-100)": "{:.1f}",
            "Lead Time (days)": "{:.1f}",
            "Cost Component": "{:.1f}",
            "Quality Component": "{:.1f}",
            "Lead Time Component": "{:.1f}",
            "Weighted Score": "{:.1f}",
        }),
        use_container_width=True,
        hide_index=True,
        height=430,
    )

    download_df = ranked.copy()
    csv_bytes = download_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download ranked shortlist / full ranking",
        data=csv_bytes,
        file_name="vendor_ranking_output.csv",
        mime="text/csv",
    )

    with st.expander("Input validation & audit checks"):
        checks = [
            ("Required columns present", all(c in df.columns for c in REQUIRED_COLUMNS)),
            ("No blank required fields", not df[REQUIRED_COLUMNS].isnull().any().any()),
            ("Vendor IDs unique", not df["Vendor ID"].duplicated().any()),
            ("Cost > 0", bool((df["Unit Cost (₹ / 100 boxes)"] > 0).all())),
            ("Quality in 0-100", bool(df["Quality Score (0-100)"].between(0, 100).all())),
            ("Lead time > 0", bool((df["Lead Time (days)"] > 0).all())),
            ("Weights total 100% after normalization", abs(sum(weights.values()) - 100) < 1e-9),
        ]
        st.table(pd.DataFrame({"Check": [c[0] for c in checks], "Status": ["PASS" if c[1] else "FAIL" for c in checks]}))

    with st.expander("Requirement-to-feature checklist"):
        checklist = pd.DataFrame([
            ["Vendor scoring on cost", "Cost component score + weighted contribution", "Covered"],
            ["Vendor scoring on quality", "Quality component score + weighted contribution", "Covered"],
            ["Vendor scoring on lead time", "Lead-time component score + weighted contribution", "Covered"],
            ["Weighted criteria user can adjust", "Custom mode with adjustable weights and automatic normalization", "Covered"],
            ["Ranked shortlist with rationale", "Top-3 ranking cards + transparent rationale + full ranking table", "Covered"],
        ], columns=["Excel requirement", "Implemented feature", "Status"])
        st.dataframe(checklist, use_container_width=True, hide_index=True)

    with st.expander("Important limitation"):
        st.write(
            "This prototype supports procurement decisions; it does not replace a procurement professional. "
            "The ranking is only as good as the quality and relevance of the input data and the chosen weights. "
            "The sample dataset is synthetic and intended only for demonstration."
        )


if __name__ == "__main__":
    run_app()
