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

# Initialize session state
if 'current_exercise' not in st.session_state:
    st.session_state.current_exercise = None
if 'exercise_started' not in st.session_state:
    st.session_state.exercise_started = False
if 'exercise_time_remaining' not in st.session_state:
    st.session_state.exercise_time_remaining = 10
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

# HEADER SA TVOJIM LOGOM
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://i.postimg.cc/853pWNYm/Gemini-Generated-Image-gokhtxgokhtxgokh.png", width=500)
with col2:
    st.title("VisionQuest")
    st.markdown("**Binocular Vision & Vergence Training System**")
st.markdown("---")

# Patient Information
col1, col2, col3 = st.columns(3)
with col1:
    patient_name = st.text_input("Patient Name", "John Doe")
with col2:
    patient_age = st.number_input("Age", min_value=3, max_value=100, value=8)
with col3:
    patient_type = st.selectbox("Patient Type", ["Child", "Adult"])

# Clinical Measurements
col1, col2 = st.columns(2)
with col1:
    npc = st.number_input("NPC (cm)", min_value=0.0, max_value=50.0, value=12.5, step=0.1, format="%.2f")
with col2:
    npa = st.number_input("NPA (cm)", min_value=0.0, max_value=50.0, value=15.5, step=0.1, format="%.2f")

# Target selection
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

# Exercise Selection
exercise = st.selectbox("Select Exercise", 
                       ["Vergence", "Fusion", "Jump Vergence", "Smooth Pursuit", "Accommodative Rock"])

# EXERCISE AREA
st.markdown("---")
st.subheader(f"🎯 {exercise} Exercise")

def start_exercise(exercise_name):
    st.session_state.current_exercise = exercise_name
    st.session_state.exercise_started = True
    st.session_state.exercise_time_remaining = 10

def stop_exercise():
    st.session_state.exercise_started = False
    st.session_state.current_exercise = None

# Display exercise
if st.session_state.exercise_started and st.session_state.current_exercise == exercise:
    # Exercise is running - PRAVE ANIMACIJE
    st.success(f"**{exercise} Exercise Running** - Time: {st.session_state.exercise_time_remaining}s")
    
    # Stvarno korisne animacije
    if exercise == "Vergence":
        st.info("🎯 Follow the target moving toward you and away")
        depth = math.sin(time.time() * 2)
        target_size = 120 + int(depth * 80)
        st.markdown(f"<div style='text-align: center; font-size: {target_size}px;'>{current_targets[0]}</div>", unsafe_allow_html=True)
        st.write(f"**Depth:** {'NEAR' if depth > 0 else 'FAR'}")
        
    elif exercise == "Fusion":
        st.info("🔮 Fuse the red and blue images into one")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown(f"<div style='text-align: center; font-size: 80px; color: red;'>{current_targets[0]}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div style='text-align: center; font-size: 40px; margin-top: 20px;'>+</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div style='text-align: center; font-size: 80px; color: blue;'>{current_targets[1] if len(current_targets) > 1 else current_targets[0]}</div>", unsafe_allow_html=True)
        st.write("**Focus:** Bring images together to see one clear target")
        
    elif exercise == "Jump Vergence":
        st.info("🔄 Quickly switch focus between targets")
        current_idx = int(time.time() * 2) % min(4, len(current_targets))
        cols = st.columns(4)
        for i in range(4):
            with cols[i]:
                if i < len(current_targets):
                    st.markdown(f"<div style='text-align: center; font-size: {80 if i == current_idx else 40}px; opacity: {1.0 if i == current_idx else 0.3};'>{current_targets[i]}</div>", unsafe_allow_html=True)
        st.write(f"**Current target:** {current_targets[current_idx]}")
        
    elif exercise == "Smooth Pursuit":
        st.info("🌀 Smoothly follow the moving target")
        pos = int((math.sin(time.time() * 3) + 1) * 50)
        empty_cols = st.columns(10)
        with empty_cols[min(9, pos // 10)]:
            st.markdown(f"<div style='text-align: center; font-size: 60px;'>{current_targets[0]}</div>", unsafe_allow_html=True)
        st.write("**Follow the target with your eyes smoothly**")
        
    elif exercise == "Accommodative Rock":
        st.info("👁️ Alternate focus between near and far")
        is_near = int(time.time()) % 2 == 0
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div style='text-align: center; font-size: {100 if is_near else 40}px; color: #d32f2f;'>NEAR</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='text-align: center; font-size: {40 if is_near else 100}px; color: #1976d2;'>FAR</div>", unsafe_allow_html=True)
        st.write(f"**Focus on:** {'NEAR target (LEFT)' if is_near else 'FAR target (RIGHT)'}")
    
    # Timer
    if st.session_state.exercise_time_remaining > 0:
        st.session_state.exercise_time_remaining -= 1
        time.sleep(1)
        st.rerun()
    else:
        st.balloons()
        st.success("✅ Exercise completed!")
        stop_exercise()
        st.rerun()
        
    if st.button("⏹️ Stop Exercise"):
        stop_exercise()
        st.rerun()
        
else:
    # Exercise setup
    st.info("Click Start to begin the exercise")
    
    if st.button(f"🎯 Start {exercise} Exercise", type="primary"):
        start_exercise(exercise)
        st.rerun()

# PROCJENA I DOJAM - POVRATAK NA ORIGINAL
st.markdown("---")
st.header("🧑‍⚕️ Session Assessment")

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

# REAL SCORE CALCULATION
if st.button("💾 Save Real Assessment", type="primary"):
    therapist_avg = (
        st.session_state.assessment_data['therapist_accuracy'] +
        st.session_state.assessment_data['therapist_stamina'] +
        st.session_state.assessment_data['therapist_compliance'] +
        st.session_state.assessment_data['therapist_motivation'] +
        st.session_state.assessment_data['therapist_technique'] +
        st.session_state.assessment_data['therapist_focus']
    ) / 6
    
    patient_avg = (st.session_state.assessment_data['patient_clarity'] + st.session_state.assessment_data['patient_comfort']) * 5
    
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
    st.dataframe(df)
    
    if st.button("📈 Generate Detailed Report"):
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

# Footer
st.markdown("---")
st.markdown("**Developed by Toni Mandusic** • © 2025 VisionQuest")

# Disclaimer
with st.expander("⚠️ Medical Disclaimer"):
    st.markdown("""
    **For qualified eye care professionals only.** 
    - All measurements under professional supervision
    - Results interpreted by licensed optometrists
    - Not a substitute for medical diagnosis
    """)