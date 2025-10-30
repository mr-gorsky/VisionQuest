import streamlit as st
import pandas as pd
from datetime import datetime
import random
import base64

# Page configuration
st.set_page_config(
    page_title="VisionQuest",
    page_icon="👁️",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0;
    }
    .disclaimer {
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 20px 0;
    }
    .exercise-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #dee2e6;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'vergence_started' not in st.session_state:
    st.session_state.vergence_started = False
if 'session_data' not in st.session_state:
    st.session_state.session_data = []

# Logo and Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-header">🔭 VisionQuest</h1>', unsafe_allow_html=True)
    st.markdown("### Binocular Vision & Vergence Training System")

# Disclaimer
with st.expander("⚠️ MEDICAL DISCLAIMER", expanded=True):
    st.markdown("""
    **Important:** This application is intended for use by qualified eye care professionals only. 
    - All measurements and exercises should be conducted under professional supervision
    - Results should be interpreted by licensed optometrists or orthoptists
    - This tool is not a substitute for professional medical diagnosis
    - Always verify measurements with standard clinical instruments
    """)

# Patient Information
st.header("👤 Patient Information")
col1, col2, col3 = st.columns(3)
with col1:
    patient_name = st.text_input("Patient Name", "John Doe")
with col2:
    patient_age = st.number_input("Age", min_value=3, max_value=100, value=8)
with col3:
    patient_type = st.selectbox("Patient Type", ["Child", "Adult"])

# Clinical Measurements
st.header("📏 Clinical Measurements")
col1, col2 = st.columns(2)
with col1:
    npc = st.number_input("Near Point of Convergence (cm)", 
                         min_value=0.0, max_value=20.0, value=6.5, step=0.1, format="%.2f")
with col2:
    npa = st.number_input("Near Point of Accommodation (cm)", 
                         min_value=0.0, max_value=30.0, value=8.5, step=0.1, format="%.2f")

# Target selection based on patient type
st.header("🎯 Target Selection")
if patient_type == "Child":
    targets = st.multiselect("Select Targets for Exercises", 
                           ["🚀 Rocket", "⚽ Football", "🐬 Dolphin", "🌟 Star", "🎈 Balloon", "🦋 Butterfly"],
                           default=["🚀 Rocket", "⚽ Football"])
else:
    targets = st.multiselect("Select Targets for Exercises",
                           ["● Circle", "▲ Triangle", "■ Square", "✚ Cross", "★ Star", "◆ Diamond"],
                           default=["● Circle", "▲ Triangle"])

# Training Exercises
st.header("💪 Training Exercises")
exercise = st.selectbox("Select Exercise", 
                       ["Vergence", "Fusion", "Jump Vergence", "Smooth Pursuit", "Accommodative Rock"])

# Exercise implementation
st.markdown("---")
st.subheader(f"🎮 {exercise} Training")

if exercise == "Vergence":
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
    st.write("**Instructions:** Follow the target as it moves closer and farther")
    st.write(f"**Selected targets:** {', '.join(targets)}")
    
    vergence_level = st.slider("Difficulty Level", 1, 10, 5)
    duration = st.slider("Session Duration (minutes)", 1, 15, 5)
    
    if st.button("🎯 Start Vergence Exercise"):
        st.session_state.vergence_started = True
        st.balloons()
        st.success(f"Vergence exercise started with {', '.join(targets)}!")
    
    if st.session_state.vergence_started:
        st.info("🎯 Follow the moving target! Keep both eyes focused.")
        progress_bar = st.progress(0)
        for i in range(100):
            progress_bar.progress(i + 1)
        st.session_state.vergence_started = False
        st.success("Exercise completed! Good job!")
    st.markdown('</div>', unsafe_allow_html=True)

elif exercise == "Fusion":
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
    st.write("**Instructions:** Fuse the two images into a single clear image")
    fusion_time = st.slider("Fusion Duration (seconds)", 10, 120, 30)
    
    if st.button("🔮 Start Fusion Exercise"):
        st.balloons()
        st.success(f"Fusion exercise started! Maintain fusion for {fusion_time} seconds")
        st.info("Keep both images clear and single!")
    st.markdown('</div>', unsafe_allow_html=True)

