import streamlit as st
import pandas as pd
from datetime import date, timedelta
import random

# -------------- PAGE CONFIG --------------
st.set_page_config(page_title="Connectora: Smart Working Growth Planner")

# -------------- SESSION SETUP --------------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "task_checks" not in st.session_state:
    st.session_state.task_checks = {}

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "last_check_date" not in st.session_state:
    st.session_state.last_check_date = None

# -------------- NAME INPUT SESSION --------------
if not st.session_state.user_name:
    name = st.text_input("👋 What's your name?")
    if name:
        st.session_state.user_name = name
        st.rerun()
else:
    st.title("🌱 Connectora: Smart Working Growth Planner")
    st.success(f"Welcome, {st.session_state.user_name}! Let's boost your growth! 🚀")

    # -------------- ROLE & TASKS --------------
    roles = [
        "Data Scientist", "Data Analyst", "Software Engineer", "Web Developer",
        "UI/UX Designer", "Cloud Engineer", "DevOps Engineer", "Product Manager",
        "Cybersecurity Analyst", "AI/ML Engineer", "Business Analyst", "QA/Test Engineer",
        "Technical Writer", "Network Engineer", "Student"
    ]

    role_tasks = {
        "Data Scientist": [
            "Train a supervised ML model", "Explore data with EDA",
            "Join a DS hackathon", "Study algorithm math", "Write a DS blog"
        ],
        "Data Analyst": [
            "Write complex SQL queries", "Create a Power BI dashboard",
            "Clean a messy dataset", "Conduct funnel analysis", "Present business insights"
        ],
        "Software Engineer": [
            "Solve 3 DSA problems", "Build a REST API", "Contribute to OSS",
            "Refactor legacy code", "Review system design patterns"
        ],
        "Web Developer": [
            "Build a portfolio site", "Clone a UI from Dribbble",
            "Learn React basics", "Study Next.js features", "Deploy with Vercel"
        ],
        "UI/UX Designer": [
            "Design in Figma", "Conduct a user test", "Build a design system",
            "Redesign a bad UI", "Explore mobile design trends"
        ],
        "Cloud Engineer": [
            "Deploy app to AWS", "Create CI/CD with GitHub Actions",
            "Explore AWS Lambda", "Build a VPC", "Estimate AWS cost"
        ],
        "DevOps Engineer": [
            "Use Docker & Compose", "Write Ansible scripts",
            "Explore Jenkins CI", "Learn Prometheus/Grafana", "Study Kubernetes basics"
        ],
        "Product Manager": [
            "Write a PRD", "Define personas", "Create a roadmap",
            "Do competitor analysis", "Map user journey"
        ],
        "Cybersecurity Analyst": [
            "Audit a site with OWASP", "Analyze HTTPS certificates",
            "Learn Wireshark", "Configure firewall rules", "Study ransomware cases"
        ],
        "AI/ML Engineer": [
            "Build an LLM chatbot", "Implement CNN in PyTorch",
            "Use HuggingFace transformers", "Try AutoML platform", "Deploy ML app with FastAPI"
        ],
        "Business Analyst": [
            "Create stakeholder report", "Draw process diagram",
            "Do SWOT/GAP analysis", "Write executive summary", "Analyze Excel dataset"
        ],
        "QA/Test Engineer": [
            "Write Selenium tests", "Create a test suite", "Track bugs in JIRA",
            "Perform regression testing", "Read software logs"
        ],
        "Technical Writer": [
            "Write API reference doc", "Publish tutorial blog",
            "Use Markdown formatting", "Review open-source docs", "Document an internal tool"
        ],
        "Network Engineer": [
            "Set up virtual router", "Study OSI layers",
            "Use Cisco Packet Tracer", "Troubleshoot with ping/tracert", "Read Wi-Fi logs"
        ],
        "Student": [
            "Set weekly study goals", "Join online tech event",
            "Complete a mini project", "Contribute to GitHub", "Write a weekly reflection"
        ]
    }

    selected_role = st.selectbox("🧑‍💼 Select Your Role", roles)
    today = str(date.today())
    today_tasks = role_tasks[selected_role]

    # -------------- TASK CHECKLIST --------------
    st.subheader("📅 Daily Planner: Check Your Tasks")

    if today not in st.session_state.task_checks:
        st.session_state.task_checks[today] = [False] * len(today_tasks)

    for i, task in enumerate(today_tasks):
        st.session_state.task_checks[today][i] = st.checkbox(
            task, value=st.session_state.task_checks[today][i]
        )

    completed = sum(st.session_state.task_checks[today])
    st.success(f"✅ Completed {completed} of {len(today_tasks)} tasks today!")

    # -------------- STREAK TRACKER --------------
    if completed == len(today_tasks):
        if st.session_state.last_check_date == str(date.today() - timedelta(days=1)):
            st.session_state.streak += 1
        elif st.session_state.last_check_date != str(date.today()):
            st.session_state.streak = 1
        st.session_state.last_check_date = today
        st.balloons()

    st.info(f"🔥 Streak: {st.session_state.streak} day(s)")

    # -------------- MOTIVATION BUDDY (AI STYLE) --------------
    name = st.session_state.user_name
    role = selected_role
    total_today = len(today_tasks)

    motivations = {
        "beginner": [
            f"Hey {name}, every expert was once a beginner. One task at a time!",
            f"{name}, your journey as a {role} starts today. Let's build habits!"
        ],
        "growing": [
            f"{name}, {st.session_state.streak} days in! Keep going strong 💪",
            f"{name}, you're gaining traction. As a {role}, growth is exponential!"
        ],
        "master": [
            f"🔥 {name}, {st.session_state.streak} days streak! You're owning this {role} life!",
            f"Legendary! {st.session_state.streak} days — stay unstoppable, {name}!"
        ],
        "low_completion": [
            f"{name}, try finishing one task to ignite momentum.",
            f"Every journey starts with a step. Complete one today!"
        ],
        "full_completion": [
            f"You nailed all {total_today} tasks! 💯",
            f"Victory! You’re unstoppable today, {name} 🚀"
        ]
    }

    if total_today == 0:
        msg = f"Hi {name}, pick a role and begin your journey today! 🌱"
    elif completed == total_today:
        msg = random.choice(motivations["full_completion"])
    elif completed < 2:
        msg = random.choice(motivations["low_completion"])
    elif st.session_state.streak >= 5:
        msg = random.choice(motivations["master"])
    elif st.session_state.streak >= 2:
        msg = random.choice(motivations["growing"])
    else:
        msg = random.choice(motivations["beginner"])

    st.info(f"💬 **Motivation Buddy Says:** _{msg}_")

    # -------------- EXPORT TO CSV --------------
    st.subheader("📤 Export Your Tasks")

    if st.button("📄 Download Completed Tasks (CSV)"):
        df = pd.DataFrame({
            "Date": [today] * len(today_tasks),
            "Task": today_tasks,
            "Completed": st.session_state.task_checks[today]
        })
        csv = df[df["Completed"]].to_csv(index=False)
        st.download_button("⬇️ Download CSV", data=csv, file_name="completed_tasks.csv", mime="text/csv")

    # -------------- ADMIN DASHBOARD --------------
    if st.checkbox("🔐 Show Admin Dashboard"):
        st.subheader("📊 Admin: View Task Sets by Role")
        for role in roles:
            with st.expander(role):
                for task in role_tasks[role]:
                    st.markdown(f"- {task}")

    # -------------- NEXT FEATURE OPTIONS --------------
    st.markdown("---")
    st.subheader("✨ What Would You Like Next?")
    st.markdown("""
    - ✅ Save checklist status per day  
    - 🔥 Add a streak counter and tracker  
    - 📄 Enable PDF/CSV export of completed tasks  
    - 👤 Build an admin dashboard with filters  
    """)

 

