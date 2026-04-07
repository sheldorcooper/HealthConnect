import streamlit as st
import time
from datetime import date
import uuid

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthConnect | Multi-Persona TPA", layout="wide", page_icon="🏥")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stCard { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #e0e0e0; }
    .kpi-card { background: linear-gradient(135deg, #fdfbfb, #ebedee); padding: 15px; border-radius: 10px; border-left: 5px solid #2ecc71; text-align: center; }
    .kpi-value { font-size: 2rem; font-weight: bold; color: #2c3e50; margin: 0; }
    .kpi-label { font-size: 0.9rem; color: #7f8c8d; text-transform: uppercase; letter-spacing: 1px; }
    .ai-alert { background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; border-radius: 5px; margin-top: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "Doctor Portal (Dr. Gupta)"
if "doc_voice_text" not in st.session_state: st.session_state.doc_voice_text = ""
if "case_status_rahul" not in st.session_state: st.session_state.case_status_rahul = "In Waiting Room"
if "ai_justification_needed" not in st.session_state: st.session_state.ai_justification_needed = False

# ==========================================
# SIDEBAR / LOGIN MANAGER
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=50)
    st.title("HealthConnect")
    st.info(f"🟢 **Logged in as:** \n\n{st.session_state.logged_in_user}")
    with st.expander("🔄 Switch Persona"):
        new_user = st.radio("Select Persona:", ["Patient App (Rahul)", "Doctor Portal (Dr. Gupta)", "TPA Dashboard (Insurer)"])
        if st.button("Switch"):
            st.session_state.logged_in_user = new_user
            st.rerun()

# ==========================================
# PERSONA 2: DOCTOR PORTAL
# ==========================================
def render_doctor_app():
    # --- HEADER & KPIs ---
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1: st.markdown("<h2>🩺 Apollo Clinical Dashboard | Dr. A. Gupta (Orthopedics)</h2>", unsafe_allow_html=True)
    with col_h2: 
        period = st.selectbox("📅 Filter Period", ["Today", "This Week", "This Month"])

    st.markdown("<hr style='margin-top: 0px;'>", unsafe_allow_html=True)

    # DYNAMIC KPI DASHBOARD
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown("<div class='kpi-card'><p class='kpi-value'>12</p><p class='kpi-label'>Appointments</p></div>", unsafe_allow_html=True)
    with k2: st.markdown("<div class='kpi-card'><p class='kpi-value'>4</p><p class='kpi-label'>Attended</p></div>", unsafe_allow_html=True)
    with k3: st.markdown("<div class='kpi-card' style='border-left-color: #f39c12;'><p class='kpi-value'>3</p><p class='kpi-label'>Pending Lab Results</p></div>", unsafe_allow_html=True)
    with k4: st.markdown("<div class='kpi-card' style='border-left-color: #e74c3c;'><p class='kpi-value'>1</p><p class='kpi-label'>Discharge Blocked (TPA)</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ACTIVE PATIENT QUEUE ---
    st.markdown("### 👥 Active Patient Queue")
    
    # Patient 1: The Case we created in Tab 1
    with st.expander(f"🟢 10:00 AM | Rahul Sharma (Age: 58) | Status: {st.session_state.case_status_rahul}", expanded=True):
        
        # Split into Patient Context (Left) and Clinical Input (Right)
        c_left, c_right = st.columns([1, 1.5], gap="large")
        
        with c_left:
            st.markdown("#### 📋 Patient Context")
            st.write("**Reason for visit:** Case #882 - Chronic Knee Pain")
            st.write("**Vitals:** BP 130/85 | Temp 98.6°F | Wt 82kg")
            
            st.markdown("**Previous History (Auto-Synced via AI Vault):**")
            st.info("📄 MRI Report (Oct 12): Grade 3 Osteoarthritis \n\n💊 Current Meds: Paracetamol 500mg")
            
            st.markdown("**Insurance Coverage:**")
            st.success("Star Health Comprehensive (₹5,00,000) - TKR Covered.")

        with c_right:
            st.markdown("#### ✍️ Clinical Encounter Entry")
            
            # Input Modality Switcher
            input_mode = st.radio("Select Input Modality:", ["🎙️ Voice Dictation", "⌨️ Manual Type", "📤 Delegate to Assistant"], horizontal=True)
            
            if input_mode == "🎙️ Voice Dictation":
                if st.button("🔴 Start Recording Voice Note"):
                    with st.spinner("Listening and Transcribing via Whisper AI..."):
                        time.sleep(2)
                        st.session_state.doc_voice_text = "Patient requires Total Knee Replacement (TKR). Planning to use Zimmer Biomet high-grade trabecular metal implant due to poor bone density. Prescribing standard pre-op blood panel."
                        st.rerun()
                notes = st.text_area("Transcribed Notes (Editable):", value=st.session_state.doc_voice_text, height=100)
            
            elif input_mode == "⌨️ Manual Type":
                notes = st.text_area("Clinical Notes:", placeholder="Type observation and treatment plan here...", height=100)
                
            elif input_mode == "📤 Delegate to Assistant":
                st.info("Upload physical OT notes or handwritten prescriptions. AI OCR will extract and structure it for you.")
                st.file_uploader("Upload Handwritten File")
                notes = ""

            # Action Bar
            st.markdown("**Clinical Actions:**")
            actions = st.multiselect("Orders:", ["Prescribe Medications", "Order Lab Tests (Pre-Op Panel)", "Schedule Surgery (TKR)", "Assign to Physiotherapist"])

            # --- THE MAGIC AGENTIC MOMENT ---
            if st.button("💾 Save Encounter & Run AI Pre-Audit", type="primary"):
                with st.spinner("🤖 Agent 2 (Strategist) cross-referencing notes with Star Health Policy..."):
                    time.sleep(2)
                    if "high-grade" in notes.lower() or "zimmer" in notes.lower():
                        st.session_state.ai_justification_needed = True
                    st.session_state.case_status_rahul = "Treatment Plan Finalized"
                    st.rerun()

            # Display the AI Guardrail Warning
            if st.session_state.ai_justification_needed:
                st.markdown("""
                <div class='ai-alert'>
                    <b>⚠️ AI Claims Strategist Warning:</b><br>
                    You selected a "High-Grade Trabecular Implant". Under Star Health Policy Clause 4.2, high-grade implants are only payable with a clinical justification.<br><br>
                    <i>Please provide a justification to prevent TPA query/delay:</i>
                </div>
                """, unsafe_allow_html=True)
                justification = st.text_input("Clinical Justification:")
                if st.button("Submit Justification & Finalize"):
                    st.success("✅ Justification attached to Verified Dossier. TPA Approval expected in < 30 mins.")
                    st.session_state.ai_justification_needed = False

    # Patient 2 (Dummy for visual queue)
    with st.expander("🟡 10:30 AM | Sunita Verma (Age: 45) | Status: Waiting for Doctor"):
        st.write("Patient details go here...")


# ==========================================
# ROUTER
# ==========================================
if st.session_state.logged_in_user == "Patient App (Rahul)":
    st.write("Patient App UI is hidden. Switch to Patient Persona in sidebar.")
elif st.session_state.logged_in_user == "Doctor Portal (Dr. Gupta)":
    render_doctor_app()
else:
    st.title("🏢 TPA Dashboard")
    st.write("Next persona UI coming soon...")
