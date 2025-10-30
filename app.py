import streamlit as st
import pandas as pd
from datetime import datetime
import random
import time
import math

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
    .exercise-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #dee2e6;
        margin: 10px 0;
        height: 500px;
        position: relative;
        overflow: hidden;
    }
    .exercise-active {
        background-color: #e8f5e8;
        border: 2px solid #28a745;
    }
    .target {
        position: absolute;
        font-size: 3rem;
        transition: all 0.5s ease;
        user-select: none;
    }
    .vergence-target {
        font-size: 4rem;
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
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
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
    st.session_state.exercise_time_remaining = 300  # 5 minutes in seconds
if 'session_data' not in st.session_state:
    st.session_state.session_data = []
if 'target_position' not in st.session_state:
    st.session_state.target_position = 50
if 'fusion_state' not in st.session_state:
    st.session_state.fusion_state = "separated"
if 'jump_target_index' not in st.session_state:
    st.session_state.jump_target_index = 0
if 'pursuit_angle' not in st.session_state:
    st.session_state.pursuit_angle = 0
if 'rock_state' not in st.session_state:
    st.session_state.rock_state = "near"

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
    current_targets = ["🚀", "⚽", "🐬", "🌟", "🎈", "🦋"]
else:
    targets = st.multiselect("Select Targets for Exercises",
                           ["● Circle", "▲ Triangle", "■ Square", "✚ Cross", "★ Star", "◆ Diamond"],
                           default=["● Circle", "▲ Triangle"])
    current_targets = ["●", "▲", "■", "✚", "★", "◆"]

# Training Exercises
st.header("💪 Training Exercises")
exercise = st.selectbox("Select Exercise", 
                       ["Vergence", "Fusion", "Jump Vergence", "Smooth Pursuit", "Accommodative Rock"])

# Exercise implementation
st.markdown("---")
st.subheader(f"🎮 {exercise} Training")

def start_exercise(exercise_name):
    st.session_state.current_exercise = exercise_name
    st.session_state.exercise_started = True
    st.session_state.exercise_progress = 0
    st.session_state.exercise_time_remaining = 300  # 5 minutes
    st.session_state.target_position = 50
    st.session_state.fusion_state = "separated"
    st.session_state.jump_target_index = 0
    st.session_state.pursuit_angle = 0
    st.session_state.rock_state = "near"

def stop_exercise():
    st.session_state.exercise_started = False
    st.session_state.current_exercise = None

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

# Display exercise
if st.session_state.exercise_started and st.session_state.current_exercise == exercise:
    # Exercise is running
    st.markdown(f'<div class="exercise-container exercise-active">', unsafe_allow_html=True)
    
    # Timer and progress
    col1, col2 = st.columns([3, 1])
    with col1:
        progress_bar = st.progress(st.session_state.exercise_progress / 100)
    with col2:
        st.metric("Time Remaining", format_time(st.session_state.exercise_time_remaining))
    
    # Exercise-specific visual display
    if exercise == "Vergence":
        st.markdown('<div class="instructions">🎯 Follow the target as it moves closer and farther. Keep it single and clear!</div>', unsafe_allow_html=True)
        
        # Vergence target moving in depth
        target_size = 50 + (50 * math.sin(time.time() * 0.5))  # Pulsing size for depth effect
        target_pos = 50 + (40 * math.sin(time.time() * 0.3))   # Moving side to side
        
        st.markdown(f"""
        <div style="position: relative; height: 300px; background: linear-gradient(45deg, #e3f2fd, #bbdefb); border-radius: 10px;">
            <div class="target vergence-target" style="top: 45%; left: {target_pos}%; font-size: {target_size}px;">
                {current_targets[0]}
            </div>
            <div style="position: absolute; bottom: 10px; left: 10px; font-size: 0.8rem; color: #666;">
                🎯 Depth: {'NEAR' if target_size > 70 else 'FAR'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Fusion":
        st.markdown('<div class="instructions">🔮 Fuse the two images into one clear image. Maintain single vision!</div>', unsafe_allow_html=True)
        
        # Fusion targets that can be brought together
        fusion_offset = 20 + (15 * math.sin(time.time() * 0.2))  # Slowly moving together/apart
        
        st.markdown(f"""
        <div style="position: relative; height: 300px; background: linear-gradient(45deg, #fff3e0, #ffe0b2); border-radius: 10px;">
            <div class="target fusion-left" style="top: 45%; left: {50 - fusion_offset}%; color: red;">
                {current_targets[0]}
            </div>
            <div class="target fusion-right" style="top: 45%; left: {50 + fusion_offset}%; color: blue;">
                {current_targets[1] if len(current_targets) > 1 else current_targets[0]}
            </div>
            <div style="position: absolute; bottom: 10px; left: 10px; font-size: 0.8rem; color: #666;">
                🔄 Fusion: {'EASY' if fusion_offset < 25 else 'CHALLENGING'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Jump Vergence":
        st.markdown('<div class="instructions">🔄 Quickly switch focus between targets. Maintain clear vision during jumps!</div>', unsafe_allow_html=True)
        
        # Jump between different targets
        jump_interval = 3  # seconds per target
        current_target_idx = int((time.time() % (len(current_targets) * jump_interval)) / jump_interval)
        
        positions = [(25, 25), (75, 25), (25, 75), (75, 75), (50, 50), (10, 50)]
        
        st.markdown(f"""
        <div style="position: relative; height: 300px; background: linear-gradient(45deg, #e8f5e8, #c8e6c9); border-radius: 10px;">
            {''.join([f'<div class="target" style="top: {pos[1]}%; left: {pos[0]}%; opacity: {0.3 if i != current_target_idx else 1.0};">{target}</div>' 
                     for i, (target, pos) in enumerate(zip(current_targets, positions))])}
            <div style="position: absolute; bottom: 10px; left: 10px; font-size: 0.8rem; color: #666;">
                🎯 Current: {current_targets[current_target_idx]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Smooth Pursuit":
        st.markdown('<div class="instructions">🌀 Smoothly follow the moving target. Keep your eyes on it!</div>', unsafe_allow_html=True)
        
        # Circular smooth pursuit
        angle = time.time() * 0.5
        radius = 35
        x = 50 + radius * math.cos(angle)
        y = 50 + radius * math.sin(angle)
        
        st.markdown(f"""
        <div style="position: relative; height: 300px; background: linear-gradient(45deg, #f3e5f5, #e1bee7); border-radius: 10px;">
            <div class="target" style="top: {y}%; left: {x}%;">
                {current_targets[0]}
            </div>
            <div style="position: absolute; top: 50%; left: 50%; width: 2px; height: 70%; background: #ccc; transform: translate(-50%, -50%);"></div>
            <div style="position: absolute; left: 50%; top: 50%; width: 70%; height: 2px; background: #ccc; transform: translate(-50%, -50%);"></div>
            <div style="position: absolute; bottom: 10px; left: 10px; font-size: 0.8rem; color: #666;">
                📐 Pattern: Circular
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Accommodative Rock":
        st.markdown('<div class="instructions">👁️ Alternate focus between near and far. Feel your eyes adjusting!</div>', unsafe_allow_html=True)
        
        # Accommodative rock between near and far
        rock_interval = 4  # seconds per switch
        is_near = int(time.time() % (rock_interval * 2)) < rock_interval
        
        st.markdown(f"""
        <div style="position: relative; height: 300px; background: linear-gradient(45deg, #fff8e1, #ffecb3); border-radius: 10px;">
            <div class="target" style="top: 45%; left: 30%; font-size: {'4rem' if is_near else '2rem'};">
                🎯 NEAR
            </div>
            <div class="target" style="top: 45%; left: 70%; font-size: {'2rem' if is_near else '4rem'};">
                🔭 FAR
            </div>
            <div style="position: absolute; bottom: 10px; left: 10px; font-size: 0.8rem; color: #666;">
                👁️ Focus: {'NEAR → Look at left target' if is_near else 'FAR → Look at right target'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⏹️ Stop Exercise"):
            stop_exercise()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Update timer and progress
    if st.session_state.exercise_time_remaining > 0:
        time.sleep(1)
        st.session_state.exercise_time_remaining -= 1
        st.session_state.exercise_progress = (300 - st.session_state.exercise_time_remaining) / 3
        st.rerun()
    else:
        st.balloons()
        st.success("🎉 Exercise completed! Great job!")
        time.sleep(2)
        stop_exercise()
        st.rerun()
        
else:
    # Exercise setup screen
    st.markdown('<div class="exercise-container">', unsafe_allow_html=True)
    st.info("🎯 Configure and start your vision training exercise")
    
    # Exercise instructions
    instructions = {
        "Vergence": "Follow a target moving in depth to improve convergence and divergence skills",
        "Fusion": "Fuse separate images from each eye into a single clear image", 
        "Jump Vergence": "Rapidly switch focus between different targets at various distances",
        "Smooth Pursuit": "Smoothly track moving targets to improve eye tracking accuracy",
        "Accommodative Rock": "Alternate focus between near and far targets to improve accommodation"
    }
    
    st.write(f"**{exercise}:** {instructions[exercise]}")
    st.write(f"**Duration:** 5 minutes")
    st.write(f"**Targets:** {', '.join(targets)}")
    
    if st.button(f"🎯 Start {exercise} Exercise", type="primary"):
        start_exercise(exercise)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Session recording and reporting (ostaje isti kao prije)
st.header("🧑‍⚕️ Session Assessment")

# Terapeut ocjenjuje
st.subheader("Therapist Evaluation")
col1, col2, col3 = st.columns(3)
with col1:
    accuracy = st.slider("Accuracy of eye movements", 0, 100, 75)
    stamina = st.slider("Stamina/Endurance", 0, 100, 70)
with col2:
    compliance = st.slider("Exercise compliance", 0, 100, 85)
    motivation = st.slider("Patient motivation", 0, 100, 80)
with col3:
    technique = st.slider("Proper technique", 0, 100, 78)
    focus = st.slider("Maintained focus", 0, 100, 72)

# Pacijentova samo-ocjena
st.subheader("Patient Feedback")
col1, col2 = st.columns(2)
with col1:
    clarity = st.slider("How clear was the image?", 1, 10, 7)
    comfort = st.slider("How comfortable was it?", 1, 10, 6)
with col2:
    difficulty = st.selectbox("Difficulty level", 
                            ["Too Easy", "Appropriate", "Challenging", "Too Difficult"])
    completed = st.radio("Did you complete the exercise?", ["Yes", "Partial", "No"])

# Klinički napredak
st.subheader("Clinical Measurements")
col1, col2 = st.columns(2)
with col1:
    post_npc = st.number_input("Post-exercise NPC (cm)", value=npc, format="%.2f")
with col2:
    post_npa = st.number_input("Post-exercise NPA (cm)", value=npa, format="%.2f")

# REALAN SCORE
if st.button("💾 Save Real Assessment"):
    # Izračunaj stvarni score
    therapist_avg = (accuracy + stamina + compliance + motivation + technique + focus) / 6
    patient_avg = ((clarity + comfort) * 5)  # Convert to percentage
    
    # Klinički improvement
    npc_improvement = max(0, (10.0 - post_npc) * 5)  # Pretpostavka: cilj je 10cm
    npa_improvement = max(0, (8.0 - post_npa) * 5)   # Pretpostavka: cilj je 8cm
    
    real_score = (therapist_avg * 0.6 + patient_avg * 0.3 + (npc_improvement + npa_improvement) * 0.1)
    
    session_data = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'patient': patient_name,
        'exercise': exercise,
        'therapist_score': round(therapist_avg),
        'patient_score': round(patient_avg),
        'clinical_improvement': round(npc_improvement + npa_improvement),
        'real_score': round(real_score),
        'post_npc': post_npc,
        'post_npa': post_npa,
        'difficulty': difficulty,
        'completed': completed
    }
    
    st.session_state.session_data.append(session_data)
    st.success(f"✅ Real assessment saved! Score: {round(real_score)}%")
# Progress Report (ostaje isti)
st.header("📊 Progress Reports")
if st.session_state.session_data:
    df = pd.DataFrame(st.session_state.session_data)
    st.dataframe(df)
    
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
        
        if len(df) > 1:
            st.subheader("NPC/NPA Progress")
            improvement_npc = df['npc_cm'].iloc[0] - npc
            improvement_npa = df['npa_cm'].iloc[0] - npa
            if improvement_npc > 0:
                st.success(f"🎉 NPC Improvement: +{improvement_npc:.2f} cm")
            if improvement_npa > 0:
                st.success(f"🎉 NPA Improvement: +{improvement_npa:.2f} cm")

# Footer
st.markdown("---")
st.markdown("### **Developed by Toni Mandusic**")
st.markdown("*Vision Therapy Professional Application*")
st.markdown("© 2024 VisionQuest - All rights reserved")