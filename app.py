"""
IMPOWR Copilot - Ask IMPOWR Demo
A natural language to SQL prototype for the SimonAIThon hackathon.

Run with: streamlit run app.py
"""
import streamlit as st
import sqlite3
import pandas as pd
import os
import json
from datetime import datetime
from openai import AzureOpenAI

# Auto-create database if it doesn't exist
DB_PATH = "impowr_demo.db"
import subprocess
if not os.path.exists(DB_PATH):
    subprocess.run(["python", "setup_database.py"])

# ============================================================
# CONFIGURATION - YOU FILL THESE IN (Step 5 of the guide)
# ============================================================
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "YOUR_ENDPOINT_HERE")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_KEY", "YOUR_KEY_HERE")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "YOUR_DEPLOYMENT_NAME_HERE")
AZURE_API_VERSION = "2024-10-21"

DB_PATH = "impowr_demo.db"

# ============================================================
# PAGE CONFIG + STYLING (IMPOWR brand colors)
# ============================================================
st.set_page_config(
    page_title="IMPOWR Copilot",
    page_icon="🔍",
    layout="wide",
)

# IMPOWR brand: navy (#1B2A4A), orange (#E8632B), white
st.markdown("""
<style>
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Overall page */
    .stApp {
        background-color: #F8F9FA;
    }

    /* Header bar */
    .impowr-header {
        background: linear-gradient(135deg, #1B2A4A 0%, #2C3E6B 100%);
        padding: 1.5rem 2rem;
        border-radius: 0 0 12px 12px;
        margin: -1rem -1rem 1.5rem -1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .impowr-logo {
        color: white;
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: 2px;
        font-family: 'Segoe UI', sans-serif;
    }
    .impowr-logo span {
        color: #E8632B;
    }
    .impowr-subtitle {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }
    .copilot-badge {
        background: #E8632B;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Query input area */
    .query-container {
        background: white;
        border: 2px solid #E0E4E8;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    /* Results card */
    .result-card {
        background: white;
        border-left: 4px solid #E8632B;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    /* SQL transparency panel */
    .sql-panel {
        background: #1B2A4A;
        color: #A8D8A8;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 0.85rem;
        overflow-x: auto;
    }

    /* Audit log */
    .audit-entry {
        background: #F0F4F0;
        border: 1px solid #D0D8D0;
        border-radius: 6px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        font-size: 0.8rem;
        color: #444;
    }

    /* Source citation */
    .source-badge {
        display: inline-block;
        background: #EEF2FF;
        border: 1px solid #C7D2FE;
        color: #4338CA;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        font-size: 0.75rem;
        margin: 0.2rem;
    }

    /* Section headers */
    .section-header {
        color: #1B2A4A;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        padding-bottom: 0.3rem;
        border-bottom: 2px solid #E8632B;
        display: inline-block;
    }

    /* Disclaimer */
    .disclaimer {
        background: #FFF7ED;
        border: 1px solid #FED7AA;
        border-radius: 6px;
        padding: 0.6rem 1rem;
        font-size: 0.75rem;
        color: #92400E;
        margin-top: 1rem;
    }

    /* Metrics row */
    .metric-box {
        background: white;
        border: 1px solid #E0E4E8;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .metric-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: #E8632B;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATABASE SCHEMA (sent to the AI so it knows the tables)
# ============================================================
DB_SCHEMA = """
You have access to a SQLite database with the following tables:

TABLE: clients
- client_id (INTEGER, PRIMARY KEY)
- first_name (TEXT)
- last_name (TEXT)
- date_of_birth (TEXT, format: YYYY-MM-DD)
- gender (TEXT: Male/Female)
- primary_language (TEXT)
- zip_code (TEXT)
- enrollment_date (TEXT, format: YYYY-MM-DD)
- status (TEXT: Active/Inactive)
- risk_level (TEXT: High/Standard/Low)

TABLE: programs
- program_id (INTEGER, PRIMARY KEY)
- program_name (TEXT)
- program_type (TEXT: Housing/Food Security/Mental Health/Disability Services/Health/Workforce)
- funder (TEXT)
- start_date (TEXT)
- status (TEXT: Active/Inactive)

TABLE: enrollments
- enrollment_id (INTEGER, PRIMARY KEY)
- client_id (INTEGER, FK -> clients)
- program_id (INTEGER, FK -> programs)
- enrolled_date (TEXT, format: YYYY-MM-DD)
- completed_date (TEXT, format: YYYY-MM-DD, NULL if not completed)
- status (TEXT: Enrolled/Completed)

TABLE: case_notes
- note_id (INTEGER, PRIMARY KEY)
- client_id (INTEGER, FK -> clients)
- program_id (INTEGER, FK -> programs)
- note_date (TEXT, format: YYYY-MM-DD)
- note_type (TEXT: Home Visit/Follow-up/Completion/Intake/Session/Enrollment/Assessment)
- summary (TEXT)
- created_by (TEXT)

TABLE: assessments
- assessment_id (INTEGER, PRIMARY KEY)
- client_id (INTEGER, FK -> clients)
- assessment_type (TEXT)
- assessment_date (TEXT, format: YYYY-MM-DD)
- score (REAL)
- risk_flag (TEXT)
- completed (INTEGER: 1=yes, 0=no)

IMPORTANT CONTEXT:
- This is an IMPOWR platform database for a community-based organization (CBO)
- Clients are members of vulnerable populations receiving social care services
- Q1 2024 = January-March 2024, Q1 2025 = January-March 2025
- The data in this demo covers 2023-2024 time period
- "Completed" enrollments mean the client finished the program
- Housing Referral Program is the most commonly completed program
"""

SYSTEM_PROMPT = f"""You are IMPOWR Copilot, an AI assistant embedded inside the IMPOWR platform.
You help caseworkers, program managers, and directors access their program data using plain English.

{DB_SCHEMA}

RULES:
1. Generate ONLY valid SQLite SQL queries. Return nothing but the SQL.
2. Use only SELECT statements. Never INSERT, UPDATE, DELETE, DROP, or ALTER.
3. Always use table and column names exactly as defined above.
4. For date filtering, use string comparison (e.g., note_date >= '2024-01-01').
5. When asked about a person by name, search using first_name and/or last_name with LIKE.
6. Join tables as needed to answer the question fully.
7. Return ONLY the raw SQL query, no explanation, no markdown, no code fences.
8. If the question cannot be answered with the available data, return: SELECT 'This question cannot be answered with the available data.' AS response
"""

SUMMARY_PROMPT = """You are IMPOWR Copilot. A caseworker asked a question and the database returned results.
Write a clear, concise, human-friendly answer based on the data below.
Be specific with numbers, names, and dates. Keep it under 4 sentences.
Do NOT make up any information not in the data.
End with a note about which database tables were used.

Question: {question}
Data returned:
{data}
"""


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def get_db_connection():
    """Connect to SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def call_azure_openai(messages):
    """Call Azure OpenAI API."""
    client = AzureOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
    )
    response = client.chat.completions.create(
        model=AZURE_DEPLOYMENT,
        messages=messages,
        temperature=0.0,
        max_tokens=1000,
    )
    return response.choices[0].message.content.strip()


