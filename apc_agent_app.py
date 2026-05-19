import streamlit as st
import time
from PyPDF2 import PdfReader

st.set_page_config(page_title="APC Agent V11", layout="wide")

# ==========================
# SESSION STATE INIT
# ==========================
if "history" not in st.session_state:
    st.session_state.history = []

# ==========================
# PDF EXTRACTION
# ==========================
def extract_pdf(file):
    reader = PdfReader(file)
    text = ""
    for p in reader.pages:
        t = p.extract_text()
        if t:
            text += t + "\n"
    return text

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
# TRIGGERS
# ==========================
def identify_triggers(text):
    results = []
    sentences = text.split(".")
    for cat, words in trigger_map.items():
        for w in words:
            if w in text.lower():
                example = next((s.strip() for s in sentences if w in s.lower()), "")
                results.append({
                    "category": cat,
                    "word": w,
                    "strength": "STRONG" if w in ["fraud", "revenue"] else "WEAK",
                    "example": example
                })
    return results

# ==========================
# HIGHLIGHT
# ==========================
def highlight(text, triggers):
    for t in triggers:
        color = "red" if t["strength"] == "STRONG" else "yellow"
        text = text.replace(t["word"], f"<mark style='background:{color}'>{t['word']}</mark>")
    return text

# ==========================
# MARKING
# ==========================
def grade(ans):
    ans = ans.lower()
    length = len(ans.split())

    if length > 500 and "ifrs" in ans:
        return "Highly Competent"
    elif length > 350:
        return "Competent"
    elif length > 250:
        return "Borderline Competent"
    elif length > 150:
        return "Limited Competent"
    return "Not Competent"

def competency_scores(ans):
    ans = ans.lower()
    return {
        "Accounting": "✅" if "ifrs" in ans else "❌",
        "Audit": "✅" if "risk" in ans else "❌",
        "Tax": "✅" if "tax" in ans else "❌",
        "FM": "✅" if "cash" in ans else "❌"
    }

# ==========================
# AI EXAMINER
# ==========================
def examiner_comments(ans, grade):
    comments = []

    if grade == "Highly Competent":
        comments.append("Strong integration and technical depth.")
    elif grade == "Competent":
        comments.append("Competent but lacks full integration.")
    else:
        comments.append("Insufficient depth and analysis.")

    if "ifrs" not in ans.lower():
        comments.append("Weak accounting reference.")
    if "risk" not in ans.lower():
        comments.append("Risk identification lacking.")

    return comments

# ==========================
# MODEL ANSWER
# ==========================
def model_answer(triggers):
    output = []
    for t in triggers:
        if t["category"] == "Accounting":
            output.append("Apply IFRS principles.")
        elif t["category"] == "Audit":
            output.append("Identify audit risks.")
        elif t["category"] == "Tax":
            output.append("Discuss tax implications.")
        elif t["category"] == "FM":
            output.append("Evaluate financial impact.")
    return list(set(output))

# ==========================
# ADAPTIVE ENGINE
# ==========================
def suggest_next_level(grade):
    if grade == "Highly Competent":
        return "Advanced case recommended ✅"
    elif grade == "Competent":
        return "Practice integration scenarios"
    else:
        return "Revise fundamentals (IFRS, audit risks)"

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
    st.title("🏠 APC Agent V11 (Elite System)")
    st.write("Full APC simulation + adaptive feedback + performance tracking")

# ==========================
# CASE ANALYSIS
# ==========================
elif page == "Case Analysis":
    file = st.file_uploader("Upload case", type=["pdf", "txt"])
    text_input = st.text_area("Or paste case")

    case = ""
    if file:
        case = extract_pdf(file) if file.type == "application/pdf" else file.read().decode("utf-8")
    elif text_input:
        case = text_input

    if st.button("Analyse Case"):
        triggers = identify_triggers(case)

        st.markdown(highlight(case, triggers), unsafe_allow_html=True)

        st.subheader("Triggers")
        for t in triggers:
            st.write(f"{t['category']} ({t['strength']}) → {t['example']}")

# ==========================
# MOCK EXAM
# ==========================
elif page == "Mock Exam":
    st.header("🧪 APC Mock Exam")

    case = st.text_area("Paste case")

    if st.button("Start"):
        st.session_state.case = case
        st.session_state.start = time.time()

        st.write("Required:")
        st.write("1. Accounting")
        st.write("2. Audit")
        st.write("3. Tax")
        st.write("4. FM")
        st.write("5. Integrated recommendation")

    if "start" in st.session_state:
        remaining = max(0, 2700 - int(time.time() - st.session_state.start))
        st.write(f"⏱ Time: {remaining}s")

# ==========================
# SUBMIT EXAM
# ==========================
elif page == "Submit Exam":
    ans = st.text_area("Enter your answer")
    case = st.session_state.get("case", "")

    if st.button("Evaluate"):
        triggers = identify_triggers(case)
        g = grade(ans)

        st.subheader(f"Result: {g}")

        st.write("Competencies:", competency_scores(ans))
        st.write("Model Answer:", model_answer(triggers))

        st.write("Comments:")
        for c in examiner_comments(ans, g):
            st.write("-", c)

        st.write("Next Step:", suggest_next_level(g))

        # Save history
        st.session_state.history.append({
            "grade": g
        })

# ==========================
# DASHBOARD ⭐
# ==========================
elif page == "Dashboard":
    st.header("📊 Performance Dashboard")

    history = st.session_state.history

    if history:
        grades = [h["grade"] for h in history]
        st.write("Attempts:", len(grades))
        st.write("Results:", grades)

        # Trend
        improvement_map = {
            "Not Competent": 1,
            "Limited Competent": 2,
            "Borderline Competent": 3,
            "Competent": 4,
            "Highly Competent": 5
        }

        numeric = [improvement_map[g] for g in grades]

        st.line_chart(numeric)

    else:
        st.write("No attempts yet")

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.caption("APC Agent V11 | Adaptive AI + Dashboard System")

