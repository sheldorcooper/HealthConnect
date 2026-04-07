import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthConnect | Multi-Persona TPA", layout="wide", page_icon="🏥")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .patient-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; margin-bottom: 20px; }
    .nav-header { font-size: 1.2rem; color: #666; padding-bottom: 10px; border-bottom: 1px solid #ddd; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- GLOBAL SESSION STATE ---
# This allows data to flow seamlessly between the different user logins
if "case_status" not in st.session_state:
    st.session_state.case_status = "Not Initiated" # Can be: Not Initiated, Active, Pending Discharge, Approved
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "👋 Hi Rahul! Ask me anything about your Star Health policy coverage before booking."}]

# ==========================================
# SIDEBAR: THE LOGIN SIMULATOR
# ==========================================
with st.sidebar:
    st.title("🔐 Platform Login")
    st.write("Simulate the end-to-end journey by logging in as different users.")
    
    # THE PERSONA SWITCHER
    active_persona = st.radio(
        "Select User Persona:",
        [
            "📱 Patient App (Rahul)", 
            "🩺 Doctor Portal (Dr. Gupta)", 
            "🤖 Agent Backend (System View)", 
            "🏢 TPA Dashboard (Insurer)"
        ]
    )
    
    st.markdown("---")
    st.title("⚙️ Demo Controls")
    app_mode = st.radio("Mode:", ["Sample Mode (Fast)", "Live API Mode"])
    st.markdown("---")
    st.caption("Project by: Rajatbhai Vaghela (Product Manager)")

# ==========================================
# PERSONA 1: PATIENT APP
# ==========================================
def render_patient_app():
    st.markdown('<div class="nav-header">📱 HealthConnect Patient App | Welcome, Rahul</div>', unsafe_allow_html=True)
    st.title("Your Health Journey")
    
    col1, col2 = st.columns([1, 1.2], gap="large")

    with col1:
        st.subheader("My Insurance Profile")
        st.markdown("""
            <div class="patient-card">
                <h4>Star Health Comprehensive</h4>
                <p><b>Policy Number:</b> #SH-8821<br>
                <b>Sum Insured:</b> ₹5,00,000<br>
                <b>Status:</b> Active (Waiting periods cleared)</p>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("Plan a Hospital Visit")
        hospital = st.selectbox("Select Hospital", ["Apollo Hospitals, Greams Road", "Fortis Healthcare"])
        surgery_type = st.selectbox("Procedure", ["Total Knee Replacement (TKR)", "Cataract Surgery"])
        date = st.date_input("Admission Date")

        if st.session_state.case_status == "Not Initiated":
            if st.button("🚀 Initiate Case & Book Slot", use_container_width=True, type="primary"):
                with st.spinner("Creating Digital Case File..."):
                    time.sleep(1.5)
                    st.session_state.case_status = "Active"
                    st.rerun()
        else:
            st.success(f"✅ Case Initiated for {surgery_type} at {hospital}.")
            st.info("👉 Switch to **Doctor Portal** in the sidebar to continue the journey.")

    with col2:
        st.subheader("🤖 Policy Pre-Check AI")
        chat_container = st.container(height=350, border=True)
        
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        s_col1, s_col2 = st.columns(2)
        user_input = None
        if s_col1.button("Is Knee Replacement covered?"): user_input = "Is Total Knee Replacement covered, and what is the room rent limit?"
        if s_col2.button("Are consumables covered?"): user_input = "Will the insurance pay for surgical consumables?"

        manual_input = st.chat_input("Ask your policy AI...")
        if manual_input: user_input = manual_input

        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with chat_container:
                with st.chat_message("user"): st.markdown(user_input)
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    ai_response = "⚠️ **Warning:** Consumables are **Not Payable**." if "consumables" in user_input.lower() else "🟢 **Yes!** Total Knee Replacement is fully covered. Room Rent limit is ₹5,000/day."
                    
                    full_response = ""
                    for chunk in ai_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
            
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()

# ==========================================
# PERSONA 2: DOCTOR PORTAL
# ==========================================
def render_doctor_app():
    st.markdown('<div class="nav-header">🩺 Apollo Hospitals Clinical Portal | Dr. Gupta (Orthopedics)</div>', unsafe_allow_html=True)
    
    if st.session_state.case_status == "Not Initiated":
        st.warning("📭 No active cases right now. (Go to the Patient App to initiate a case first).")
    else:
        st.title("Live Case: Rahul Sharma")
        st.write("This is where the Doctor or Clinical Assistant will input data digitally.")
        st.info("We will build the Voice-to-Text and OCR upload UI here next.")

# ==========================================
# PERSONA 3: SYSTEM ADMIN / AGENT BACKEND
# ==========================================
def render_agent_backend():
    st.markdown('<div class="nav-header">🤖 HealthConnect Agentic Orchestration Logs</div>', unsafe_allow_html=True)
    st.title("AI Processing Engine")
    st.write("This screen shows the multi-agent system cross-referencing clinical notes with the policy PDF.")

# ==========================================
# PERSONA 4: TPA DASHBOARD
# ==========================================
def render_tpa_app():
    st.markdown('<div class="nav-header">🏢 Star Health TPA Command Center | Officer Desk</div>', unsafe_allow_html=True)
    st.title("Claims Verification Queue")
    st.write("This is where the 8-hour wait becomes a 30-minute approval via the Verified AI Dossier.")

# ==========================================
# ROUTING LOGIC
# ==========================================
if active_persona == "📱 Patient App (Rahul)":
    render_patient_app()
elif active_persona == "🩺 Doctor Portal (Dr. Gupta)":
    render_doctor_app()
elif active_persona == "🤖 Agent Backend (System View)":
    render_agent_backend()
elif active_persona == "🏢 TPA Dashboard (Insurer)":
    render_tpa_app()
