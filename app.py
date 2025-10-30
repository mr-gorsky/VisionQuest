import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import random
from fpdf import FPDF
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="VisionQuest",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4a6fa5;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #6b8cbc;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .session-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4a6fa5;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<h1 class="main-header">VisionQuest</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Binocular Vision & Vergence Training System</p>', unsafe_allow_html=True)

# Initialize session state
if 'sessions' not in st.session_state:
    st.session_state.sessions = []
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {
        'name': '',
        'age': '',
        'condition': '',
        'therapist': ''
    }

# Sidebar for patient information
with st.sidebar:
    st.header("Patient Information")
    
    st.session_state.patient_data['name'] = st.text_input("Patient Name", value=st.session_state.patient_data['name'])
    st.session_state.patient_data['age'] = st.text_input("Age", value=st.session_state.patient_data['age'])
    st.session_state.patient_data['condition'] = st.selectbox(
        "Condition",
        ["Amblyopia", "Strabismus", "Convergence Insufficiency", "Other Binocular Dysfunction"]
    )
    st.session_state.patient_data['therapist'] = st.text_input("Therapist", value=st.session_state.patient_data['therapist'])
    
    st.header("Quick Actions")
    if st.button("New Training Session"):
        st.session_state.sessions.append({
            'date': datetime.now(),
            'exercise': 'Vergence',
            'duration': 5,
            'score': random.randint(60, 95),
            'difficulty': 'Medium'
        })
        st.success("New session added!")
    
    if st.button("Clear All Sessions"):
        st.session_state.sessions = []
        st.warning("All sessions cleared!")

# Main content - Two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Training Application")
    
    # Embed the HTML application
    with open('visionquest.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    st.components.v1.html(html_content, height=600, scrolling=True)

with col2:
    st.header("Session Management")
    
    # Quick session setup
    with st.expander("Start New Session"):
        exercise_type = st.selectbox(
            "Exercise Type",
            ["Vergence", "Fusion", "Jump Vergence", "Smooth Pursuit"]
        )
        
        duration = st.slider("Duration (minutes)", 1, 15, 5)
        difficulty = st.select_slider(
            "Difficulty",
            options=["Very Easy", "Easy", "Medium", "Hard", "Very Hard"],
            value="Medium"
        )
        
        if st.button("Start Session", type="primary"):
            new_session = {
                'date': datetime.now(),
                'exercise': exercise_type,
                'duration': duration,
                'score': random.randint(60, 95),
                'difficulty': difficulty
            }
            st.session_state.sessions.append(new_session)
            st.success(f"Started {exercise_type} session!")

# Progress tracking section
st.header("Progress Tracking & Analytics")

if st.session_state.sessions:
    # Convert sessions to DataFrame for easier manipulation
    sessions_df = pd.DataFrame(st.session_state.sessions)
    
    # Display recent sessions
    st.subheader("Recent Sessions")
    for i, session in enumerate(st.session_state.sessions[-5:]):  # Show last 5 sessions
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**{session['exercise']}** - {session['date'].strftime('%Y-%m-%d %H:%M')}")
            with col2:
                st.write(f"Duration: {session['duration']}min")
            with col3:
                st.write(f"Score: {session['score']}%")
            with col4:
                st.write(f"Difficulty: {session['difficulty']}")
            st.divider()
    
    # Progress chart
    st.subheader("Progress Over Time")
    
    # Create sample progress data
    dates = [datetime.now() - timedelta(days=x) for x in range(14, 0, -1)]
    progress_data = {
        'Date': dates,
        'Vergence Score': [random.randint(60, 95) for _ in range(14)],
        'Fusion Score': [random.randint(55, 90) for _ in range(14)],
        'Jump Vergence Score': [random.randint(50, 85) for _ in range(14)]
    }
    progress_df = pd.DataFrame(progress_data)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    for column in progress_df.columns[1:]:
        ax.plot(progress_df['Date'], progress_df[column], marker='o', label=column)
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Score (%)')
    ax.set_title('Training Progress Over Time')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    st.pyplot(fig)

else:
    st.info("No sessions recorded yet. Start a training session to see progress analytics!")

# Report generation section
st.header("Reports & Export")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Generate Progress Report")
    
    if st.button("Generate PDF Report"):
        if st.session_state.sessions:
            # Create simple PDF report
            pdf = FPDF()
            pdf.add_page()
            
            # Title
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, "VisionQuest Progress Report", ln=True, align='C')
            pdf.ln(10)
            
            # Patient information
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Patient Information:", ln=True)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 10, f"Name: {st.session_state.patient_data['name']}", ln=True)
            pdf.cell(0, 10, f"Age: {st.session_state.patient_data['age']}", ln=True)
            pdf.cell(0, 10, f"Condition: {st.session_state.patient_data['condition']}", ln=True)
            pdf.cell(0, 10, f"Therapist: {st.session_state.patient_data['therapist']}", ln=True)
            pdf.ln(10)
            
            # Session summary
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Session Summary:", ln=True)
            pdf.set_font("Arial", '', 12)
            
            total_sessions = len(st.session_state.sessions)
            avg_score = sum(s['score'] for s in st.session_state.sessions) / total_sessions
            
            pdf.cell(0, 10, f"Total Sessions: {total_sessions}", ln=True)
            pdf.cell(0, 10, f"Average Score: {avg_score:.1f}%", ln=True)
            pdf.ln(10)
            
            # Save PDF to bytes buffer
            pdf_buffer = BytesIO()
            pdf.output(pdf_buffer)
            pdf_buffer.seek(0)
            
            # Create download link
            b64_pdf = base64.b64encode(pdf_buffer.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="visionquest_report.pdf">Download PDF Report</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            st.success("PDF report generated successfully!")
        else:
            st.warning("No sessions available to generate report.")

with col2:
    st.subheader("Export Data")
    
    if st.session_state.sessions:
        # Convert to DataFrame for export
        export_df = pd.DataFrame(st.session_state.sessions)
        
        # CSV export
        csv = export_df.to_csv(index=False)
        b64_csv = base64.b64encode(csv.encode()).decode()
        href_csv = f'<a href="data:file/csv;base64,{b64_csv}" download="visionquest_sessions.csv">Export to CSV</a>'
        st.markdown(href_csv, unsafe_allow_html=True)
        
        # Excel export
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            export_df.to_excel(writer, sheet_name='Sessions', index=False)
        excel_buffer.seek(0)
        b64_excel = base64.b64encode(excel_buffer.read()).decode()
        href_excel = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64_excel}" download="visionquest_sessions.xlsx">Export to Excel</a>'
        st.markdown(href_excel, unsafe_allow_html=True)
    else:
        st.info("No data available for export.")

# Footer
st.markdown("---")
st.markdown(
    "**VisionQuest** - Binocular Vision Training System | "
    "For orthoptists, optometrists, and patients with amblyopia and binocular dysfunctions"
)