elif exercise == "Jump Vergence":
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
    st.write("**Instructions:** Quickly switch focus between different targets")
    target_count = st.selectbox("Number of Targets", [2, 4, 6, 8])
    speed = st.radio("Speed", ["Slow", "Medium", "Fast"])
    
    if st.button("🔄 Start Jump Vergence"):
        st.success(f"Jump vergence started with {target_count} targets at {speed.lower()} speed!")
        st.write(f"Targets: {', '.join(targets[:target_count])}")
    st.markdown('</div>', unsafe_allow_html=True)

elif exercise == "Smooth Pursuit":
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
    st.write("**Instructions:** Smoothly follow the moving target")
    speed = st.radio("Pursuit Speed", ["Slow", "Medium", "Fast"])
    pattern = st.selectbox("Movement Pattern", ["Horizontal", "Vertical", "Circular", "Figure-8"])
    
    if st.button("🌀 Start Smooth Pursuit"):
        st.success(f"Smooth pursuit started - {pattern} pattern at {speed.lower()} speed!")
    st.markdown('</div>', unsafe_allow_html=True)

elif exercise == "Accommodative Rock":
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
    st.write("**Instructions:** Alternate focus between near and far targets")
    cycles = st.slider("Number of Cycles", 5, 50, 20)
    
    if st.button("👁️ Start Accommodative Rock"):
        st.success(f"Accommodative rock started - {cycles} cycles!")
        st.info("Alternate focus: NEAR → FAR → NEAR")
    st.markdown('</div>', unsafe_allow_html=True)

# Session recording
if st.button("💾 Save Session Results"):
    session_data = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'patient': patient_name,
        'age': patient_age,
        'type': patient_type,
        'exercise': exercise,
        'npc_cm': npc,
        'npa_cm': npa,
        'score': random.randint(70, 95),
        'duration': random.randint(3, 10)
    }
    st.session_state.session_data.append(session_data)
    st.success("Session results saved successfully!")

# Progress Report
st.header("📊 Progress Reports")
if st.session_state.session_data:
    df = pd.DataFrame(st.session_state.session_data)
    st.dataframe(df)
    
    # Generate report
    if st.button("📈 Generate Progress Report"):
        st.subheader("Progress Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sessions", len(df))
            st.metric("Average Score", f"{df['score'].mean():.1f}%")
        with col2:
            st.metric("Current NPC", f"{npc} cm")
            st.metric("Current NPA", f"{npa} cm")
        with col3:
            st.metric("Favorite Exercise", df['exercise'].mode()[0])
            st.metric("Progress Trend", "📈 Improving" if len(df) > 1 and df['score'].iloc[-1] > df['score'].iloc[0] else "📊 Stable")
        
        # NPC/NPA progress
        if len(df) > 1:
            st.subheader("NPC/NPA Progress")
            st.write(f"Initial NPC: {df['npc_cm'].iloc[0]} cm → Current NPC: {npc} cm")
            st.write(f"Initial NPA: {df['npa_cm'].iloc[0]} cm → Current NPA: {npa} cm")
            
            improvement_npc = df['npc_cm'].iloc[0] - npc
            improvement_npa = df['npa_cm'].iloc[0] - npa
            
            if improvement_npc > 0:
                st.success(f"🎉 NPC Improvement: +{improvement_npc:.2f} cm")
            if improvement_npa > 0:
                st.success(f"🎉 NPA Improvement: +{improvement_npa:.2f} cm")
else:
    st.info("No session data available. Complete exercises and save results to generate reports.")

# Footer
st.markdown("---")
st.markdown("---")
st.markdown("### **Developed by Toni Mandusic**")
st.markdown("*Vision Therapy Professional Application*")
st.markdown("© 2024 VisionQuest - All rights reserved")

# Export functionality
if st.session_state.session_data:
    st.sidebar.header("📤 Export Data")
    if st.sidebar.button("Export to CSV"):
        df = pd.DataFrame(st.session_state.session_data)
        csv = df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"visionquest_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )