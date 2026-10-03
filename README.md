# AI-Powered Vendor Selection & Procurement Recommender

Academic end-term project for the listed use case **#6: Vendor selection or procurement recommender**.

## What the app does

The app compares vendors on the three criteria specified in the assignment use-case menu:

1. Cost
2. Quality
3. Lead time

The user can change the weighting of those criteria. The app normalizes each criterion to a 0-100 score, calculates a weighted score, ranks every vendor, and produces a top-3 shortlist with an auditable rationale.

## Technology

- Python
- Streamlit
- pandas
- No paid API
- No API key required

The project deliberately uses an **explainable weighted decision model** instead of an external LLM for the core recommendation. Procurement ranking is a structured decision problem, so a deterministic model makes the result reproducible and easier to audit. The app also generates a concise rationale from the score components.

## Dataset

`data/vendor_data.csv` contains 30 synthetic vendor records for corrugated shipping boxes. The data is fabricated for academic demonstration and is not presented as real supplier information.

## Folder structure

```text
vendor_procurement_app/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── vendor_data.csv
│   └── vendor_data.xlsx
├── submission/
│   ├── Project_Summary_and_Demo_Guide.docx
│   ├── project_summary.md
│   ├── demo_script.md
│   ├── professor_qa.md
│   └── requirements_checklist.md
└── tests/
    └── test_logic.py
```

## Exact setup steps

### Windows / macOS / Linux

1. Install Python 3.10 or newer.
2. Open Terminal / Command Prompt.
3. Move into the project folder:

```bash
cd vendor_procurement_app
```

4. Create a virtual environment:

```bash
python -m venv .venv
```

5. Activate it.

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

6. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

7. Start the app:

```bash
python -m streamlit run app.py
```

8. Streamlit will open the app in your browser. If it does not, open the local URL shown in the terminal, usually `http://localhost:8501`.

## Fast demo path

Start with **Balanced** weighting (40% Cost, 35% Quality, 25% Lead Time). The top vendor should be **WestArc Packaging** in the supplied synthetic dataset.

Then switch to **Speed-first** weighting (20% Cost, 25% Quality, 55% Lead Time). The leading vendor changes to **NovaCarton Co.** This demonstrates that the recommendation responds to management priorities instead of being a fixed answer.

## Custom data format

If you upload your own CSV, use these exact column names:

- Vendor ID
- Vendor Name
- Category
- Region
- Unit Cost (₹ / 100 boxes)
- Quality Score (0-100)
- Lead Time (days)

The app validates required columns, blanks, duplicate IDs, numeric fields, positive cost/lead-time values, quality range, and non-zero weights.

## Important academic limitation

The sample data is synthetic. The app is a decision-support prototype and should not be used as a real procurement authority without validated supplier data, commercial terms, compliance checks, and human approval.
