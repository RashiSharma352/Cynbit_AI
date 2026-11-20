# Technical Approach Report — AI Lead Intelligence & Support Copilot

**Prepared by:** Rashi Sharma  
**Role:** AI/ML Engineer Intern

## 1. Objective

Build a small functional proof of concept that accepts a text enquiry and returns:
- Predicted service category.
- A simple priority estimate and explanation.
- The closest matching item in a compact service knowledge base.
- A suggested response template.

The objective is to demonstrate an end-to-end baseline, not to claim production readiness.

## 2. Architecture

```text
User enquiry
    |
    v
Input validation and whitespace normalisation
    |
    +----------------------------+
    |                            |
    v                            v
TF-IDF + Naive Bayes       Keyword priority rules
category prediction        High / Medium / Low
    |                            |
    +-------------+--------------+
                  |
                  v
       TF-IDF knowledge retrieval
       (cosine similarity)
                  |
                  v
       Approved-style reply template
                  |
                  v
       Human review in Streamlit UI
```

## 3. Model choices

### Service classification

- Text representation: scikit-learn `TfidfVectorizer`, unigrams and bigrams.
- Baseline classifier: `MultinomialNB`.
- Reason: lightweight, fast, interpretable baseline for short text and easy local execution.
- Classes: AI Automation; Web & Mobile Development; Cloud & Infrastructure; CRM & Marketing Automation; Product & Platform Inquiry; General Support.

The training CSV contains only synthetic examples created for this assessment. The displayed confidence is the model's raw class probability and is **not calibrated**.

### Priority estimation

The PoC uses transparent keyword rules rather than pretending to train a priority model without representative labelled data. Explicit urgent/production terms map to High; strong buying or response-intent terms also map to High; otherwise a short enquiry maps to Low and other enquiries map to Medium. This is a demonstration rule set and should be replaced or validated with operational labels.

### Knowledge retrieval

A TF-IDF vectorizer represents the service knowledge snippets. Cosine similarity returns the closest snippet. This is a retrieval baseline, not a generative LLM or a full RAG system. The suggested response is a reviewed template associated with the retrieved service area.

## 4. Data pipeline

1. **Input:** one enquiry string from the Streamlit form.
2. **Validation:** reject very short input and normalise whitespace.
3. **Classification:** transform text and predict a service category.
4. **Priority:** apply transparent urgency rules.
5. **Retrieval:** compare the enquiry to the small service knowledge base.
6. **Response:** display the associated draft template.
7. **Human decision:** user reviews and edits; the PoC does not send email or write to a CRM.

### Data provenance

- `data/synthetic_inquiries.csv`: illustrative, synthetic examples authored for this PoC.
- Knowledge snippets: concise summaries of publicly available Cynbit website service descriptions.
- No real customer data, private records or credentials are included.

## 5. Prompt engineering and LLM architecture

This first version deliberately does not call an external LLM API. It uses retrieval and deterministic response templates to keep the prototype reproducible, inexpensive and auditable without API keys.

A production extension could use a retrieval-augmented generation (RAG) pattern:
- Retrieve only approved, versioned service and FAQ documents.
- Provide the LLM with the enquiry, retrieved passages and a strict response schema.
- Instruct it to use only supplied sources, state when information is missing, avoid inventing prices/timelines/commitments, and return an escalation flag.
- Require human approval before sending any reply.
- Log prompt/model versions and reviewer edits under an approved retention policy.

Example system instruction for a future implementation:

> You are a support-drafting assistant. Use only the supplied approved knowledge snippets. Do not invent prices, delivery dates, guarantees or policies. If the information is missing or confidence is low, ask a clarifying question or recommend human escalation. Draft a concise professional response. Never send the response.

## 6. Evaluation plan

The present synthetic dataset is suitable only for checking that the demo runs. It is not a valid measure of real-world performance.

For a pilot:
- Obtain permission to use historical enquiries and anonymise them.
- Create a human-labelled, stratified train/validation/test split.
- Compare Naive Bayes with Logistic Regression and Linear SVM.
- Report macro-F1, per-class precision/recall, confusion matrix and calibration.
- Have reviewers score retrieval relevance and reply factuality.
- Measure routing accuracy, review time, override rate and escalation quality.
- Test edge cases, spelling errors, mixed-service requests and out-of-scope questions.

## 7. Execution plan

| Phase | Work |
|---|---|
| 1. Discovery | Confirm enquiry channels, taxonomy, owners and success metrics |
| 2. Data readiness | Approve, anonymise and label sample enquiries |
| 3. Baseline | Train/evaluate text classifier and retrieval |
| 4. Workflow | Add review screen, audit trail and escalation |
| 5. Pilot | Run in shadow/recommendation-only mode |
| 6. Production decision | Security, privacy, integration and acceptance review |

## 8. Security and responsible use

- Do not paste real personal, financial or confidential data into this demo.
- Do not commit secrets, API keys or customer records.
- Use role-based access, encryption and retention controls in a production system.
- Keep a human in the loop for priority and all customer-facing responses.
- Provide a manual override and an escalation path.
- Review performance across service categories and monitor drift.

## 9. Current limitations

- Small synthetic training dataset.
- No held-out real-world evaluation.
- Priority is rule-based.
- Retrieval corpus is small and static.
- Response generation uses templates, not an LLM.
- No CRM, email, telephony or production deployment integration.

These limitations are explicit so that the PoC is not mistaken for a production system.
