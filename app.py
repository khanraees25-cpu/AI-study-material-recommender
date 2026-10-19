import streamlit as st
import math
import re
from collections import Counter
from datetime import date, timedelta

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="StudyAI - Smart Study Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,0.18), transparent 25%),
        radial-gradient(circle at 90% 20%, rgba(168,85,247,0.15), transparent 25%),
        #090b14;
    color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1400px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #0e111d;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white;
}

/* Main title */

.hero {
    padding: 30px;
    border-radius: 24px;
    background:
        linear-gradient(135deg,
        rgba(99,102,241,0.30),
        rgba(168,85,247,0.20),
        rgba(14,165,233,0.12));
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 15px 50px rgba(0,0,0,0.30);
    margin-bottom: 25px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin: 0;
}

.hero-subtitle {
    font-size: 17px;
    color: #cbd5e1;
    margin-top: 8px;
}

.badge {
    display: inline-block;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 7px 14px;
    border-radius: 30px;
    font-size: 13px;
    margin-top: 15px;
}

/* Cards */

.card {
    background: rgba(20,24,38,0.85);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
}

.card:hover {
    border-color: rgba(129,140,248,0.5);
}

.material-title {
    font-size: 21px;
    font-weight: 700;
    color: #ffffff;
}

.material-desc {
    color: #aeb8cc;
    font-size: 14px;
    line-height: 1.6;
}

.score {
    font-size: 28px;
    font-weight: 800;
    color: #a5b4fc;
}

.reason {
    background: rgba(99,102,241,0.10);
    border-left: 3px solid #818cf8;
    padding: 10px 14px;
    border-radius: 8px;
    color: #dbeafe;
    font-size: 13px;
}

.priority-high {
    color: #fca5a5;
    font-weight: 700;
}

.priority-medium {
    color: #fde68a;
    font-weight: 700;
}

.priority-low {
    color: #86efac;
    font-weight: 700;
}

/* Metrics */

.metric-card {
    background: rgba(20,24,38,0.85);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 18px;
    text-align: center;
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    color: #c4b5fd;
}

.metric-label {
    font-size: 13px;
    color: #94a3b8;
}

/* Tabs */

button[data-baseweb="tab"] {
    font-size: 15px;
}

/* Buttons */

.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.10);
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #a5b4fc;
    transform: translateY(-1px);
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "completed" not in st.session_state:
    st.session_state.completed = []

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "uploaded_materials" not in st.session_state:
    st.session_state.uploaded_materials = []

if "study_days" not in st.session_state:
    st.session_state.study_days = 7

# ============================================================
# DATASET
# ============================================================

