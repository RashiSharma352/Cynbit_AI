import streamlit as st
from engine import analyse_inquiry

st.set_page_config(page_title="Cynbit Lead Intelligence Copilot", page_icon="🤖", layout="wide")
st.title("🤖 AI Lead Intelligence & Support Copilot")
st.caption("Assessment proof of concept | Synthetic sample data | Human review required")

st.info("Paste a sample customer inquiry. The prototype predicts a service category, estimates priority, retrieves related service information and drafts a suggested reply.")

examples = {
    "AI automation": "We need an AI agent to qualify website leads and answer common customer questions. Can you share a demo and pricing?",
    "Web development": "We need a responsive customer portal with login, dashboard and payment integration.",
    "Cloud": "Our production application is experiencing an outage and we need urgent help with AWS infrastructure.",
    "CRM automation": "We want to connect website forms to our CRM and automate lead follow-up emails.",
    "Product inquiry": "Please share information about Cynbit Studio and its AI code evaluation features.",
}
choice = st.selectbox("Load an example (optional)", ["Choose an example"] + list(examples.keys()))
default_text = examples.get(choice, "")
inquiry = st.text_area("Customer inquiry", value=default_text, height=140, placeholder="Example: We want to automate customer support using an AI assistant...")
if st.button("Analyse inquiry", type="primary", use_container_width=True):
    try:
        result = analyse_inquiry(inquiry)
        c1, c2, c3 = st.columns(3)
        c1.metric("Predicted service category", result["category"])
        c2.metric("Lead priority", result["priority"])
        c3.metric("Model confidence", f'{result["confidence"]:.0%}')
        st.subheader("Why this result?")
        st.write(result["priority_reason"])
        st.write(f'**Related knowledge:** {result["matched_service"]} (retrieval similarity: {result["match_score"]:.0%})')
        st.subheader("Suggested customer reply")
        st.text_area("Draft (edit before sending)", value=result["suggested_reply"], height=130)
        st.warning(result["disclaimer"])
    except ValueError as exc:
        st.error(str(exc))

with st.expander("How this prototype works"):
    st.markdown("""
    1. TF-IDF converts the inquiry into text features.
    2. A Multinomial Naive Bayes classifier predicts one of six service categories.
    3. Transparent keyword rules estimate urgency; this is not a trained priority model.
    4. TF-IDF cosine similarity retrieves the closest item from a small public-information knowledge base.
    5. A reviewed reply template is suggested. No email is sent automatically.
    """)
st.caption("All training examples are synthetic and created for this assessment. Do not enter personal, confidential or sensitive customer data.")
