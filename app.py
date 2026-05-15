import streamlit as st
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- INITIALIZATION & DIRECTORY CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "db_folder")

# Set up page with a widescreen professional layout
st.set_page_config(
    page_title="BHP | Vendor Intelligence Portal",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- BHP BRAND THEMING (CSS Injection) ---
st.markdown("""
    <style>
        /* Main page adjustments */
        .main {
            padding: 2rem 3rem;
            background-color: #FFFFFF;
        }
        /* Top Accent Branding Bar */
        .bhp-top-bar {
            height: 6px;
            background: linear-gradient(90deg, #E35302 0%, #FF7A33 100%);
            margin-top: -3.5rem;
            margin-left: -3rem;
            margin-right: -3rem;
            margin-bottom: 2rem;
        }
        /* Styling the header block */
        .main-header {
            font-family: 'Arial Black', -apple-system, sans-serif;
            color: #111111;
            font-weight: 900;
            letter-spacing: -1px;
            margin-bottom: 0.2rem;
            text-transform: uppercase;
        }
        .main-header span {
            color: #E35302;
        }
        .sub-header {
            color: #555555;
            font-size: 1.05rem;
            margin-bottom: 2.5rem;
            font-weight: 500;
        }
        /* Styling the Primary Action Buttons to BHP Orange */
        div.stButton > button:first-child {
            background-color: #E35302;
            color: white;
            border-radius: 4px;
            border: none;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #BD4300;
            color: white;
            box-shadow: 0 4px 8px rgba(227, 83, 2, 0.2);
        }
        /* Form configuration adjustments */
        div[data-testid="stForm"] {
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            border-radius: 8px;
            padding: 2rem;
        }
        /* Vendor Result Cards */
        .vendor-card {
            background-color: #FCFDFD;
            border-left: 4px solid #E35302;
            border-top: 1px solid #EAECEF;
            border-right: 1px solid #EAECEF;
            border-bottom: 1px solid #EAECEF;
            border-radius: 0px 6px 6px 0px;
            padding: 1.25rem 1.5rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        }
        .vendor-meta {
            color: #E35302;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        .user-profile {
            padding: 12px;
            background-color: #1E1E1E;
            border-left: 3px solid #E35302;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #EAECEF;
            font-family: monospace;
        }
    </style>
""", unsafe_allow_html=True)

# Inject top brand bar
st.markdown("<div class='bhp-top-bar'></div>", unsafe_allow_html=True)

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- AUTHENTICATION STATE ENGINE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# --- LOGIN SECURITY GATE ---
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; font-weight:800; color:#111111; margin-top: 3rem;'>🔒 SECURE ACCESS</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666666; font-size:0.95rem; margin-bottom:2rem;'>BHP Procurement & Vendor Verification Network</p>", unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Corporate Email Address (@bhp.com)")
            key = st.text_input("Master Access Key", type="password")
            submit = st.form_submit_button("Verify Identity Credentials", use_container_width=True)
            
            if submit:
                if email.lower().endswith("@bhp.com") and key == "BHP_Innovation_2026!":
                    st.session_state.authenticated = True
                    st.session_state.user_email = email.lower()
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid corporate domain or entry credentials.")
        st.stop()

# --- THE APPLICATION DASHBOARD (Post-Login) ---

# Sidebar Navigation Panel
with st.sidebar:
    st.markdown("### 🧑‍💻 Verified Session")
    st.markdown(f"<div class='user-profile'>{st.session_state.user_email}</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 📊 Index Metrics")
    if os.path.exists(CHROMA_DIR):
        try:
            db_instance = Chroma(persist_directory=CHROMA_DIR, embedding_function=get_embeddings())
            total_vectors = len(db_instance.get()['ids'])
            st.metric(label="Indexed Knowledge Nodes", value=f"{total_vectors:,}")
        except:
            st.metric(label="Indexed Knowledge Nodes", value="Connected")
    else:
        st.error("System Status: Brain Offline")
        
    st.markdown("---")
    st.caption("BHP Global Supply Chain & Procurement Division. Deployment operates continuously and independently of user infrastructure.")

# Main Presentation Interface
st.markdown("<h1 class='main-header'>BHP <span>Vendor Intelligence</span> Portal</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Semantic Parsing Engine Across Contractor SLA Documentation, Compliance Records, and Capability Matrices</p>", unsafe_allow_html=True)

# Main Query Entry Interface
query = st.text_input("", placeholder="Enter vendor name, SLA parameters, equipment compliance codes, or contractual queries...", label_visibility="collapsed")

# Advanced Filter Layout
filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 3])
with filter_col1:
    results_limit = st.selectbox("Maximum Citation Matches", [5, 10, 15, 25], index=0)
with filter_col2:
    min_score = st.slider("Match Strictness Matrix", 0.0, 1.0, 0.4)

st.markdown("<br>", unsafe_allow_html=True)

# --- QUERY HANDLING & EXECUTION PIPELINE ---
if query:
    if os.path.exists(CHROMA_DIR):
        with st.spinner("Executing structural cross-matching against indexed vendor profile data..."):
            db = Chroma(persist_directory=CHROMA_DIR, embedding_function=get_embeddings())
            
            # Execute Vector Search
            results = db.similarity_search(query, k=results_limit)
            
            if results:
                st.markdown(f"### Relevant Vendor Specifications Located ({len(results)} matches):")
                
                for idx, document_node in enumerate(results):
                    # Resolve system file source path data safely
                    full_source = document_node.metadata.get("source", "System-Sourced Data File")
                    clean_filename = os.path.basename(full_source)
                    page_num = document_node.metadata.get("page", None)
                    page_string = f" — Page {page_num + 1}" if page_num is not None else ""
                    
                    # Custom Structured Result Blocks (Styled in BHP Border Orange)
                    st.markdown(f"""
                        <div class="vendor-card">
                            <div class="vendor-meta">📋 VENDOR RECORD CITATION {idx + 1} | SOURCE: {clean_filename}{page_string}</div>
                            <div style="font-size: 0.95rem; color: #222222; line-height: 1.6; font-family: -apple-system, sans-serif;">
                                {document_node.page_content[:1500]}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No corporate vendor logs met the precision requirements specified.")
    else:
        st.error("Database structural index folder missing. Bundle your 'db_folder' into the root directory via GitHub.")