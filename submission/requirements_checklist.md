# Requirement-to-Feature Checklist

| Source | Requirement | Implemented in app | Evidence to show in demo |
|---|---|---|---|
| Use Case #6 | Vendor scoring on cost | Yes | Cost Component + weighted score |
| Use Case #6 | Vendor scoring on quality | Yes | Quality Component + weighted score |
| Use Case #6 | Vendor scoring on lead time | Yes | Lead Time Component + weighted score |
| Use Case #6 | Weighted criteria user can adjust | Yes | Weighting mode -> Custom + sliders |
| Use Case #6 | Ranked shortlist with rationale | Yes | Top-3 cards + rationale + full ranking |
| Professor instruction | Pick one listed use case | Yes | Use Case #6 explicitly selected |
| Professor instruction | Use sample data | Yes | 30-record synthetic dataset included |
| Section A, Q1 | Problem and user | Yes | Project summary + demo opening |
| Section A, Q2/Q3 | Strengths and limitations | Yes | Explainable model + limitations |
| Section A, Q6 | Competitor comparison | Prepared | See Professor Q&A |
| Section A, Q7 | Adoption/monetization | Prepared | See Professor Q&A |
| Section B, Q1 | Model/API choice | Prepared | Deterministic weighted model; no paid API |
| Section B, Q2 | Guardrails / constraints | Yes | Validation + bounded criteria + deterministic formula |
| Section B, Q3 | Out-of-scope handling | Yes | App only ranks structured vendor data; malformed/out-of-scope CSV is rejected |
| Section B, Q4 | Data privacy | Prepared | No third-party API; local prototype |
| Section B, Q5 | Failure mode | Yes | Validation errors stop the ranking before output |
| Section C, Q1-Q4 | Honest capability assessment | Prepared | See Professor Q&A |
| Section D, Q1 | Edge-case test + user ease | Yes | Invalid quality score test + audit checks |
| Section E, Q1 | Input-to-output workflow | Yes | Data -> weights -> normalization -> weighted score -> ranking |
| Section E, Q2 | Input validation | Yes | Audit checks + upload validation |
| Section E, Q3 | Rule-of-thumb check | Yes | Transparent component scores make disagreements visible |
| Section E, Q4 | Explainability | Yes | Formula + score breakdown + rationale |
| Section E, Q5 | Session/state | Yes | Streamlit session maintains the selected controls during a live run; refresh can reset transient state |
| Section E, Q6 | Scaling | Prepared | See Professor Q&A |
| Section E, Q7 | Similar-input stability | Yes | Same data + same weights always produces the same deterministic ranking |
