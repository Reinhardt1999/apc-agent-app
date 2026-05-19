import streamlit as st
import time

st.set_page_config(page_title="APC Agent V11", layout="wide")

# ==========================
# SESSION STATE
# ==========================
if "history" not in st.session_state:
    st.session_state.history = []

# ==========================
# CONFIG
# ==========================
trigger_map = {
    "Accounting": ["revenue", "ifrs", "lease", "impairment"],
    "Audit": ["control", "fraud", "risk"],
    "Tax": ["tax", "vat", "sars"],
    "FM": ["cash", "liquidity", "budget"],
    "Ethics": ["pressure", "conflict", "governance"]
}

# ==========================
# TRIGGER IDENTIFICATION
# ==========================
def identify_triggers(text):
    results = []
    sentences = text.split(".")

    for category, words in trigger_map.items():
        for word in words:
            if word in text.lower():
                example = next((s.strip() for s in sentences if word in s.lower()), "")
                results.append({
                    "category": category,
                    "word": word,
                    "strength": "STRONG" if word in ["fraud", "revenue"] else "WEAK",
                    "example": example
                })

    return results

# ==========================
# HIGHLIGHT CASE TEXT
# ==========================
def highlight(text, triggers):
    for t in triggers:
        color = "red" if t["strength"] == "STRONG" else "yellow"
        text = text.replace(
            t["word"],
            f"<mark style='background:{color}'>{t['word']}</mark>"
        )
    return text

# ==========================
# MARKING ENGINE
# ==========================
def grade(answer):
    answer = answer.lower()
    length = len(answer.split())

    if length > 500 and "ifrs" in answer:
        return "Highly Competent"
    elif length > 350:
        return "Competent"
    elif length > 250:
        return "Borderline Competent"
    elif length > 150:
        return "Limited Competent"
    return "Not Competent"

# ==========================
# COMPETENCY SCORING
# ==========================
def competency_scores(answer):
    answer = answer.lower()

    return {
        "Accounting (III)": "✅" if "ifrs" in answer else "❌",
        "Audit (IV)": "✅" if "risk" in answer else "❌",
        "Tax (VII)": "✅" if "tax" in answer else "❌",
        "Financial Management (V)": "✅" if "cash" in answer or "liquidity" in answer else "❌"
    }

# ==========================
# MISSED TRIGGERS
# ==========================
def missed_triggers(triggers, answer):
    return [t["word"] for t in triggers if t["word"] not in answer.lower()]

# ==========================
# MODEL ANSWERS
# ==========================
def model_answer(triggers):
    output = []

    for t in triggers:
        if t["category"] == "Accounting":
            output.append("Apply IFRS principles and evaluate recognition, measurement and disclosure.")

        elif t["category"] == "Audit":
            output.append("Identify significant risks and design audit procedures in line with ISA standards.")

        elif t["category"] == "Tax":
            output.append("Evaluate tax implications, timing differences and compliance requirements.")

        elif t["category"] == "FM":
            output.append("Assess liquidity, cash flow impact and financial sustainability.")

        elif t["category"] == "Ethics":
            output.append("Apply ethical reasoning using the SAICA Code of Professional Conduct.")

    return list(set(output))

# ==========================
# AI EXAMINER COMMENTS
# ==========================
def examiner_comments(answer, grade):
    comments = []

    if grade == "Highly Competent":
        comments.append("Strong integrated response demonstrating sound judgement and technical depth.")

    elif grade == "Competent":
        comments.append("Generally competent response but lacks deeper integration across disciplines.")

    elif grade == "Borderline Competent":
        comments.append("Basic understanding shown but lacks sufficient analysis and depth.")

    elif grade == "Limited Competent":
        comments.append("Answer shows limited technical understanding and weak application.")

    else:
        comments.append("Response does not demonstrate required competency level.")

    if "ifrs" not in answer.lower():
        comments.append("Insufficient application of IFRS principles.")

    if "risk" not in answer.lower():
        comments.append("Audit risks are not clearly identified.")

    if "recommend" not in answer.lower():
        comments.append("Lack of clear recommendations and professional judgement.")

    return comments

