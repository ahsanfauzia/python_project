
import streamlit as st


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --orange: #FF7900;
        --orange-hover: #E56800;
        --black: #101010;
        --card: #202020;
        --white: #FFFFFF;
        --muted: #CCCCCC;
        --border: #444444;
    }

    /* GLOBAL APPLICATION */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #101010 !important;
        color: #FFFFFF !important;
    }

    .stApp {
        background:
        radial-gradient(
            circle at 85% 0%,
            rgba(255,121,0,0.09),
            transparent 35%
        ),
        #101010 !important;
    }

    .main .block-container {
        padding: 2.5rem 3rem 4rem;
        max-width: 1450px;
    }

    /* FORCE WHITE TEXT */
    .stApp p,
    .stApp li,
    .stApp label,
    .stApp span,
    .stApp div[data-testid="stMarkdownContainer"],
    .stApp div[data-testid="stMarkdownContainer"] p,
    .stApp div[data-testid="stMarkdownContainer"] li,
    .stApp [data-testid="stWidgetLabel"],
    .stApp [data-testid="stWidgetLabel"] p {
        color: #FFFFFF;
    }

    /* HEADINGS */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 800 !important;
    }

    .hero h1 {
        font-size: clamp(42px, 6vw, 72px);
        line-height: 1.08;
        letter-spacing: -3px;
        margin: 15px 0;
    }

    .hero h1 span {
        color: #FF7900 !important;
    }

    .hero p {
        color: #CCCCCC !important;
        font-size: 17px;
        line-height: 1.8;
        max-width: 650px;
    }

    .eyebrow {
        color: #FF7900 !important;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 3px;
    }

    .page-title {
        color: #FFFFFF !important;
        font-size: 42px;
        letter-spacing: -2px;
        margin: 8px 0;
    }

    .muted {
        color: #CCCCCC !important;
        font-size: 15px;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: #080808 !important;
        border-right: 1px solid #333333;
    }

    [data-testid="stSidebar"] > div {
        background: #080808 !important;
    }

    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] h2 {
        color: #FF7900 !important;
        font-size: 27px;
    }

    [data-testid="stSidebar"] .stButton button {
        background: transparent !important;
        border: 1px solid transparent !important;
        color: #FFFFFF !important;
        text-align: left;
        border-radius: 10px;
        padding: 12px 15px;
        transition: 0.2s ease;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background: #38200D !important;
        color: #FF9638 !important;
        border-color: #FF7900 !important;
    }

    /* FEATURE CARDS */
    .feature-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-top: 30px;
    }

    .feature {
        background: #202020;
        border: 1px solid #444444;
        border-radius: 16px;
        padding: 22px;
        transition: 0.2s ease;
    }

    .feature:hover {
        border-color: #FF7900;
        transform: translateY(-3px);
    }

    .feature b {
        color: #FF7900 !important;
        font-size: 15px;
    }

    .feature p {
        color: #CCCCCC !important;
        font-size: 14px;
        line-height: 1.6;
    }

    .panel, .mini-card, .empty {
        background: #202020 !important;
        border: 1px solid #444444;
        border-radius: 18px;
        padding: 23px;
        color: #FFFFFF !important;
    }

    .mini-card {
        line-height: 2.1;
    }

    .empty {
        text-align: center;
        padding: 40px;
    }

    /* METRIC CARDS */
    [data-testid="stMetric"] {
        background: #202020 !important;
        border: 1px solid #444444;
        border-radius: 15px;
        padding: 20px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #FFFFFF !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #FF7900 !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"],
    [data-testid="stMetricDelta"] * {
        color: #FFFFFF !important;
    }

    /* BUTTONS */
    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button {
        background: #FF7900 !important;
        color: #FFFFFF !important;
        border: 1px solid #FF7900 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 11px 20px;
        transition: all 0.2s ease;
    }

    .stButton > button p,
    .stFormSubmitButton > button p,
    .stDownloadButton > button p {
        color: #FFFFFF !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover,
    .stDownloadButton > button:hover {
        background: #E56800 !important;
        border-color: #E56800 !important;
        color: #FFFFFF !important;
        box-shadow: 0 5px 18px rgba(255,121,0,0.25);
    }

    /* INPUTS */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stNumberInput label,
    .stFileUploader label {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    input,
    textarea {
        background: #202020 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: 1px solid #666666 !important;
        border-radius: 9px !important;
        caret-color: #FF7900 !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus,
    input:focus,
    textarea:focus {
        border-color: #FF7900 !important;
        box-shadow: 0 0 0 1px #FF7900 !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #BBBBBB !important;
        -webkit-text-fill-color: #BBBBBB !important;
        opacity: 1 !important;
    }

    /* SELECTBOX AND DROPDOWN */
    [data-baseweb="select"] > div {
        background: #202020 !important;
        border: 1px solid #666666 !important;
    }

    [data-baseweb="select"] *,
    [data-baseweb="popover"] *,
    [role="option"] {
        color: #FFFFFF !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="menu"] {
        background: #202020 !important;
    }

    [role="option"]:hover {
        background: #38200D !important;
    }

    /* RADIO BUTTONS */
    .stRadio label,
    .stRadio p,
    .stRadio span,
    .stCheckbox label,
    .stCheckbox p,
    .stCheckbox span {
        color: #FFFFFF !important;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        border-bottom: 1px solid #444444;
    }

    .stTabs [data-baseweb="tab"] {
        color: #FFFFFF !important;
        background: transparent !important;
    }

    .stTabs [data-baseweb="tab"] p {
        color: #FFFFFF !important;
    }

    .stTabs [aria-selected="true"] {
        color: #FF7900 !important;
        border-bottom: 3px solid #FF7900 !important;
    }

    .stTabs [aria-selected="true"] p {
        color: #FF7900 !important;
    }

    /* FILE UPLOADER */
    [data-testid="stFileUploader"] {
        background: #202020 !important;
        border: 1px dashed #FF7900 !important;
        border-radius: 14px;
        padding: 15px;
    }

    [data-testid="stFileUploader"] * {
        color: #FFFFFF !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: #202020 !important;
    }

    /* PROGRESS BAR */
    [data-testid="stProgressBar"] {
        background: #333333 !important;
        border-radius: 20px;
    }

    [data-testid="stProgressBar"] > div > div {
        background: #FF7900 !important;
    }

    /* SKILL TAGS */
    .tag {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 20px;
        margin: 4px;
        font-size: 13px;
        font-weight: 600;
    }

    .good {
        background: #123D2B;
        color: #8FF0B7 !important;
        border: 1px solid #246B43;
    }

    .warn {
        background: #43240F;
        color: #FFD09B !important;
        border: 1px solid #96501B;
    }

    /* DATAFRAME */
    [data-testid="stDataFrame"] {
        background: #202020 !important;
        border: 1px solid #444444;
        border-radius: 12px;
    }

    [data-testid="stDataFrame"] * {
        color: #FFFFFF !important;
    }

    /* ALERTS */
    [data-testid="stAlert"] {
        background: #202020 !important;
        border-radius: 12px;
    }

    [data-testid="stAlert"] * {
        color: #FFFFFF !important;
    }

    /* CAPTIONS */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] * {
        color: #CCCCCC !important;
    }

    /* EXPANDERS */
    [data-testid="stExpander"] {
        background: #202020 !important;
        border: 1px solid #444444 !important;
        border-radius: 12px;
    }

    [data-testid="stExpander"] * {
        color: #FFFFFF !important;
    }

    /* DIVIDERS */
    hr {
        border-color: #444444 !important;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #101010;
    }

    ::-webkit-scrollbar-thumb {
        background: #FF7900;
        border-radius: 10px;
    }

    /* FOCUS ACCESSIBILITY */
    button:focus-visible,
    input:focus-visible,
    textarea:focus-visible {
        outline: 2px solid #FF7900 !important;
        outline-offset: 2px !important;
    }

    </style>
    """, unsafe_allow_html=True)


def render_sidebar(user):
    with st.sidebar:
        st.markdown("## ✦ TalentLens")
        st.caption("AI CAREER INTELLIGENCE")
        st.markdown("---")

        pages = [
            "Overview",
            "New analysis",
            "Latest report",
            "History",
            "About"
        ]

        current = st.session_state.get("page", "Overview")

        for page in pages:
            label = ("🟠 " if current == page else "　") + page

            if st.button(
                label,
                key="nav_" + page,
                use_container_width=True
            ):
                st.session_state.page = page
                st.rerun()

        st.markdown("---")
        st.caption("SIGNED IN AS")
        st.write(user["name"])
        st.caption(user["email"])

        if st.button("↪ Sign out", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "Overview"
            st.rerun()

        st.markdown("---")
        st.caption("TalentLens AI · Local Edition")
