import streamlit as st
from pathlib import Path
from datetime import datetime
import pandas as pd
from modules.auth import init_db, register_user, login_user
from modules.resume import extract_resume_text, analyze_resume
from modules.matcher import match_resume_to_job
from modules.storage import save_analysis, list_analyses, delete_analysis
from modules.ui import inject_css, render_sidebar

st.set_page_config(page_title="TalentLens AI", page_icon="✦", layout="wide", initial_sidebar_state="expanded")
init_db()
inject_css()

if "user" not in st.session_state:
    st.session_state.user = None

def auth_screen():
    st.markdown('<div class="hero"><div class="eyebrow">AI-POWERED CAREER INTELLIGENCE</div><h1>Make every application<br><span>count.</span></h1><p>Understand your resume, uncover skill gaps, and see how well you match a role — in one private workspace.</p></div>', unsafe_allow_html=True)
    left, right = st.columns([1.1, 0.9], gap="large")
    with left:
        st.markdown("### Your job search, with more signal.")
        st.markdown("""
        <div class="feature-grid">
          <div class="feature"><b>01 · Resume intelligence</b><p>Extract skills, experience and useful signals from your CV.</p></div>
          <div class="feature"><b>02 · Role matching</b><p>Compare your profile against a job description with explainable scoring.</p></div>
          <div class="feature"><b>03 · Actionable gaps</b><p>See matched skills, missing skills and practical next steps.</p></div>
          <div class="feature"><b>04 · Private workspace</b><p>Your analyses are saved to your account on this device.</p></div>
        </div>""", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Sign in", "Create account"])
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Sign in →", use_container_width=True):
                user = login_user(email, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid email or password.")
        with tab2:
            name = st.text_input("Your name", key="reg_name")
            email2 = st.text_input("Email address", key="reg_email")
            pw2 = st.text_input("Create password", type="password", key="reg_pw")
            pw3 = st.text_input("Confirm password", type="password", key="reg_pw2")
            if st.button("Create my workspace →", use_container_width=True):
                if not name.strip() or not email2.strip() or len(pw2) < 8:
                    st.error("Enter your name and email. Password must be at least 8 characters.")
                elif pw2 != pw3:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = register_user(name.strip(), email2.strip(), pw2)
                    if ok:
                        st.success(msg + " You can now sign in.")
                    else:
                        st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.user:
    auth_screen()
    st.stop()

user = st.session_state.user
render_sidebar(user)
page = st.session_state.get("page", "Overview")

if page == "Overview":
    st.markdown('<div class="eyebrow">YOUR WORKSPACE</div><h1 class="page-title">Good to see you, '+user["name"].split()[0]+'.</h1><p class="muted">A clearer view of your fit, strengths and next move.</p>', unsafe_allow_html=True)
    history = list_analyses(user["id"])
    c1,c2,c3 = st.columns(3)
    c1.metric("Analyses completed", len(history))
    c2.metric("Average match score", f'{round(sum(x["score"] for x in history)/len(history))}%' if history else "—")
    c3.metric("Latest activity", history[0]["created_at"][:10] if history else "—")
    st.markdown("### Recent analyses")
    if history:
        df = pd.DataFrame(history)[["role_title","company","score","created_at"]]
        df.columns = ["Role","Company","Match score","Date"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="empty"><h3>Your first match starts here.</h3><p>Upload a resume and paste a job description to get a detailed, explainable match report.</p></div>', unsafe_allow_html=True)
        if st.button("Start a new analysis →"):
            st.session_state.page = "New analysis"; st.rerun()

elif page == "New analysis":
    st.markdown('<div class="eyebrow">RESUME × ROLE</div><h1 class="page-title">New match analysis</h1><p class="muted">Use a PDF, DOCX or TXT resume. Your file is processed locally by this app and is not sent to an external AI provider.</p>', unsafe_allow_html=True)
    with st.form("analysis_form"):
        col1,col2 = st.columns(2)
        with col1:
            resume_file = st.file_uploader("Upload your resume", type=["pdf","docx","txt"])
            role_title = st.text_input("Job title", placeholder="e.g. Python Developer")
            company = st.text_input("Company (optional)", placeholder="e.g. Acme")
        with col2:
            st.markdown("**What you'll get**")
            st.markdown('<div class="mini-card">✓ Match score and scoring breakdown<br>✓ Skills found in your resume<br>✓ Skills missing from the job description<br>✓ Resume strengths and improvement tips</div>', unsafe_allow_html=True)
        jd = st.text_area("Paste the complete job description", height=230, placeholder="Paste responsibilities, requirements and qualifications here...")
        submitted = st.form_submit_button("Analyze my match →", use_container_width=True)
    if submitted:
        if not resume_file or not jd.strip() or not role_title.strip():
            st.error("Please upload a resume, add a job title and paste the job description.")
        else:
            try:
                raw = resume_file.getvalue()
                text = extract_resume_text(resume_file.name, raw)
                if len(text.strip()) < 80:
                    st.error("We could not extract enough text. Try a text-based PDF or DOCX (not a scanned image).")
                else:
                    with st.spinner("Reading your resume and comparing it with the role..."):
                        profile = analyze_resume(text)
                        result = match_resume_to_job(text, jd)
                        analysis_id = save_analysis(user["id"], role_title.strip(), company.strip(), resume_file.name, result["score"], profile, result, jd)
                    st.session_state.last_result = {"profile":profile,"result":result,"role":role_title,"company":company,"analysis_id":analysis_id}
                    st.session_state.page = "Latest report"
                    st.rerun()
            except Exception as e:
                st.error(f"Could not analyze this file: {e}")

elif page == "Latest report":
    data = st.session_state.get("last_result")
    if not data:
        st.info("Run a new analysis to see your report.")
        if st.button("New analysis"): st.session_state.page="New analysis"; st.rerun()
    else:
        r, p = data["result"], data["profile"]
        st.markdown('<div class="eyebrow">MATCH REPORT · '+data["role"].upper()+'</div><h1 class="page-title">Your role-fit snapshot</h1>', unsafe_allow_html=True)
        a,b,c = st.columns([1,1,1])
        a.metric("Overall match", f'{r["score"]}%')
        b.metric("Relevant skills found", f'{len(r["matched_skills"])} / {max(1,len(r["required_skills"]))}')
        c.metric("Skills to strengthen", len(r["missing_skills"]))
        st.progress(r["score"]/100)
        st.caption("This is a screening aid, not a hiring decision or a guarantee of interview selection.")
        l, rr = st.columns(2)
        with l:
            st.markdown("### Strong matches")
            if r["matched_skills"]:
                for s in r["matched_skills"]: st.markdown(f'<span class="tag good">{s}</span>', unsafe_allow_html=True)
            else: st.write("No direct skill matches detected. Check wording and add relevant skills you genuinely have.")
        with rr:
            st.markdown("### Skills to strengthen")
            if r["missing_skills"]:
                for s in r["missing_skills"]: st.markdown(f'<span class="tag warn">{s}</span>', unsafe_allow_html=True)
            else: st.success("All detected job skills appear in your resume.")
        st.markdown("### Score breakdown")
        st.caption("A transparent heuristic based on skill coverage and text similarity — not a trained hiring model.")
        st.progress(r["skill_score"]/100); st.write(f'Skill coverage · {r["skill_score"]}%')
        st.progress(r["similarity_score"]/100); st.write(f'Text relevance · {r["similarity_score"]}%')
        st.markdown("### Resume profile detected")
        x,y,z = st.columns(3)
        x.metric("Words", p["word_count"]); y.metric("Email found", "Yes" if p["email"] else "Not detected"); z.metric("Phone found", "Yes" if p["phone"] else "Not detected")
        st.markdown("**Detected skills**")
        st.write(", ".join(p["skills"]) if p["skills"] else "No skills detected from the built-in skill dictionary.")
        st.markdown("### Recommended next steps")
        for tip in r["recommendations"]: st.markdown(f"- {tip}")
        report = pd.DataFrame([{"Role":data["role"],"Company":data["company"],"Overall match":r["score"],"Skill coverage":r["skill_score"],"Text relevance":r["similarity_score"],"Matched skills":", ".join(r["matched_skills"]),"Missing skills":", ".join(r["missing_skills"])}])
        st.download_button("Download report (CSV)", report.to_csv(index=False).encode("utf-8"), "talentlens_report.csv", "text/csv")
        if st.button("Analyze another role →"): st.session_state.page="New analysis"; st.rerun()

elif page == "History":
    st.markdown('<div class="eyebrow">YOUR ACTIVITY</div><h1 class="page-title">Analysis history</h1>', unsafe_allow_html=True)
    history = list_analyses(user["id"])
    if not history: st.info("No analyses yet.")
    else:
        df = pd.DataFrame(history)
        st.dataframe(df[["id","role_title","company","score","created_at"]].rename(columns={"id":"ID","role_title":"Role","company":"Company","score":"Score","created_at":"Created"}), use_container_width=True, hide_index=True)
        selected = st.number_input("Analysis ID to delete", min_value=1, step=1)
        if st.button("Delete selected analysis", type="secondary"):
            delete_analysis(user["id"], int(selected)); st.success("Analysis deleted."); st.rerun()

elif page == "About":
    st.markdown('<div class="eyebrow">PRODUCT NOTES</div><h1 class="page-title">About TalentLens AI</h1>', unsafe_allow_html=True)
    st.write("TalentLens AI is a local-first resume and job-description matching workspace. It uses transparent NLP techniques (TF-IDF cosine similarity and skill coverage) to help candidates review how clearly their resume communicates role-relevant experience.")
    st.warning("The score is an estimate, not a prediction of hiring outcomes. Keep your resume truthful, verify every suggestion, and do not add skills you cannot demonstrate.")
