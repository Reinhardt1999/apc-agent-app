import streamlit as st
import time

st.set_page_config(page_title="APC Agent V3", layout="wide")

# ==========================
# FUNCTIONS
# ==========================

def classify_risk(word):
    high = ["fraud", "going concern"]
    medium = ["revenue", "tax", "ifrs"]

    if word.lower() in high:
        return "HIGH"
    elif word.lower() in medium:
        return "MEDIUM"
    return "LOW"


def identify_triggers(text):
    keywords = {
        "Accounting": ["revenue", "ifrs", "lease", "impairment"],
        "Audit": ["control", "fraud", "risk"],
        "Tax": ["tax", "vat", "sars"],
        "Financial Management": ["cash", "liquidity", "budget"],
        "Ethics": ["pressure", "conflict", "governance"]
    }

    results = []

    for category, words in keywords.items():
        for word in words:
            if word in text.lower():
                risk = classify_risk(word)
                results.append((category, word, risk))

    return list(set(results))


def competency_level(ans):
    ans = ans.lower()

    indicators = ["therefore", "recommend", "because", "risk", "ifrs", "audit"]
    score = sum([1 for w in indicators if w in ans])

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
# HOME
# ==========================

if page == "Home":
    st.title("🏠 APC Preparation Agent (CA SA)")

    st.markdown("""
    ### Welcome

    This tool helps you prepare for the **SAICA APC** through:

    - 📄 Trigger Identification  
    - 📘 Research Pack Development  
    - 🧪 Exam Simulation  
    - ✅ Competency-Based Marking  

    Use the sidebar to navigate.
    """)

# ==========================
# ANALYSE CASE
# ==========================

elif page == "Analyse Case":
    st.header("📄 Analyse Case Study")

    uploaded_file = st.file_uploader("Upload case (txt)", type=["txt"])
    typed_input = st.text_area("Or paste case study")

    case = ""

    if uploaded_file:
        case = uploaded_file.read().decode("utf-8")
    elif typed_input:
        case = typed_input

    if st.button("Identify Triggers"):
        if case:
            triggers = identify_triggers(case)

            st.subheader("Detected Issues")

            if triggers:
                for t in triggers:
                    st.write(f"✅ {t[0]} → {t[1]} ({t[2]} risk)")
            else:
                st.info("No triggers detected")
        else:
            st.warning("Please upload or paste a case")

# ==========================
# RESEARCH PACK
# ==========================

elif page == "Research Pack":
    st.header("📘 Research Pack Generator")

    case = st.text_area("Paste case study")

    if st.button("Generate Research Pack"):
        if case:
            triggers = identify_triggers(case)

            summary = "Key Issues Identified:\n"
            for t in triggers:
                summary += "- {} ({} risk)\n".format(t[0], t[2])

            st.subheader("Executive Summary")
            st.text(summary)

            st.subheader("Audit")
            st.write("Focus on control weaknesses and fraud risk areas.")

            st.subheader("Accounting")
            st.write("Apply relevant IFRS standards and ensure correct recognition and measurement.")

            st.subheader("Tax")
            st.write("Assess compliance risks and SARS exposure.")

            st.subheader("Financial Management")
            st.write("Evaluate cash flow, liquidity and sustainability.")

        else:
            st.warning("Enter a case first")

# ==========================
# PRACTICE EXAM
# ==========================

elif page == "Practice Exam":
    st.header("🧪 APC Simulation")

    case = st.text_area("Paste case study")

    if st.button("Generate Exam"):
        if case:
            st.subheader("Case Study")
            st.write(case)

            st.subheader("REQUIRED")

            st.write("1. Evaluate accounting treatment")
            st.write("2. Identify audit risks and procedures")
            st.write("3. Discuss tax implications")
            st.write("4. Provide an integrated recommendation")

            # TIMER START
            st.session_state.start_time = time.time()

    if "start_time" in st.session_state:
        elapsed = int(time.time() - st.session_state.start_time)
        remaining = max(0, 2700 - elapsed)
        st.write(f"⏱ Time Remaining: {remaining} seconds")

# ==========================
# SUBMIT ANSWER
# ==========================

elif page == "Submit Answer":
    st.header("✅ Submit & Get Marked")

    uploaded_ans = st.file_uploader("Upload answer (txt)", type=["txt"])
    typed_ans = st.text_area("Or enter your answer")

    answer = ""

    if uploaded_ans:
        answer = uploaded_ans.read().decode("utf-8")
    elif typed_ans:
        answer = typed_ans

    if st.button("Mark Attempt"):
        if answer:
            level = competency_level(answer)

            st.subheader(f"Performance: {level}")

            st.subheader("Feedback")

            feedback = generate_feedback(answer)

            if feedback:
                for f in feedback:
                    st.write(f)
            else:
                st.write("✅ Strong integrated response")

        else:
            st.warning("Please provide an answer")

# ==========================
# FOOTER
# ==========================

st.markdown("---")
st.caption("APC Agent V3 | Built for CA(SA) Success")
``
