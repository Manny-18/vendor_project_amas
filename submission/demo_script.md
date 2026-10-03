# 2-3 Minute Demo Script

## Opening (20-25 seconds)
"My project is an AI-powered vendor selection and procurement recommender. I selected Use Case #6 from the provided menu. The business problem is simple: procurement teams often have to balance cost, quality and lead time. My app makes those trade-offs explicit and generates a ranked vendor shortlist."

## Demo 1: Default / Balanced case (40-45 seconds)
1. Open the app.
2. Keep **Balanced** weighting: Cost 40%, Quality 35%, Lead Time 25%.
3. Point to the **Decision Snapshot** and say:
   "The app is evaluating 30 synthetic suppliers. It produces a top-three shortlist and shows the weighted score for each supplier."
4. Point to **WestArc Packaging** and say:
   "WestArc is ranked first under the balanced priorities. The rationale explains which criterion contributes most and where the trade-off sits."
5. Show the formula:
   "Each criterion is normalized to 0-100 and combined using the selected management weights. Because the calculation is deterministic, the result is auditable."

## Demo 2: Change the business priority (40-45 seconds)
1. Change **Weighting mode** to **Speed-first**.
2. Point to the new ranking and say:
   "Now I am changing the management priority. Lead time becomes 55% of the decision."
3. Show **NovaCarton Co.** moving to rank one.
4. Say:
   "The result changes because management has changed the decision objective. This is the key decision-support feature: the app does not pretend there is one universally correct vendor."

## Demo 3: Validation / audit (25-30 seconds)
1. Open **Input validation & audit checks**.
2. Say:
   "The app checks required columns, blanks, duplicate IDs, positive values, the quality range and weight normalization. This prevents poor inputs from silently producing a recommendation."

## Close (15-20 seconds)
"The output is a ranked shortlist rather than an autonomous purchasing decision. The sample data is synthetic. In a real deployment, I would connect the model to validated supplier, contract and historical performance data and keep human approval in the workflow."

## Exact demo sequence

**Input 1:** Balanced
- Cost = 40%
- Quality = 35%
- Lead Time = 25%
- Expected #1: WestArc Packaging

**Input 2:** Speed-first
- Cost = 20%
- Quality = 25%
- Lead Time = 55%
- Expected #1: NovaCarton Co.

**Optional Input 3:** Custom
- Cost = 60
- Quality = 25
- Lead Time = 15
- Expected #1: WestArc Packaging
