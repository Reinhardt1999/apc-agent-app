import streamlit as st

st.set_page_config(page_title="APC Agent (CA(SA))", layout="wide")

st.title("🧠 APC Preparation Agent (CA(SA))")

# ==========================
# SECTION 1: TRIGGERS
# ==========================
st.header("1️⃣ Trigger Identification")

case_text = st.text_area("Paste Case Study Here")

if st.button("Identify Triggers"):
    triggers = []

    keywords = {
        "Accounting": ["revenue", "lease", "impairment", "IFRS"],
        "Audit": ["control", "fraud", "risk", "audit"],
        "Tax": ["vat", "tax", "deferred", "SARS"],
        "Financial Management": ["cash", "budget", "loan", "liquidity"],
        "Ethics": ["conflict", "pressure", "governance"]
    }

    for category, words in keywords.items():
        for word in words:
            if word.lower() in case_text.lower():
                triggers.append(f"{category}: {word}")

    if triggers:
        st.subheader("Identified Triggers")
        for t in set(triggers):
            st.write(f"✅ {t}")
    else:
        st.info("No triggers detected. Try adding more context.")

# ==========================
# SECTION 2: RESEARCH PACK
# ==========================
st.header("2️⃣ Research Pack Generator")

issue = st.text_input("Key Issue")

st.subheader("Executive Summary")
exec_summary = st.text_area("Write executive summary")

st.subheader("Audit")
audit_section = st.text_area("Audit analysis")

st.subheader("Accounting")
accounting_section = st.text_area("Accounting (IFRS)")

st.subheader("Tax")
tax_section = st.text_area("Tax analysis")

st.subheader("Financial Management")
fm_section = st.text_area("Financial Management")

st.subheader("Recommendation")
recommendation = st.text_area("Final integrated recommendation")

if st.button("Generate Pack"):
    st.success("✅ Research Pack Created")
    st.markdown("### Executive Summary")
    st.write(exec_summary)

    st.markdown("### Audit")
    st.write(audit_section)

    st.markdown("### Accounting")
    st.write(accounting_section)

    st.markdown("### Tax")
    st.write(tax_section)

    st.markdown("### Financial Management")
    st.write(fm_section)

    st.markdown("### Recommendation")
    st.write(recommendation)

# ==========================
# SECTION 3: QUESTION ENGINE
# ==========================
st.header("3️⃣ Question Builder + Marking")

topic = st.text_input("Enter Topic (e.g. revenue recognition)")

if st.button("Generate Question"):
    question = f"Evaluate the risks relating to {topic} and provide recommendations."
    st.subheader("Generated Question")
    st.write(question)

# Candidate Answer
st.subheader("Submit Your Answer")
answer = st.text_area("Write your answer here")

# ==========================
# MARKING LOGIC
# ==========================

def mark_answer(ans):
    score = 0
    feedback = []

    # Technical keywords check
    if "IFRS" in ans:
        score += 8
        feedback.append("✅ Good use of IFRS")
    else:
        score += 3
        feedback.append("⚠️ Add IFRS references")

    if "risk" in ans.lower():
        score += 8
        feedback.append("✅ Risks identified")
    else:
        score += 3
        feedback.append("⚠️ Identify more risks")

    if "recommend" in ans.lower():
        score += 8
        feedback.append("✅ Recommendations provided")
    else:
        score += 3
        feedback.append("⚠️ Provide clearer recommendations")

    if len(ans) > 300:
        score += 8
        feedback.append("✅ Good depth")
    else:
        score += 3
        feedback.append("⚠️ Expand your analysis")

    # Structure assumption
    score += 8

    return score, feedback

if st.button("Mark My Answer"):
    score, feedback = mark_answer(answer)

    st.subheader(f"Score: {score}/40")

    if score >= 32:
        level = "Distinction"
    elif score >= 24:
        level = "Competent"
    elif score >= 16:
        level = "Marginal"
    else:
        level = "Not Competent"

    st.write(f"Performance Level: {level}")

    st.subheader("Feedback")
    for f in feedback:
        st.write(f)

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.caption("Built for SAICA APC Prep | Focus: Integration + Judgement")
