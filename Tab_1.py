import streamlit as st
import time
from datetime import date
import uuid
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthConnect | Agentic Ecosystem", layout="wide", page_icon="🏥")

# --- ADVANCED CUSTOM CSS ---
st.markdown("""
    <style>
    .main-header { font-size: 2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 20px; }
    .stCard { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #e0e0e0; }
    .kpi-card { background: white; padding: 20px; border-radius: 10px; border-top: 5px solid #3B82F6; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .kpi-value { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; margin: 0; }
    .kpi-label { font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 600; }
    .ai-box { background-color: #F8FAFC; border: 1px dashed #3B82F6; padding: 15px; border-radius: 10px; margin-top: 10px; }
    .blog-card { background: #EFF6FF; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #3B82F6; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "Patient App (Rahul)"
if "case_status" not in st.session_state: st.session_state.case_status = "Active"
if "appointments" not in st.session_state: st.session_state.appointments = []
if "doc_notes" not in st.session_state: st.session_state.doc_notes = ""
if "ai_processed" not in st.session_state: st.session_state.ai_processed = False

# --- DUMMY DATA FOR DASHBOARD INTERACTIVITY ---
DASHBOARD_STATS = {
    "Today": {"total": 12, "pending": 3, "attended": 9, "claims": 1},
    "This Week": {"total": 84, "pending": 12, "attended": 72, "claims": 8},
    "This Month": {"total": 320, "pending": 45, "attended": 275, "claims": 32}
}

# ==========================================
# SHARED SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=60)
    st.title("HealthConnect")
    st.write(f"Logged in: **{st.session_state.logged_in_user}**")
    
    with st.expander("🔄 Switch Platform Access"):
        target = st.radio("Switch to:", ["Patient App (Rahul)", "Doctor Portal (Dr. Gupta)", "TPA Dashboard (Insurer)"])
        if st.button("Confirm Switch"):
            st.session_state.logged_in_user = target
            st.rerun()
    
    st.markdown("---")
    st.caption("AI-Powered Claims Pre-Auth Platform")

# ==========================================
# PERSONA 1: PATIENT APP UI
# ==========================================
def render_patient_app():
    st.markdown("<div class='main-header'>👋 Welcome back, Rahul!</div>", unsafe_allow_html=True)
    
    p_tab1, p_tab2, p_tab3 = st.tabs(["🏥 Dashboard & Booking", "📂 Records Vault", "🛡️ AI Policy Chat"])
    
    with p_tab1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.subheader("Daily Health Insights")
            st.markdown("""<div class='blog-card'><b>Managing Knee Pain</b><br><small>3 exercises to do at home.</small></div>""", unsafe_allow_html=True)
            st.markdown("""<div class='blog-card'><b>Heart Health</b><br><small>Why walking 10k steps matters.</small></div>""", unsafe_allow_html=True)
        
        with c2:
            st.subheader("Book Appointment")
            with st.container(border=True):
                city = st.selectbox("City", ["Delhi", "Mumbai", "Bangalore"])
                hosp = st.selectbox("Hospital", ["Apollo", "Fortis", "Max"])
                doc = st.selectbox("Doctor", ["Dr. Gupta (Ortho)", "Dr. Verma (Cardio)"])
                if st.button("Confirm Appointment", type="primary"):
                    st.success(f"Confirmed with {doc} at {hosp}!")

    with p_tab2:
        st.subheader("Clinical History")
        st.info("No documents uploaded yet. Start by creating a folder.")
        
    with p_tab3:
        st.subheader("Insurance Assistant")
        st.chat_input("Ask about your coverage...")

# ==========================================
# PERSONA 2: DOCTOR PORTAL UI
# ==========================================
def render_doctor_app():
    # 1. INTERACTIVE HEADER & FILTERS
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1: st.markdown("<div class='main-header'>🩺 Physician Command Center</div>", unsafe_allow_html=True)
    with col_h2: 
        filter_val = st.selectbox("📊 Dashboard View", ["Today", "This Week", "This Month"])
    
    # 2. DYNAMIC KPIs (These change based on filter_val)
    stats = DASHBOARD_STATS[filter_val]
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{stats['total']}</p><p class='kpi-label'>Total Patients</p></div>", unsafe_allow_html=True)
    with k2: st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{stats['attended']}</p><p class='kpi-label'>Attended</p></div>", unsafe_allow_html=True)
    with k3: st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{stats['pending']}</p><p class='kpi-label'>Pending</p></div>", unsafe_allow_html=True)
    with k4: st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{stats['claims']}</p><p class='kpi-label'>TPA Flags</p></div>", unsafe_allow_html=True)

    st.markdown("### 📋 Active Consultation")
    
    with st.container(border=True):
        st.write("**Patient:** Rahul Sharma (Age: 58) | **History:** Grade 3 Osteoarthritis | **Insurer:** Star Health")
        
        d_left, d_right = st.columns([1, 1], gap="large")
        
        with d_left:
            st.markdown("#### Clinical Input")
            mode = st.radio("Input Method", ["Voice-to-Text", "Manual Entry", "Scan Paper Notes"], horizontal=True)
            
            if mode == "Voice-to-Text":
                if st.button("🎙️ Start Transcription"):
                    with st.spinner("AI Scribe Listening..."):
                        time.sleep(2)
                        st.session_state.doc_notes = "Patient diagnosed with advanced arthritis. Prescribe Tab. Pan-D once daily for 10 days, Tab. Osteo-Plus twice daily for 30 days. Order MRI Right Knee and Blood CBC. Recommend Total Knee Replacement with Zimmer High-Grade Implant."
                        st.rerun()
            
            notes = st.text_area("Observations & Treatment Plan:", value=st.session_state.doc_notes, height=180)
            
            if st.button("✨ Process Encounter (AI Scribe)", type="primary", use_container_width=True):
                st.session_state.ai_processed = True
                st.rerun()

        with d_right:
            st.markdown("#### Agentic AI Extraction")
            if st.session_state.ai_processed:
                st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
                st.write("🤖 **Agent 1 (Scribe):** Structuring clinical data...")
                
                # Mock AI Extraction Tables
                st.markdown("**💊 Prescriptions Identified:**")
                meds_data = {
                    "Medicine": ["Tab. Pan-D", "Tab. Osteo-Plus"],
                    "Dosage": ["Once Daily", "Twice Daily"],
                    "Duration": ["10 Days", "30 Days"]
                }
                st.table(pd.DataFrame(meds_data))
                
                st.markdown("**🔬 Lab Tests Ordered:**")
                st.write("- MRI Right Knee\n- Blood CBC")
                
                st.markdown("**🚩 Insurance Guardrail (Agent 2):**")
                if "zimmer" in notes.lower() or "high-grade" in notes.lower():
                    st.warning("Zimmer High-Grade Implant detected. Pre-auth requires a clinical justification for this specific model.")
                    justification = st.text_input("Enter Justification for Star Health:")
                    if st.button("Sync to TPA & Patient Profile"):
                        st.success("Case Updated! Patient and TPA have been notified.")
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Awaiting clinical input to begin structuring data...")

# ==========================================
# MAIN ROUTER
# ==========================================
if st.session_state.logged_in_user == "Patient App (Rahul)":
    render_patient_app()
elif st.session_state.logged_in_user == "Doctor Portal (Dr. Gupta)":
    render_doctor_app()
else:
    st.title("🏢 TPA Dashboard")
    st.write("This persona will be built next to receive the AI Dossier.")
