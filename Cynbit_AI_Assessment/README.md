# Cynbit AI Assessment — AI Lead Intelligence & Support Copilot

**Applicant:** Rashi Sharma  
**Role:** AI/ML Engineer Intern  
**Project type:** Assessment proof of concept (PoC)

## 1. Problem and proposed opportunity

Cynbit publicly describes AI agents, LLM automation, CRM automation, software services and a proprietary SaaS product ecosystem. A useful internal opportunity is an **AI Lead Intelligence & Support Copilot** that helps a small team process inbound website enquiries consistently.

The PoC demonstrates:
- Service-category prediction from an inquiry.
- A transparent rule-based priority estimate.
- Retrieval of the closest relevant service information.
- A suggested response draft for human review.

## 2. Run locally

Use Python 3.10 or later.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Open the local URL shown by Streamlit (usually http://localhost:8501).

## 3. Run tests

```bash
pytest -q
```

## 4. Project structure

```text
Cynbit_AI_Assessment/
├── app/
│   ├── engine.py
│   └── streamlit_app.py
├── data/
│   └── synthetic_inquiries.csv
├── docs/
│   ├── AI_Opportunity_Report.md
│   └── Technical_Approach_Report.md
├── tests/
│   └── test_engine.py
├── requirements.txt
└── README.md
```

## 5. Data and limitations

The CSV contains **synthetic examples**, not Cynbit customer records. The knowledge base contains a concise summary of publicly described Cynbit service areas. The classifier is a baseline trained on a small illustrative dataset; its confidence is not a calibrated business probability and it must not be used for autonomous decisions. Priority is estimated using transparent keyword rules, not a trained model. The reply is a template, not a generated or verified company commitment.

Before production use, Cynbit would need approved historical enquiries, consent and retention rules, human-labelled categories, evaluation, security review, access controls and monitoring.

## 6. Public references reviewed

- https://www.cynbit.in/
- https://www.cynbit.in/services
- https://www.cynbit.in/products
- https://www.cynbit.in/contact
- https://in.linkedin.com/company/cynbit-in

## 7. Suggested next steps for a production pilot

1. Confirm the workflow and category taxonomy with Cynbit's team.
2. Collect and anonymise approved historical enquiries.
3. Create a human-labelled training and test set.
4. Compare baseline models and evaluate macro-F1, per-class precision/recall and priority agreement.
5. Add CRM integration only after permission and security review.
6. Pilot in recommendation-only mode with human approval for every reply.
