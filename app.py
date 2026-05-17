import sys
import pysqlite3
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import os
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- PAGE SETUP ---
st.set_page_config(page_title="BHP Vendor Intelligence Portal", page_icon="🔍", layout="wide")

# Initialize session state variables cleanly at startup
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# --- SECURE CREDENTIAL SYSTEM ---
if not st.session_state["authenticated"]:
    st.title("🔒 BHP Global Procurement Network")
    st.subheader("Vendor Knowledge Graph Node Authorization")
    
    email = st.text_input("Corporate Email Address", placeholder="username@bhp.com", key="auth_email")
    passcode = st.text_input("Master Access Key", type="password", key="auth_passcode")
    
    if st.button("Verify Identity Credentials"):
        if email.strip().lower().endswith("@bhp.com") and passcode == "BHP_Innovation_2026!":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Authentication Fault: Invalid domain signature or access key.")
    st.stop()

# --- MAIN APPLICATION SYSTEM (Only runs after login) ---
st.title("🔍 BHP Vendor Intelligence Engine")
st.caption("Connected to Vector Storage Node // Secure Session Active")

# Fixed relative folder mapping for the Chroma data folder inside your repo
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "db_folder")

@st.cache_resource
def get_embeddings():
    try:
        return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    except Exception:
        return None

# Instantiate Database Connection safely with a strict fallback
db = None
embeddings = get_embeddings()

if embeddings and os.path.exists(CHROMA_DIR):
    try:
        db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
        st.sidebar.success("📊 Database Hub Status: Connected")
    except Exception as e:
        st.sidebar.error(f"❌ Initialization Fault: {str(e)}")
else:
    st.sidebar.error("⚠️ Data Layer Missing: 'db_folder' registry cannot be found.")

# Sidebar Metrics Panel
st.sidebar.markdown("---")
st.sidebar.markdown("### System Metrics")
st.sidebar.metric(label="Security Level", value="Restricted")
st.sidebar.metric(label="Indexed Nodes", value="Active (788MB)")

# User Query Operations Matrix
query = st.text_input("Enter procurement query, vendor specifications, or contract terms:", 
                     placeholder="e.g., Which vendors supply high-capacity haul truck tires in Western Australia?",
                     key="user_query")

if query:
    if db is not None:
        with st.spinner("Executing vector search matrix..."):
            try:
                results = db.similarity_search(query, k=4)
                
                st.markdown(f"### Target Match Vector Array Output")
                for idx, doc in enumerate(results):
                    with st.expander(f"Reference Match Record #{idx+1}", expanded=True):
                        st.write(doc.page_content)
                        
                        # --- SMART DOCUMENT LINKING SYSTEM ---
                        if hasattr(doc, 'metadata') and doc.metadata:
                            st.caption(f"**Source Origin Metadata:** {doc.metadata}")
                            
                            source_path = doc.metadata.get("source", "")
                            file_name = os.path.basename(source_path) if source_path else ""
                            
                            if file_name:
                                onedrive_base = "https://mysite.bhpbilliton.com.mcas.ms/my?id=%2Fpersonal%2Fmariafrancesca%5Fpabelico%5Fbhp%5Fcom%2FDocuments%2FVendorDocs"
                                safe_file_name = file_name.replace(" ", "%20")
                                full_download_url = f"{onedrive_base}%2F{safe_file_name}&ga=1"
                                
                                st.markdown(f"🔗 [Open Original Document ({file_name})]({full_download_url})")
            except Exception as search_error:
                st.error(f"Search Execution Error: {str(search_error)}")
    else:
        st.error("Operation Aborted: Connection to the underlying database collection is offline.")