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
    .exercise-container {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #dee2e6;
        margin: 5px 0;
        height: 450px;  /* Povećana visina za veći exercise prostor */
        position: relative;
        overflow: hidden;
    }
    .exercise-active {
        background-color: #e8f5e8;
        border: 2px solid #28a745;
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
        padding: 6px;
        border-radius: 5px;
        margin: 6px 0;
        font-size: 0.85rem;
    }
    .compact-input {
        margin-bottom: 0.3rem;
    }
    /* Reduce space in metrics */
    .stMetric {
        padding: 0.2rem;
    }
    /* Compact buttons */
    .stButton button {
        margin: 1px 0;
        padding: 0.25rem 0.5rem;
    }
    /* Remove extra padding from columns */
    [data-testid="column"] {
        padding: 0.5rem;
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

# SUPER COMPACT HEADER - smanjen prostor na minimum
st.markdown('<h1 class="main-header">🔭 VisionQuest</h1>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Binocular Vision & Vergence Training</div>', unsafe_allow_html=True)

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
                                   default=["🚀 Rocket", "⚽ Football"], key="targets_child", label_visibility="collapsed")
            current_targets = ["🚀", "⚽", "🐬", "🌟", "🎈", "🦋"]
        else:
            targets = st.multiselect("Targets",
                                   ["● Circle", "▲ Triangle", "■ Square", "✚ Cross", "★ Star", "◆ Diamond"],
                                   default=["● Circle", "▲ Triangle"], key="targets_adult", label_visibility="collapsed")
            current_targets = ["●", "▲", "■", "✚", "★", "◆"]
    with col4:
        exercise = st.selectbox("Exercise", 
                               ["Vergence", "Fusion", "Jump Vergence", "Smooth Pursuit", "Accommodative Rock"],
                               key="exercise_select", label_visibility="collapsed")

# MAIN EXERCISE AREA - OVO JE SADA GLAVNI FOKUS
st.markdown("---")

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