def generate_sql(question):
    """Convert natural language question to SQL."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    sql = call_azure_openai(messages)
    # Clean up any markdown formatting the model might add
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql


def execute_sql(sql):
    """Execute SQL and return results as DataFrame."""
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(sql, conn)
        return df, None
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()


def generate_summary(question, data_str):
    """Generate a human-friendly summary of the results."""
    messages = [
        {"role": "system", "content": "You are IMPOWR Copilot, a helpful assistant for social care organizations."},
        {"role": "user", "content": SUMMARY_PROMPT.format(question=question, data=data_str)},
    ]
    return call_azure_openai(messages)


def extract_tables_used(sql):
    """Extract table names from SQL for citation."""
    tables = []
    sql_upper = sql.upper()
    for table in ["clients", "programs", "enrollments", "case_notes", "assessments"]:
        if table.upper() in sql_upper:
            tables.append(table)
    return tables


# ============================================================
# INITIALIZE SESSION STATE
# ============================================================
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []
if "query_count" not in st.session_state:
    st.session_state.query_count = 0


# ============================================================
# UI LAYOUT
# ============================================================

# Header
st.markdown("""
<div class="impowr-header">
    <div>
        <div class="impowr-logo">IMP<span>O</span>WR</div>
        <div class="impowr-subtitle">Electronic Social & Health Record</div>
    </div>
    <div class="copilot-badge">✦ Copilot</div>
