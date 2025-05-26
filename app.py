import streamlit as st 
from datetime import date
import json
import os

# Sample rule-based tasks
TASK_LIBRARY = {
    ("Data Analyst", "Networking"): "Send 2 LinkedIn connection requests to analysts",
    ("Data Scientist", "Portfolio Building"): "Update your GitHub with 1 new project",
    ("Software Engineer", "Interview Prep"): "Solve 2 DSA problems on LeetCode",
    ("Any", "Resume Upgrade"): "Refactor your resume with 1 new achievement",
}

# Initialize progress tracker
if "progress" not in st.session_state:
    st.session_state.progress = {}

# --- UI HEADER ---
st.title("📈 Connectora: Smart Working Growth Planner")
st.subheader("Daily Personalized Task Tracker")

# --- User Personalization Form ---
with st.form("user_form"):
    name = st.text_input("Your Name")
    role = st.selectbox("Select Your Role", ["Data Analyst", "Data Scientist", "Software Engineer", "Other"])
    goal = st.selectbox("Choose Your Current Focus Goal", ["Networking", "Portfolio Building", "Interview Prep", "Resume Upgrade"])
    submitted = st.form_submit_button("Generate Today's Task")

# --- Task Recommendation Logic ---
if submitted:
    today = str(date.today())
    key = (role, goal)
    fallback_key = ("Any", goal)
    
    task = TASK_LIBRARY.get(key) or TASK_LIBRARY.get(fallback_key) or "Take a 30-min break and reflect on your growth"
    
    st.session_state.progress[today] = {
        "name": name,
        "role": role,
        "goal": goal,
        "task": task,
        "status": "Pending"
    }

# --- Show Today's Task ---
today = str(date.today())
if today in st.session_state.progress:
    today_task = st.session_state.progress[today]
    st.write(f"### 🗓️ Task for {today}")
    st.info(f"👉 **{today_task['task']}**")
    
    # Mark as completed
    if st.button("✅ Mark as Done"):
        st.session_state.progress[today]["status"] = "Completed"
        st.success("Great job! Task marked as completed. ✅")

# --- Progress History ---
if st.checkbox("📊 Show Progress History"):
    st.write("### 📅 Your Past Tasks")
    for task_date, entry in st.session_state.progress.items():
        st.write(f"- `{task_date}`: {entry['task']} — **{entry['status']}**")

# --- Save to file (optional) ---
SAVE_FILE = "progress.json"

def save_progress():
    with open(SAVE_FILE, "w") as f:
        json.dump(st.session_state.progress, f)

def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            st.session_state.progress = json.load(f)

if st.button("💾 Save Progress"):
    save_progress()
    st.success("Progress saved!")

if st.button("🔄 Load Previous Progress"):
    load_progress()
    st.info("Progress loaded!")
