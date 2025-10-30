import streamlit as st
import pandas as pd
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="VisionQuest",
    page_icon="👁️",
    layout="wide"
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
</style>
""", unsafe_allow_html=True)

# App header
st.markdown('<h1 class="main-header">VisionQuest</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Binocular Vision & Vergence Training System</p>', unsafe_allow_html=True)

# Initialize session state
if 'sessions' not in st.session_state:
    st.session_state.sessions = []

# Sidebar
with st.sidebar:
    st.header("Patient Information")
    patient_name = st.text_input("Patient Name", "John Doe")
    patient_age = st.text_input("Age", "8")
    condition = st.selectbox("Condition", ["Amblyopia", "Strabismus", "Convergence Insufficiency"])
    
    st.header("Quick Actions")
    if st.button("New Training Session"):
        st.session_state.sessions.append({
            'date': datetime.now(),
            'exercise': 'Vergence',
            'duration': 5,
            'score': random.randint(60, 95)
        })
        st.success("New session added!")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Training Application")
    
    # Simple exercise selector
    exercise = st.selectbox("Select Exercise", 
                           ["Vergence Training", "Fusion Training", "Jump Vergence", "Smooth Pursuit"])
    
    # Training parameters
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        speed = st.select_slider("Speed", options=["Slow", "Medium", "Fast"], value="Medium")
    with col_b:
        difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard"], value="Medium")
    with col_c:
        duration = st.slider("Duration (min)", 1, 15, 5)
    
    # Start training button
    if st.button("Start Training Session", type="primary"):
        st.info(f"Starting {exercise} at {speed} speed for {duration} minutes")
        
        # Simulate training session
        new_session = {
            'date': datetime.now(),
            'exercise': exercise,
            'duration': duration,
            'score': random.randint(60, 95),
            'speed': speed,
            'difficulty': difficulty
        }
        st.session_state.sessions.append(new_session)
        st.success("Training session completed!")

with col2:
    st.header("Session History")
    
    if st.session_state.sessions:
        for i, session in enumerate(st.session_state.sessions[-5:]):
            with st.container():
                st.write(f"**{session['exercise']}**")
                st.write(f"Date: {session['date'].strftime('%Y-%m-%d %H:%M')}")
                st.write(f"Score: {session['score']}%")
                st.write(f"Duration: {session['duration']}min")
                st.divider()
    else:
        st.info("No sessions recorded yet")

# Progress section
st.header("Progress Analytics")

if st.session_state.sessions:
    # Convert to DataFrame
    sessions_df = pd.DataFrame(st.session_state.sessions)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sessions", len(st.session_state.sessions))
    with col2:
        avg_score = sessions_df['score'].mean()
        st.metric("Average Score", f"{avg_score:.1f}%")
    with col3:
        total_duration = sessions_df['duration'].sum()
        st.metric("Total Training Time", f"{total_duration} min")
    with col4:
        best_score = sessions_df['score'].max()
        st.metric("Best Score", f"{best_score}%")
    
    # Simple progress chart
    st.subheader("Session Scores Over Time")
    chart_data = sessions_df[['date', 'score']].set_index('date')
    st.line_chart(chart_data)
    
else:
    st.info("Start training sessions to see progress analytics")

# Footer
st.markdown("---")
st.markdown("**VisionQuest** - Binocular Vision Training System")