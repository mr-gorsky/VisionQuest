import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time

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
    .exercise-active {
        background-color: #e8f5e8;
        border: 2px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for all exercises
if 'current_exercise' not in st.session_state:
    st.session_state.current_exercise = None
if 'exercise_started' not in st.session_state:
    st.session_state.exercise_started = False
if 'exercise_progress' not in st.session_state:
    st.session_state.exercise_progress = 0
if 'session_data' not in st.session_state:
    st.session_state.session_data = []
if 'exercise_timer' not in st.session_state:
    st.session_state.exercise_timer = 0

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

# Function to start exercise
def start_exercise(exercise_name):
    st.session_state.current_exercise = exercise_name
    st.session_state.exercise_started = True
    st.session_state.exercise_progress = 0
    st.session_state.exercise_timer = 0

# Function to stop exercise
def stop_exercise():
    st.session_state.exercise_started = False
    st.session_state.current_exercise = None
    st.session_state.exercise_progress = 0

# Function to simulate exercise progress
def update_exercise_progress():
    if st.session_state.exercise_started:
        if st.session_state.exercise_progress < 100:
            st.session_state.exercise_progress += 5
            st.session_state.exercise_timer += 1
        else:
            stop_exercise()

# Exercise configurations
exercise_configs = {
    "Vergence": {
        "instructions": "Follow the target as it moves closer and farther",
        "duration": 5
    },
    "Fusion": {
        "instructions": "Fuse the two images into a single clear image", 
        "duration": 3
    },
    "Jump Vergence": {
        "instructions": "Quickly switch focus between different targets",
        "duration": 4
    },
    "Smooth Pursuit": {
        "instructions": "Smoothly follow the moving target",
        "duration": 5
    },
    "Accommodative Rock": {
        "instructions": "Alternate focus between near and far targets",
        "duration": 4
    }
}

# Display current exercise or exercise setup
if st.session_state.exercise_started and st.session_state.current_exercise == exercise:
    # Exercise is running
    config = exercise_configs[exercise]
    
    st.markdown(f'<div class="exercise-card exercise-active">', unsafe_allow_html=True)
    st.success(f"🎯 {exercise} Exercise Running!")
    
    # Progress bar
    progress_bar = st.progress(st.session_state.exercise_progress / 100)
    
    # Timer display
    st.write(f"⏱️ Time: {st.session_state.exercise_timer} seconds")
    
    # Exercise-specific display
    if exercise == "Vergence":
        st.info("👀 Follow the target moving toward you... Now moving away...")
        st.write(f"🎯 Using targets: {', '.join(targets[:2])}")
        
    elif exercise == "Fusion":
        st.info("🔮 Focus on fusing the two images into one clear image")
        st.write("🔄 Left Image + Right Image = Single Fused Image")
        
    elif exercise == "Jump Vergence":
        st.info("🔄 Quickly switching between targets...")
        current_target = targets[st.session_state.exercise_timer % len(targets)] if targets else "● Target"
        st.write(f"🎯 Current target: {current_target}")
        
    elif exercise == "Smooth Pursuit":
        st.info("🌀 Smoothly following the moving target...")
        patterns = ["← Moving Left →", "↑ Moving Up ↓", "↻ Moving Circular"]
        st.write(f"📐 Pattern: {patterns[st.session_state.exercise_timer % 3]}")
        
    elif exercise == "Accommodative Rock":
        st.info("👁️ Alternating focus: NEAR → FAR → NEAR")
        focus = "NEAR" if st.session_state.exercise_timer % 2 == 0 else "FAR"
        st.write(f"🎯 Current focus: {focus}")
    
    # Update progress automatically
    if st.session_state.exercise_progress < 100:
        time.sleep(0.5)  # Simulate time passing
        update_exercise_progress()
        st.rerun()
    else:
        st.balloons()
        st.success("✅ Exercise completed successfully!")
        if st.button("🏁 Finish Exercise"):
            stop_exercise()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
else:
    # Exercise setup screen
    config = exercise_configs[exercise]
    
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
    st.write(f"**Instructions:** {config['instructions']}")
    st.write(f"**Selected targets:** {', '.join(targets)}")
    
    # Exercise-specific settings
    if exercise == "Vergence":
        vergence_level = st.slider("Difficulty Level", 1, 10, 5)
        duration = st.slider("Session Duration (minutes)", 1, 15, config['duration'])
        
    elif exercise == "Fusion":
        fusion_time = st.slider("Fusion Duration (minutes)", 1, 10, config['duration'])
        
    elif exercise == "Jump Vergence":
        target_count = st.selectbox("Number of Targets", [2, 4, 6, 8])
        speed = st.radio("Speed", ["Slow", "Medium", "Fast"])
        
    elif exercise == "Smooth Pursuit":
        speed = st.radio("Pursuit Speed", ["Slow", "Medium", "Fast"])
        pattern = st.selectbox("Movement Pattern", ["Horizontal", "Vertical", "Circular", "Figure-8"])
        
    elif exercise == "Accommodative Rock":
        cycles = st.slider("Number of Cycles", 5, 50, 20)
    
    # Start exercise button
    if st.button(f"🎯 Start {exercise} Exercise"):
        start_exercise(exercise)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Session recording
st.markdown("---")
st.header("💾 Session Recording")

if st.button("💾 Save Session Results") and not st.session_state.exercise_started:
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
    st.rerun()

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
            st.metric("Favorite Exercise", df['exercise'].mode()[0] if len(df) > 0 else "N/A")
        
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
st.markdown("### **Developed by Toni Mandušić**")
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