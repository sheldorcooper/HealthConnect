import streamlit as st
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthConnect | Agentic TPA", layout="wide", page_icon="🏥")

# --- CUSTOM CSS FOR BETTER UI ---
st.markdown("""
    <style>
    .patient-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 20px;
    }
    .metric-value { font-size: 1.5rem; font-weight: bold; color: #1f77b4; }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
# This keeps memory of actions while the user clicks around
if "case_initiated" not in st.session_state:
    st.session_state.case_initiated = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "👋 Hi Rahul! I am your HealthConnect AI. Ask me anything about your Star Health policy coverage before you book your surgery."}
    ]

# --- SIDEBAR (Global Demo Settings) ---
with st.sidebar:
    st.title("⚙️ Demo Controls")
    app_mode = st.radio("Application Mode:", ["Sample Mode (Recruiter Safe)", "Live API Mode (Interview)"])
    st.markdown("---")
    st.markdown("**Current Patient:** Mr. Rahul Sharma")
    st.markdown("**Insurer:** Star Health (Policy: #SH-8821)")
    st.markdown("---")
    st.markdown("**Built by:** Rajatbhai Vaghela (Product Manager)")

# --- APP HEADER ---
st.title("🏥 HealthConnect")
st.markdown("### Eliminating the 8-hour discharge delay with Agentic AI.")

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📱 1. Patient App (Booking)", 
    "🩺 2. Doctor Desk", 
    "🤖 3. The Agentic Brain", 
    "✅ 4. TPA Officer"
])

# ==========================================
# TAB 1: PATIENT DISCOVERY & BOOKING
# ==========================================
with tab1:
    st.header("Step 1: Patient Discovery & Pre-Verification")
    st.write("Patients verify their policy via AI *before* admission, preventing surprises and saving hours of TPA queries later.")
    st.markdown("---")

    # Split into two columns: Left for Booking, Right for AI Chat
    col1, col2 = st.columns([1, 1.2], gap="large")

    # --- LEFT COLUMN: PATIENT PROFILE & BOOKING ---
    with col1:
        st.subheader("👤 Patient Profile")
        
        # HTML/CSS Card for visual appeal
        st.markdown("""
            <div class="patient-card">
                <h4>Rahul Sharma (Age: 58)</h4>
                <p><b>Policy:</b> Star Health Comprehensive Health Insurance<br>
                <b>Sum Insured:</b> ₹5,00,000<br>
                <b>Waiting Period:</b> Cleared (Active since 2018)</p>
            </div>
        """, unsafe_allow_html=True)

        st.subheader("🏥 Initiate New Case")
        hospital = st.selectbox("Select Hospital/Provider", ["Apollo Hospitals, Greams Road", "Fortis Healthcare", "Max Super Speciality"])
        surgery_type = st.selectbox("Planned Procedure", ["Total Knee Replacement (TKR)", "Cataract Surgery", "Cardiac Bypass"])
        date = st.date_input("Planned Admission Date")

        # Action Button
        if not st.session_state.case_initiated:
            if st.button("🚀 Initiate Case & Create Digital Avatar", use_container_width=True, type="primary"):
                with st.spinner("Creating Live Case File & Syncing Policy Data..."):
                    time.sleep(1.5) # Simulate processing
                    st.session_state.case_initiated = True
                    st.rerun()
        else:
            st.success("✅ Digital Case File Active! Data is now bridging to the Doctor's Desk.")
            st.info("👉 *Recruiter Note: The journey now moves to Tab 2 (Doctor Desk).*")

    # --- RIGHT COLUMN: RAG AI CHATBOT ---
    with col2:
        st.subheader("🤖 Policy Pre-Check AI (RAG)")
        st.write("Querying: `Star_Health_Policy_Document.pdf`")
        
        # Chat Interface Container
        chat_container = st.container(height=350, border=True)
        
        # Display Chat History
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # Suggested Questions (Recruiter Friendly)
        st.write("💡 **Suggested Queries (Click to test):**")
        s_col1, s_col2 = st.columns(2)
        
        # Logic for suggested buttons or manual text input
        user_input = None
        if s_col1.button("Is Knee Replacement covered?"):
            user_input = "Is Total Knee Replacement covered, and what is the room rent limit?"
        if s_col2.button("Are consumables covered?"):
            user_input = "Will the insurance pay for surgical consumables like gloves?"

        manual_input = st.chat_input("Or type your own question...")
        if manual_input:
            user_input = manual_input

        # Process the input
        if user_input:
            # Add user message to state
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # Display user message instantly
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(user_input)
                
                # Simulate AI Thinking & Responding
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    # Hardcoded "Sample Mode" responses based on keywords
                    if "consumables" in user_input.lower():
                        ai_response = "⚠️ **Warning:** Under Star Health Clause 5.1, non-medical consumables (e.g., gloves, masks, specific syringes) are **Not Payable**. You will need to pay for these out-of-pocket."
                    else:
                        ai_response = "🟢 **Yes!** Total Knee Replacement is fully covered. Since your Sum Insured is ₹5L, your **Room Rent limit is 1% (₹5,000/day)**. There are no active waiting periods for this procedure."
                    
                    # Typing effect
                    full_response = ""
                    for chunk in ai_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
            
            # Save AI response to state
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun()

# Placeholders for the other tabs so the app doesn't break
with tab2: st.write("Tab 2 UI coming soon...")
with tab3: st.write("Tab 3 UI coming soon...")
with tab4: st.write("Tab 4 UI coming soon...")