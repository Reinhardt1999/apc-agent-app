import streamlit as st
import time

st.set_page_config(page_title="APC Agent Pro", layout="wide")

# ==========================
# NAVIGATION
# ==========================
page = st.sidebar.selectbox("Navigate", [
    "Home",
    "Analyse Case",
    "Research Pack",
    "Practice Exam",
    "Submit Answer"
])

# ==========================
# HOME PAGE
# ==========================
if page == "Home":
    st.title("🏠 APC Preparation Agent (CA SA)")

    st.write("""
    Simulate the SAICA APC with structured tools:
    - Trigger identification
    - Research pack building
    - Exam simulation
    - Competency-based marking
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.info("📄 Analyse Case")
        st.info("📘 Build Research Pack")

    with col2:
        st.info("🧪 Practice Exam")
        st.info("✅ Submit & Get Marked")

# ==========================
# FUNCTIONS
# ==========================
def identify_triggers(text):
    keywords = {
        "Accounting": ["revenue", "IFRS", "lease", "impairment"],
        "Audit": ["control", "fraud", "risk"],
        "Tax": ["tax", "VAT", "SARS"],
        "Financial Management": ["cash", "liquidity", "budget"],
        "Ethics": ["pressure", "conflict", "governance"]
    }

    results = []

    for category, words in keywords.items():
        for word in words:
            if word.lower() in text.lower():
                risk = classify_risk(word)
                results.append((category, word, risk))

    return list(set(results))


def classify_risk(word):
    high = ["fraud", "going concern"]
    medium = ["revenue", "tax", "IFRS"]

    if word in high:
        return "HIGH"
    elif word in medium:
        return "MEDIUM"
    return "LOW"


def competency_level(ans):
    ans = ans.lower()

    strong = ["therefore", "recommend", "because", "risk", "ifrs", "audit"]

    score = sum([1 for w in strong if w in ans])

    if len(ans) > 500 and score >= 5:
        return "Highly Competent"
    elif len(ans) > 350 and score >= 4:
        return "Competent"
    elif len(ans) > 250:
        return "Borderline Competent"
    elif len(ans) > 150:
        return "Limited Competent"
    else:
        return "Not Competent"


def generate_feedback(ans):
    feedback = []

    if "ifrs" not in ans.lower():
        feedback.append("⚠️ Include IFRS references")

    if "risk" not in ans.lower():
        feedback.append("⚠️ Clearly identify risks")

    if "recommend" not in ans.lower():
        feedback.append("⚠️ Provide clear recommendations")

    if "therefore" not in ans.lower():
        feedback.append("⚠️ Strengthen your conclusion")

    if len(ans.split()) < 200:
        feedback.append("⚠️ Increase depth of analysis")

    return feedback

# ==========================
# ANALYSE CASE
# ==========================
elif page == "Analyse Case":
    st.header("📄 Analyse Case Study")

    uploaded_file = st.file_uploader("Upload case (txt)", type=["txt"])
    text_input = st.text_area("Or paste case")

    case = ""

    if uploaded_file:
        case = uploaded_file.read().decode("utf-8")
    elif text_input:
        case = text_input

    if st.button("Identify Triggers"):
        if case:
            triggers = identify_triggers(case)

            st.subheader("Detected Issues")

            for t in triggers:
                st.write(f"✅ {t[0]} → {t[1]} ({t[2]} risk)")
        else:
            st.warning("Upload or paste a case")

# ==========================
# RESEARCH PACK
# ==========================
elif page == "Research Pack":
    st.header("📘 Research Pack Generator")

    case = st.text_area("Paste case")

    if st.button("Generate Pack"):
        if case:
            triggers = identify_triggers(case)

            summary = "Key Risks Identified:\n"
            for t in triggers:
                summary += f"- {t[0]} ({t[2]} risk)\n"

            audit = "Audit focus on control weaknesses and fraud risk."
            accounting = "Apply IFRS standards appropriately."
            tax = "Assess SARS exposure and compliance."
            fm = "Evaluate liquidity and sustainability."

            st.subheader("Executive Summary")
            st.write(summary)

            st.subheader("Audit")
            st.write(audit)

            st.subheader("Accounting")
            st.write(accounting)

            st.subheader("Tax")
            st.write(tax)

            st.subheader("Financial Management")
            st.write(fm)

        else:
            st.warning("Enter a case")

# ==========================
# PRACTICE EXAM
# ==========================
elif page == "Practice Exam":
    st.header("🧪 APC Simulation")

    case = st.text_area("Paste case for simulation")

    if st.button("Generate Exam"):
        if case:
            triggers = identify_triggers(case)

            st.subheader("Case Study")
            st.write(case)

            st.subheader("REQUIRED:")

            st.write("1. Evaluate accounting treatment")
            st.write("2. Identify audit risks & procedures")
            st.write("3. Discuss tax implications")
            st.write("4. Provide integrated recommendation")

            # TIMER

