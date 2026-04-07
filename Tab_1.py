import streamlit as st
import time
from datetime import date
import uuid

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthConnect | Patient Portal", layout="wide", page_icon="🏥")

# --- ADVANCED CUSTOM CSS ---
st.markdown("""
    <style>
    .stCard { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #e0e0e0; }
    .blog-card { background: linear-gradient(135deg, #e3f2fd, #bbdefb); padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #2196f3; transition: 0.3s; cursor: pointer; }
    .blog-card:hover { transform: scale(1.02); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    .notif-badge { background-color: #ff4b4b; color: white; padding: 2px 8px; border-radius: 50%; font-size: 0.8rem; vertical-align: top; margin-left: 5px; }
    .sec-header { color: #2c3e50; font-weight: 600; border-bottom: 2px solid #3498db; padding-bottom: 5px; margin-bottom: 15px; margin-top: 20px;}
    a { text-decoration: none; color: inherit; }
    </style>
""", unsafe_allow_html=True)

# --- DUMMY DATA FOR CASCADING DROPDOWNS ---
HOSPITAL_DATA = {
    "Delhi NCR": {
        "Max Super Speciality": ["Dr. A. Gupta (Orthopedics)", "Dr. V. Sharma (Cardiology)"],
        "Fortis Escorts": ["Dr. S. Mehta (Cardiology)", "Dr. R. Singh (General Surgery)"]
    },
    "Mumbai": {
        "Apollo Navi Mumbai": ["Dr. K. Desai (Neurology)", "Dr. P. Patil (Orthopedics)"],
        "Hinduja Hospital": ["Dr. L. Joshi (Pediatrics)"]
    },
    "Bangalore": {
        "Manipal Hospital": ["Dr. N. Reddy (Orthopedics)"],
        "Narayana Health": ["Dr. M. Rao (Cardiac Surgeon)"]
    }
}

# --- SESSION STATE INITIALIZATION ---
if "logged_in_user" not in st.session_state: st.session_state.logged_in_user = "Patient App (Rahul)"
if "appointments" not in st.session_state: st.session_state.appointments = []
# Vault holds records: dict with id, hospital, doctor, date, files, summary_status
if "vault_records" not in st.session_state: 
    st.session_state.vault_records = [
        {"id": "1", "hospital": "Apollo Greams Road", "doctor": "Dr. Raj", "date": "2023-10-12", "files": ["MRI_Report.pdf"], "summary": True}
    ]
if "chat_history" not in st.session_state: st.session_state.chat_history = [{"role": "assistant", "content": "👋 Hi Rahul! I am your AI Assistant. How can I help you with your health or insurance today?"}]
if "creating_record" not in st.session_state: st.session_state.creating_record = False

# ==========================================
# SIDEBAR / LOGIN MANAGER
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=50)
    st.title("HealthConnect")
    st.info(f"🟢 **Logged in as:** \n\n{st.session_state.logged_in_user}")
    with st.expander("🔄 Switch Persona / Logout"):
        new_user = st.radio("Select Persona:", ["Patient App (Rahul)", "Doctor Portal (Dr. Gupta)", "TPA Dashboard (Insurer)"])
        if st.button("Switch"):
            st.session_state.logged_in_user = new_user
            st.rerun()