# ==========================
# ADAPTIVE LEARNING
# ==========================
def suggest_next_step(grade):
    if grade == "Highly Competent":
        return "✅ Attempt advanced integrated APC cases."

    elif grade == "Competent":
        return "📈 Improve integration between accounting, audit and tax."

    elif grade == "Borderline Competent":
        return "⚠️ Revise IFRS and audit risk identification."

    elif grade == "Limited Competent":
        return "❗ Focus on core technical knowledge and structure."

    return "🚨 Rebuild foundation before attempting full APC cases."

# ==========================
# NAVIGATION
# ==========================
page = st.sidebar.selectbox("Navigation", [
    "Home",
    "Case Analysis",
    "Mock Exam",
    "Submit Exam",
    "Dashboard"
])

# ==========================
# HOME
# ==========================
if page == "Home":
    st.title("🏠 APC Agent V11")

    st.markdown("""
    ### Full APC Simulation Platform

    ✅ Trigger Identification  
    ✅ Case Analysis (highlighting)  
    ✅ Mock Exam Simulation (45 min)  
    ✅ AI Examiner Feedback  
    ✅ Competency Scoring  
    ✅ Performance Tracking  

    Built to prepare you for the **SAICA APC**.
    """)

# ==========================
# CASE ANALYSIS
# ==========================
elif page == "Case Analysis":

    case = st.text_area("Paste your case study here")

    if st.button("Analyse Case"):

        triggers = identify_triggers(case)

        st.subheader("📄 Highlighted Case")
        st.markdown(highlight(case, triggers), unsafe_allow_html=True)

        st.subheader("📊 Identified Triggers")

        for t in triggers:
            icon = "🔴" if t["strength"] == "STRONG" else "🟡"
            st.write(f"{icon} {t['category']} → {t['example']}")

# ==========================
# MOCK EXAM
# ==========================
elif page == "Mock Exam":

    st.header("🧪 APC Mock Exam")

    case = st.text_area("Paste case study")

    if st.button("Start Exam"):
        st.session_state.case = case
        st.session_state.start = time.time()

        st.subheader("REQUIRED")
        st.write("1. Accounting (IFRS)")
        st.write("2. Audit Risks and Procedures")
        st.write("3. Tax Implications")
        st.write("4. Financial Management")
        st.write("5. Integrated Recommendation")

    if "start" in st.session_state:
        elapsed = int(time.time() - st.session_state.start)
        remaining = max(0, 2700 - elapsed)
        st.write(f"⏱ Time Remaining: {remaining} seconds")

# ==========================
# SUBMIT EXAM
# ==========================
elif page == "Submit Exam":

    st.header("✅ Submit Your Answer")

    answer = st.text_area("Enter your full answer here")
    case = st.session_state.get("case", "")

    if st.button("Evaluate Answer"):

        triggers = identify_triggers(case)

        final_result = grade(answer)
        st.subheader(f"🎯 Final Result: {final_result}")

        st.subheader("📊 Competency Breakdown")
        st.write(competency_scores(answer))

        st.subheader("❌ Missed Triggers")
        missed = missed_triggers(triggers, answer)
        st.write(missed if missed else "None")

        st.subheader("📘 Model Answer Guidance")
        for item in model_answer(triggers):
            st.write("-", item)

        st.subheader("🧠 Examiner Feedback")
        for c in examiner_comments(answer, final_result):
            st.write("-", c)

        st.subheader("📈 Recommended Next Step")
        st.write(suggest_next_step(final_result))

        # Save performance
        st.session_state.history.append({"grade": final_result})

# ==========================
# DASHBOARD
# ==========================
elif page == "Dashboard":

    st.header("📊 Performance Dashboard")

    history = st.session_state.history

    if history:
        grades = [h["grade"] for h in history]

        st.write("Total Attempts:", len(grades))
        st.write("Results History:", grades)

        mapping = {
            "Not Competent": 1,
            "Limited Competent": 2,
            "Borderline Competent": 3,
            "Competent": 4,
            "Highly Competent": 5
        }

        numeric_scores = [mapping[g] for g in grades]

        st.line_chart(numeric_scores)

    else:
        st.write("No attempts yet")

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.caption("APC Agent V11 | Final Full System")

