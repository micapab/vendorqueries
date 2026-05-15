import sys
import pysqlite3
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import os
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- PAGE SETUP ---
st.set_page_config(page_title="BHP Vendor Intelligence Portal", page_icon="🔍", layout="wide")

# Custom BHP Corporate Styling
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    h1 { color: #E05206; font-family: 'Arial Black', sans-serif; }
    .stButton>button { background-color: #E05206; color: white; border-radius: 4px; }
    .stButton>button:hover { background-color: #BA4203; color: white; }
    </style>
""", unsafe_allowed_html=True)

# --- SECURE CREDENTIAL SYSTEM ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔒 BHP Global Procurement Network")
    st.subheader("Vendor Knowledge Graph Node Authorization")
    
    email = st.text_input("Corporate Email Address", placeholder="username@bhp.com")
    passcode = st.text_input("Master Access Key", type="password")
    
    if st.button("Verify Identity Credentials"):
        if email.strip().lower().endswith("@bhp.com") and passcode == "BHP_Innovation_2026!":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Authentication Fault: Invalid domain signature or access key.")
    st.stop()

# --- MAIN APPLICATION SYSTEM ---
st.title("🔍 BHP Vendor Intelligence Engine")
st.caption("Connected to Vector Storage Node // Secure Session Active")

# Fixed relative folder mapping for the Chroma data folder inside your repo
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "db_folder")

@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Instantiate Database Connection safely
if os.path.exists(CHROMA_DIR):
    try:
        db = Chroma(persist_directory=CHROMA_DIR, embedding_function=get_embeddings())
        st.sidebar.success("📊 Database Hub Status: Connected")
    except Exception as e:
        st.sidebar.error(f"❌ Initialization Fault: {str(e)}")
        db = None
else:
    st.sidebar.error("⚠️ Data Layer Missing: 'db_folder' registry cannot be found.")
    db = None

# Sidebar Metrics Panel
st.sidebar.markdown("---")
st.sidebar.markdown("### System Metrics")
st.sidebar.metric(label="Security Level", value="Restricted")
st.sidebar.metric(label="Indexed Nodes", value="Active (788MB)")

# User Query Operations Matrix
query = st.text_input("Enter procurement query, vendor specifications, or contract terms:", 
                     placeholder="e.g., Which vendors supply high-capacity haul truck tires in Western Australia?")

if query:
    if db is not None:
        with st.spinner("Executing vector search matrix..."):
            results = db.similarity_search(query, k=4)
            
            st.markdown(f"### Target Match Vector Array Output")
            for idx, doc in enumerate(results):
                with st.expander(f"Reference Match Record #{idx+1}", expanded=True):
                    st.write(doc.page_content)
                    if doc.metadata:
                        st.caption(f"**Source Origin Metadata:** {doc.metadata}")
    else:
        st.error("Operation Aborted: Connection to the underlying database collection is offline.")