
import streamlit as st
from datetime import date, datetime, timedelta
import pandas as pd
import altair as alt
import ics

# --- Session Initialization ---
if "progress" not in st.session_state:
    st.session_state.progress = {}
    st.session_state.points = 0

# --- UI Header ---
st.title("📈 Connectora: Smart Working Growth Planner")
st.markdown("Plan your day with personalized career-building tasks and track your progress!")

# --- Task Library ---
TASK_LIBRARY = {
    ("Data Analyst", "Networking"): "Send 2 LinkedIn connection requests to analysts",
    ("Data Analyst", "Portfolio Building"): "Update your Tableau dashboard with new data",
    ("Data Analyst", "Interview Prep"): "Practice 3 SQL interview questions",
    ("Data Analyst", "Resume Upgrade"): "Add metrics to 1 past project in your resume",

    ("Data Scientist", "Networking"): "Comment on a LinkedIn post in a DS community",
    ("Data Scientist", "Portfolio Building"): "Upload a new ML project to GitHub",
    ("Data Scientist", "Interview Prep"): "Practice 2 scenario-based ML questions",
    ("Data Scientist", "Resume Upgrade"): "Refactor resume to highlight ML tools used",

    ("Software Engineer", "Networking"): "Engage in a GitHub issue or PR discussion",
    ("Software Engineer", "Portfolio Building"): "Push a new feature to your GitHub project",
    ("Software Engineer", "Interview Prep"): "Solve 2 DSA problems from recent interviews",
    ("Software Engineer", "Resume Upgrade"): "Tailor resume for a backend role",

    ("Other", "Networking"): "Connect with someone in your industry",
    ("Other", "Portfolio Building"): "Document one new project idea",
    ("Other", "Interview Prep"): "Practice 3 behavioral interview questions",
    ("Other", "Resume Upgrade"): "Clean up resume formatting and spelling",

    ("Any", "Resume Upgrade"): "Refactor your resume with 1 new achievement"
}

# --- Task Form ---
with st.form("task_form"):
    role = st.selectbox("Select Your Role", ["Data Analyst", "Data Scientist", "Software Engineer", "Other"])
    goal = st.selectbox("Choose Your Goal", ["Networking", "Portfolio Building", "Interview Prep", "Resume Upgrade"])
    submitted = st.form_submit_button("Generate Task")

# --- Task Assignment ---
today = str(date.today())
if submitted:
    key = (role, goal)
    fallback_key = ("Any", goal)
    task = TASK_LIBRARY.get(key) or TASK_LIBRARY.get(fallback_key) or "Reflect on your learning goals today."

    if today not in st.session_state.progress:
        st.session_state.progress[today] = {
            "role": role,
            "goal": goal,
            "task": task,
            "status": "Pending"
        }

# --- Display Task ---
if today in st.session_state.progress:
    task_data = st.session_state.progress[today]
    color = "🟩" if task_data["status"] == "Completed" else "🟥"
    st.markdown(f"### 📅 Task for **{today}**")
    st.info(f"{color} **{task_data['task']}**")

    if task_data["status"] == "Pending":
        if st.button("✅ Mark as Completed"):
            st.session_state.progress[today]["status"] = "Completed"
            st.session_state.points += 10
            st.success("Nice job! You've earned 10 points 🎉")

# --- Progress Summary ---
completed = sum(1 for t in st.session_state.progress.values() if t["status"] == "Completed")
pending = sum(1 for t in st.session_state.progress.values() if t["status"] == "Pending")
st.metric("✅ Completed Tasks", completed)
st.metric("🕒 Pending Tasks", pending)
st.metric("🏅 Points Earned", st.session_state.points)

# --- Task History Visualization ---
if st.session_state.progress:
    df = pd.DataFrame(st.session_state.progress).T
    df["date"] = df.index
    chart = alt.Chart(df).mark_bar().encode(
        x='date:T',
        y=alt.Y('count():Q', title='Tasks'),
        color='status:N'
    ).properties(title="📊 Task Completion Trend", width=600)
    st.altair_chart(chart)

# --- CSV Download ---
if st.session_state.progress:
    df_out = pd.DataFrame(st.session_state.progress).T.reset_index()
    df_out.columns = ["Date", "Role", "Goal", "Task", "Status"]
    csv = df_out.to_csv(index=False)
    st.download_button("📥 Download Progress", data=csv, file_name="progress.csv")

# --- Add to Calendar ---
if today in st.session_state.progress:
    cal = ics.Calendar()
    e = ics.Event()
    e.name = "Connectora Task"
    e.begin = datetime.now()
    e.duration = timedelta(minutes=30)
    e.description = st.session_state.progress[today]["task"]
    cal.events.add(e)
    st.download_button("📅 Add to Calendar", data=str(cal), file_name="connectora_task.ics")

# --- Feedback ---
st.markdown("## 💬 Feedback")
st.feedback("Tell us what you'd like improved or added:")