materials = [

    {
        "title": "Python Programming Fundamentals",
        "subject": "Python",
        "topic": "Programming",
        "difficulty": "Beginner",
        "type": "Video",
        "style": "Visual",
        "duration": 35,
        "rating": 4.8,
        "description": "Learn Python variables, loops, functions and basic programming concepts.",
        "keywords": ["python", "programming", "loops", "functions", "variables"]
    },

    {
        "title": "Python Practice Problems",
        "subject": "Python",
        "topic": "Programming",
        "difficulty": "Intermediate",
        "type": "Practice",
        "style": "Practice",
        "duration": 45,
        "rating": 4.7,
        "description": "Hands-on programming problems to improve Python problem-solving skills.",
        "keywords": ["python", "coding", "practice", "problems", "functions"]
    },

    {
        "title": "DBMS Complete Revision Notes",
        "subject": "DBMS",
        "topic": "Database",
        "difficulty": "Beginner",
        "type": "Notes",
        "style": "Reading",
        "duration": 30,
        "rating": 4.9,
        "description": "Quick revision notes covering DBMS fundamentals, keys, normalization and SQL.",
        "keywords": ["dbms", "database", "sql", "normalization", "keys"]
    },

    {
        "title": "SQL Query Practice Lab",
        "subject": "DBMS",
        "topic": "SQL",
        "difficulty": "Intermediate",
        "type": "Practice",
        "style": "Practice",
        "duration": 50,
        "rating": 4.8,
        "description": "Practice SELECT, JOIN, GROUP BY, nested queries and database operations.",
        "keywords": ["sql", "query", "join", "database", "practice"]
    },

    {
        "title": "Computer Networks Visual Guide",
        "subject": "Computer Networks",
        "topic": "Networking",
        "difficulty": "Beginner",
        "type": "Video",
        "style": "Visual",
        "duration": 40,
        "rating": 4.9,
        "description": "Understand OSI model, TCP/IP, routers, switches and networking protocols.",
        "keywords": ["network", "osi", "tcp", "ip", "router", "switch"]
    },

    {
        "title": "Computer Networks Exam Notes",
        "subject": "Computer Networks",
        "topic": "Networking",
        "difficulty": "Intermediate",
        "type": "Notes",
        "style": "Reading",
        "duration": 25,
        "rating": 4.6,
        "description": "Exam-oriented notes for important Computer Networks concepts.",
        "keywords": ["network", "exam", "tcp", "ip", "protocols"]
    },

    {
        "title": "Machine Learning Made Easy",
        "subject": "Machine Learning",
        "topic": "AI",
        "difficulty": "Beginner",
        "type": "Video",
        "style": "Visual",
        "duration": 45,
        "rating": 4.9,
        "description": "Simple explanation of supervised learning, regression and classification.",
        "keywords": ["machine learning", "ai", "supervised", "regression", "classification"]
    },

    {
        "title": "ML Algorithms Cheat Sheet",
        "subject": "Machine Learning",
        "topic": "Algorithms",
        "difficulty": "Intermediate",
        "type": "Notes",
        "style": "Reading",
        "duration": 25,
        "rating": 4.8,
        "description": "Quick revision of Linear Regression, Decision Trees, KNN and other algorithms.",
        "keywords": ["ml", "algorithms", "regression", "knn", "decision tree"]
    },

    {
        "title": "Machine Learning Coding Practice",
        "subject": "Machine Learning",
        "topic": "Programming",
        "difficulty": "Advanced",
        "type": "Practice",
        "style": "Practice",
        "duration": 60,
        "rating": 4.7,
        "description": "Implement machine learning algorithms using Python.",
        "keywords": ["machine learning", "python", "coding", "algorithms"]
    },

    {
        "title": "Data Structures Quick Revision",
        "subject": "DSA",
        "topic": "Data Structures",
        "difficulty": "Intermediate",
        "type": "Notes",
        "style": "Reading",
        "duration": 30,
        "rating": 4.7,
        "description": "Arrays, stacks, queues, linked lists, trees and searching algorithms.",
        "keywords": ["dsa", "array", "stack", "queue", "tree", "searching"]
    },

    {
        "title": "DSA Problem Solving Session",
        "subject": "DSA",
        "topic": "Algorithms",
        "difficulty": "Advanced",
        "type": "Practice",
        "style": "Practice",
        "duration": 60,
        "rating": 4.9,
        "description": "Solve algorithmic problems and improve logical thinking.",
        "keywords": ["dsa", "algorithm", "problem", "coding", "practice"]
    },

    {
        "title": "Theory of Computation Simplified",
        "subject": "TOC",
        "topic": "Automata",
        "difficulty": "Beginner",
        "type": "Video",
        "style": "Visual",
        "duration": 35,
        "rating": 4.8,
        "description": "Understand DFA, NFA, regular expressions and finite automata.",
        "keywords": ["toc", "dfa", "nfa", "automata", "regex"]
    },

    {
        "title": "TOC Exam Questions",
        "subject": "TOC",
        "topic": "Automata",
        "difficulty": "Intermediate",
        "type": "Practice",
        "style": "Practice",
        "duration": 40,
        "rating": 4.6,
        "description": "Important exam questions and practice problems from Theory of Computation.",
        "keywords": ["toc", "exam", "dfa", "nfa", "automata"]
    }
]

