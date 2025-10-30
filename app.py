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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: bold;
    }
    .subheader {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.3rem;
    }
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 1rem;
    }
    .logo-img {
        height: 100px;
        width: auto;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .exercise-area {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border: 3px solid #dee2e6;
        margin: 1rem 0;
        min-height: 400px;
        text-align: center;
    }
    .exercise-active {
        background: #e8f5e8;
        border: 3px solid #28a745;
    }
    .target {
        font-size: 4rem;
        margin: 1rem;
        transition: all 0.3s ease;
    }
    .vergence-container {
        position: relative;
        height: 200px;
        background: linear-gradient(45deg, #e3f2fd, #bbdefb);
        border-radius: 10px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .fusion-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        height: 200px;
        background: linear-gradient(45deg, #fff3e0, #ffe0b2);
        border-radius: 10px;
        margin: 1rem 0;
    }
    .jump-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        height: 200px;
        background: linear-gradient(45deg, #e8f5e8, #c8e6c9);
        border-radius: 10px;
        margin: 1rem 0;
        padding: 1rem;
    }
    .pursuit-container {
        position: relative;
        height: 200px;
        background: linear-gradient(45deg, #f3e5f5, #e1bee7);
        border-radius: 10px;
        margin: 1rem 0;
    }
    .rock-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        height: 200px;
        background: linear-gradient(45deg, #fff8e1, #ffecb3);
        border-radius: 10px;
        margin: 1rem 0;
    }
    .status-info {
        position: absolute;
        bottom: 10px;
        left: 10px;
        font-size: 0.9rem;
        color: #666;
        background: rgba(255,255,255,0.8);
        padding: 5px 10px;
        border-radius: 5px;
    }
    .assessment-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #dee2e6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_exercise' not in st.session_state:
    st.session_state.current_exercise = None
if 'exercise_started' not in st.session_state:
    st.session_state.exercise_started = False
if 'exercise_time_remaining' not in st.session_state:
    st.session_state.exercise_time_remaining = 10  # Kraće za test
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

# PROFESSIONAL HEADER
st.markdown("""
<div class="header-container">
    <div class="logo-container">
        <img src="https://i.ibb.co/TqwF8SD/Gemini-Generated-Image-gokhtxgokhtxgokh.jpg" 
             class="logo-img" 
             alt="VisionQuest Logo">
    </div>
    <h1 class="main-header">VisionQuest</h1>
    <div class="subheader">Professional Binocular Vision & Vergence Training System</div>
</div>
""", unsafe_allow_html=True)

# Patient Information
with st.container():
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        patient_name = st.text_input("Patient Name", "John Doe")
    with col2:
        patient_age = st.number_input("Age", min_value=3, max_value=100, value=8)
    with col3:
        patient_type = st.selectbox("Patient Type", ["Child", "Adult"])
    with col4:
        if st.button("🔄 Reset Session"):
            st.session_state.session_data = []
            st.rerun()

# Clinical Measurements
with st.container():
    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
    with col1:
        npc = st.number_input("NPC (cm)", min_value=0.0, max_value=50.0, value=12.5, step=0.1, format="%.2f")
    with col2:
        npa = st.number_input("NPA (cm)", min_value=0.0, max_value=50.0, value=15.5, step=0.1, format="%.2f")
    with col3:
        if patient_type == "Child":
            targets = st.multiselect("Targets", 
                                   ["🚀 Rocket", "⚽ Football", "🐬 Dolphin", "🌟 Star", "🎈 Balloon", "🦋 Butterfly"],
                                   default=["🚀 Rocket", "⚽ Football"])
            current_targets = ["🚀", "⚽", "🐬", "🌟", "🎈", "🦋"]
        else:
            targets = st.multiselect("Targets",
                                   ["● Circle", "▲ Triangle", "■ Square", "✚ Cross", "★ Star", "◆ Diamond"],
                                   default=["● Circle", "▲ Triangle"])
            current_targets = ["●", "▲", "■", "✚", "★", "◆"]
    with col4:
        exercise = st.selectbox("Exercise", 
                               ["Vergence", "Fusion", "Jump Vergence", "Smooth Pursuit", "Accommodative Rock"])

# MAIN EXERCISE AREA - PRAVE ANIMACIJE
st.markdown("---")
st.subheader(f"🎯 {exercise} Training")

def start_exercise(exercise_name):
    st.session_state.current_exercise = exercise_name
    st.session_state.exercise_started = True
    st.session_state.exercise_time_remaining = 10  # 10 sekundi za test

def stop_exercise():
    st.session_state.exercise_started = False
    st.session_state.current_exercise = None

# Display exercise
if st.session_state.exercise_started and st.session_state.current_exercise == exercise:
    exercise_class = "exercise-area exercise-active"
else:
    exercise_class = "exercise-area"

st.markdown(f'<div class="{exercise_class}">', unsafe_allow_html=True)

if st.session_state.exercise_started and st.session_state.current_exercise == exercise:
    # Exercise is running
    st.success(f"**{exercise} Exercise Running** - Time remaining: {st.session_state.exercise_time_remaining}s")
    
    # ANIMIRANE VJEŽBE
    if exercise == "Vergence":
        st.markdown("### 🎯 Follow the target moving in depth")
        movement = math.sin(time.time() * 2) * 40
        target_size = 3 + abs(math.sin(time.time() * 3)) * 2
        
        st.markdown(f"""
        <div class="vergence-container">
            <div class="target" style="font-size: {target_size}rem; transform: translateX({movement}px);">
                {current_targets[0]}
            </div>
            <div class="status-info">
                🔍 Depth: {'NEAR' if target_size > 4 else 'FAR'} | Position: {int(movement)}px
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Fusion":
        st.markdown("### 🔮 Fuse the images into one")
        separation = 30 + math.sin(time.time() * 1.5) * 20
        
        st.markdown(f"""
        <div class="fusion-container">
            <div class="target" style="color: red; font-size: 3rem;">{current_targets[0]}</div>
            <div style="font-size: 1.5rem; color: #666;">FUSION ZONE</div>
            <div class="target" style="color: blue; font-size: 3rem;">{current_targets[1] if len(current_targets) > 1 else current_targets[0]}</div>
            <div class="status-info">
                📏 Separation: {int(separation)}% | {'FUSING' if separation < 40 else 'SEPARATED'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Jump Vergence":
        st.markdown("### 🔄 Rapidly switch focus between targets")
        current_idx = int(time.time() * 2) % len(current_targets)
        
        st.markdown(f"""
        <div class="jump-container">
            <div class="target" style="font-size: {'4rem' if current_idx == 0 else '2rem'}; opacity: {'1' if current_idx == 0 else '0.3'};">{current_targets[0]}</div>
            <div class="target" style="font-size: {'4rem' if current_idx == 1 else '2rem'}; opacity: {'1' if current_idx == 1 else '0.3'};">{current_targets[1] if len(current_targets) > 1 else current_targets[0]}</div>
            <div class="target" style="font-size: {'4rem' if current_idx == 2 else '2rem'}; opacity: {'1' if current_idx == 2 else '0.3'};">{current_targets[2] if len(current_targets) > 2 else current_targets[0]}</div>
            <div class="target" style="font-size: {'4rem' if current_idx == 3 else '2rem'}; opacity: {'1' if current_idx == 3 else '0.3'};">{current_targets[3] if len(current_targets) > 3 else current_targets[0]}</div>
            <div class="status-info">
                🎯 Current: {current_targets[current_idx]} | Switch every 0.5s
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Smooth Pursuit":
        st.markdown("### 🌀 Smoothly track the moving target")
        angle = time.time() * 2
        radius = 70
        x = 50 + math.cos(angle) * radius
        y = 50 + math.sin(angle) * radius
        
        st.markdown(f"""
        <div class="pursuit-container">
            <div class="target" style="position: absolute; left: {x}%; top: {y}%; font-size: 3rem;">
                {current_targets[0]}
            </div>
            <div class="status-info">
                📐 Circular Pattern | Speed: Medium
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Accommodative Rock":
        st.markdown("### 👁️ Alternate focus between near and far")
        is_near = int(time.time() * 1) % 2 == 0
        
        st.markdown(f"""
        <div class="rock-container">
            <div class="target" style="font-size: {'4rem' if is_near else '1.5rem'}; color: {'#d32f2f' if is_near else '#666'};">
                🎯 NEAR
            </div>
            <div class="target" style="font-size: {'1.5rem' if is_near else '4rem'}; color: {'#666' if is_near else '#1976d2'};">
                🔭 FAR
            </div>
            <div class="status-info">
                👁️ Focus: {'NEAR (Look LEFT)' if is_near else 'FAR (Look RIGHT)'}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Timer control
    if st.session_state.exercise_time_remaining > 0:
        st.session_state.exercise_time_remaining -= 1
        time.sleep(1)
        st.rerun()
    else:
        st.balloons()
        st.success("🎉 Exercise completed successfully!")
        stop_exercise()
        st.rerun()
        
    if st.button("⏹️ Stop Exercise", type="secondary"):
        stop_exercise()
        st.rerun()
        
else:
    # Exercise setup
    instructions = {
        "Vergence": "Target moves in depth to train convergence/divergence",
        "Fusion": "Fuse separate images into single vision", 
        "Jump Vergence": "Rapid focus switching between multiple targets",
        "Smooth Pursuit": "Smooth tracking of moving objects",
        "Accommodative Rock": "Alternating focus between near and far distances"
    }
    
    st.info(f"**{exercise}**: {instructions[exercise]}")
    st.write(f"**Duration:** 10 seconds (test) | **Targets:** {', '.join(targets[:2])}")
    
    if st.button(f"🎯 Start {exercise} Exercise", type="primary", use_container_width=True):
        start_exercise(exercise)
        st.rerun()

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