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

# JEDNOSTAVAN HEADER - bez CSS ludosti
st.title("🔭 VisionQuest")
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

# SIMPLE EXERCISE AREA - bez glupih pravokutnika
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
        # Kreiraj 3D efekt s veličinom
        depth = math.sin(time.time() * 2)
        target_size = 120 + int(depth * 80)  # 40-200px
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
        # Koristi Streamlit columns za pokretni efekt
        pos = int((math.sin(time.time() * 3) + 1) * 50)  # 0-100%
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

# Ostali kod ostaje isti...
st.markdown("---")
st.header("📊 Session Recording")

if st.button("💾 Save Session Results"):
    session_data = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'patient': patient_name,
        'exercise': exercise,
        'npc_cm': npc,
        'npa_cm': npa,
        'duration': 10
    }
    st.session_state.session_data.append(session_data)
    st.success("Session saved successfully!")

# Progress Reports
if st.session_state.session_data:
    st.header("📈 Progress Reports")
    df = pd.DataFrame(st.session_state.session_data)
    st.dataframe(df)

# Footer
st.markdown("---")
st.markdown("**Developed by Toni Mandusic** • © 2025 VisionQuest")