</div>
""", unsafe_allow_html=True)

# Dashboard metrics
col1, col2, col3, col4 = st.columns(4)
conn = get_db_connection()
active_clients = pd.read_sql_query("SELECT COUNT(*) as c FROM clients WHERE status='Active'", conn).iloc[0]['c']
active_programs = pd.read_sql_query("SELECT COUNT(*) as c FROM programs WHERE status='Active'", conn).iloc[0]['c']
total_enrollments = pd.read_sql_query("SELECT COUNT(*) as c FROM enrollments", conn).iloc[0]['c']
incomplete_assessments = pd.read_sql_query("SELECT COUNT(*) as c FROM assessments WHERE completed=0", conn).iloc[0]['c']
conn.close()

with col1:
    st.markdown(f'<div class="metric-box"><div class="metric-number">{active_clients}</div><div class="metric-label">Active Clients</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-box"><div class="metric-number">{active_programs}</div><div class="metric-label">Active Programs</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-box"><div class="metric-number">{total_enrollments}</div><div class="metric-label">Total Enrollments</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-box"><div class="metric-number" style="color:#DC2626">{incomplete_assessments}</div><div class="metric-label">Pending Assessments</div></div>', unsafe_allow_html=True)

st.markdown("---")

# Main query interface
st.markdown('<div class="section-header">Ask IMPOWR</div>', unsafe_allow_html=True)
st.markdown("Ask any question about your clients, programs, or outcomes in plain English.")

# Example questions
example_questions = [
    "How many clients completed the housing referral program?",
    "Show me all high-risk clients",
    "Summarize Marcus Thompson's case history",
    "Which assessments are incomplete?",
    "How many clients are enrolled in each program?",
    "Show me case notes for clients in the behavioral health program",
]

# Quick question buttons
st.markdown("**Try a sample question:**")
cols = st.columns(3)
for i, q in enumerate(example_questions):
    with cols[i % 3]:
        if st.button(q, key=f"example_{i}", use_container_width=True):
            st.session_state["current_question"] = q

# Text input
question = st.text_input(
    "Your question:",
    value=st.session_state.get("current_question", ""),
    placeholder="e.g., How many clients completed housing referrals in Q1?",
    label_visibility="collapsed",
)

# Process query
if st.button("Ask IMPOWR →", type="primary", use_container_width=True) and question:
    st.session_state.query_count += 1

    with st.spinner("Querying your data..."):
        try:
            # Step 1: Generate SQL
            sql = generate_sql(question)

            # Step 2: Execute SQL
            df, error = execute_sql(sql)

            if error:
                st.error(f"Query error: {error}")
            elif df is not None and len(df) > 0:
                # Step 3: Generate summary
                data_str = df.head(20).to_string(index=False)
                summary = generate_summary(question, data_str)
                tables_used = extract_tables_used(sql)

                # Display results
                st.markdown(f"""
                <div class="result-card">
                    <div class="section-header">Answer</div>
                    <p style="font-size: 1.05rem; color: #1B2A4A; line-height: 1.6; margin-top: 0.5rem;">
                        {summary}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Data table
                with st.expander(f"📊 View Source Data ({len(df)} records)", expanded=False):
                    st.dataframe(df, use_container_width=True, hide_index=True)

                # SQL Transparency
                with st.expander("🔍 View Generated SQL (Transparency Layer)", expanded=False):
                    st.markdown(f'<div class="sql-panel">{sql}</div>', unsafe_allow_html=True)

                # Source citation
                st.markdown("**Sources:** " + " ".join([f'<span class="source-badge">📁 {t}</span>' for t in tables_used]), unsafe_allow_html=True)

                # Audit log entry
                log_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "user": "demo_caseworker",
                    "question": question,
                    "tables_accessed": tables_used,
                    "records_returned": len(df),
                    "query_id": f"QRY-{st.session_state.query_count:04d}",
                }
                st.session_state.audit_log.insert(0, log_entry)

            else:
                st.info("No records found matching your question.")

        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            st.info("Make sure your Azure OpenAI credentials are set correctly in the app.py file or as environment variables.")

# Disclaimer
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ IMPOWR Copilot Prototype</strong> — All data shown is synthetic. No real PHI is used. 
    Every response is a draft for human review. AI suggests, caseworkers decide. 
    Built on Azure OpenAI with HIPAA BAA coverage. Data never leaves the customer's Azure tenant.
</div>
""", unsafe_allow_html=True)

# Audit Log Sidebar
with st.sidebar:
    st.markdown("""
    <div style="background:#1B2A4A; color:white; padding:1rem; border-radius:8px; margin-bottom:1rem;">
        <div style="font-size:1.2rem; font-weight:700;">IMP<span style="color:#E8632B;">O</span>WR Copilot</div>
        <div style="font-size:0.75rem; opacity:0.7; margin-top:0.3rem;">HIPAA Audit Trail</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**Instance:** Demo CBO Organization")
    st.markdown(f"**User:** Maria (Community Health Worker)")
    st.markdown(f"**Session queries:** {st.session_state.query_count}")
    st.markdown("---")

    st.markdown("### 📋 Audit Log")
    if st.session_state.audit_log:
        for entry in st.session_state.audit_log[:10]:
            st.markdown(f"""
            <div class="audit-entry">
                <strong>{entry['query_id']}</strong> · {entry['timestamp']}<br>
                <em>"{entry['question'][:60]}..."</em><br>
                Tables: {', '.join(entry['tables_accessed'])} · {entry['records_returned']} records
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("_No queries yet. Ask a question to begin._")

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.7rem; color:#888; text-align:center;">
        Alpha Architects · SimonAIThon 2025<br>
        Prototype — Synthetic Data Only
    </div>
    """, unsafe_allow_html=True)
