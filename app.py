import streamlit as st
import pandas as pd
from datetime import datetime

# -------------------- TITLE & HEADER -------------------- #
st.set_page_config(page_title="Networg - Smart Networking Planner", layout="centered")
st.title("🤖 Networg")
st.markdown("### AI-Driven Smart Networking Planner for Students & Freshers")
st.markdown("Helping you reach the right mentors, professionals, and recruiters based on your goals.🚀")

# -------------------- INPUT SECTION -------------------- #
st.markdown("## 🎯 Your Networking Intent")

name = st.text_input("What's your name?")
career_goal = st.selectbox("Choose your career goal:", [
    "Data Scientist", "Data Analyst", "Machine Learning Engineer", "Software Developer", "Frontend Developer",
    "Backend Developer", "Full Stack Developer", "Product Manager", "Business Analyst", "DevOps Engineer",
    "Cloud Architect", "UI/UX Designer", "Cybersecurity Analyst", "QA Engineer", "Database Administrator",
    "AI Researcher", "Mobile App Developer", "AR/VR Developer", "Data Engineer", "Blockchain Developer",
    "Site Reliability Engineer", "Game Developer", "IT Support Specialist", "Solutions Architect", "Scrum Master",
    "Network Engineer", "Systems Analyst", "Technical Writer", "NLP Engineer", "Bioinformatics Scientist"
])

goal = st.text_area("What do you want help with? (e.g., portfolio review, job referral, learning path)")

company = st.text_input("Dream company or industry you want to connect in (e.g., Google, FinTech, EdTech):")
contact_date = st.date_input("When do you plan to reach out to someone?", min_value=datetime.today())

# -------------------- AI-STYLE OUTPUT -------------------- #
def generate_networking_plan(name, goal, career_goal, company):
    return f"""
Hi {name},

Here’s your AI-generated networking plan:

🔹 **Career Focus**: {career_goal}  
🔹 **Goal**: {goal}  
🔹 **Target**: Professionals working at or connected to **{company}**  
🔹 **What To Do**:
- Search for professionals in {company} on LinkedIn with '{career_goal}' in their title.
- Send a personalized connection request (mention mutual interests, recent projects, or alumni networks).
- Follow up after 2-3 days if no response. Share your goal clearly.
- Ask for advice, not favors – show curiosity and clarity.

🤖 *Tip: Connect with 2 new people weekly. Track your progress and stay consistent.*

Good luck, {name}!
"""

# -------------------- NETWORK PLAN BUTTON -------------------- #
if st.button("🧠 Generate My Smart Networking Plan"):
    plan = generate_networking_plan(name, goal, career_goal, company)
    st.markdown("### ✨ Your Plan")
    st.text_area("Here’s your networking plan:", value=plan, height=250)
    st.download_button("📥 Download Plan", plan, file_name="networking_plan.txt")

# -------------------- CALENDAR REMINDER -------------------- #
def generate_calendar_reminder(name, goal, company, contact_date):
    return f"""📅 Networking Reminder

Hello {name},

🔗 You planned to reach out to someone from **{company}** regarding:
🎯 Goal: {goal}

🕒 Suggested Contact Date: {contact_date.strftime('%A, %d %B %Y')}

💡 Tip: Follow up with a personalized message that references shared interests or career paths.

You've got this!
"""

if st.button("📆 Generate Reminder"):
    reminder = generate_calendar_reminder(name, goal, company, contact_date)
    st.markdown("### 📌 Your Networking Reminder")
    st.text_area("Reminder Content", reminder, height=220)
    st.download_button("📥 Download Reminder", reminder, file_name="reminder.txt")

# -------------------- FEEDBACK SECTION -------------------- #
st.markdown("---")
st.markdown("## 💬 Share Your Feedback")

feedback = st.text_area("How can we make Networg even better?")
if st.button("🚀 Submit Feedback"):
    st.success("Thank you for your valuable input! ❤️")

# -------------------- FOOTER -------------------- #
st.markdown("---")
st.markdown("Made with ❤️ for students and freshers by someone who gets the struggle.")
