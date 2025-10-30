import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time
import math
import base64

# Page configuration
st.set_page_config(
    page_title="VisionQuest",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling and compact layout
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.2rem;
        padding: 0;
    }
    .subheader {
        text-align: center;
        color: #666;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    .logo-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 0.5rem;
    }
    .logo-img {
        height: 80px;
        width: auto;
    }
    .title-text {
        text-align: center;
    }
    .exercise-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #dee2e6;
        margin: 5px 0;
        min-height: 200px;
        position: relative;
    }
    .exercise-active {
        background-color: #e8f5e8;
        border: 2px solid #28a745;
        height: 450px;
    }
    .exercise-setup {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        height: 100%;
    }
    .target {
        position: absolute;
        font-size: 2.5rem;
        transition: all 0.5s ease;
        user-select: none;
    }
    .vergence-target {
        font-size: 3.5rem;
        z-index: 10;
    }
    .fusion-left {
        left: 30%;
        transform: translateX(-50%);
    }
    .fusion-right {
        right: 30%;
        transform: translateX(50%);
    }
    .instructions {
        background-color: #d1ecf1;
        padding: 8px;
        border-radius: 5px;
        margin: 8px 0;
        font-size: 0.9rem;
    }
    .assessment-section {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin: 10px 0;
    }
    .status-info {
        position: absolute;
        bottom: 10px;
        left: 10px;
        font-size: 0.8rem;
        color: #666;
    }
    .demo-preview {
        background: linear-gradient(45deg, #e3f2fd, #bbdefb);
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        text-align: center;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_exercise' not in st.session_state:
    st.session_state.current_exercise = None
if 'exercise_started' not in st.session_state:
    st.session_state.exercise_started = False
if 'exercise_progress' not in st.session_state:
    st.session_state.exercise_progress = 0
if 'exercise_time_remaining' not in st.session_state:
    st.session_state.exercise_time_remaining = 300
if 'session_data' not in st.session_state:
    st.session_state.session_data = []
if 'assessment_data' not in st.session_state:
    st.session_state.assessment_data = {
        'therapist_accuracy': 75,
        'therapist_stamina': 70,
        'therapist_compliance': 85,
        'therapist_motivation': 80,
        'therapist_technique': 78,
        'therapist_focus': 72,
        'patient_clarity': 7,
        'patient_comfort': 6,
        'patient_difficulty': "Appropriate",
        'patient_completed': "Yes",
        'post_npc': 12.5,
        'post_npa': 15.5
    }

# CUSTOM HEADER WITH YOUR LOGO
st.markdown("""
<div class="logo-header">
    <img src="https://ibb.co/mVrFrfsv" 
         class="logo-img" 
         alt="VisionQuest Logo">
    <div class="title-text">
        <h1 class="main-header">VisionQuest</h1>
        <div class="subheader">BINOCULAR VISION & VERGENCE TRAINING</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Patient Information - ULTRA COMPACT
with st.container():
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        patient_name = st.text_input("Patient", "John Doe", key="patient_name", label_visibility="collapsed")
    with col2:
        patient_age = st.number_input("Age", min_value=3, max_value=100, value=8, key="patient_age", label_visibility="collapsed")
    with col3:
        patient_type = st.selectbox("Type", ["Child", "Adult"], key="patient_type", label_visibility="collapsed")
    with col4:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.session_data = []
            st.rerun()

# Clinical Measurements - FIXED NPC/NPC RANGES
with st.container():
    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
    with col1:
        npc = st.number_input("NPC (cm)", min_value=0.0, max_value=50.0, value=12.5, step=0.1, format="%.2f", key="npc")
    with col2:
        npa = st.number_input("NPA (cm)", min_value=0.0, max_value=50.0, value=15.5, step=0.1, format="%.2f", key="npa")
    with col3:
        if patient_type == "Child":
            targets = st.multiselect("Targets", 
                                   ["🚀 Rocket", "⚽ Football", "🐬 Dolphin", "🌟 Star", "🎈 Balloon", "🦋 Butterfly"],
                                   default=["🚀 Rocket", "⚽ Football"], key="targets_child")
            current_targets = ["🚀", "⚽", "🐬", "🌟", "🎈", "🦋"]
        else:
            targets = st.multiselect("Targets",
                                   ["● Circle", "▲ Triangle", "■ Square", "✚ Cross", "★ Star", "◆ Diamond"],
                                   default=["● Circle", "▲ Triangle"], key="targets_adult")
            current_targets = ["●", "▲", "■", "✚", "★", "◆"]
    with col4:
        exercise = st.selectbox("Exercise", 
                               ["Vergence", "Fusion", "Jump Vergence", "Smooth Pursuit", "Accommodative Rock"],
                               key="exercise_select")

# MAIN EXERCISE AREA
st.markdown("---")
st.subheader(f"🎯 {exercise} Exercise")

def start_exercise(exercise_name):
    st.session_state.current_exercise = exercise_name
    st.session_state.exercise_started = True
    st.session_state.exercise_progress = 0
    st.session_state.exercise_time_remaining = 300

def stop_exercise():
    st.session_state.exercise_started = False
    st.session_state.current_exercise = None

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

# Display exercise
if st.session_state.exercise_started and st.session_state.current_exercise == exercise:
    # Exercise is running - KORISTI VISOKI CONTAINER
    st.markdown(f'<div class="exercise-container exercise-active">', unsafe_allow_html=True)
    
    # Compact progress and timer
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        progress_bar = st.progress(st.session_state.exercise_progress / 100)
    with col2:
        st.metric("Time", format_time(st.session_state.exercise_time_remaining))
    with col3:
        if st.button("⏹️ Stop", use_container_width=True):
            stop_exercise()
            st.rerun()
    
    # Exercise-specific visual display
    display_height = "320px"
    
    if exercise == "Vergence":
        st.markdown('<div class="instructions">Follow the target moving closer/farther</div>', unsafe_allow_html=True)
        
        target_size = 50 + (50 * math.sin(time.time() * 0.5))
        target_pos = 50 + (40 * math.sin(time.time() * 0.3))
        
        st.markdown(f"""
        <div style="position: relative; height: {display_height}; background: linear-gradient(45deg, #e3f2fd, #bbdefb); border-radius: 10px;">
            <div class="target vergence-target" style="top: 45%; left: {target_pos}%; font-size: {target_size}px;">
                {current_targets[0]}
            </div>
            <div class="status-info">
                Depth: {'NEAR' if target_size > 70 else 'FAR'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Fusion":
        st.markdown('<div class="instructions">Fuse two images into one clear image</div>', unsafe_allow_html=True)
        
        fusion_offset = 20 + (15 * math.sin(time.time() * 0.2))
        
        st.markdown(f"""
        <div style="position: relative; height: {display_height}; background: linear-gradient(45deg, #fff3e0, #ffe0b2); border-radius: 10px;">
            <div class="target fusion-left" style="top: 45%; left: {50 - fusion_offset}%; color: red;">
                {current_targets[0]}
            </div>
            <div class="target fusion-right" style="top: 45%; left: {50 + fusion_offset}%; color: blue;">
                {current_targets[1] if len(current_targets) > 1 else current_targets[0]}
            </div>
            <div class="status-info">
                Fusion: {'EASY' if fusion_offset < 25 else 'CHALLENGING'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Jump Vergence":
        st.markdown('<div class="instructions">Quickly switch focus between targets</div>', unsafe_allow_html=True)
        
        jump_interval = 3
        current_target_idx = int((time.time() % (len(current_targets) * jump_interval)) / jump_interval)
        positions = [(25, 25), (75, 25), (25, 75), (75, 75), (50, 50), (10, 50)]
        
        st.markdown(f"""
        <div style="position: relative; height: {display_height}; background: linear-gradient(45deg, #e8f5e8, #c8e6c9); border-radius: 10px;">
            {''.join([f'<div class="target" style="top: {pos[1]}%; left: {pos[0]}%; opacity: {0.3 if i != current_target_idx else 1.0};">{target}</div>' 
                     for i, (target, pos) in enumerate(zip(current_targets, positions))])}
            <div class="status-info">
                Current: {current_targets[current_target_idx]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Smooth Pursuit":
        st.markdown('<div class="instructions">Smoothly follow the moving target</div>', unsafe_allow_html=True)
        
        angle = time.time() * 0.5
        radius = 35
        x = 50 + radius * math.cos(angle)
        y = 50 + radius * math.sin(angle)
        
        st.markdown(f"""
        <div style="position: relative; height: {display_height}; background: linear-gradient(45deg, #f3e5f5, #e1bee7); border-radius: 10px;">
            <div class="target" style="top: {y}%; left: {x}%;">
                {current_targets[0]}
            </div>
            <div class="status-info">
                Pattern: Circular
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Accommodative Rock":
        st.markdown('<div class="instructions">Alternate focus between near and far</div>', unsafe_allow_html=True)
        
        rock_interval = 4
        is_near = int(time.time() % (rock_interval * 2)) < rock_interval
        
        st.markdown(f"""
        <div style="position: relative; height: {display_height}; background: linear-gradient(45deg, #fff8e1, #ffecb3); border-radius: 10px;">
            <div class="target" style="top: 45%; left: 30%; font-size: {'3.5rem' if is_near else '1.8rem'};">
                NEAR
            </div>
            <div class="target" style="top: 45%; left: 70%; font-size: {'1.8rem' if is_near else '3.5rem'};">
                FAR
            </div>
            <div class="status-info">
                Focus: {'NEAR - Look at left target' if is_near else 'FAR - Look at right target'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Update timer and progress
    if st.session_state.exercise_time_remaining > 0:
        time.sleep(1)
        st.session_state.exercise_time_remaining -= 1
        st.session_state.exercise_progress = (300 - st.session_state.exercise_time_remaining) / 3
        st.rerun()
    else:
        st.balloons()
        stop_exercise()
        st.rerun()
        
else:
    # Exercise setup screen - KORISTI NISKI CONTAINER
    st.markdown('<div class="exercise-container">', unsafe_allow_html=True)
    st.markdown('<div class="exercise-setup">', unsafe_allow_html=True)
    
    instructions = {
        "Vergence": "Follow target moving in depth to improve convergence and divergence skills",
        "Fusion": "Fuse separate images from each eye into a single clear image", 
        "Jump Vergence": "Rapidly switch focus between different targets at various distances",
        "Smooth Pursuit": "Smoothly track moving targets to improve eye tracking accuracy",
        "Accommodative Rock": "Alternate focus between near and far targets to improve accommodation"
    }
    
    st.write(f"**{exercise}**")
    st.write(f"{instructions[exercise]}")
    
    # Demo preview
    st.markdown('<div class="demo-preview">', unsafe_allow_html=True)
    if exercise == "Vergence":
        st.write(f"Preview: {current_targets[0]} moving in depth")
    elif exercise == "Fusion":
        st.write(f"Preview: {current_targets[0]} + {current_targets[1]} fusion")
    elif exercise == "Jump Vergence":
        st.write(f"Preview: Multiple target switching")
    elif exercise == "Smooth Pursuit":
        st.write(f"Preview: {current_targets[0]} circular motion")
    elif exercise == "Accommodative Rock":
        st.write("Preview: NEAR ↔ FAR alternating")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write(f"**Duration:** 5 minutes | **Targets:** {', '.join(targets[:2])}")
    
    if st.button(f"🎯 Start {exercise} Exercise", type="primary", use_container_width=True):
        start_exercise(exercise)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# REAL ASSESSMENT SECTION
st.markdown("---")
st.header("🧑‍⚕️ Session Assessment")

with st.container():
    st.markdown('<div class="assessment-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Therapist Evaluation")
        st.session_state.assessment_data['therapist_accuracy'] = st.slider(
            "Accuracy of eye movements", 0, 100, st.session_state.assessment_data['therapist_accuracy'])
        st.session_state.assessment_data['therapist_stamina'] = st.slider(
            "Stamina/Endurance", 0, 100, st.session_state.assessment_data['therapist_stamina'])
        st.session_state.assessment_data['therapist_compliance'] = st.slider(
            "Exercise compliance", 0, 100, st.session_state.assessment_data['therapist_compliance'])
        st.session_state.assessment_data['therapist_motivation'] = st.slider(
            "Patient motivation", 0, 100, st.session_state.assessment_data['therapist_motivation'])
        st.session_state.assessment_data['therapist_technique'] = st.slider(
            "Proper technique", 0, 100, st.session_state.assessment_data['therapist_technique'])
        st.session_state.assessment_data['therapist_focus'] = st.slider(
            "Maintained focus", 0, 100, st.session_state.assessment_data['therapist_focus'])
    
    with col2:
        st.subheader("Patient Feedback & Measurements")
        st.session_state.assessment_data['patient_clarity'] = st.slider(
            "Image clarity (1-10)", 1, 10, st.session_state.assessment_data['patient_clarity'])
        st.session_state.assessment_data['patient_comfort'] = st.slider(
            "Comfort level (1-10)", 1, 10, st.session_state.assessment_data['patient_comfort'])
        st.session_state.assessment_data['patient_difficulty'] = st.selectbox(
            "Difficulty level", ["Too Easy", "Appropriate", "Challenging", "Too Difficult"],
            index=["Too Easy", "Appropriate", "Challenging", "Too Difficult"].index(st.session_state.assessment_data['patient_difficulty']))
        st.session_state.assessment_data['patient_completed'] = st.radio(
            "Exercise completion", ["Yes", "Partial", "No"],
            index=["Yes", "Partial", "No"].index(st.session_state.assessment_data['patient_completed']))
        
        st.session_state.assessment_data['post_npc'] = st.number_input(
            "Post-exercise NPC (cm)", min_value=0.0, max_value=50.0, 
            value=st.session_state.assessment_data['post_npc'], step=0.1, format="%.2f")
        st.session_state.assessment_data['post_npa'] = st.number_input(
            "Post-exercise NPA (cm)", min_value=0.0, max_value=50.0, 
            value=st.session_state.assessment_data['post_npa'], step=0.1, format="%.2f")
    
    st.markdown('</div>', unsafe_allow_html=True)

# REAL SCORE CALCULATION
if st.button("💾 Save Real Assessment", type="primary", use_container_width=True):
    # Calculate real scores
    therapist_avg = (
        st.session_state.assessment_data['therapist_accuracy'] +
        st.session_state.assessment_data['therapist_stamina'] +
        st.session_state.assessment_data['therapist_compliance'] +
        st.session_state.assessment_data['therapist_motivation'] +
        st.session_state.assessment_data['therapist_technique'] +
        st.session_state.assessment_data['therapist_focus']
    ) / 6
    
    patient_avg = (st.session_state.assessment_data['patient_clarity'] + st.session_state.assessment_data['patient_comfort']) * 5
    
    # Clinical improvement
    npc_improvement = max(0, (10.0 - st.session_state.assessment_data['post_npc']) * 5)
    npa_improvement = max(0, (8.0 - st.session_state.assessment_data['post_npa']) * 5)
    
    real_score = (therapist_avg * 0.6 + patient_avg * 0.3 + (npc_improvement + npa_improvement) * 0.1)
    
    session_data = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'patient': patient_name,
        'exercise': exercise,
        'therapist_score': round(therapist_avg),
        'patient_score': round(patient_avg),
        'clinical_improvement': round(npc_improvement + npa_improvement),
        'real_score': round(real_score),
        'pre_npc': npc,
        'post_npc': st.session_state.assessment_data['post_npc'],
        'pre_npa': npa,
        'post_npa': st.session_state.assessment_data['post_npa'],
        'difficulty': st.session_state.assessment_data['patient_difficulty'],
        'completed': st.session_state.assessment_data['patient_completed']
    }
    
    st.session_state.session_data.append(session_data)
    st.success(f"✅ Real assessment saved! Score: {round(real_score)}%")

# Progress Reports
st.header("📊 Progress Reports")
if st.session_state.session_data:
    df = pd.DataFrame(st.session_state.session_data)
    st.dataframe(df, use_container_width=True)
    
    if st.button("📈 Generate Detailed Report", use_container_width=True):
        st.subheader("Clinical Progress Summary")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sessions", len(df))
            st.metric("Average Real Score", f"{df['real_score'].mean():.1f}%")
        with col2:
            st.metric("Therapist Avg", f"{df['therapist_score'].mean():.1f}%")
            st.metric("Patient Avg", f"{df['patient_score'].mean():.1f}%")
        with col3:
            current_npc_improvement = df['pre_npc'].iloc[0] - df['post_npc'].iloc[-1]
            current_npa_improvement = df['pre_npa'].iloc[0] - df['post_npa'].iloc[-1]
            st.metric("NPC Improvement", f"{current_npc_improvement:+.2f} cm")
            st.metric("NPA Improvement", f"{current_npa_improvement:+.2f} cm")

# Compact Footer
st.markdown("---")
st.markdown("**Developed by Toni Mandusic** | *Vision Therapy Professional Application* | © 2025 VisionQuest")

# Disclaimer in expander at the bottom
with st.expander("⚠️ Medical Disclaimer"):
    st.markdown("""
    **For qualified eye care professionals only.** 
    - All measurements and exercises should be conducted under professional supervision
    - Results should be interpreted by licensed optometrists or orthoptists  
    - This tool is not a substitute for professional medical diagnosis
    - Always verify measurements with standard clinical instruments
    """)