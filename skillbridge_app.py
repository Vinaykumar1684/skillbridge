"""
SkillBridge - AI-Powered Voluntary Skill Development Portal
SPExHACK '26 Prototype
Author: SPExHACK '26 Team

Run: pip install streamlit plotly
Then: streamlit run skillbridge_app.py
"""

import streamlit as st
import json
import time
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="SkillBridge - AI Skill Development Portal",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FF9900, #232F3E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-top: -10px;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border-left: 4px solid #FF9900;
    }
    .skill-gap-high { color: #d32f2f; font-weight: bold; }
    .skill-gap-medium { color: #f57c00; font-weight: bold; }
    .skill-gap-low { color: #388e3c; font-weight: bold; }
    .match-score { 
        font-size: 3rem; 
        font-weight: 700; 
        color: #FF9900; 
    }
    .task-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        border-left: 4px solid #232F3E;
    }
    .step-card {
        background: #fff3e0;
        border-radius: 8px;
        padding: 12px;
        margin: 8px 0;
        border-left: 3px solid #FF9900;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SAMPLE DATA (Pre-computed AI responses)
# ============================================================

TASKS = [
    {"id": "T001", "title": "Build Automated Data Quality Dashboard", "owner": "Neha Kapoor (L6, Data Engineering)", "skills_required": ["Python", "SQL", "Data Visualization", "Streamlit"], "duration": "2 weeks", "category": "Stretch Assignment", "description": "Create an automated dashboard to monitor catalog data quality metrics across 5 marketplaces."},
    {"id": "T002", "title": "Design Customer Feedback Analysis Pipeline", "owner": "Arjun Mehta (L6, ML Engineering)", "skills_required": ["NLP", "Python", "AWS Lambda", "Data Analysis"], "duration": "3 weeks", "category": "Stretch Assignment", "description": "Build a pipeline to categorize and summarize 1000+ daily customer feedback entries using NLP."},
    {"id": "T003", "title": "Create Compliance Audit Automation Script", "owner": "Kavitha Iyer (L5, Compliance)", "skills_required": ["Python", "Excel Automation", "Process Design", "SOP Knowledge"], "duration": "1 week", "category": "Quick Win", "description": "Automate the weekly compliance checklist generation from multiple data sources."},
    {"id": "T004", "title": "Lead Sprint Retrospective Improvements", "owner": "Karthik Nair (L6, Program Management)", "skills_required": ["Project Management", "Facilitation", "Process Improvement", "Stakeholder Communication"], "duration": "4 weeks", "category": "Leadership Development", "description": "Design and facilitate improved sprint retrospective format for a 15-person team."},
    {"id": "T005", "title": "Develop Internal Knowledge Base Chatbot", "owner": "Sanjay Kumar (L6, Software Dev)", "skills_required": ["LLM/AI", "Python", "RAG Architecture", "API Development"], "duration": "3 weeks", "category": "Stretch Assignment", "description": "Build a chatbot that answers team FAQs using RAG over internal wikis and SOPs."},
    {"id": "T006", "title": "Process Mapping & Optimization for Onboarding", "owner": "Meera Patel (L5, Operations)", "skills_required": ["Process Mapping", "Documentation", "Training Design", "Stakeholder Management"], "duration": "2 weeks", "category": "Quick Win", "description": "Map the current onboarding process, identify bottlenecks, and propose an optimized workflow."},
    {"id": "T007", "title": "Build Seller Performance Metrics Tracker", "owner": "Vikram Singh (L6, Business Intelligence)", "skills_required": ["SQL", "QuickSight", "Data Modeling", "Business Analysis"], "duration": "2 weeks", "category": "Stretch Assignment", "description": "Create a QuickSight dashboard tracking seller performance KPIs across 3 categories."},
    {"id": "T008", "title": "Mentor Junior Associates on Catalog Standards", "owner": "Deepa Rao (L6, Catalog Quality)", "skills_required": ["Mentoring", "Catalog Knowledge", "Communication", "Training Delivery"], "duration": "Ongoing (4 hrs/week)", "category": "Leadership Development", "description": "Mentor 3-4 new associates on catalog quality standards and audit procedures."},
    {"id": "T009", "title": "Automate Weekly Status Report Generation", "owner": "Arun Krishnan (L5, Program Management)", "skills_required": ["Python", "Excel Automation", "Data Aggregation", "Reporting"], "duration": "1 week", "category": "Quick Win", "description": "Build a script to auto-generate weekly status reports from JIRA/SIM data."},
    {"id": "T010", "title": "Cross-Marketplace Data Reconciliation Tool", "owner": "Nisha Gupta (L6, Data Engineering)", "skills_required": ["Python", "SQL", "AWS S3", "Data Validation", "ETL"], "duration": "3 weeks", "category": "Stretch Assignment", "description": "Build a tool to reconcile product data across IN, US, and EU marketplaces for consistency."},
]

PROFILES = {
    "Ravi Shankar (Operations Associate)": {
        "name": "Ravi Shankar",
        "current_role": "Operations Associate (L4)",
        "current_skills": ["Process Execution", "SOP Compliance", "Data Entry", "Excel", "Quality Auditing", "Reporting"],
        "interests": ["Python scripting", "SQL for data querying", "Automating Excel reports", "Basic data visualization"],
        "goal": "Learn Python and SQL to automate repetitive tasks in my current role"
    },
    "Priya Nair (Software Dev Engineer)": {
        "name": "Priya Nair",
        "current_role": "Software Dev Engineer (L4)",
        "current_skills": ["Java", "Python", "AWS Lambda", "DynamoDB", "REST APIs", "Unit Testing"],
        "interests": ["ML model training", "System design patterns", "Mentoring junior devs"],
        "goal": "Learn Machine Learning to build smarter automation in my projects"
    },
    "Deepak Verma (Business Analyst)": {
        "name": "Deepak Verma",
        "current_role": "Business Analyst (L5)",
        "current_skills": ["SQL", "Excel Advanced", "QuickSight", "Business Requirements", "Stakeholder Management", "Data Modeling"],
        "interests": ["AI product design", "Writing technical PRDs", "Prioritization frameworks"],
        "goal": "Learn AI/ML product thinking to design better data-driven features"
    },
    "Ananya Rao (Catalog Quality Associate)": {
        "name": "Ananya Rao",
        "current_role": "Catalog Quality Associate (L4)",
        "current_skills": ["Catalog Management", "Data Validation", "Excel", "Process Documentation", "SOP Knowledge", "Stakeholder Communication"],
        "interests": ["Agile/Scrum methods", "JIRA project tracking", "Cross-team coordination", "Metrics-driven decision making"],
        "goal": "Learn project coordination and process improvement frameworks"
    }
}

AI_RESULTS = {
    "Ravi Shankar (Operations Associate)": {
        "readiness_score": 42,
        "strong_foundations": [
            "✅ Process understanding — you already know what needs automating",
            "✅ Domain expertise in compliance/catalog — valuable for building relevant tools",
            "✅ Documentation skills — essential for technical roles"
        ],
        "skill_gaps": [
            {"skill": "Python Programming", "current": "Beginner", "needed": "Intermediate", "priority": "HIGH", "time": "4-6 weeks"},
            {"skill": "SQL & Data Querying", "current": "Basic", "needed": "Intermediate", "priority": "HIGH", "time": "3-4 weeks"},
            {"skill": "AI/ML Fundamentals", "current": "Awareness", "needed": "Working Knowledge", "priority": "MEDIUM", "time": "6-8 weeks"},
            {"skill": "Data Visualization", "current": "Excel Charts", "needed": "Streamlit/QuickSight", "priority": "MEDIUM", "time": "2-3 weeks"}
        ],
        "learning_path": [
            {"step": 1, "action": "Python for Data Analysis (AWS Skill Builder)", "duration": "2 weeks", "type": "Course"},
            {"step": 2, "action": "SQL Fundamentals + Practice on Catalog Data", "duration": "2 weeks", "type": "Course"},
            {"step": 3, "action": "🎯 Take task: 'Automate Weekly Status Report' (T009)", "duration": "1 week", "type": "Stretch Task"},
            {"step": 4, "action": "Build automation for your own compliance workflow", "duration": "1 week", "type": "Self-Project"},
            {"step": 5, "action": "🎯 Take task: 'Compliance Audit Automation Script' (T003)", "duration": "1 week", "type": "Stretch Task"}
        ],
        "matched_tasks": ["T003", "T006", "T009"],
        "timeline": "8-12 weeks to stretch-assignment ready"
    },
    "Priya Nair (Software Dev Engineer)": {
        "readiness_score": 71,
        "strong_foundations": [
            "✅ Strong programming base — can build production systems",
            "✅ AWS experience — ML services will come naturally",
            "✅ API development — key for ML model serving"
        ],
        "skill_gaps": [
            {"skill": "ML Model Training & Evaluation", "current": "Basic", "needed": "Intermediate", "priority": "HIGH", "time": "6-8 weeks"},
            {"skill": "System Design (L5 bar)", "current": "Component-level", "needed": "End-to-end", "priority": "HIGH", "time": "4-6 weeks"},
            {"skill": "Technical Leadership", "current": "IC only", "needed": "Mentoring + Design Reviews", "priority": "MEDIUM", "time": "Ongoing"}
        ],
        "learning_path": [
            {"step": 1, "action": "AWS ML Specialty Prep Course", "duration": "3 weeks", "type": "Course"},
            {"step": 2, "action": "🎯 Take task: 'Customer Feedback Analysis Pipeline' (T002)", "duration": "3 weeks", "type": "Stretch Task"},
            {"step": 3, "action": "🎯 Take task: 'Internal Knowledge Base Chatbot' (T005)", "duration": "3 weeks", "type": "Stretch Task"},
            {"step": 4, "action": "Mentor 1-2 L3/L4 SDEs on your team", "duration": "Ongoing", "type": "Leadership"}
        ],
        "matched_tasks": ["T002", "T005", "T010"],
        "timeline": "6-8 weeks to ML stretch assignments"
    },
    "Deepak Verma (Business Analyst)": {
        "readiness_score": 58,
        "strong_foundations": [
            "✅ Data fluency — can slice any dataset to find insights",
            "✅ Stakeholder management — core PM skill already present",
            "✅ Business requirements writing — translates to PRD authoring"
        ],
        "skill_gaps": [
            {"skill": "Product Roadmap & Prioritization", "current": "Contributor", "needed": "Owner", "priority": "HIGH", "time": "4-6 weeks"},
            {"skill": "Technical Architecture Understanding", "current": "Consumer", "needed": "Conversational", "priority": "HIGH", "time": "4 weeks"},
            {"skill": "AI/ML Product Thinking", "current": "Awareness", "needed": "Can spec AI features", "priority": "MEDIUM", "time": "3-4 weeks"}
        ],
        "learning_path": [
            {"step": 1, "action": "Amazon Product Management Internal Course", "duration": "2 weeks", "type": "Course"},
            {"step": 2, "action": "🎯 Take task: 'Seller Performance Metrics Tracker' (T007)", "duration": "2 weeks", "type": "Stretch Task"},
            {"step": 3, "action": "Shadow a TPM for 2 sprints — attend design reviews", "duration": "4 weeks", "type": "Shadow"},
            {"step": 4, "action": "🎯 Take task: 'Lead Sprint Retrospective Improvements' (T004)", "duration": "4 weeks", "type": "Stretch Task"}
        ],
        "matched_tasks": ["T004", "T007", "T006"],
        "timeline": "10-12 weeks to PM-ready stretch assignments"
    },
    "Ananya Rao (Catalog Quality Associate)": {
        "readiness_score": 55,
        "strong_foundations": [
            "✅ Stakeholder communication — already coordinating across teams",
            "✅ Process documentation — core PM/PgM skill",
            "✅ Catalog domain expertise — valuable institutional knowledge"
        ],
        "skill_gaps": [
            {"skill": "Program Management Frameworks", "current": "Awareness", "needed": "Practitioner", "priority": "HIGH", "time": "4-6 weeks"},
            {"skill": "Project Planning & Tracking", "current": "Basic (Excel)", "needed": "JIRA/Asana proficient", "priority": "HIGH", "time": "3-4 weeks"},
            {"skill": "Cross-Functional Leadership", "current": "Within team", "needed": "Cross-team influence", "priority": "MEDIUM", "time": "Ongoing"},
            {"skill": "Data-Driven Decision Making", "current": "Basic reporting", "needed": "Metrics-driven prioritization", "priority": "MEDIUM", "time": "3-4 weeks"}
        ],
        "learning_path": [
            {"step": 1, "action": "Amazon Program Management Foundations (Internal Course)", "duration": "2 weeks", "type": "Course"},
            {"step": 2, "action": "JIRA & Agile Project Tracking (AWS Skill Builder)", "duration": "1 week", "type": "Course"},
            {"step": 3, "action": "🎯 Take task: 'Process Mapping & Optimization for Onboarding' (T006)", "duration": "2 weeks", "type": "Stretch Task"},
            {"step": 4, "action": "🎯 Take task: 'Lead Sprint Retrospective Improvements' (T004)", "duration": "4 weeks", "type": "Stretch Task"}
        ],
        "matched_tasks": ["T004", "T006", "T009"],
        "timeline": "10-14 weeks to PgM-ready stretch assignments"
    }
}

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg", width=120)
    st.markdown("---")
    st.markdown("### 🎯 SkillBridge")
    st.markdown("*AI-Powered Voluntary Skill Development*")
    st.markdown("---")
    
    page = st.radio("Navigate", [
        "🏠 Home",
        "🧠 AI Skill Matcher",
        "📋 Task Marketplace",
        "📊 Impact Dashboard"
    ])
    
    st.markdown("---")
    st.markdown("##### 🏗️ Tech Stack")
    st.markdown("""
    - Amazon Bedrock (Claude)
    - Titan Embeddings
    - OpenSearch (Semantic Match)
    - RAG Architecture
    """)
    st.markdown("---")
    st.caption("SPExHACK '26 | SkillBridge Team")

# ============================================================
# HOME PAGE
# ============================================================
if page == "🏠 Home":
    st.markdown('<p class="main-header">SkillBridge</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Voluntary Skill Development Portal — Learn, Match, Grow</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Problem statement
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>45+ min</h3>
            <p>Average time to find the right learning resource across fragmented platforms</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>3-5 days</h3>
            <p>Time for task owners to find qualified candidates for stretch assignments</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>40%</h3>
            <p>Stretch assignments go unfilled due to lack of visibility</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### How SkillBridge Works")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 1️⃣ Authenticate & Consent")
        st.markdown("Sign in via Midway SSO. Grant read-only access. AI auto-imports your profile from Phonetool, Amazon Learn, Forte & JIRA.")
    with col2:
        st.markdown("#### 2️⃣ AI Matches")
        st.markdown("Bedrock analyzes your auto-imported skills, identifies gaps, and semantically matches you to real stretch tasks.")
    with col3:
        st.markdown("#### 3️⃣ Learn & Grow")
        st.markdown("Follow your AI-curated path. Complete real tasks. Get validated by task owners. Level up.")
    
    st.markdown("---")
    st.markdown("### 🏆 Key Differentiator")
    st.info("**Zero manual input. Midway authentication + AI auto-imports your complete skill profile. Every other tool stops at 'here's a course.' SkillBridge closes the last mile — connecting learning to REAL stretch assignments, validating skills through practice, not just certificates.**")

# ============================================================
# AI SKILL MATCHER PAGE
# ============================================================
elif page == "🧠 AI Skill Matcher":
    st.markdown('<p class="main-header">AI Skill Matcher</p>', unsafe_allow_html=True)
    st.markdown("*Powered by Amazon Bedrock (Claude) + Titan Embeddings*")
    st.markdown("---")
    
    # Midway Authentication Flow
    st.markdown("#### 🔐 Midway Authentication")
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "consent_given" not in st.session_state:
        st.session_state.consent_given = False
    if "profile_imported" not in st.session_state:
        st.session_state.profile_imported = False
    
    if not st.session_state.authenticated:
        st.info("🔒 Sign in with Amazon Midway to auto-import your profile")
        if st.button("🔑 Sign in with Midway SSO", type="primary", use_container_width=True):
            with st.spinner("Authenticating via Midway..."):
                time.sleep(1.5)
            st.session_state.authenticated = True
            st.rerun()
    
    elif not st.session_state.consent_given:
        st.success("✅ Authenticated as **Ravi Shankar**")
        st.markdown("---")
        st.markdown("#### 📋 Data Access Consent")
        st.markdown("SkillBridge needs permission to import your profile from the following systems:")
        st.markdown("""
        | Source | What we'll pull |
        |--------|----------------|
        | 📇 **Phonetool** | Role, level, team, manager, tenure |
        | 📄 **FCJP (Job Profile)** | Required competencies for your role |
        | 🎓 **Amazon Learn / Skill Builder** | Completed courses & certifications |
        | ⭐ **Forte** | Skills endorsed by your manager |
        | 🔧 **JIRA / SIM history** | Tools & technologies used in your work |
        """)
        st.warning("⚠️ This is read-only access. SkillBridge will never modify your data.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ I Consent — Import My Profile", type="primary", use_container_width=True):
                st.session_state.consent_given = True
                st.rerun()
        with col2:
            if st.button("❌ Deny Access", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
    
    elif not st.session_state.profile_imported:
        st.success("✅ Authenticated as **Ravi Shankar** | ✅ Consent granted")
        st.markdown("---")
        st.markdown("#### 🤖 Importing your profile...")
        with st.spinner("🤖 AI importing your profile from 5 systems..."):
            time.sleep(1)
            st.markdown("  ✓ Phonetool — Role & team data retrieved")
            time.sleep(0.8)
            st.markdown("  ✓ Amazon Learn — 12 completed courses found")
            time.sleep(0.8)
            st.markdown("  ✓ Forte — 6 skill endorsements found")
            time.sleep(0.8)
            st.markdown("  ✓ JIRA/SIM — 8 months of work history analyzed")
            time.sleep(0.8)
            st.markdown("  ✓ FCJP — Role competency mapping loaded")
        st.session_state.profile_imported = True
        st.rerun()
    
    else:
        st.success("✅ Authenticated as **Ravi Shankar** | ✅ Profile auto-imported")
        st.markdown("---")
        
        # Role Selection
        if "user_roles" not in st.session_state:
            st.session_state.user_roles = []
        
        st.markdown("#### 🎭 How would you like to participate?")
        st.markdown("*Select one or more roles (you can change these anytime)*")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            r1 = st.checkbox("🎓 **Learner**", value=True, help="Get AI skill analysis, follow learning paths, apply for stretch tasks")
            if r1:
                st.caption("Discover skill gaps, get personalized learning paths, and apply for stretch assignments")
        with col2:
            r2 = st.checkbox("📋 **Task Owner**", help="Post stretch assignments, get AI-matched candidates, validate completions")
            if r2:
                st.caption("Post tasks you need help with and let AI find the best-matched volunteers")
        with col3:
            st.markdown("🔗 **Mentoring Portal**")
            st.caption("Integration planned — connects with existing Amazon Mentoring Portal in a future release")
        
        selected_roles = []
        if r1: selected_roles.append("Learner")
        if r2: selected_roles.append("Task Owner")
        
        if selected_roles:
            st.markdown(f"**Your roles:** {' • '.join(selected_roles)}")
        else:
            st.warning("Please select at least one role to continue")
            st.stop()
        
        st.markdown("---")
        
        # For demo: allow switching between profiles to show different scenarios
        st.markdown("#### 👤 Your AI-Generated Profile")
        st.caption("*Demo mode: switch between sample profiles to see different matching results*")
        selected_profile = st.selectbox(
            "Demo profile:",
            list(PROFILES.keys()),
            index=0
        )
        
        profile = PROFILES[selected_profile]
    
        # Show auto-imported profile card
        st.markdown(f"""
        <div style="background:#f0f7ff; border-radius:10px; padding:20px; border-left:4px solid #0073bb;">
            <b>🤖 Auto-Imported Profile</b> (from Phonetool + Amazon Learn + Forte + JIRA)
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"**👤 {profile['name']}**")
            st.markdown(f"📍 {profile['current_role']}")
            st.markdown(f"🎯 Goal: *{profile['goal']}*")
            st.markdown("**Skills Detected:**")
            for skill in profile['current_skills']:
                st.markdown(f"  • {skill}")
        
        with col2:
            st.markdown("**Learning Interests (from Skill Builder activity):**")
            for interest in profile['interests']:
                st.markdown(f"  🔍 {interest}")
            st.markdown("---")
            st.markdown("*✏️ Something wrong? Click below to edit.*")
            st.button("✏️ Edit Profile", key="edit_profile")
        
        st.markdown("---")
        
        # AI Analysis button
        if st.button("🚀 Run AI Analysis", type="primary", use_container_width=True):
            result = AI_RESULTS[selected_profile]
            
            # Simulate AI processing
            with st.spinner("🤖 Amazon Bedrock analyzing your profile..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress.progress(i + 1)
            
            st.success("✅ AI Analysis Complete!")
            st.markdown("---")
            
            # Readiness Score
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f'<div style="text-align:center"><span class="match-score">{result["readiness_score"]}%</span><br><b>Career Readiness Score</b></div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Strengths
            st.markdown("### 💪 Your Strong Foundations")
            for s in result["strong_foundations"]:
                st.markdown(s)
            
            st.markdown("---")
            
            # Skill Gaps
            st.markdown("### 📊 Skill Gap Analysis")
            for gap in result["skill_gaps"]:
                priority_color = "🔴" if gap["priority"] == "HIGH" else "🟡"
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                with col1:
                    st.markdown(f"**{gap['skill']}**")
                with col2:
                    st.markdown(f"{gap['current']} → {gap['needed']}")
                with col3:
                    st.markdown(f"{priority_color} {gap['priority']}")
                with col4:
                    st.markdown(f"⏱️ {gap['time']}")
            
            st.markdown("---")
            
            # Personalized Learning Path
            st.markdown("### 🗺️ Your Personalized Learning Path")
            st.markdown(f"*Estimated timeline: {result['timeline']}*")
            for item in result["learning_path"]:
                icon = "📚" if item["type"] == "Course" else "🎯" if item["type"] == "Stretch Task" else "👥" if item["type"] == "Shadow" else "🔨"
                st.markdown(f"""
                <div class="step-card">
                    <b>Step {item['step']}</b> ({item['duration']}) — {icon} {item['type']}<br>
                    {item['action']}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Matched Tasks
            st.markdown("### 🎯 AI-Matched Stretch Tasks For You")
            matched = [t for t in TASKS if t["id"] in result["matched_tasks"]]
            for task in matched:
                st.markdown(f"""
                <div class="task-card">
                    <b>{task['title']}</b><br>
                    👤 Owner: {task['owner']} | ⏱️ {task['duration']} | 🏷️ {task['category']}<br>
                    <i>{task['description']}</i><br>
                    Skills: {', '.join(task['skills_required'])}
                </div>
                """, unsafe_allow_html=True)

# ============================================================
# TASK MARKETPLACE PAGE
# ============================================================
elif page == "📋 Task Marketplace":
    st.markdown('<p class="main-header">Task Marketplace</p>', unsafe_allow_html=True)
    st.markdown("*Browse available stretch assignments, quick wins, and leadership opportunities*")
    st.markdown("---")
    
    # Tab view: Browse Tasks vs Post a Task
    tab1, tab2 = st.tabs(["🔍 Browse Tasks (Learner)", "➕ Post a Task (Task Owner)"])
    
    with tab2:
        st.markdown("#### Post a Stretch Assignment / Quick Win")
        st.markdown("*AI will match your task to the best-fit volunteers automatically*")
        st.markdown("---")
        
        post_title = st.text_input("Task Title", placeholder="e.g., Build Data Quality Dashboard")
        post_desc = st.text_area("Description", placeholder="What needs to be done? What will the volunteer learn?", height=100)
        post_skills = st.multiselect("Skills Required", ["Python", "SQL", "Data Visualization", "Excel Automation", "NLP", "AWS Lambda", "Project Management", "Process Mapping", "LLM/AI", "RAG Architecture", "QuickSight", "Streamlit", "Communication", "Mentoring"])
        
        col1, col2 = st.columns(2)
        with col1:
            post_duration = st.selectbox("Estimated Duration", ["1 week", "2 weeks", "3 weeks", "4+ weeks", "Ongoing"])
        with col2:
            post_category = st.selectbox("Category", ["Stretch Assignment", "Quick Win", "Leadership Development", "Cross-Team Collaboration"])
        
        if st.button("🚀 Post Task & Find Matches", type="primary", use_container_width=True):
            if post_title and post_desc:
                with st.spinner("🤖 AI finding best-matched volunteers..."):
                    time.sleep(2)
                st.success("✅ Task posted! AI found 3 potential matches:")
                st.markdown("""
                | Rank | Volunteer | Match Score | Why |
                |------|-----------|:-----------:|-----|
                | 1 | Ravi Shankar (L4, Operations) | **87%** | SOP expertise + learning Python |
                | 2 | Ritu Sharma (L4, Operations) | **72%** | Process mapping + Excel automation |
                | 3 | Ankit Das (L3, Data Entry) | **65%** | Eager learner, completed SQL course |
                """)
            else:
                st.error("Please fill in title and description")
    
    with tab1:
    # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            category_filter = st.selectbox("Category", ["All", "Stretch Assignment", "Quick Win", "Leadership Development"])
        with col2:
            skill_filter = st.text_input("Filter by skill", placeholder="e.g., Python, SQL...")
        with col3:
            duration_filter = st.selectbox("Duration", ["All", "1 week", "2 weeks", "3 weeks", "4+ weeks"])
        
        st.markdown("---")
        
        # Display tasks
        for task in TASKS:
            if category_filter != "All" and task["category"] != category_filter:
                continue
            if skill_filter and skill_filter.lower() not in [s.lower() for s in task["skills_required"]]:
                continue
            
            with st.expander(f"**{task['title']}** — {task['category']} ({task['duration']})"):
                st.markdown(f"**Owner:** {task['owner']}")
                st.markdown(f"**Description:** {task['description']}")
                st.markdown(f"**Skills Required:** {', '.join(task['skills_required'])}")
                st.markdown(f"**Duration:** {task['duration']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.button(f"🙋 Express Interest", key=f"interest_{task['id']}")
                with col2:
                    st.button(f"💬 Ask Owner", key=f"ask_{task['id']}")

# ============================================================
# IMPACT DASHBOARD PAGE
# ============================================================
elif page == "📊 Impact Dashboard":
    st.markdown('<p class="main-header">Impact Dashboard</p>', unsafe_allow_html=True)
    st.markdown("*Measuring process efficiency improvements*")
    st.markdown("---")
    
    # Before vs After metrics
    st.markdown("### ⚡ Process Efficiency Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Resource Discovery", "< 30 sec", delta="-45 min", delta_color="inverse")
    with col2:
        st.metric("Task-Candidate Matching", "Instant", delta="-3-5 days", delta_color="inverse")
    with col3:
        st.metric("Unfilled Assignments", "< 10%", delta="-30%", delta_color="inverse")
    with col4:
        st.metric("Skill Validation Cycle", "Real-time", delta="-weeks", delta_color="inverse")
    
    st.markdown("---")
    
    # Simulated adoption metrics
    st.markdown("### 📈 Projected Adoption (6-month forecast)")
    
    col1, col2 = st.columns(2)
    with col1:
        months = ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"]
        users = [25, 60, 110, 180, 270, 400]
        
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=users, mode='lines+markers', 
                                  line=dict(color='#FF9900', width=3),
                                  marker=dict(size=10)))
        fig.update_layout(title="Active Users", yaxis_title="Users", height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        tasks_completed = [5, 18, 42, 78, 125, 190]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=months, y=tasks_completed, marker_color='#232F3E'))
        fig2.update_layout(title="Stretch Tasks Completed", yaxis_title="Tasks", height=300)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # Annual impact projection
    st.markdown("### 💰 Annual Impact Projection")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>2,400 hrs</h2>
            <p>Saved annually in resource discovery time (400 users × 6 hrs/year each)</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>190+</h2>
            <p>Stretch assignments completed (vs ~0 today without visibility)</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>85%</h2>
            <p>Reduction in task owner time spent finding candidates</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔧 Technical Innovation Stack")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        | Layer | Technology |
        |-------|-----------|
        | Skill Gap Analysis | Amazon Bedrock (Claude) |
        | Semantic Matching | Titan Embeddings + OpenSearch |
        | Recommendations | RAG over Learning Catalog |
        | Validation | LLM-based skill assessment |
        """)
    with col2:
        st.markdown("""
        **Why it's innovative:**
        - 🔄 **Closes the loop** — Learn → Match → Apply → Validate
        - 🎯 **Two-sided AI** — matches learners AND task owners
        - 🧠 **Semantic, not keyword** — understands skill relationships
        - 📈 **Adaptive** — improves with usage data
        """)

    st.markdown("---")
    st.markdown("### 🚀 Production Roadmap")
    st.markdown("*From hackathon prototype to Amazon-internal platform*")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#fff3e0; border-radius:10px; padding:15px; text-align:center; border-top:4px solid #FF9900;">
            <h4>🏗️ Prototype (Now)</h4>
            <p style="font-size:0.85rem;">
            • Streamlit UI<br>
            • Pre-computed AI responses<br>
            • Local JSON data<br>
            • No authentication<br>
            • Single user demo
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#e3f2fd; border-radius:10px; padding:15px; text-align:center; border-top:4px solid #0073bb;">
            <h4>🧪 Pilot (3 months)</h4>
            <p style="font-size:0.85rem;">
            • React + Cloudscape UI<br>
            • Live Bedrock API calls<br>
            • Midway SSO authentication<br>
            • Phonetool + Amazon Learn + Forte APIs<br>
            • 100+ user pilot for testing & data collection
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#e8f5e9; border-radius:10px; padding:15px; text-align:center; border-top:4px solid #388e3c;">
            <h4>🌍 Production (6 months)</h4>
            <p style="font-size:0.85rem;">
            • AWS Amplify deployment<br>
            • DynamoDB + OpenSearch<br>
            • Forte + JIRA + AWS Skill Builder + SQL Bank + CGAP<br>
            • Mentoring Portal integration<br>
            • Org-wide rollout (1000+ users)
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("""
    | Component | Prototype | Production |
    |-----------|-----------|-----------|
    | Frontend | Streamlit | React + AWS Amplify + Cloudscape |
    | AI Engine | Pre-computed responses | Amazon Bedrock (Claude) real-time |
    | Matching | JSON lookup | Titan Embeddings + OpenSearch |
    | Database | In-memory JSON | DynamoDB + S3 |
    | Auth | None | Midway SSO (Federated Auth) |
    | Data Sources | Sample profiles | Phonetool + Forte + JIRA + Learn + AWS Skill Builder + SQL Bank + CGAP |
    | Hosting | Local / Streamlit Cloud | VPC-deployed on AWS (internal only) |
    | Mentoring | N/A (future) | Integrated with Amazon Mentoring Portal |
    """)

