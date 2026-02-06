import streamlit as st
from groq import Groq
import json
import os
from dotenv import load_dotenv
import random
import time

load_dotenv()

# Initialize Groq client with API key from environment variable
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Initialize session state
def init_session_state():
    if 'level' not in st.session_state:
        st.session_state.level = 1
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'wrong_attempts' not in st.session_state:
        st.session_state.wrong_attempts = 0
    if 'highest_level' not in st.session_state:
        st.session_state.highest_level = 1
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'achievements' not in st.session_state:
        st.session_state.achievements = set()
    if 'show_celebration' not in st.session_state:
        st.session_state.show_celebration = False

# Custom CSS with dark mode support
def load_custom_css():
    st.markdown("""
        <style>
        /* Dark mode compatible question box */
        .question-box {
            padding: 20px;
            border-radius: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            margin: 20px 0;
            border: 2px solid #4169e1;
            color: inherit;
        }
        
        /* Achievement animation */
        .achievement-unlocked {
            padding: 10px;
            background-color: #ffd700;
            border-radius: 5px;
            color: #000;
            text-align: center;
            animation: glow 1s ease-in-out infinite alternate;
            margin: 10px 0;
        }
        
        @keyframes glow {
            from { box-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #ffd700; }
            to { box-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #ffd700; }
        }
        
        /* Streak counter */
        .streak-counter {
            font-size: 24px;
            font-weight: bold;
            color: #ff4b4b;
            margin: 10px 0;
        }
        
        /* Custom button styles */
        .stButton > button {
            width: 100%;
            margin: 5px 0;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        /* Radio button spacing */
        .stRadio > div {
            margin: 10px 0;
        }
        </style>
    """, unsafe_allow_html=True)

def generate_question(level):
    try:
        difficulty = "basic" if level <= 3 else "intermediate" if level <= 6 else "advanced"
        
        prompt = f"""Generate a {difficulty} multiple-choice question about space exploration, Mars, or astronomy.
        The response should be in this exact JSON format:
        {{
            "question": "The question text here",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_index": 0,
            "explanation": "Detailed explanation why this is correct"
        }}
        Make sure the difficulty matches level {level}."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",

            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error generating question: {str(e)}")
        return None

def celebrate_correct_answer():
    # Trigger balloons
    st.balloons()
    
    # Success message with animation
    st.markdown("""
        <div style="animation: fadeIn 1s">
            <h2 style="color: #00ff00; text-align: center;">🎉 Correct Answer! 🎉</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Celebration messages
    messages = [
        "Amazing work, Space Cadet! 🌟",
        "You're a Cosmic Genius! 🚀",
        "Keep reaching for the stars! ⭐",
        "Astronomical knowledge! 🌍",
        "Out of this world! 🌌"
    ]
    message = messages[st.session_state.level % len(messages)]
    st.markdown(f"### {message}")
    
    # Add celebration state
    st.session_state.show_celebration = True

def main():
    load_custom_css()
    
    if not os.getenv('GROQ_API_KEY'):
        st.error("Please set your GROQ_API_KEY environment variable before running the app.")
        st.stop()
    
    init_session_state()
    
    # Welcome screen
    if not st.session_state.username:
        st.title("🌌 Welcome to Space Explorer Quiz!")
        st.markdown("""
            Embark on an incredible journey through space! Test your knowledge of astronomy, 
            space exploration, and the mysteries of the cosmos.
        """)
        username = st.text_input("Enter your space explorer name:")
        if username:
            st.session_state.username = username
            st.balloons()
            st.success(f"Welcome aboard, Space Explorer {username}! 🚀")
            time.sleep(1)  # Brief pause for effect
            st.rerun()
    
    else:
        st.title(f"🚀 Space Explorer Quiz - Navigator {st.session_state.username}")
        
        # Sidebar stats
        with st.sidebar:
            st.markdown("### 📊 Mission Stats")
            st.markdown(f"🏆 Highest Level: {st.session_state.highest_level}")
            st.markdown(f"📈 Current Score: {st.session_state.score}")
            
            # Animated streak counter
            if st.session_state.streak > 0:
                st.markdown(f"""
                    <div class='streak-counter'>
                        🔥 Streak: {st.session_state.streak}
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"📝 Total Questions: {st.session_state.total_questions}")
        
        # Main quiz interface
        st.header(f"Level {st.session_state.level}")
        progress = min(st.session_state.level / 10, 1.0)
        st.progress(progress, text=f"Mission Progress: {int(progress * 100)}%")
        
        if 'quiz_started' not in st.session_state:
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                if st.button("🚀 Launch Mission", use_container_width=True):
                    st.session_state.quiz_started = True
                    st.rerun()
        else:
            if not st.session_state.current_question:
                with st.spinner("Preparing next challenge..."):
                    question_data = generate_question(st.session_state.level)
                    if question_data:
                        st.session_state.current_question = question_data
                    else:
                        st.error("Failed to generate question. Please try again.")
                        st.stop()
            
            # Question display with dark mode support
            st.markdown(f"""
            <div class='question-box'>
                <h3>{st.session_state.current_question['question']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Answer options
            selected_option = st.radio(
                "Select your answer:", 
                st.session_state.current_question['options'],
                key=f"question_{st.session_state.level}"
            )
            
            col1, col2 = st.columns([1, 2])
            with col1:
                if st.button("🚀 Submit Answer", use_container_width=True):
                    correct_index = st.session_state.current_question['correct_index']
                    if selected_option == st.session_state.current_question['options'][correct_index]:
                        celebrate_correct_answer()
                        st.session_state.level += 1
                        st.session_state.score += (10 - st.session_state.wrong_attempts)
                        st.session_state.streak += 1
                        st.session_state.total_questions += 1
                        st.session_state.highest_level = max(st.session_state.highest_level, st.session_state.level)
                        
                        # Show celebration before clearing question
                        time.sleep(1)  # Brief pause for celebration
                        st.session_state.current_question = None
                        st.session_state.wrong_attempts = 0
                        st.rerun()
                    else:
                        st.session_state.wrong_attempts += 1
                        st.session_state.streak = 0
                        st.error("❌ Not quite right! Try again!")
                        if st.session_state.wrong_attempts >= 2:
                            st.markdown(f"💡 **Hint:** {st.session_state.current_question['explanation']}")
            
            with col2:
                if st.button("🔄 Start New Mission", use_container_width=True):
                    for key in ['level', 'current_question', 'wrong_attempts', 'quiz_started', 'score', 'streak']:
                        st.session_state[key] = 0 if key != 'current_question' else None
                    st.session_state.level = 1
                    st.rerun()

if __name__ == "__main__":
    main()