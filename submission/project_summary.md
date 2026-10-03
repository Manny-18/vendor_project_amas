# 1-Page Project Summary

## AI-Powered Vendor Selection & Procurement Recommender
**Academic format:** App | **Use Case:** #6 from the End-Term Project Use Case Menu

### Problem Statement
Procurement decisions often require a trade-off between cost, supplier quality and lead time. The application provides a structured way to compare vendors and make the trade-off explicit instead of relying on a single metric.

### Target Users
Procurement managers, purchase executives and small/medium business operators evaluating suppliers.

### Business Value
The app reduces manual comparison effort, makes decision criteria transparent, supports what-if analysis, and produces an auditable shortlist. The key value is not simply ranking vendors; it is showing how the ranking changes when management priorities change.

### Features Delivered
- Vendor scoring on cost, quality and lead time.
- User-adjustable weights, with automatic normalization to 100%.
- Ranked top-3 shortlist with business rationale.
- Full vendor comparison table and score breakdown.
- Optional CSV upload for custom data.
- Input validation and audit checks.
- Downloadable ranking output.

### Technology Used
Python, Streamlit and pandas. The core decision model is an explainable weighted scoring / MCDA-style approach using min-max normalization. No paid API or external LLM is required.

### Sample Data
30 synthetic vendor records for corrugated shipping boxes. Fields include vendor ID, vendor name, category, region, unit cost, quality score and lead time. The data is generated solely for academic demonstration.

### Limitations
Results depend on the quality of supplier inputs and the chosen weights. The prototype does not include negotiated commercial terms, compliance checks, supplier capacity risk, or verified historical performance. It is decision support, not an autonomous procurement approval system.

### Future Scope
Add validated historical supplier-performance data, supplier-risk alerts, contract-price analysis, ERP/CRM integration, purchase-volume constraints, and an approval workflow. A controlled LLM layer could later be added for natural-language explanations while keeping the core ranking deterministic.

**Assignment alignment:** The use-case menu requires scoring on cost/quality/lead time, adjustable weighted criteria, and a ranked shortlist with rationale; all three are implemented in the application.