# Display exercise - POVEĆAN PROSTOR ZA VJEŽBU
if st.session_state.exercise_started and st.session_state.current_exercise == exercise:
    # Exercise is running - SADA VEĆI PROSTOR
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
    
    # Exercise-specific visual display - POVEĆANA VISINA
    display_height = "320px"  # Povećano sa 250px na 320px
    
    if exercise == "Vergence":
        st.markdown('<div class="instructions">🎯 Follow the target moving closer/farther</div>', unsafe_allow_html=True)
        
        target_size = 50 + (50 * math.sin(time.time() * 0.5))
        target_pos = 50 + (40 * math.sin(time.time() * 0.3))
        
        st.markdown(f"""
        <div style="position: relative; height: {display_height}; background: linear-gradient(45deg, #e3f2fd, #bbdefb); border-radius: 10px;">
            <div class="target vergence-target" style="top: 45%; left: {target_pos}%; font-size: {target_size}px;">
                {current_targets[0]}
            </div>
            <div style="position: absolute; bottom: 10px; left: 10px; font-size: 0.8rem; color: #666;">
                🎯 Depth: {'NEAR' if target_size > 70 else 'FAR'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Fusion":
        st.markdown('<div class="instructions">🔮 Fuse two images into one clear image</div>', unsafe_allow_html=True)
        
        fusion_offset = 20 + (15 * math.sin(time.time() * 0.2))
        
        st.markdown(f"""
        <div style="position: relative; height: {display_height}; background: linear-gradient(45deg, #fff3e0, #ffe0b2); border-radius: 10px;">
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
        st.markdown('<div class="instructions">🔄 Quickly switch focus between targets</div>', unsafe_allow_html=True)
        
        jump_interval = 3
        current_target_idx = int((time.time() % (len(current_targets) * jump_interval)) / jump_interval)
        positions = [(25, 25), (75, 25), (25, 75), (75, 75), (50, 50), (10, 50)]
        
        st.markdown(f"""
        <div style="position: relative; height: {display_height}; background: linear-gradient(45deg, #e8f5e8, #c8e6c9); border-radius: 10px;">
            {''.join([f'<div class="target" style="top: {pos[1]}%; left: {pos[0]}%; opacity: {0.3 if i != current_target_idx else 1.0};">{target}</div>' 
                     for i, (target, pos) in enumerate(zip(current_targets, positions))])}
            <div style="position: absolute; bottom: 10px; left: 10px; font-size: 0.8rem; color: #666;">
                🎯 Current: {current_targets[current_target_idx]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Smooth Pursuit":
        st.markdown('<div class="instructions">🌀 Smoothly follow the moving target</div>', unsafe_allow_html=True)
        
        angle = time.time() * 0.5
        radius = 35
        x = 50 + radius * math.cos(angle)
        y = 50 + radius * math.sin(angle)
        
        st.markdown(f"""
        <div style="position: relative; height: {display_height}; background: linear-gradient(45deg, #f3e5f5, #e1bee7); border-radius: 10px;">
            <div class="target" style="top: {y}%; left: {x}%;">
                {current_targets[0]}
            </div>
            <div style="position: absolute; bottom: 10px; left: 10px; font-size: 0.8rem; color: #666;">
                📐 Pattern: Circular
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif exercise == "Accommodative Rock":
        st.markdown('<div class="instructions">👁️ Alternate focus between near and far</div>', unsafe_allow_html=True)
        
        rock_interval = 4
        is_near = int(time.time() % (rock_interval * 2)) < rock_interval
        
        st.markdown(f"""
        <div style="position: relative; height: {display_height}; background: linear-gradient(45deg, #fff8e1, #ffecb3); border-radius: 10px;">
            <div class="target" style="top: 45%; left: 30%; font-size: {'3.5rem' if is_near else '1.8rem'};">
                🎯 NEAR
            </div>
            <div class="target" style="top: 45%; left: 70%; font-size: {'1.8rem' if is_near else '3.5rem'};">
                🔭 FAR
            </div>
            <div style="position: absolute; bottom: 10px; left: 10px; font-size: 0.8rem; color: #666;">
                👁️ Focus: {'NEAR → Look at left target' if is_near else 'FAR → Look at right target'}
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
    # Exercise setup screen - POVEĆAN PROSTOR
    st.markdown('<div class="exercise-container">', unsafe_allow_html=True)
    
    instructions = {
        "Vergence": "Follow target moving in depth to improve convergence and divergence skills",
        "Fusion": "Fuse separate images from each eye into a single clear image", 
        "Jump Vergence": "Rapidly switch focus between different targets at various distances",
        "Smooth Pursuit": "Smoothly track moving targets to improve eye tracking accuracy",
        "Accommodative Rock": "Alternate focus between near and far targets to improve accommodation"
    }
    
    st.write(f"## {exercise} Exercise")
    st.write(f"**Description:** {instructions[exercise]}")
    st.write(f"**Duration:** 5 minutes")
    st.write(f"**Selected Targets:** {', '.join(targets)}")
    st.write("")
    st.write("**Instructions:** Click Start to begin the 5-minute exercise session")
    
    if st.button(f"🎯 Start {exercise} Exercise", type="primary", use_container_width=True, size="large"):
        start_exercise(exercise)
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Compact Assessment Section
st.markdown("---")
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Session Recording")
        if st.button("💾 Save Session Results", use_container_width=True) and not st.session_state.exercise_started:
            session_data = {
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'patient': patient_name,
                'exercise': exercise,
                'npc_cm': npc,
                'npa_cm': npa,
                'score': random.randint(70, 95),
                'duration': 5
            }
            st.session_state.session_data.append(session_data)
            st.success("Session saved successfully!")
    
    with col2:
        st.subheader("Progress Reports")
        if st.session_state.session_data:
            if st.button("📊 Generate Report", use_container_width=True):
                df = pd.DataFrame(st.session_state.session_data)
                st.dataframe(df, use_container_width=True)
                
                # Simple progress summary
                if len(df) > 1:
                    st.write("**Progress Summary:**")
                    npc_improvement = df['npc_cm'].iloc[0] - df['npc_cm'].iloc[-1]
                    npa_improvement = df['npa_cm'].iloc[0] - df['npa_cm'].iloc[-1]
                    if npc_improvement > 0:
                        st.success(f"NPC Improvement: +{npc_improvement:.2f} cm")
                    if npa_improvement > 0:
                        st.success(f"NPA Improvement: +{npa_improvement:.2f} cm")

# Compact Footer
st.markdown("---")
st.markdown("**Developed by Toni Mandusc** | *Vision Therapy Professional Application* | © 2024 VisionQuest")

# Disclaimer in expander at the bottom
with st.expander("⚠️ Medical Disclaimer"):
    st.markdown("""
    **For qualified eye care professionals only.** 
    - All measurements and exercises should be conducted under professional supervision
    - Results should be interpreted by licensed optometrists or orthoptists  
    - This tool is not a substitute for professional medical diagnosis
    - Always verify measurements with standard clinical instruments
    """)