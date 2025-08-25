import streamlit as st
st.set_page_config(
    page_title="TalentScout Hiring Assistant", 
    page_icon="🤖",
    layout="wide"
)

from langchain_ollama import OllamaLLM
import sqlite3
import re
import json
@st.cache_resource
def init_llm():
    try:
        return OllamaLLM(model='llama3', temperature=0.5)
    except Exception as e:
        st.error(f"Error initializing LLM: {e}")
        return None

llm = init_llm()
@st.cache_resource
def init_database():
    conn = sqlite3.connect("talent_scout.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        experience INTEGER,
        position TEXT,
        location TEXT,
        tech_stack TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    c.execute("PRAGMA table_info(answers)")
    columns = [column[1] for column in c.fetchall()]
    
    if 'answers' not in [table[0] for table in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]:
        # Create table if it doesn't exist
        c.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER,
            question TEXT,
            user_answer TEXT,
            correct_answer TEXT,
            is_correct BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(candidate_id) REFERENCES candidates(id)
        )
        """)
    elif 'is_correct' not in columns:
        c.execute("ALTER TABLE answers ADD COLUMN is_correct BOOLEAN DEFAULT 0")
    
    conn.commit()
    return conn

conn = init_database()
def init_session_states():
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    
    if "greeted" not in st.session_state:
        st.session_state.greeted = False
    
    if "mcq_index" not in st.session_state:
        st.session_state.mcq_index = 0
        
    if "mcqs" not in st.session_state:
        st.session_state.mcqs = []
        
    if "candidate_id" not in st.session_state:
        st.session_state.candidate_id = None
        
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
        
    if "mcq_completed" not in st.session_state:
        st.session_state.mcq_completed = False

init_session_states()
def parse_mcqs_improved(mcq_text, tech_stack):
    """Improved MCQ parsing with better error handling"""
    mcqs = []
    question_pattern = r'Q(?:uestion)?\s*\d*\s*:?\s*(.*?)(?=\n|$)'
    options_pattern = r'([A-D])\)\s*(.*?)(?=\n|$)'
    answer_pattern = r'Answer:\s*([A-D])'
    blocks = re.split(r'\n\n+|(?=Q(?:uestion)?\s*\d+)', mcq_text)
    
    for block in blocks:
        if not block.strip():
            continue
        question_match = re.search(question_pattern, block, re.IGNORECASE)
        if not question_match:
            continue
            
        question = question_match.group(1).strip()
        if not question:
            continue
        options = {}
        option_matches = re.findall(options_pattern, block, re.IGNORECASE)
        for letter, text in option_matches:
            options[letter.upper()] = text.strip()
        answer_match = re.search(answer_pattern, block, re.IGNORECASE)
        if not answer_match or len(options) < 2:
            continue
            
        correct_answer = answer_match.group(1).upper()
        
        if correct_answer in options:
            mcqs.append({
                "question": question,
                "options": options,
                "correct": correct_answer
            })
    
    return mcqs[:5]  # Limit to 5 questions

def generate_mcqs(tech_stack):
    """Generate MCQs with improved prompt and error handling"""
    if not llm:
        st.error("LLM not available. Cannot generate questions.")
        return []
    
    try:
        prompt_mcq = f"""
        Generate exactly 5 multiple-choice technical questions for a candidate with experience in: {tech_stack}

        Use this EXACT format for each question:

        Question 1: [Your question here]
        A) Option A
        B) Option B  
        C) Option C
        D) Option D
        Answer: A

        Question 2: [Your question here]
        A) Option A
        B) Option B
        C) Option C  
        D) Option D
        Answer: B

        Make questions practical and relevant to the technologies mentioned. Ensure exactly one correct answer per question.
        """
        
        with st.spinner("Generating technical questions..."):
            mcq_text = llm.invoke(prompt_mcq)
            
        mcqs = parse_mcqs_improved(mcq_text, tech_stack)
        
        if len(mcqs) < 3:
            st.warning("Could not generate enough questions. Using fallback questions.")
            return get_fallback_mcqs(tech_stack)
            
        return mcqs
        
    except Exception as e:
        st.error(f"Error generating MCQs: {e}")
        return get_fallback_mcqs(tech_stack)

def get_fallback_mcqs(tech_stack):
    """Fallback MCQs in case generation fails"""
    fallback_questions = [
        {
            "question": "What is the primary purpose of version control systems like Git?",
            "options": {
                "A": "To compile code",
                "B": "To track changes in code over time",
                "C": "To deploy applications", 
                "D": "To test code quality"
            },
            "correct": "B"
        },
        {
            "question": "Which HTTP method is typically used to retrieve data from a server?",
            "options": {
                "A": "POST",
                "B": "PUT",
                "C": "GET",
                "D": "DELETE"
            },
            "correct": "C"
        },
        {
            "question": "What does API stand for?",
            "options": {
                "A": "Application Programming Interface",
                "B": "Advanced Programming Instructions",
                "C": "Automated Program Integration",
                "D": "Application Process Integration"
            },
            "correct": "A"
        },
        {
            "question": "What is the difference between == and === in JavaScript?",
            "options": {
                "A": "No difference",
                "B": "== checks type and value, === checks only value",
                "C": "== checks only value, === checks type and value",
                "D": "=== is used for assignment"
            },
            "correct": "C"
        },
        {
            "question": "Which database type is MongoDB?",
            "options": {
                "A": "Relational database",
                "B": "Graph database",
                "C": "Document database (NoSQL)",
                "D": "Key-value database"
            },
            "correct": "C"
        }
    ]
    return fallback_questions

def safe_db_operation(operation_func, *args, **kwargs):
    """Safely execute database operations with error handling"""
    try:
        return operation_func(*args, **kwargs)
    except Exception as e:
        st.error(f"Database error: {e}")
        return None
st.title("🎯 TalentScout Hiring Assistant")
if not st.session_state.greeted:
    st.info("👋 Hello! Welcome to TalentScout Hiring Assistant. I will guide you through the initial screening process and ask technical questions about your experience.")
    st.session_state.greeted = True

# ---------------- Candidate Info Form ---------------- #
if not st.session_state.form_submitted:
    st.subheader("📝 Candidate Information")
    
    with st.form("candidate_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            phone = st.text_input("Phone Number *")
        
        with col2:
            experience = st.number_input("Years of Experience *", min_value=0, max_value=50, value=0)
            positions = [
                "Frontend Developer", "Backend Developer", "Full Stack Developer",
                "Data Scientist", "DevOps Engineer", "Mobile App Developer",
                "QA Engineer", "UI/UX Designer", "Product Manager"
            ]
            position = st.selectbox("Desired Position *", positions)
            location = st.text_input("Current Location *")
        
        tech_stack = st.text_area("Tech Stack & Skills *", 
                                 placeholder="e.g., Python, Django, React, MySQL, Docker, AWS, Git")
        
        submitted = st.form_submit_button("Submit & Start Assessment", use_container_width=True)
    if submitted:
        if not all([full_name, email, phone, position, location, tech_stack]):
            st.warning("⚠️ Please fill out all required fields marked with * before submitting.")
        else:
            def save_candidate():
                c = conn.cursor()
                c.execute("""
                    INSERT INTO candidates (full_name,email,phone,experience,position,location,tech_stack) 
                    VALUES (?,?,?,?,?,?,?)
                """, (full_name, email, phone, experience, position, location, tech_stack))
                conn.commit()
                return c.lastrowid
            
            candidate_id = safe_db_operation(save_candidate)
            
            if candidate_id:
                st.session_state.candidate_id = candidate_id
                st.session_state.form_submitted = True
                st.session_state.conversation.append({
                    "role": "user",
                    "content": f"Candidate: {full_name} | Position: {position} | Tech Stack: {tech_stack}"
                })
                st.session_state.mcqs = generate_mcqs(tech_stack)
                
                st.success("✅ Information saved! Starting technical assessment...")
                st.rerun()

# ---------------- MCQ Round ---------------- #
if (st.session_state.form_submitted and 
    st.session_state.mcqs and 
    st.session_state.candidate_id and 
    not st.session_state.mcq_completed):
    
    st.subheader("🧠 Technical Assessment")
    
    current_index = st.session_state.mcq_index
    total_questions = len(st.session_state.mcqs)
    
    if current_index < total_questions:
        mcq = st.session_state.mcqs[current_index]
        progress = (current_index) / total_questions
        st.progress(progress, text=f"Question {current_index + 1} of {total_questions}")
        st.markdown(f"**Question {current_index + 1}:** {mcq['question']}")

        options_list = [f"{k}) {v}" for k, v in mcq['options'].items()]
        selected_option = st.radio("Select your answer:", options_list, 
                                 key=f"mcq_{current_index}")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Submit Answer", key=f"btn_{current_index}", 
                        use_container_width=True, type="primary"):
                
                # Get selected letter
                selected_letter = selected_option.split(')')[0]
                is_correct = selected_letter == mcq["correct"]
                def save_answer():
                    c = conn.cursor()
                    c.execute("PRAGMA table_info(answers)")
                    columns = [column[1] for column in c.fetchall()]
                    
                    if 'is_correct' in columns:
                        c.execute("""
                            INSERT INTO answers (candidate_id, question, user_answer, correct_answer, is_correct) 
                            VALUES (?,?,?,?,?)
                        """, (st.session_state.candidate_id, mcq["question"], 
                              selected_letter, mcq["correct"], is_correct))
                    else:
                        c.execute("""
                            INSERT INTO answers (candidate_id, question, user_answer, correct_answer) 
                            VALUES (?,?,?,?)
                        """, (st.session_state.candidate_id, mcq["question"], 
                              selected_letter, mcq["correct"]))
                    
                    conn.commit()
                    return True
                
                if safe_db_operation(save_answer):
                    # Show result
                    if is_correct:
                        st.success("✅ Correct!")
                    else:
                        correct_text = mcq['options'][mcq['correct']]
                        st.error(f"❌ Wrong! Correct answer: {mcq['correct']}) {correct_text}")
                    
                    # Move to next question
                    st.session_state.mcq_index += 1
                    
                    if st.session_state.mcq_index >= total_questions:
                        st.session_state.mcq_completed = True
                    import time
                    time.sleep(2)
                    st.rerun()
if st.session_state.mcq_completed:
    st.subheader("🎉 Assessment Completed!")
    def calculate_score():
        c = conn.cursor()
        
        c.execute("PRAGMA table_info(answers)")
        columns = [column[1] for column in c.fetchall()]
        
        if 'is_correct' in columns:
            c.execute("""
                SELECT COUNT(*) as total, 
                       SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
                FROM answers 
                WHERE candidate_id = ?
            """, (st.session_state.candidate_id,))
        else:
            c.execute("""
                SELECT user_answer, correct_answer
                FROM answers 
                WHERE candidate_id = ?
            """, (st.session_state.candidate_id,))
            
            results = c.fetchall()
            total = len(results)
            correct = sum(1 for user_ans, correct_ans in results if user_ans == correct_ans)
            return (total, correct)
        
        return c.fetchone()
    
    score_result = safe_db_operation(calculate_score)
    
    if score_result:
        total_questions = score_result[0] if score_result[0] else 0
        correct_answers = score_result[1] if score_result[1] else 0
        score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Questions", total_questions)
        with col2:
            st.metric("Correct Answers", correct_answers)
        with col3:
            st.metric("Score", f"{score_percentage:.1f}%")
        if score_percentage >= 80:
            st.success("🌟 Excellent performance! You're ready for the next round.")
        elif score_percentage >= 60:
            st.info("👍 Good job! Consider reviewing some concepts.")
        else:
            st.warning("📚 Keep learning! Review the fundamentals.")
            
        st.info("Thank you for completing the assessment. Our team will review your application and get back to you soon!")
    if st.button("Start New Assessment"):
        # Reset session states
        for key in ["form_submitted", "mcq_completed", "mcq_index", "mcqs", "candidate_id"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# ---------------- Display Conversation ---------------- #
if st.session_state.conversation:
    with st.expander("📝 Session Log"):
        for i, chat in enumerate(st.session_state.conversation):
            if chat["role"] == "user":
                st.markdown(f"**Candidate:** {chat['content']}")
            else:
                st.markdown(f"**TalentScout:** {chat['content']}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>TalentScout Hiring Assistant | "
    "Powered by AI 🤖</p>", 
    unsafe_allow_html=True
)