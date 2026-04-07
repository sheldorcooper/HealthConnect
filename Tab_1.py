import streamlit as st
import time
from datetime import date
import uuid
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthConnect | Full-Stack Agentic Health", layout="wide", page_icon="🏥")

# --- MASTER CSS (Combined for all personas) ---
st.markdown("""
    <style>
    /* Global Styles */
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 20px; }
    .stCard { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #e0e0e0; }
    .sec-header { color: #2c3e50; font-weight: 600; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-bottom: 15px; margin-top: 20px;}
    
    /* Patient Specific */
    .blog-card { background: linear-gradient(135deg, #e3f2fd, #bbdefb); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #2196f3; transition: 0.3s; cursor: pointer; color: #1E3A8A; }
    .blog-card:hover { transform: scale(1.02); }
    .notif-badge { background-color: #ff4b4b; color: white; padding: 2px 8px; border-radius: 50%; font-size: 0.8rem; vertical-align: top; margin-left: 5px; }
    
    /* Doctor Specific */
    .kpi-card { background: white; padding: 20px; border-radius: 10px; border-top: 5px solid #3B82F6; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .kpi-value { font-size: 2.2rem; font-weight: bold; color: #1E3A8A; margin: 0; }
    .kpi-label { font-size: 0.8rem; color: #64748B; text-transform: uppercase; font-weight: 600; }
    .ai-box { background-color: #F8FAFC; border: 1px dashed #3B82F6; padding: 15px; border-radius: 10px; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- MASTER DATA ---
HOSPITAL_DATA = {
    "Delhi NCR": {
        "Max Super Speciality": ["Dr. A. Gupta (Ortho)", "Dr. V. Sharma (Cardio)"],
        "Fortis Escorts": ["Dr. S. Mehta (Cardio)", "Dr. R. Singh (Surgery)"]
    },
    "Mumbai": {
        "Apollo Navi Mumbai": ["Dr. K. Desai (Neuro)", "Dr. P. Patil (Ortho)"],
        "Hinduja Hospital": ["Dr. L. Joshi (Pediatrics)"]
    }
}

DOC_DASHBOARD_STATS = {
    "Today": {"total": 12, "attended": 9, "pending": 3, "flags": 1},
    "This Week": {"total": 84, "attended": 72, "pending": 12, "flags": 8},
    "This Month": {"total": 320, "attended": 275, "pending": 45, "flags": 32}
}

# --- SESSION STATE INITIALIZATION ---
if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "Patient App (Rahul)"
if "vault_records" not in st.session_state: st.session_state.vault_records = [{"id": "1", "hospital": "Apollo Greams Road", "doctor": "Dr. Raj", "date": "2023-10-12", "files": ["MRI_Report.pdf"], "summary": True}]
if "chat_history" not in st.session_state: st.session_state.chat_history = [{"role": "assistant", "content": "👋 Hi Rahul! I'm your AI Assistant."}]
if "doc_notes" not in st.session_state: st.session_state.doc_notes = ""
if "ai_processed_doc" not in st.session_state: st.session_state.ai_processed_doc = False
if "creating_record" not in st.session_state: st.session_state.creating_record = False

# ==========================================
# SHARED SIDEBAR
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=60)
    st.title("HealthConnect")
    st.info(f"**Current Access:** \n\n{st.session_state.logged_in_user}")
    
    with st.expander("🔄 Switch Platform / Logout"):
        target = st.radio("Select Persona:", ["Patient App (Rahul)", "Doctor Portal (Dr. Gupta)", "TPA Dashboard (Insurer)"])
        if st.button("Confirm Switch"):
            st.session_state.logged_in_user = target
            st.rerun()
    st.markdown("---")
    st.caption("Agentic HealthTech Demo v1.0")

# ==========================================
# PERSONA 1: HIGH-FIDELITY PATIENT APP
# ==========================================
def render_patient_app():
    col1, col2 = st.columns([4, 1])
    with col1: st.markdown("<div class='main-header'>👋 Good Morning, Rahul!</div>", unsafe_allow_html=True)
    with col2: st.markdown("<div style='text-align: right; padding-top: 15px;'>🔔 Notifications <span class='notif-badge'>2</span></div>", unsafe_allow_html=True)

    pt_tab1, pt_tab2, pt_tab3 = st.tabs(["🏠 Home & Booking", "📂 Medical Vault", "🛡️ AI Insurance Chat"])

    with pt_tab1:
        c1, c2 = st.columns([1, 2], gap="large")
        with c1:
            st.markdown("<div class='sec-header'>📰 Daily Health Tips</div>", unsafe_allow_html=True)
            st.markdown("""
                <a href='https://www.webmd.com' target='_blank' style='text-decoration:none;'>
                    <div class='blog-card'><b>🦴 Preparing for Knee Surgery</b><br><small>Click to read recovery tips.</small></div>
                </a>
                <div class='blog-card'><b>🥗 Heart-Healthy Diets</b><br><small>5 foods to reduce cholesterol.</small></div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='sec-header'>📅 Book Appointment</div>", unsafe_allow_html=True)
            with st.container(border=True):
                city = st.selectbox("1. Select City", list(HOSPITAL_DATA.keys()))
                hospital = st.selectbox("2. Select Hospital", list(HOSPITAL_DATA[city].keys()))
                doctor = st.selectbox("3. Select Specialist", HOSPITAL_DATA[city][hospital])
                st.date_input("4. Date")
                if st.button("🚀 Confirm Booking", type="primary", use_container_width=True):
                    st.success(f"Appointment confirmed with {doctor}!")

    with pt_tab2:
        st.markdown("<div class='sec-header'>📂 Manage Clinical Records</div>", unsafe_allow_html=True)
        if st.button("➕ Create New Medical Record Folder"):
            st.session_state.creating_record = not st.session_state.creating_record
        
        if st.session_state.creating_record:
            with st.container(border=True):
                v_col1, v_col2 = st.columns(2)
                h_name = v_col1.text_input("Hospital Name")
                d_name = v_col2.text_input("Doctor Name")
                if st.button("Save Folder"):
                    new_rec = {"id": str(uuid.uuid4()), "hospital": h_name, "doctor": d_name, "date": str(date.today()), "files": [], "summary": False}
                    st.session_state.vault_records.insert(0, new_rec)
                    st.session_state.creating_record = False
                    st.rerun()

        for i, record in enumerate(st.session_state.vault_records):
            with st.expander(f"🏥 {record['hospital']} | 🩺 {record['doctor']}", expanded=(i==0)):
                up_col, sum_col = st.columns([1, 1])
                with up_col:
                    st.file_uploader("Upload Rx/Reports", key=f"file_{record['id']}")
                    if st.button("✨ Generate AI Summary", key=f"sum_{record['id']}"):
                        record['summary'] = True
                        st.rerun()
                with sum_col:
                    if record['summary']:
                        st.success("🤖 AI Extraction Complete: \n- Diagnosis: Grade 3 Osteoarthritis \n- Rec: MRI Knee")

    with pt_tab3:
        st.markdown("<div class='sec-header'>🛡️ AI Insurance Concierge</div>", unsafe_allow_html=True)
        mode = st.radio("Context:", ["General Policy", "Case-Specific"], horizontal=True)
        chat_container = st.container(height=300, border=True)
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]): st.markdown(msg["content"])
        u_input = st.chat_input("Ask about your Star Health coverage...")
        if u_input:
            st.session_state.chat_history.append({"role": "user", "content": u_input})
            st.session_state.chat_history.append({"role": "assistant", "content": "Based on your policy, Knee Surgery is fully covered."})
            st.rerun()

