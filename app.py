import streamlit as st
import pandas as pd
from datetime import datetime

# -------- PROJECT IMPORTS --------
from file_parser import parse_file
from data_profiler import profile
from llm_profiler import llm_profile
from llm_chat import chat_with_data
from llm_summary import generate_executive_summary
from llm_analysis_agent import generate_brief_analysis
from visual_agent import generate_basic_graph
import exporter

from openai import OpenAI
from openai import OpenAIError

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Universal Agentic AI",
    layout="wide"
)

# =========================================================
# SESSION STATE INITIALIZATION
# =========================================================
defaults = {
    "language": "English",
    "dark_mode": False,
    "api_key": None,
    "api_valid": False,   # 🔑 validation flag
    "current_file_path": None,
    "data": None,
    "profile": None,
    "llm_understanding": None,
    "brief_analysis": None,
    "chat_history": [],
    "generated_files": {},
    "file_history": [],
    "status_uploaded": False,
    "status_analyzed": False,
    "status_summary": False,
    "status_export": False,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# API KEY VALIDATION FUNCTION
# =========================================================
def validate_api_key(api_key: str) -> bool:
    """
    Validates API key by making a lightweight request.
    """
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()   # very small call
        return True
    except OpenAIError:
        return False
    except Exception:
        return False

# =========================================================
# API KEY GUARD (USED BEFORE AI CALLS)
# =========================================================
def require_valid_api_key():
    if not st.session_state.api_valid:
        st.warning("🔑 Valid API key required to use AI features.")
        st.stop()

# =========================================================
# SIDEBAR – SETTINGS
# =========================================================
st.sidebar.title("⚙️ Settings")

st.session_state.language = st.sidebar.selectbox(
    "🌐 Select Language",
    ["English", "Hindi"]
)

st.session_state.dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔑 API Configuration")

api_input = st.sidebar.text_input(
    "Enter your API Key",
    type="password",
    placeholder="sk-xxxxxxxxxxxxxxxx"
)

if st.sidebar.button("Validate API Key"):
    if api_input:
        with st.spinner("Validating API key..."):
            is_valid = validate_api_key(api_input)
            st.session_state.api_key = api_input
            st.session_state.api_valid = is_valid

        if is_valid:
            st.sidebar.success("✅ API key is valid")
        else:
            st.sidebar.error("❌ Invalid API key")
    else:
        st.sidebar.warning("Please enter an API key")

# API key status
if st.session_state.api_valid:
    st.sidebar.success("AI Features Enabled")
else:
    st.sidebar.info("AI Features Disabled")

# =========================================================
# LANGUAGE HELPER
# =========================================================
def t(en, hi):
    return hi if st.session_state.language == "Hindi" else en

# =========================================================
# GLOBAL CSS (LIGHT / DARK)
# =========================================================
if st.session_state.dark_mode:
    bg = "#0f172a"
    card = "#020617"
    text = "#e5e7eb"
    chat_bg = "#1e293b"
    chat_border = "#38bdf8"
else:
    bg = "#f5f7fa"
    card = "#ffffff"
    text = "#111827"
    chat_bg = "#f1f5f9"
    chat_border = "#2563eb"

st.markdown(f"""
<style>
.stApp {{ background-color: {bg}; color: {text}; }}

.card {{
    background-color: {card};
    padding: 1.2rem;
    border-radius: 10px;
    border: 1px solid #334155;
    margin-bottom: 1.2rem;
}}

h1, h2, h3 {{ color: {text}; }}

.stButton > button {{
    background-color: #2563eb;
    color: white;
    border-radius: 6px;
}}

.stDownloadButton > button {{
    background-color: #059669;
    color: white;
}}

@keyframes fadeSlideIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.chat-message {{
    animation: fadeSlideIn 0.4s ease-in-out;
    background-color: {chat_bg};
    color:{text};
    padding: 0.8rem;
    border-radius: 6px;
    margin-top: 0.6rem;
    border-left: 4px solid {chat_border};
}}
</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================
st.title(t(
    "🤖 Universal Agentic AI – Decision Support System",
    "🤖 यूनिवर्सल एजेंटिक एआई – निर्णय समर्थन प्रणाली"
))

# =========================================================
# SIDEBAR NAVIGATION + STATUS
# =========================================================
st.sidebar.markdown("---")
page = st.sidebar.radio(
    t("📂 Navigation", "📂 नेविगेशन"),
    ["Upload", "Analysis", "Summary", "Export"]
)

st.sidebar.markdown("---")
st.sidebar.subheader(t("📊 Status", "📊 स्थिति"))

def status_item(label_en, label_hi, done):
    icon = "✔️" if done else "❌"
    st.sidebar.write(f"{icon} {t(label_en, label_hi)}")

status_item("File Uploaded", "फ़ाइल अपलोड हुई", st.session_state.status_uploaded)
status_item("Data Analyzed", "डेटा विश्लेषण पूर्ण", st.session_state.status_analyzed)
status_item("Summary Generated", "सारांश तैयार", st.session_state.status_summary)
status_item("Ready for Export", "डाउनलोड हेतु तैयार", st.session_state.status_export)

# =========================================================
# CHAT COMPONENT
# =========================================================
def chat_with_data_component():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(t("💬 Chat with Data", "💬 डेटा से संवाद"))

    if not st.session_state.api_valid:
        st.info("🔒 Enable AI by validating API key in sidebar")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    q = st.text_input(t("Ask a question", "प्रश्न पूछें"))

    if q:
        ans = chat_with_data(
            st.session_state.llm_understanding,
            q,
            api_key=st.session_state.api_key
        )
        st.session_state.chat_history.append({"Q": q, "A": ans})

        st.markdown(
            f"<div class='chat-message'><b>{t('Answer','उत्तर')}:</b> {ans}</div>",
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# UPLOAD PAGE
# =========================================================
if page == "Upload":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(t("📤 Upload File", "📤 फ़ाइल अपलोड करें"))

    uploaded = st.file_uploader(
        t("Upload:- Word / Excel / Powerpoint & PDF",
          "Word / Excel / PDF & Powerpoint अपलोड करें"),
        type=["xlsx", "xls", "pdf", "docx", "pptx"]
    )

    if uploaded:
        st.session_state.current_file_path = uploaded.name
        with open(uploaded.name, "wb") as f:
            f.write(uploaded.getbuffer())

        ext = uploaded.name.split(".")[-1].lower()
        file_type_map = {
            "xlsx": "excel", "xls": "excel",
            "pdf": "pdf", "docx": "word","doc": "word",
            "pptx": "ppt"
            
        }

        st.session_state.data = parse_file(uploaded.name, file_type_map.get(ext))
        st.session_state.profile = profile(st.session_state.data)

        if st.session_state.api_valid:
            with st.spinner("AI is understanding the file..."):
                st.session_state.llm_understanding = llm_profile(
                    st.session_state.data,
                    st.session_state.profile,
                    api_key=st.session_state.api_key
                )

            st.session_state.status_uploaded = True
            st.session_state.status_analyzed = True
            st.success("File uploaded and analyzed")
        else:
            st.warning("File uploaded. Validate API key to enable AI analysis.")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# ANALYSIS PAGE
# =========================================================
elif page == "Analysis":

    if not st.session_state.llm_understanding:
        st.info("Upload file and enable AI to view analysis.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("🧠 AI Understanding")
            st.write(st.session_state.llm_understanding)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="card">', unsafe_allow_html=True)
            if st.button("Generate Brief Analysis"):
                require_valid_api_key()
                st.session_state.brief_analysis = generate_brief_analysis(
                    st.session_state.llm_understanding,
                    api_key=st.session_state.api_key
                )
            if st.session_state.brief_analysis:
                st.write(st.session_state.brief_analysis)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            chat_with_data_component()

# =========================================================
# SUMMARY PAGE
# =========================================================
elif page == "Summary":

    if st.button("Generate Executive Summary"):
        require_valid_api_key()

        summary_text = generate_executive_summary(
            st.session_state.chat_history,
            st.session_state.llm_understanding,
            api_key=st.session_state.api_key
        )

        summary = {
            "title": "Executive Summary",
            "bullets": [l for l in summary_text.split("\n") if l.strip()]
        }

        chart_path = generate_basic_graph(st.session_state.data)

        st.session_state.generated_files = {
            "word": exporter.export_word(summary),
            "excel": exporter.export_excel(summary),
            "ppt": exporter.export_ppt(summary, chart_path),
            "pdf": exporter.export_pdf(summary),
            "image": exporter.export_image(summary)
        }

        st.session_state.status_summary = True
        st.session_state.status_export = True

        st.success("Executive summary generated")

# =========================================================
# EXPORT PAGE
# =========================================================
elif page == "Export":

    if not st.session_state.generated_files:
        st.info("No outputs generated yet.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("⬇️ Download Outputs")

        for k, v in st.session_state.generated_files.items():
            st.download_button(k.upper(), open(v, "rb"), v)


        st.markdown('</div>', unsafe_allow_html=True)