# ==========================================
# PATIENT APP
# ==========================================
def render_patient_app():
    # Header
    col1, col2 = st.columns([4, 1])
    with col1: st.markdown("<h2>👋 Good Morning, Rahul!</h2>", unsafe_allow_html=True)
    with col2: st.markdown("<div style='text-align: right; padding-top: 15px;'>🔔 Notifications <span class='notif-badge'>2</span></div>", unsafe_allow_html=True)

    # Tabs
    pt_tab1, pt_tab2, pt_tab3 = st.tabs(["🏠 Home & Booking", "📂 Medical Vault (AI Records)", "🛡️ Contextual AI Chat"])

    # ---------------------------------------------------------
    # TAB 1: INTERACTIVE BOOKING & BLOGS
    # ---------------------------------------------------------
    with pt_tab1:
        c1, c2 = st.columns([1, 2], gap="large")
        
        # EXTERNAL LINKS FOR BLOGS
        with c1:
            st.markdown("<div class='sec-header'>📰 Daily Health Tips</div>", unsafe_allow_html=True)
            st.markdown("""
                <a href='https://www.webmd.com/osteoarthritis/knee-replacement-surgery' target='_blank'>
                    <div class='blog-card'>
                        <b>🦴 Preparing for Knee Surgery</b><br>
                        <small>Click to read top tips for a faster recovery.</small>
                    </div>
                </a>
                <a href='https://www.healthline.com/nutrition/heart-healthy-foods' target='_blank'>
                    <div class='blog-card'>
                        <b>🥗 Heart-Healthy Diets</b><br>
                        <small>Click to discover 5 foods to reduce cholesterol.</small>
                    </div>
                </a>
            """, unsafe_allow_html=True)

        # CASCADING BOOKING ENGINE
        with c2:
            st.markdown("<div class='sec-header'>📅 Book a New Appointment</div>", unsafe_allow_html=True)
            with st.container(border=True):
                # Interactive Cascading Logic
                b_col1, b_col2 = st.columns(2)
                selected_city = b_col1.selectbox("1. Select City", list(HOSPITAL_DATA.keys()))
                
                # Hospital list depends on City
                hospitals_in_city = list(HOSPITAL_DATA[selected_city].keys())
                selected_hospital = b_col2.selectbox("2. Select Hospital", hospitals_in_city)
                
                # Doctor list depends on Hospital
                b_col3, b_col4 = st.columns(2)
                doctors_in_hospital = HOSPITAL_DATA[selected_city][selected_hospital]
                selected_doctor = b_col3.selectbox("3. Select Specialist", doctors_in_hospital)
                
                case_link = b_col4.selectbox("4. Link Medical History?", ["🆕 Create New Clinical Case", "🔗 Case #882: Chronic Knee Pain"])
                
                b_col5, b_col6 = st.columns(2)
                apt_date = b_col5.date_input("5. Select Date", min_value=date.today())
                slot = b_col6.selectbox("6. Available Slots", ["10:00 AM", "11:30 AM", "02:00 PM"])
                
                if st.button("🚀 Confirm Booking", type="primary", use_container_width=True):
                    st.success(f"✅ Appointment booked with {selected_doctor} at {selected_hospital} on {apt_date}.")

    # ---------------------------------------------------------
    # TAB 2: MEDICAL VAULT (RECORD CREATION & OCR)
    # ---------------------------------------------------------
    with pt_tab2:
        st.markdown("<div class='sec-header'>📂 Manage Clinical Records</div>", unsafe_allow_html=True)
        st.write("Create a record envelope for a visit, then upload prescriptions/bills to generate an AI summary.")
        
        # Toggle Record Creation Form
        if st.button("➕ Create New Medical Record Folder"):
            st.session_state.creating_record = not st.session_state.creating_record

        if st.session_state.creating_record:
            with st.container(border=True):
                st.subheader("New Visit Details")
                v_col1, v_col2, v_col3 = st.columns(3)
                new_hosp = v_col1.text_input("Hospital / Clinic Name", "Max Super Speciality")
                new_doc = v_col2.text_input("Treating Doctor", "Dr. A. Gupta")
                new_date = v_col3.date_input("Date of Visit")
                if st.button("Save Folder"):
                    new_record = {"id": str(uuid.uuid4()), "hospital": new_hosp, "doctor": new_doc, "date": str(new_date), "files": [], "summary": False}
                    st.session_state.vault_records.insert(0, new_record) # Add to top
                    st.session_state.creating_record = False
                    st.rerun()

        st.markdown("### 🗂️ Your Record Vault")
        # Display all records
        for i, record in enumerate(st.session_state.vault_records):
            with st.expander(f"🏥 {record['hospital']} | 🩺 {record['doctor']} | 📅 {record['date']}", expanded=(i==0)):
                col_up, col_sum = st.columns([1, 1.5], gap="large")
                
                with col_up:
                    st.write("**Uploaded Documents:**")
                    if record['files']:
                        for f in record['files']: st.markdown(f"📄 `{f}`")
                    else:
                        st.caption("No files uploaded yet.")
                    
                    # Upload action specific to this folder
                    uploaded_file = st.file_uploader("Upload Rx, Bill, or Lab Report", key=f"up_{record['id']}")
                    if uploaded_file and st.button("Process File", key=f"btn_{record['id']}"):
                        with st.spinner("Uploading and running AI OCR..."):
                            time.sleep(2)
                            record['files'].append(uploaded_file.name)
                            st.rerun()

                with col_sum:
                    st.write("**🧠 AI Clinical Summary:**")
                    if record['summary']:
                        st.markdown("""
                        <div class='stCard' style='border-left: 4px solid #2ecc71; padding: 10px; margin-top:0;'>
                            <b>Extracted Data:</b><br>
                            • <b>Diagnosis:</b> Grade 3 Osteoarthritis<br>
                            • <b>Rx:</b> Paracetamol 500mg, Calcium<br>
                            • <b>Code:</b> M19.011 (Auto-tagged)
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        if record['files']:
                            if st.button("✨ Generate AI Summary", type="primary", key=f"sum_{record['id']}"):
                                with st.spinner("Agents extracting entities..."):
                                    time.sleep(2)
                                    record['summary'] = True
                                    st.rerun()
                        else:
                            st.info("Upload a document first to generate an AI summary.")

    # ---------------------------------------------------------
    # TAB 3: CONTEXT-AWARE INSURANCE CHAT
    # ---------------------------------------------------------
    with pt_tab3:
        st.markdown("<div class='sec-header'>🛡️ AI Insurance Concierge</div>", unsafe_allow_html=True)
        
        chat_col1, chat_col2 = st.columns([1, 2], gap="large")
        
        with chat_col1:
            st.subheader("⚙️ Chat Context")
            chat_mode = st.radio("What do you want to discuss?", ["General Policy Inquiry", "Case-Specific Pre-Auth"])
            
            if chat_mode == "Case-Specific Pre-Auth":
                st.markdown("---")
                st.write("**Active Case Context:**")
                st.selectbox("Select Insurer", ["Star Health (Policy: SH-8821)"])
                st.selectbox("Select Medical Case", ["Case #882: Knee Pain (Apollo Greams)"])
                st.info("💡 *The AI now has context of your specific doctor, diagnosis, and policy limits.*")
            else:
                st.info("💡 *The AI will answer general questions based on your overall policy PDF.*")

        with chat_col2:
            st.subheader("💬 Live Chat")
            chat_container = st.container(height=350, border=True)
            with chat_container:
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]): st.markdown(msg["content"])
            
            # Interactive chat input
            user_input = st.chat_input("Ask about waiting periods, room rent, copays...")
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with chat_container:
                    with st.chat_message("user"): st.markdown(user_input)
                    with st.chat_message("assistant"):
                        # Dummy contextual response
                        if chat_mode == "Case-Specific Pre-Auth" and "knee" in user_input.lower():
                            ai_msg = "Looking at your case (#882) at Apollo Greams Road: Total Knee Replacement **is covered**. Your Star Health policy covers room rent up to ₹5,000/day. However, surgical consumables (approx ₹8,000) will be out-of-pocket."
                        else:
                            ai_msg = "Under your Star Health policy, you have a Sum Insured of ₹5,00,000. General waiting periods (2 years) have been cleared."
                        
                        st.markdown(ai_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_msg})

# ==========================================
# ROUTER
# ==========================================
if st.session_state.logged_in_user == "Patient App (Rahul)":
    render_patient_app()
else:
    st.title(st.session_state.logged_in_user)
    st.write("Next persona UI coming soon...")
