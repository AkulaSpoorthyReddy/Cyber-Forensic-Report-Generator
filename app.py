import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
from forensic_engine import ForensicBrain
from report_gen import ForensicReport

st.set_page_config(page_title="Forensic Audit Terminal", layout="wide")

# Theme styling configuration
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    .stApp { background-color: #0A1128; color: #E0E1DD; font-family: 'JetBrains Mono', monospace; }
    
    [data-testid="stSidebar"] { background-color: #001F3F; border-right: 1px solid #415A77; }
    
    .shield-hex {
        width: 45px; height: 55px; background: #E9C46A;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        display: flex; align-items: center; justify-content: center; margin-bottom: 10px;
    }
    .shield-inner { width: 32px; height: 42px; background: #0A1128; clip-path: inherit; }
    
    /* Native element overrides to match your aesthetic */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #1B263B !important; 
        border: 1px solid #415A77 !important;
        border-radius: 4px !important;
    }
    .phase-indicator {
        background-color: #4ECCA3; color: #0A1128; font-weight: bold;
        padding: 6px 12px; border-radius: 2px; font-size: 0.85rem; display: inline-block;
        margin-bottom: 15px; letter-spacing: 0.05em;
    }
    .risk-badge { padding: 5px 15px; border-radius: 2px; font-weight: bold; font-size: 0.8rem; }
    h1, h2, h3, h4 { color: #F8FAFC !important; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# Persistent State Management for Local Authentication Accounts
if 'user_db' not in st.session_state: 
    st.session_state.user_db = {"admin": "rootpassword"} 
if 'auth_active' not in st.session_state: 
    st.session_state.auth_active = False
if 'current_operator' not in st.session_state: 
    st.session_state.current_operator = ""
if 'step' not in st.session_state: 
    st.session_state.step = 1

# --- SIDEBAR NODE DIAGNOSTICS ---
with st.sidebar:
    st.markdown('<div class="shield-hex"><div class="shield-inner"></div></div>', unsafe_allow_html=True)
    st.subheader("NODE MANAGEMENT SYSTEM")
    st.caption("CORE INTERACTION ENGINE: CHROMA VECTOR SYSTEM")
    st.caption("ENCRYPTION MODEL: KERNEL SHA-256")
    st.divider()
    if st.session_state.auth_active:
        st.write(f"OPERATOR LOGGED IN: **{st.session_state.current_operator.upper()}**")
        if st.button("TERMINATE SESSION RUN"):
            st.session_state.auth_active = False
            st.session_state.current_operator = ""
            st.session_state.step = 1
            st.rerun()
    else:
        st.write("NODE STATUS: LOCKOUT / UNAUTHENTICATED")

# --- AUTHENTICATION INTERFACE LAYER (SIGN-IN / SIGN-UP) ---
if not st.session_state.auth_active:
    st.title("CYBER-FORENSIC REQUISITION ENGINE OPERATIONS")
    _, col, _ = st.columns([1, 1.5, 1])
    
    with col:
        with st.container(border=True):
            auth_mode = st.radio("GATEWAY ACCESS METHOD", ["SIGN-IN EXISTENT GATEWAY", "SIGN-UP NEW NODE CREDENTIALS"], horizontal=True)
            st.write("---")
            
            if auth_mode == "SIGN-IN EXISTENT GATEWAY":
                st.subheader("OPERATOR VERIFICATION PORTAL")
                login_id = st.text_input("OPERATOR IDENTITY CODE", key="login_id_input")
                login_pw = st.text_input("SECURITY ACCESS PASSKEY", type="password", key="login_pw_input")
                
                if st.button("EXECUTE VERIFICATION ROUTINE"):
                    if login_id in st.session_state.user_db and st.session_state.user_db[login_id] == login_pw:
                        st.session_state.auth_active = True
                        st.session_state.current_operator = login_id
                        st.success("Verification routine complete. Redirecting...")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Access Refused: Invalid credentials match recorded on registry.")
                        
            else:
                st.subheader("PROVISION NEW RUNTIME IDENTITY")
                reg_id = st.text_input("CREATE OPERATOR IDENTITY CODE", key="reg_id_input")
                reg_pw = st.text_input("GENERATE SECURITY ACCESS PASSKEY", type="password", key="reg_pw_input")
                reg_confirm = st.text_input("CONFIRM SECURITY ACCESS PASSKEY", type="password", key="reg_conf_input")
                
                if st.button("PROVISION AUTHENTICATION NODE"):
                    if not reg_id or not reg_pw:
                        st.error("Provisioning Error: Allocation segments cannot be empty.")
                    elif reg_pw != reg_confirm:
                        st.error("Provisioning Error: Validation matching array fault between keys.")
                    elif reg_id in st.session_state.user_db:
                        st.error("Provisioning Error: Specified ID token already allocated in system core.")
                    else:
                        st.session_state.user_db[reg_id] = reg_pw
                        st.session_state.auth_active = True
                        st.session_state.current_operator = reg_id
                        st.success("New operator token assigned completely! Logging into system space...")
                        time.sleep(0.6)
                        st.rerun()

# --- SECURE OPERATIONS DASHBOARD ---
else:
    st.title("CYBER-FORENSIC REQUISITION ENGINE OPERATIONS")

    # PHASE 1: ARTIFACT INGESTION
    if st.session_state.step == 1:
        st.markdown('<span class="phase-indicator">ACTIVE MONITOR: PHASE 01 (INGESTION MODULE)</span>', unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("<h3 style='margin-top:0;'>DATA ENTRY PIPELINE AND FILE IDENTIFICATION</h3>", unsafe_allow_html=True)
            
            up_file = st.file_uploader("DROP LOG DATASETS OR EVIDENCE DIRECTLY", type=['csv','txt','json'], label_visibility="collapsed")
            if up_file:
                if 'brain' not in st.session_state: st.session_state.brain = ForensicBrain()
                
                if up_file.name.endswith('.csv'): 
                    st.session_state.data = pd.read_csv(up_file)
                else: 
                    st.session_state.data = pd.DataFrame([{"raw": up_file.read().decode()}])
                
                st.session_state.f_hash = st.session_state.brain.get_integrity_hash(st.session_state.data)
                st.code(f"COMPUTED REQUISITION SIGNATURE IDENTIFIER SHA-256: {st.session_state.f_hash}", language="bash")
                
                if st.button("EXECUTE NEURAL SIGNATURE MATCHING ENGINE"):
                    st.session_state.results = st.session_state.brain.find_similar_cases_live(st.session_state.data)
                    st.session_state.step = 2
                    st.rerun()

    # PHASE 2: DIAGNOSTIC CALCULATION
    elif st.session_state.step == 2:
        st.markdown('<span class="phase-indicator">✓ PHASE 01 PIPELINE VERIFIED & FINISHED</span>', unsafe_allow_html=True)
        st.markdown('<span class="phase-indicator" style="background-color:#38BDF8;">ACTIVE MONITOR: PHASE 02 (DIAGNOSTIC CALCULATION)</span>', unsafe_allow_html=True)
        st.markdown("### COMPILING ANALYTICAL NODE RESULTS MATRIX")
        
        res = st.session_state.results
        c1, c2 = st.columns([1.4, 1])
        with c1:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = res['certainty'],
                title = {'text': "CONFIDENCE PROFILE RATIO SCORE (%)", 'font': {'color': '#E9C46A', 'size': 13, 'family':'JetBrains Mono'}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickcolor': '#E0E1DD'}, 
                    'bar': {'color': res['risk_color']}, 
                    'bgcolor': "#0D1B2A",
                    'steps': [{'range': [0, 100], 'line': {'color': '#415A77', 'width': 1}}]
                }
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#E0E1DD', height=330)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            with st.container(border=True):
                st.markdown(f"""
                <h4 style="color:#E9C46A; margin-top:0; letter-spacing:0.05em;">DIAGNOSTIC METRICS BLOCK</h4>
                <p><b>ASSIGNED CASE NUM:</b> {res['case_no']}</p>
                <p><b>GENERATED DATE:</b> {res['generated_date']}</p>
                <p><b>HEURISTIC THREAT TYPE:</b> {res['category']}</p>
                <p><b>CRITICALITY EVAL:</b> <span class="risk-badge" style="background:{res['risk_color']}; color:#0A1128;">{res['risk']}</span></p>
                <hr style="border-color:#415A77">
                <p style="font-size:0.8rem; line-height:1.4;"><b>SUMMARY TIMELINE FINDINGS:</b><br>{res['summary']}</p>
                <p style="font-size:0.8rem; line-height:1.4;"><b>MODUS PROFILE ANALYSIS:</b><br>{res['modus']}</p>
                """, unsafe_allow_html=True)

        if st.button("FINALIZE COMPILING ENCRYPTED DOSSIER"):
            p_bar = st.progress(0)
            txt_slot = st.empty()
            
            pipeline_steps = [
                "Initializing System State Detection Formats...",
                "Running Comparative Linear Array Cross-Checks...",
                "Assembling Structured Table Arrays...",
                "Encoding Report Metadata Accents and Themes..."
            ]
            
            for index, step_msg in enumerate(pipeline_steps):
                txt_slot.code(f"[SYS_RUN] -> {step_msg}", language="bash")
                p_bar.progress((index + 1) * 25)
                time.sleep(0.5)
                
            engine = ForensicReport()
            st.session_state.pdf_report = engine.generate_full_report(
                st.session_state.current_operator, res, st.session_state.f_hash
            )
            st.session_state.step = 3
            st.rerun()

    # PHASE 3: DOSSIER EXPORT AND DISPATCH
    elif st.session_state.step == 3:
        st.markdown('<span class="phase-indicator">✓ PHASE 01 PIPELINE VERIFIED & FINISHED</span>', unsafe_allow_html=True)
        st.markdown('<span class="phase-indicator">✓ PHASE 02 PROCESS DIAGNOSTICS COMPLETED</span>', unsafe_allow_html=True)
        st.markdown('<span class="phase-indicator" style="background-color:#A855F7;">ACTIVE MONITOR: PHASE 03 (DOSSIER DISPATCH)</span>', unsafe_allow_html=True)
        
        st.markdown("### ARCHIVE TRANSMISSION SECURED AND SEALED")
        st.info(f"Official Target Master Signature Physical Hash: {st.session_state.f_hash}")
        
        st.download_button(
            label="📥 DOWNLOAD FORMAL COMPENSATED PDF DOSSIER",
            data=st.session_state.pdf_report,
            file_name=f"Forensic_Engine_Dossier_{st.session_state.f_hash[:8]}.pdf",
            mime="application/pdf"
        )
        
        st.write("")
        if st.button("RESET SYSTEM TERMINAL FOR NEXT RUN"):
            st.session_state.step = 1
            st.rerun()