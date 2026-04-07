import streamlit as st
import time
from datetime import date

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthConnect | Patient Portal", layout="wide", page_icon="🏥")

# --- ADVANCED CUSTOM CSS FOR STELLAR UI ---
st.markdown("""
    <style>
    /* Main Cards */
    .stCard { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #e0e0e0; }
    /* Health Blog Cards */
    .blog-card { background: linear-gradient(135deg, #e3f2fd, #bbdefb); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #2196f3; }
    /* Notification Badge */
    .notif-badge { background-color: #ff4b4b; color: white; padding: 2px 8px; border-radius: 50%; font-size: 0.8rem; vertical-align: top; margin-left: 5px; }
    /* Section Headers */
    .sec-header { color: #2c3e50; font-weight: 600; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-bottom: 15px; margin-top: 20px;}
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE MANAGEMENT ---
if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "Patient App (Rahul)"
if "appointments" not in st.session_state: st.session_state.appointments = []
if "vault_docs" not in st.session_state: st.session_state.vault_docs = False
if "chat_history" not in st.session_state: st.session_state.chat_history = [{"role": "assistant", "content": "👋 Hi Rahul! Ask me anything about your Star Health policy."}]

# ==========================================
# COLLAPSIBLE SIDEBAR & LOGIN MANAGER
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=50) # Fake Logo
    st.title("HealthConnect")
    
    st.markdown("### 🔐 Session Manager")
    st.info(f"🟢 **Logged in as:** \n\n{st.session_state.logged_in_user}")
    
    with st.expander("🔄 Switch Persona / Logout"):
        new_user = st.radio("Select Persona:", ["Patient App (Rahul)", "Doctor Portal (Dr. Gupta)", "TPA Dashboard (Insurer)"])
        if st.button("Switch"):
            st.session_state.logged_in_user = new_user
            st.rerun()
            
    st.markdown("---")
    st.caption("Demo Mode | Built by Rajatbhai Vaghela")

# ==========================================
# PERSONA 1: PATIENT APP MAIN UI
# ==========================================
def render_patient_app():
    # Header & Greeting
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<h2>👋 Good Morning, Rahul! Let's manage your health.</h2>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align: right; padding-top: 15px;'>🔔 Notifications <span class='notif-badge'>2</span></div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin-top: 0px;'>", unsafe_allow_html=True)

    # PATIENT APP INNER TABS
    pt_tab1, pt_tab2, pt_tab3 = st.tabs(["🏠 Home & Booking", "📂 Medical Vault (AI OCR)", "🛡️ Insurance Pre-Check AI"])

    # ---------------------------------------------------------
    # TAB 1: HOME & APPOINTMENT BOOKING
    # ---------------------------------------------------------
    with pt_tab1:
        c1, c2 = st.columns([1, 2], gap="large")
        
        # Left Col: Articles & Engagement
        with c1:
            st.markdown("<div class='sec-header'>📰 Daily Health Tips</div>", unsafe_allow_html=True)
            st.markdown("""
                <div class='blog-card'>
                    <b>🦴 Managing Joint Pain</b><br>
                    <small>Tips for preparing for Orthopedic consultations.</small>
                </div>
                <div class='blog-card'>
                    <b>🥗 Heart-Healthy Diets</b><br>
                    <small>Top 5 foods to reduce cholesterol this winter.</small>
                </div>
            """, unsafe_allow_html=True)

        # Right Col: Booking Engine
        with c2:
            st.markdown("<div class='sec-header'>📅 Book a New Appointment</div>", unsafe_allow_html=True)
            with st.container(border=True):
                # Row 1: Location & Facility
                b_col1, b_col2 = st.columns(2)
                city = b_col1.selectbox("City", ["Delhi NCR", "Mumbai", "Bangalore"])
                hospital = b_col2.selectbox("Hospital", ["Apollo Greams Road", "Fortis Escorts", "Max Super Speciality"])
                
                # Row 2: Doctor & Link Case
                b_col3, b_col4 = st.columns(2)
                doctor = b_col3.selectbox("Specialist / Doctor", ["Dr. A. Gupta (Orthopedics)", "Dr. S. Mehta (Cardiology)"])
                case_link = b_col4.selectbox("Link to Previous Case?", ["🆕 Create New Case", "🔗 Case #882: Knee Pain History"])
                
                # Row 3: Calendar & Slots
                b_col5, b_col6 = st.columns(2)
                apt_date = b_col5.date_input("Select Date", min_value=date.today())
                slot = b_col6.selectbox("Available Slots", ["10:00 AM", "11:30 AM", "02:00 PM", "04:15 PM"])
                
                if st.button("🚀 Confirm Booking & Create Case", type="primary", use_container_width=True):
                    with st.spinner("Syncing with hospital system..."):
                        time.sleep(1)
                        st.session_state.appointments.append(f"{doctor} at {hospital} on {apt_date} ({slot})")
                        st.success("✅ Appointment Confirmed! Case ID #883 created. Your details have been sent to the Doctor's desk.")

            if st.session_state.appointments:
                st.info(f"**Upcoming Appointment:** {st.session_state.appointments[-1]}")

    # ---------------------------------------------------------
    # TAB 2: MEDICAL VAULT & AI STRUCTURING
    # ---------------------------------------------------------
    with pt_tab2:
        st.markdown("<div class='sec-header'>📂 Your Medical History & AI Uploader</div>", unsafe_allow_html=True)
        st.write("Upload messy prescriptions or lab reports. Our AI will automatically structure them for your doctor and insurer.")
        
        v_col1, v_col2 = st.columns([1, 1], gap="large")
        
        with v_col1:
            st.subheader("📤 Upload Document")
            uploaded_file = st.file_uploader("Upload Prescription/Lab Test (PDF, JPG)", type=["pdf", "jpg", "png"])
            if uploaded_file and not st.session_state.vault_docs:
                with st.spinner("🤖 Agentic AI reading and structuring document..."):
                    time.sleep(2.5) # Simulate OCR and LLM processing
                    st.session_state.vault_docs = True
                    st.rerun()

            if st.session_state.vault_docs:
                st.success("✅ Document processed successfully!")
                
        with v_col2:
            st.subheader("🧠 AI Structured Summary")
            if st.session_state.vault_docs:
                st.markdown("""
                <div class='stCard' style='border-left: 4px solid #2ecc71;'>
                    <b>Extracted Clinical Data:</b><br>
                    <ul>
                        <li><b>Diagnosis:</b> Grade 3 Osteoarthritis (Right Knee)</li>
                        <li><b>Prescribed Meds:</b> Paracetamol 500mg, Calcium Supplements</li>
                        <li><b>Recommended Actions:</b> MRI Right Knee, Physiotherapy consult</li>
                        <li><b>ICD-10 Mapping:</b> M19.011 (Auto-tagged for Insurance)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Upload a document on the left to see the AI magic.")

        st.markdown("---")
        st.subheader("🏥 Past Hospital Records")
        with st.expander("Apollo Greams Road (2023)"):
            st.write("📄 MRI Scan Report - Right Knee (Oct 12, 2023)")
            st.write("📄 Discharge Summary - Minor Arthroscopy (Nov 05, 2023)")
        with st.expander("Max Super Speciality (2021)"):
            st.write("📄 Complete Blood Count (CBC) - Routine")

    # ---------------------------------------------------------
    # TAB 3: INSURANCE CHATBOT
    # ---------------------------------------------------------
    with pt_tab3:
        st.markdown("<div class='sec-header'>🛡️ Check Policy Coverage (Star Health)</div>", unsafe_allow_html=True)
        st.write("Don't wait for hospital billing. Ask the AI if your planned procedure is covered.")
        
        chat_container = st.container(height=300, border=True)
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]): st.markdown(msg["content"])
                
        user_input = st.chat_input("Ask about knee surgery, room rent, or consumables...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.rerun() # In a real app, you'd process the LLM response here. (Simplified for this UI demo to show layout).

# ==========================================
# ROUTER
# ==========================================
if st.session_state.logged_in_user == "Patient App (Rahul)":
    render_patient_app()
elif st.session_state.logged_in_user == "Doctor Portal (Dr. Gupta)":
    st.title("🩺 Doctor Portal")
    st.write("UI Coming next...")
else:
    st.title("🏢 TPA Dashboard")
    st.write("UI Coming next...")
