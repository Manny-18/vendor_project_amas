# Likely Professor Questions & Strong Answers

## A. Business & Strategic Framing

**Q: What specific problem does this app solve, and for whom?**

A: It supports procurement managers who need to compare suppliers across multiple criteria. The app makes the trade-off between cost, quality and lead time explicit and produces a shortlist rather than requiring manual spreadsheet comparison.

**Q: What does your app do better than a human or a spreadsheet?**

A: It standardizes the scoring logic, recalculates the ranking instantly when weights change, and makes the score components visible. A human still owns the final procurement decision.

**Q: Where can the app give an unreliable output?**

A: If the input data is outdated, biased or incomplete, the ranking can be misleading. The model is mathematically consistent, but it cannot know whether the supplier data itself is commercially valid.

**Q: Who are two real competitors?**

A: A real-world procurement workflow may use enterprise source-to-pay platforms such as SAP Ariba or Coupa, while a small team may use Excel/Google Sheets. My prototype is narrower: it focuses on transparent three-criteria vendor ranking and what-if weighting in a lightweight academic app.

**Q: How would you monetize it?**

A: A future B2B version could use a subscription model for small procurement teams, with paid integrations to ERP/procurement systems and supplier-risk modules. The academic prototype is intentionally free.

## B. AI / Technical Understanding

**Q: Which model or API are you using, and why?**

A: There is no external LLM API in the core decision path. I chose an explainable weighted scoring model because this use case is a structured multi-criteria decision problem. That gives zero API cost, low latency, deterministic output and full auditability. A future version could add a controlled LLM only for natural-language summaries.

**Q: Walk me through your system design.**

A: The input layer validates vendor data. The decision layer normalizes cost, quality and lead time to 0-100. User-selected weights are normalized to 100%. The app multiplies each component by its weight, adds the contributions, ranks vendors, and then converts the component scores into a short rationale.

**Q: What happens outside the intended scope?**

A: The app is designed for structured vendor data. A malformed CSV, missing column, blank required field, duplicate ID or invalid numeric range is rejected with an error rather than silently processed. It does not answer general procurement questions unrelated to the structured vendor dataset.

**Q: How is data privacy handled?**

A: The academic version does not send vendor data to a third-party API. Data is processed locally by the Streamlit application. In a real deployment, I would add access control, encryption, retention rules and audit logs.

**Q: What is the failure mode?**

A: The main failure mode is bad or unrepresentative input data. The app handles structural errors through validation, but it cannot independently verify whether a supplier's quality score is truthful.

## C. Critical Thinking / Honest Capability Assessment

**Q: Give an example of a misleading output.**

A: If a supplier has an unusually low cost recorded because of a data-entry error, the model may rank it too highly when cost has a large weight. The arithmetic would be correct but the business conclusion would be wrong.

**Q: What would you not trust it to do unsupervised?**

A: I would not let it approve purchase orders, sign contracts, or select a supplier without human review. Those decisions require commercial, legal, operational and compliance checks beyond three numerical criteria.

**Q: Who is accountable if the output is wrong?**

A: In a real deployment, accountability should remain with the business decision process. The app is a decision-support tool, not the legal or commercial decision-maker.

**Q: Biggest limitation?**

A: The model optimizes only the criteria included in the input. If the decision-maker ignores an important factor such as capacity, payment terms, financial health or compliance, the model cannot compensate for that omission.

## D / E. Execution & App-Specific Questions

**Q: Show an edge case.**

A: I tested a quality score above 100. The app rejects it before ranking. I also test duplicate vendor IDs, missing fields and non-positive cost/lead time values.

**Q: Walk through input-to-output flow.**

A: CSV/vendor table -> validation -> management weights -> criterion normalization -> weighted score -> descending rank -> top-3 shortlist -> rationale and downloadable output.

**Q: How can a user catch a disagreement with a rule-of-thumb?**

A: The app exposes the individual cost, quality and lead-time component scores. A user can see why the weighted score is high or low instead of seeing only a black-box rank.

**Q: How is the output explained?**

A: I show the scoring formula, each component score, the weighted score and a written rationale. This gives both numeric and business-readable explanations.

**Q: What happens if two users enter the same data and weights?**

A: They get the same ranking because the core model is deterministic. That is deliberate: consistency is more valuable here than creative variation.

**Q: How would this scale to 100 users/day?**

A: The current version is a single local Streamlit prototype. For 100 users/day, I would move data processing behind an application service, store data in a managed database, add authentication, caching where appropriate, and log requests/results for auditability.

## Optional closing line

"The design choice I made was to keep the decision engine simple, transparent and deterministic, and use AI only where it creates value without compromising auditability."
