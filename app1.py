import streamlit as st
from resume_parser import extract_text_from_pdf
from ai_analyzer import parse_resume, match_resume_to_job

# ── Page config ──────────────────────────────────────────
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    /* Overall page padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Header styling */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6366F1, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        color: #9CA3AF;
        font-size: 0.95rem;
        margin-top: 0.2rem;
    }

    /* Card styling */
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }

    /* Skill chips */
    .skill-chip {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        color: #A5B4FC;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px 4px 4px 0;
        font-size: 0.85rem;
        font-weight: 500;
    }
    .skill-chip.matched {
        background: rgba(34, 197, 94, 0.15);
        color: #86EFAC;
        border-color: rgba(34, 197, 94, 0.3);
    }
    .skill-chip.missing {
        background: rgba(239, 68, 68, 0.15);
        color: #FCA5A5;
        border-color: rgba(239, 68, 68, 0.3);
    }

    /* Metric tile */
    .metric-tile {
        text-align: center;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-label {
        color: #9CA3AF;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Section title */
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Recommendation badge */
    .badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .badge.strong { background: rgba(34,197,94,0.15); color: #4ADE80; border: 1px solid rgba(34,197,94,0.3); }
    .badge.moderate { background: rgba(251,191,36,0.15); color: #FBBF24; border: 1px solid rgba(251,191,36,0.3); }
    .badge.weak { background: rgba(239,68,68,0.15); color: #F87171; border: 1px solid rgba(239,68,68,0.3); }

    /* Hide default Streamlit footer/menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────
st.markdown('<div class="main-header">📄 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by Groq • Instant resume parsing and job-fit scoring</div>', unsafe_allow_html=True)
st.write("")

# ── Sidebar: Job Description ──────────────────────────────
with st.sidebar:
    st.markdown("### 📋 Job description")
    job_desc = st.text_area(
        "Paste the job description",
        height=280,
        placeholder="e.g. We are looking for a Python developer with experience in Django, REST APIs, and SQL...",
        label_visibility="collapsed"
    )
    st.divider()
    st.markdown("### 📤 Upload resume")
    uploaded_file = st.file_uploader("PDF only", type=["pdf"], label_visibility="collapsed")
    st.divider()
    analyze_btn = st.button("🔍 Analyze resume", use_container_width=True, type="primary")

# ── Helper: badge class ────────────────────────────────────
def badge_class(rec):
    rec = rec.lower()
    if "strong" in rec: return "strong"
    if "moderate" in rec: return "moderate"
    return "weak"

# ── Main content ────────────────────────────────────────────
if analyze_btn and uploaded_file and job_desc:
    with st.spinner("Analyzing resume against job description..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        parsed = parse_resume(resume_text)
        match = match_resume_to_job(resume_text, job_desc)

    score = match.get("match_score", 0)
    recommendation = match.get("recommendation", "")

    # ── Top metrics row ─────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        color = "#4ADE80" if score >= 70 else "#FBBF24" if score >= 45 else "#F87171"
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-value" style="color:{color}">{score}%</div>
            <div class="metric-label">Match score</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-value">{len(parsed.get('skills', []))}</div>
            <div class="metric-label">Skills found</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-value">{len(match.get('matched_skills', []))}</div>
            <div class="metric-label">Matched skills</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="metric-value">{len(match.get('missing_skills', []))}</div>
            <div class="metric-label">Missing skills</div>
        </div>""", unsafe_allow_html=True)

    st.write("")
    st.markdown(f'<span class="badge {badge_class(recommendation)}">{recommendation}</span>', unsafe_allow_html=True)
    st.progress(score / 100)
    st.write("")

    # ── Tabs for organization ───────────────────────────────
    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🎯 Job match", "💼 Experience & education"])

    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**Name:** {parsed.get('name', 'N/A')}")
            st.markdown(f"**Email:** {parsed.get('email', 'N/A')}")
            st.markdown(f"**Phone:** {parsed.get('phone', 'N/A')}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🛠️ Skills</div>', unsafe_allow_html=True)
            chips = "".join([f'<span class="skill-chip">{s}</span>' for s in parsed.get("skills", [])])
            st.markdown(chips, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 Summary</div>', unsafe_allow_html=True)
        st.write(match.get("summary", ""))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">✅ Matched skills</div>', unsafe_allow_html=True)
            chips = "".join([f'<span class="skill-chip matched">{s}</span>' for s in match.get("matched_skills", [])])
            st.markdown(chips or "_None found_", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">💪 Strengths</div>', unsafe_allow_html=True)
            for s in match.get("strengths", []):
                st.markdown(f"- {s}")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">❌ Missing skills</div>', unsafe_allow_html=True)
            chips = "".join([f'<span class="skill-chip missing">{s}</span>' for s in match.get("missing_skills", [])])
            st.markdown(chips or "_None — great fit!_", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">⚠️ Gaps</div>', unsafe_allow_html=True)
            for s in match.get("weaknesses", []):
                st.markdown(f"- {s}")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-title">🎓 Education</div>', unsafe_allow_html=True)
        for edu in parsed.get("education", []):
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(f"**{edu.get('degree', 'N/A')}** — {edu.get('institution', 'N/A')} ({edu.get('year', 'N/A')})")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">💼 Work experience</div>', unsafe_allow_html=True)
        for exp in parsed.get("experience", []):
            with st.expander(f"{exp.get('title', '')} @ {exp.get('company', '')} ({exp.get('duration', '')})"):
                st.write(exp.get("description", ""))

else:
    st.markdown("""
    <div class="card" style="text-align:center; padding: 3rem;">
        <h3>👋 Get started</h3>
        <p style="color:#9CA3AF;">Paste a job description and upload a resume PDF in the sidebar, then click <b>Analyze resume</b>.</p>
    </div>
    """, unsafe_allow_html=True)