# ==========================================
# PERSONA 2: HIGH-FIDELITY DOCTOR PORTAL
# ==========================================
def render_doctor_app():
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1: st.markdown("<div class='main-header'>🩺 Physician Command Center</div>", unsafe_allow_html=True)
    with col_h2: filter_val = st.selectbox("📊 View Dashboard", ["Today", "This Week", "This Month"])

    s = DOC_DASHBOARD_STATS[filter_val]
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{s['total']}</p><p class='kpi-label'>Appointments</p></div>", unsafe_allow_html=True)
    with k2: st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{s['attended']}</p><p class='kpi-label'>Attended</p></div>", unsafe_allow_html=True)
    with k3: st.markdown(f"<div class='kpi-card'><p class='kpi-value'>{s['pending']}</p><p class='kpi-label'>Pending</p></div>", unsafe_allow_html=True)
    with k4: st.markdown(f"<div class='kpi-card' style='border-top-color:#e74c3c;'><p class='kpi-value'>{s['flags']}</p><p class='kpi-label'>TPA Flags</p></div>", unsafe_allow_html=True)

    st.markdown("### 📋 Current Consultation: Rahul Sharma")
    with st.container(border=True):
        d_left, d_right = st.columns([1, 1.2], gap="large")
        with d_left:
            st.markdown("#### Clinical Input")
            mode = st.radio("Input Modality", ["🎙️ Voice-to-Text", "⌨️ Manual Entry"], horizontal=True)
            if mode == "🎙️ Voice-to-Text":
                if st.button("🔴 Start AI Scribe"):
                    with st.spinner("Listening..."):
                        time.sleep(1.5)
                        st.session_state.doc_notes = "Diagnosed Arthritis. Tab. Pan-D once daily for 10 days. Order MRI Knee. Use Zimmer High-Grade Implant."
                        st.rerun()
            notes = st.text_area("Encounter Notes:", value=st.session_state.doc_notes, height=150)
            if st.button("✨ Process Encounter", type="primary", use_container_width=True):
                st.session_state.ai_processed_doc = True
                st.rerun()
        with d_right:
            st.markdown("#### Agentic Scribe Results")
            if st.session_state.ai_processed_doc:
                st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
                st.markdown("**💊 Medicines Extracted:**")
                st.table(pd.DataFrame({"Medicine": ["Tab. Pan-D"], "Dosage": ["Once Daily"], "Duration": ["10 Days"]}))
                st.markdown("**🔬 Ordered Lab Tests:**")
                st.write("- MRI Right Knee")
                if "zimmer" in notes.lower():
                    st.warning("⚠️ TPA Alert: High-grade implant needs clinical justification.")
                    st.text_input("Enter Justification:")
                    if st.button("Submit to Insurer"): st.success("Synced!")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.info("Input clinical notes on the left to see AI extraction.")

# ==========================================
# MASTER ROUTER
# ==========================================
if st.session_state.logged_in_user == "Patient App (Rahul)":
    render_patient_app()
elif st.session_state.logged_in_user == "Doctor Portal (Dr. Gupta)":
    render_doctor_app()
else:
    st.title("🏢 TPA Dashboard")
    st.info("This will be the final step: The AI-Generated Dossier.")
