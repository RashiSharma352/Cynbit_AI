import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = __import__("pathlib").Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "synthetic_inquiries.csv"

KNOWLEDGE_BASE = [
    {
        "title": "AI automation, agents and LLM solutions",
        "category": "AI Automation",
        "content": "Cynbit describes autonomous AI agents, LLM automation, AI voice agents and AI stack integration. Potential work includes intelligent assistants, document handling and workflow automation.",
        "reply": "Thanks for reaching out. Cynbit works on AI automation, LLM integrations and intelligent agent workflows. Please share the process you want to automate, the systems involved and your expected outcome so the team can assess a suitable approach."
    },
    {
        "title": "Web and mobile software development",
        "category": "Web & Mobile Development",
        "content": "Cynbit offers full-stack web and mobile platform development, backend systems and custom software solutions.",
        "reply": "Thanks for your interest. Cynbit supports custom web and mobile software development. Please share your target users, key features, preferred platforms and expected timeline so the team can understand your requirements."
    },
    {
        "title": "Cloud and infrastructure",
        "category": "Cloud & Infrastructure",
        "content": "Cynbit lists cloud infrastructure, AWS and Azure deployment, backend foundations, legacy migration and scalable systems.",
        "reply": "Thanks for contacting us. Cynbit works with cloud infrastructure and scalable backend systems. Please share your current hosting setup, scale requirements and the main issue or outcome you are targeting."
    },
    {
        "title": "CRM, marketing automation and SEO",
        "category": "CRM & Marketing Automation",
        "content": "Cynbit lists CRM automation, lead nurturing, funnel optimization, performance ads and technical SEO services.",
        "reply": "Thanks for your inquiry. Cynbit's digital growth services include CRM automation, lead nurturing and technical SEO. Please tell us which CRM or marketing tools you use and what workflow you would like to improve."
    },
    {
        "title": "Cynbit products and platforms",
        "category": "Product & Platform Inquiry",
        "content": "Cynbit's public website describes a proprietary SaaS ecosystem including Cynbit Studio, Revio AI Review Assistant and TenantEase. Product details should be confirmed with the company.",
        "reply": "Thanks for your interest in Cynbit's products. Please let us know which platform you are interested in and whether you are enquiring as an individual, institution or business. The team can then share the most relevant information."
    },
    {
        "title": "General enquiries and support",
        "category": "General Support",
        "content": "For general enquiries, project discussions or support, Cynbit publishes opportunities@cynbit.in and support@cynbit.in on its contact page.",
        "reply": "Thanks for contacting Cynbit. We have noted your enquiry. Please share any relevant project or support reference and the best way to reach you. For direct assistance, the public contact page lists support@cynbit.in."
    },
]

def load_model():
    df = pd.read_csv(DATA_PATH)
    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True, stop_words="english")),
        ("classifier", MultinomialNB(alpha=0.35)),
    ])
    model.fit(df["inquiry"].astype(str), df["category"].astype(str))
    return model

MODEL = load_model()
KB_VECTOR = TfidfVectorizer(stop_words="english")
KB_MATRIX = KB_VECTOR.fit_transform([x["content"] + " " + x["title"] for x in KNOWLEDGE_BASE])

def classify_priority(text):
    t = text.lower()
    urgent_terms = ["urgent", "production down", "outage", "blocked", "asap", "immediately", "critical", "deadline today"]
    high_intent_terms = ["pricing", "quote", "demo", "proposal", "call me", "purchase", "production issue"]
    if any(term in t for term in urgent_terms):
        return "High", "Urgency keyword detected"
    if any(term in t for term in high_intent_terms):
        return "High", "Strong buying or response intent detected"
    if len(text.split()) < 5:
        return "Low", "Short inquiry; more context is needed"
    return "Medium", "No explicit urgency signal detected"

def analyse_inquiry(text):
    text = re.sub(r"\s+", " ", (text or "")).strip()
    if len(text) < 8:
        raise ValueError("Please enter a little more detail (at least 8 characters).")
    probabilities = MODEL.predict_proba([text])[0]
    classes = MODEL.named_steps["classifier"].classes_
    best_idx = probabilities.argmax()
    category = str(classes[best_idx])
    confidence = float(probabilities[best_idx])
    priority, priority_reason = classify_priority(text)

    query_vec = KB_VECTOR.transform([text])
    similarities = cosine_similarity(query_vec, KB_MATRIX)[0]
    kb_idx = int(similarities.argmax())
    knowledge = KNOWLEDGE_BASE[kb_idx]

    return {
        "category": category,
        "confidence": confidence,
        "priority": priority,
        "priority_reason": priority_reason,
        "matched_service": knowledge["title"],
        "match_score": float(similarities[kb_idx]),
        "suggested_reply": knowledge["reply"],
        "disclaimer": "Prototype suggestion only. A human team member must verify category, priority and reply before contacting a customer."
    }