# ============================================================
# PURE PYTHON TF-IDF
# ============================================================

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def cosine_similarity(text1, text2):

    words1 = tokenize(text1)
    words2 = tokenize(text2)

    if not words1 or not words2:
        return 0

    c1 = Counter(words1)
    c2 = Counter(words2)

    all_words = set(c1) | set(c2)

    dot = sum(c1[w] * c2[w] for w in all_words)

    mag1 = math.sqrt(sum(v * v for v in c1.values()))
    mag2 = math.sqrt(sum(v * v for v in c2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot / (mag1 * mag2)


# ============================================================
# AI RECOMMENDATION ENGINE
# ============================================================

def recommend_materials(subject, difficulty, style, max_time, exam_days, query=""):

    results = []

    for material in materials + st.session_state.uploaded_materials:

        score = 0
        reasons = []

        # Subject match
        if material["subject"] == subject:
            score += 35
            reasons.append("matches your selected subject")

        # Difficulty
        if material["difficulty"] == difficulty:
            score += 20
            reasons.append("matches your difficulty level")

        # Learning style
        if material["style"] == style:
            score += 15
            reasons.append("matches your learning style")

        # Time
        if material["duration"] <= max_time:
            score += 10
            reasons.append("fits your available study time")
        else:
            score -= 5

        # Exam urgency
        if exam_days <= 3:
            if material["type"] in ["Notes", "Practice"]:
                score += 15
                reasons.append("useful for quick exam preparation")

        elif exam_days <= 7:
            if material["type"] in ["Notes", "Practice"]:
                score += 8

        # Rating
        score += material["rating"] * 2

        # Search similarity
        if query.strip():

            material_text = (
                material["title"] + " " +
                material["description"] + " " +
                " ".join(material["keywords"])
            )

            similarity = cosine_similarity(query, material_text)

            score += similarity * 25

            if similarity > 0.15:
                reasons.append("matches your search")

        score = min(100, max(0, round(score)))

        results.append({
            "material": material,
            "score": score,
            "reasons": reasons
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🎓 StudyAI")

    st.caption("Your intelligent study companion")

    st.divider()

    page = st.radio(
        "Navigate",
        [
            "🏠 Dashboard",
            "🤖 AI Recommendations",
            "📅 Smart Study Planner",
            "📝 Quick Quiz",
            "📄 Upload Material",
            "⭐ My Favorites"
        ]
    )

    st.divider()

    st.markdown("### ⚙️ Student Profile")

    student_name = st.text_input(
        "Your name",
        "Student"
    )

    study_goal = st.selectbox(
        "Main goal",
        [
            "Exam Preparation",
            "Concept Understanding",
            "Programming Practice",
            "Quick Revision",
            "Assignment Preparation"
        ]
    )

    st.divider()

    st.caption("AI Study Material Recommender")
    st.caption("Content-based recommendation system")


# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">

<div class="hero-title">
🎓 StudyAI
</div>

<div class="hero-subtitle">
Your personal AI-powered study material recommender.
Find the right material based on your subject, difficulty,
learning style, time and exam urgency.
</div>

<div class="badge">
🤖 Smart Recommendation Engine &nbsp; • &nbsp;
📚 Personalized Learning &nbsp; • &nbsp;
📊 Progress Tracking
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.subheader(f"👋 Welcome, {student_name}!")

    completed_count = len(st.session_state.completed)
    favorite_count = len(st.session_state.favorites)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-number">13+</div>
        <div class="metric-label">Study Materials</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-number">{completed_count}</div>
        <div class="metric-label">Completed</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-number">{favorite_count}</div>
        <div class="metric-label">Favorites</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        progress = min(100, completed_count * 10)

        st.markdown(f"""
        <div class="metric-card">
        <div class="metric-number">{progress}%</div>
        <div class="metric-label">Progress</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.subheader("🚀 What would you like to do?")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown("""
        <div class="card">

        <div style="font-size:35px;">🤖</div>

        <h3>AI Recommendations</h3>

        <p class="material-desc">
        Tell StudyAI what you want to learn and receive
        personalized study materials.
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button("Find Materials →", key="find"):
            st.info("Select 🤖 AI Recommendations from the sidebar.")

    with c2:

        st.markdown("""
        <div class="card">

        <div style="font-size:35px;">📅</div>

        <h3>Smart Study Plan</h3>

        <p class="material-desc">
        Create a simple daily plan based on your exam date
        and available study hours.
        </p>

        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown("""
        <div class="card">

        <div style="font-size:35px;">🧠</div>

        <h3>Quick Quiz</h3>

        <p class="material-desc">
        Test your understanding with topic-based questions.
        </p>

        </div>
        """, unsafe_allow_html=True)

    st.subheader("🔥 Popular Study Areas")

    subjects = Counter([m["subject"] for m in materials])

    cols = st.columns(len(subjects))

    for col, (subject, count) in zip(cols, subjects.items()):

        with col:

            st.markdown(f"""
            <div class="card" style="text-align:center;">

            <div style="font-size:30px;">📚</div>

            <b>{subject}</b>

            <p class="material-desc">
            {count} resources
            </p>

            </div>
            """, unsafe_allow_html=True)


# ============================================================
# AI RECOMMENDATIONS
# ============================================================

elif page == "🤖 AI Recommendations":

    st.subheader("🤖 AI Study Material Recommender")

    st.write(
        "Answer a few questions and StudyAI will calculate "
        "a personalized recommendation score."
    )

    col1, col2 = st.columns(2)

    with col1:

        subject = st.selectbox(
            "📚 What do you want to study?",
            sorted(set(m["subject"] for m in materials))
        )

        difficulty = st.selectbox(
            "🎯 Your level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        style = st.selectbox(
            "🧠 How do you learn best?",
            ["Visual", "Reading", "Practice"]
        )

    with col2:

        max_time = st.slider(
            "⏱️ Available time per resource (minutes)",
            10,
            120,
            45
        )

        exam_days = st.slider(
            "📅 Days remaining before exam",
            1,
            30,
            7
        )

        query = st.text_input(
            "🔎 What specific topic are you looking for?",
            placeholder="e.g. SQL joins, Python loops, DFA..."
        )

    st.divider()

    if st.button("✨ Generate AI Recommendations", use_container_width=True):

        results = recommend_materials(
            subject,
            difficulty,
            style,
            max_time,
            exam_days,
            query
        )

        st.success(
            f"Found {len(results)} personalized recommendations!"
        )

        for index, result in enumerate(results[:6]):

            m = result["material"]
            score = result["score"]

            if score >= 75:
                priority = "HIGH"
                priority_class = "priority-high"
            elif score >= 50:
                priority = "MEDIUM"
                priority_class = "priority-medium"
            else:
                priority = "LOW"
                priority_class = "priority-low"

            st.markdown(f"""
            <div class="card">

            <div style="display:flex; justify-content:space-between;">

            <div>

            <div class="material-title">
            {index + 1}. {m["title"]}
            </div>

            <p class="material-desc">
            {m["description"]}
            </p>

            </div>

            <div style="text-align:right;">

            <div class="score">
            {score}%
            </div>

            <div class="{priority_class}">
            {priority} PRIORITY
            </div>

            </div>

            </div>

            <hr style="border-color:rgba(255,255,255,0.08);">

            <span>📚 {m["subject"]}</span>
            &nbsp;&nbsp;
            <span>📖 {m["type"]}</span>
            &nbsp;&nbsp;
            <span>⏱️ {m["duration"]} min</span>
            &nbsp;&nbsp;
            <span>⭐ {m["rating"]}</span>

            <br><br>

            <div class="reason">
            💡 Why recommended:
            {", ".join(result["reasons"])}
            </div>

            </div>
            """, unsafe_allow_html=True)

            b1, b2 = st.columns(2)

            with b1:

                if st.button(
                    "⭐ Add to Favorites",
                    key=f"fav_{index}"
                ):

                    if m["title"] not in st.session_state.favorites:
                        st.session_state.favorites.append(m["title"])

                    st.toast("Added to favorites! ⭐")

            with b2:

                if st.button(
                    "✅ Mark Completed",
                    key=f"done_{index}"
                ):

                    if m["title"] not in st.session_state.completed:
                        st.session_state.completed.append(m["title"])

                    st.toast("Material completed! 🎉")


# ============================================================
# STUDY PLANNER
# ============================================================

elif page == "📅 Smart Study Planner":

    st.subheader("📅 Smart Study Planner")

    st.write(
        "Create a simple personalized study schedule."
    )

    exam_date = st.date_input(
        "📆 Select your exam date",
        date.today() + timedelta(days=7)
    )

    daily_hours = st.slider(
        "⏰ Hours available per day",
        1,
        10,
        3
    )

    subjects = st.multiselect(
        "📚 Select subjects",
        sorted(set(m["subject"] for m in materials)),
        default=["Python", "DBMS"]
    )

    if st.button("🪄 Generate Study Plan", use_container_width=True):

        today = date.today()

        days_left = max(
            1,
            (exam_date - today).days
        )

        total_hours = days_left * daily_hours

        st.success(
            f"You have approximately {days_left} days and "
            f"{total_hours} study hours available."
        )

        if not subjects:
            st.warning("Please select at least one subject.")

        else:

            for i in range(min(days_left, 14)):

                current_day = today + timedelta(days=i)

                subject = subjects[i % len(subjects)]

                if i == 0:
                    task = "Start with important concepts"
                elif i % 3 == 1:
                    task = "Study concepts + make notes"
                elif i % 3 == 2:
                    task = "Solve practice questions"
                else:
                    task = "Revise + self-test"

                st.markdown(f"""
                <div class="card">

                <b>Day {i + 1} — {current_day.strftime("%d %b")}</b>

                <p class="material-desc">
                📚 Subject: <b>{subject}</b><br>
                🎯 Task: {task}<br>
                ⏰ Study time: {daily_hours} hour(s)
                </p>

                </div>
                """, unsafe_allow_html=True)


# ============================================================
# QUIZ
# ============================================================

elif page == "📝 Quick Quiz":

    st.subheader("🧠 Quick Knowledge Quiz")

    quiz_topic = st.selectbox(
        "Choose a topic",
        [
            "Python",
            "DBMS",
            "Computer Networks",
            "Machine Learning",
            "DSA",
            "TOC"
        ]
    )

    quiz_questions = {

        "Python": [
            {
                "q": "Which keyword is used to define a function in Python?",
                "options": ["func", "define", "def", "function"],
                "answer": "def"
            },
            {
                "q": "Which data type stores key-value pairs?",
                "options": ["List", "Tuple", "Dictionary", "Set"],
                "answer": "Dictionary"
            }
        ],

        "DBMS": [
            {
                "q": "What does SQL stand for?",
                "options": [
                    "Structured Query Language",
                    "Simple Query Language",
                    "System Query Language",
                    "Sequential Query Language"
                ],
                "answer": "Structured Query Language"
            },
            {
                "q": "Which key uniquely identifies a record?",
                "options": [
                    "Foreign Key",
                    "Primary Key",
                    "Candidate Key",
                    "Composite Key"
                ],
                "answer": "Primary Key"
            }
        ],

        "Computer Networks": [
            {
                "q": "Which device connects different networks?",
                "options": [
                    "Switch",
                    "Router",
                    "Hub",
                    "Repeater"
                ],
                "answer": "Router"
            },
            {
                "q": "How many layers are there in the OSI model?",
                "options": ["5", "6", "7", "8"],
                "answer": "7"
            }
        ],

        "Machine Learning": [
            {
                "q": "Which is a supervised learning algorithm?",
                "options": [
                    "Linear Regression",
                    "K-Means",
                    "PCA",
                    "Apriori"
                ],
                "answer": "Linear Regression"
            },
            {
                "q": "What is used as the input to an ML model?",
                "options": [
                    "Features",
                    "Labels only",
                    "Output",
                    "Accuracy"
                ],
                "answer": "Features"
            }
        ],

        "DSA": [
            {
                "q": "Which data structure follows LIFO?",
                "options": [
                    "Queue",
                    "Stack",
                    "Array",
                    "Tree"
                ],
                "answer": "Stack"
            },
            {
                "q": "Which structure follows FIFO?",
                "options": [
                    "Stack",
                    "Queue",
                    "Tree",
                    "Graph"
                ],
                "answer": "Queue"
            }
        ],

        "TOC": [
            {
                "q": "What does DFA stand for?",
                "options": [
                    "Deterministic Finite Automaton",
                    "Digital Finite Algorithm",
                    "Dynamic Finite Automaton",
                    "Deterministic Functional Algorithm"
                ],
                "answer": "Deterministic Finite Automaton"
            },
            {
                "q": "Which machine accepts regular languages?",
                "options": [
                    "Finite Automaton",
                    "Turing Machine only",
                    "Stack",
                    "Compiler"
                ],
                "answer": "Finite Automaton"
            }
        ]
    }

    questions = quiz_questions[quiz_topic]

    answers = []

    for i, q in enumerate(questions):

        st.markdown(f"### Q{i + 1}. {q['q']}")

        answer = st.radio(
            "Choose answer:",
            q["options"],
            key=f"quiz_{quiz_topic}_{i}"
        )

        answers.append(answer)

    if st.button("🎯 Check My Score"):

        score = 0

        for i, q in enumerate(questions):

            if answers[i] == q["answer"]:
                score += 1

        percentage = int(
            score / len(questions) * 100
        )

        st.success(
            f"🎉 You scored {score}/{len(questions)} ({percentage}%)"
        )

        if percentage == 100:
            st.balloons()
            st.success("Excellent! 🔥")

        elif percentage >= 50:
            st.info("Good job! Revise the incorrect concepts.")

        else:
            st.warning(
                "You should review this topic before moving ahead."
            )


# ============================================================
# PDF UPLOAD
# ============================================================

elif page == "📄 Upload Material":

    st.subheader("📄 Upload Your Own Study Material")

    st.write(
        "Upload a PDF and StudyAI will extract basic information "
        "from it and add it to your personal study library."
    )

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        try:

            from pypdf import PdfReader

            reader = PdfReader(uploaded_file)

            text = ""

            for page_data in reader.pages:

                extracted = page_data.extract_text()

                if extracted:
                    text += extracted

            word_count = len(text.split())

            st.metric(
                "Extracted Words",
                word_count
            )

            subject = st.selectbox(
                "Assign Subject",
                sorted(set(m["subject"] for m in materials))
            )

            if st.button("➕ Add to My Study Library"):

                new_material = {
                    "title": uploaded_file.name,
                    "subject": subject,
                    "topic": "Uploaded Material",
                    "difficulty": "Intermediate",
                    "type": "PDF",
                    "style": "Reading",
                    "duration": max(15, min(120, word_count // 100)),
                    "rating": 4.5,
                    "description":
                        f"Your uploaded study material containing approximately {word_count} words.",
                    "keywords": tokenize(text[:1000])
                }

                st.session_state.uploaded_materials.append(
                    new_material
                )

                st.success(
                    "📚 Added successfully! It can now appear in AI recommendations."
                )

        except Exception as e:

            st.error(
                f"Could not read the PDF: {e}"
            )


# ============================================================
# FAVORITES
# ============================================================

elif page == "⭐ My Favorites":

    st.subheader("⭐ My Favorite Materials")

    if not st.session_state.favorites:

        st.info(
            "You haven't saved any materials yet. "
            "Go to AI Recommendations and add some! ⭐"
        )

    else:

        for favorite in st.session_state.favorites:

            matching = [
                m for m in materials + st.session_state.uploaded_materials
                if m["title"] == favorite
            ]

            if matching:

                m = matching[0]

                st.markdown(f"""
                <div class="card">

                <div class="material-title">
                ⭐ {m["title"]}
                </div>

                <p class="material-desc">
                {m["description"]}
                </p>

                📚 {m["subject"]}
                &nbsp;&nbsp;
                📖 {m["type"]}
                &nbsp;&nbsp;
                ⏱️ {m["duration"]} min
                &nbsp;&nbsp;
                ⭐ {m["rating"]}

                </div>
                """, unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<br><br>

<div style="
text-align:center;
color:#64748b;
padding:25px;
border-top:1px solid rgba(255,255,255,0.08);
">

🎓 <b>StudyAI</b> — AI Study Material Recommender

<br>

Personalized learning • Smart recommendations • Better preparation

</div>

""", unsafe_allow_html=True)