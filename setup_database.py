"""
IMPOWR Copilot Demo - Database Setup
Run this ONCE to create the synthetic database.
Command: python setup_database.py
"""
import sqlite3
import os

DB_PATH = "impowr_demo.db"

# Remove old database if exists
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ============================================================
# TABLE 1: CLIENTS
# ============================================================
cursor.execute("""
CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth TEXT,
    gender TEXT,
    primary_language TEXT DEFAULT 'English',
    zip_code TEXT,
    enrollment_date TEXT,
    status TEXT DEFAULT 'Active',
    risk_level TEXT DEFAULT 'Standard'
)
""")

clients = [
    (1, 'Marcus', 'Thompson', '1985-03-14', 'Male', 'English', '14604', '2024-01-15', 'Active', 'High'),
    (2, 'Elena', 'Rodriguez', '1992-07-22', 'Female', 'Spanish', '14606', '2024-02-01', 'Active', 'Standard'),
    (3, 'James', 'Washington', '1978-11-03', 'Male', 'English', '14605', '2023-09-10', 'Active', 'High'),
    (4, 'Aisha', 'Patel', '1990-05-18', 'Female', 'English', '14607', '2024-03-20', 'Active', 'Standard'),
    (5, 'Robert', 'Chen', '1965-08-30', 'Male', 'Mandarin', '14608', '2023-06-15', 'Active', 'High'),
    (6, 'Maria', 'Santos', '1988-12-11', 'Female', 'Spanish', '14604', '2024-01-30', 'Active', 'Standard'),
    (7, 'David', 'Kim', '1975-04-25', 'Male', 'Korean', '14609', '2023-11-01', 'Inactive', 'Standard'),
    (8, 'Sarah', 'Johnson', '1995-09-07', 'Female', 'English', '14610', '2024-04-01', 'Active', 'Low'),
    (9, 'Anthony', 'Brown', '1982-01-19', 'Male', 'English', '14604', '2023-08-22', 'Active', 'High'),
    (10, 'Lisa', 'Nguyen', '1998-06-14', 'Female', 'Vietnamese', '14611', '2024-02-14', 'Active', 'Standard'),
    (11, 'Michael', 'Davis', '1970-10-05', 'Male', 'English', '14605', '2023-07-01', 'Active', 'High'),
    (12, 'Jennifer', 'Martinez', '1993-02-28', 'Female', 'Spanish', '14606', '2024-03-15', 'Active', 'Standard'),
    (13, 'Carlos', 'Reyes', '1987-08-17', 'Male', 'Spanish', '14604', '2023-10-10', 'Active', 'Standard'),
    (14, 'Fatima', 'Ali', '1991-04-02', 'Female', 'Somali', '14607', '2024-01-05', 'Active', 'High'),
    (15, 'Thomas', 'Wilson', '1960-12-20', 'Male', 'English', '14608', '2023-05-15', 'Inactive', 'Low'),
    (16, 'Grace', 'Lee', '1996-07-09', 'Female', 'English', '14609', '2024-04-10', 'Active', 'Standard'),
    (17, 'Daniel', 'Garcia', '1983-03-31', 'Male', 'Spanish', '14610', '2024-02-20', 'Active', 'High'),
    (18, 'Priya', 'Sharma', '1989-11-15', 'Female', 'Hindi', '14604', '2023-12-01', 'Active', 'Standard'),
    (19, 'Kevin', 'Moore', '1977-06-23', 'Male', 'English', '14605', '2023-09-30', 'Active', 'High'),
    (20, 'Amanda', 'Taylor', '1994-01-08', 'Female', 'English', '14606', '2024-03-25', 'Active', 'Low'),
]
cursor.executemany("INSERT INTO clients VALUES (?,?,?,?,?,?,?,?,?,?)", clients)

# ============================================================
# TABLE 2: PROGRAMS
# ============================================================
cursor.execute("""
CREATE TABLE programs (
    program_id INTEGER PRIMARY KEY,
    program_name TEXT NOT NULL,
    program_type TEXT,
    funder TEXT,
    start_date TEXT,
    status TEXT DEFAULT 'Active'
)
""")

programs = [
    (1, 'Housing Referral Program', 'Housing', 'HUD CoC Grant', '2023-01-01', 'Active'),
    (2, 'Food Assistance Network', 'Food Security', 'USDA SNAP-Ed', '2023-01-01', 'Active'),
    (3, 'Behavioral Health Support', 'Mental Health', 'SAMHSA Block Grant', '2023-06-01', 'Active'),
    (4, 'IDD Residential Services', 'Disability Services', 'OPWDD Medicaid Waiver', '2023-01-01', 'Active'),
    (5, 'Chronic Disease Management', 'Health', 'NY DOH Prevention Grant', '2024-01-01', 'Active'),
    (6, 'Employment Readiness', 'Workforce', 'WIOA Title I', '2023-09-01', 'Active'),
]
cursor.executemany("INSERT INTO programs VALUES (?,?,?,?,?,?)", programs)

# ============================================================
# TABLE 3: ENROLLMENTS (clients in programs)
# ============================================================
cursor.execute("""
CREATE TABLE enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    program_id INTEGER,
    enrolled_date TEXT,
    completed_date TEXT,
    status TEXT DEFAULT 'Enrolled',
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
)
""")

enrollments = [
    (1, 1, 1, '2024-01-20', '2024-03-15', 'Completed'),
    (2, 1, 3, '2024-02-01', None, 'Enrolled'),
    (3, 2, 2, '2024-02-05', '2024-03-30', 'Completed'),
    (4, 2, 1, '2024-03-01', '2024-03-28', 'Completed'),
    (5, 3, 1, '2023-09-15', '2024-01-10', 'Completed'),
    (6, 3, 4, '2023-10-01', None, 'Enrolled'),
    (7, 4, 2, '2024-03-25', None, 'Enrolled'),
    (8, 4, 5, '2024-04-01', None, 'Enrolled'),
    (9, 5, 5, '2023-07-01', None, 'Enrolled'),
    (10, 5, 1, '2023-08-01', '2024-02-15', 'Completed'),
    (11, 6, 2, '2024-02-01', '2024-03-20', 'Completed'),
    (12, 6, 1, '2024-02-15', '2024-03-25', 'Completed'),
    (13, 7, 6, '2023-11-05', '2024-02-01', 'Completed'),
    (14, 8, 2, '2024-04-05', None, 'Enrolled'),
    (15, 9, 1, '2023-09-01', '2024-01-30', 'Completed'),
    (16, 9, 3, '2023-10-01', None, 'Enrolled'),
    (17, 10, 2, '2024-02-20', '2024-03-15', 'Completed'),
    (18, 10, 5, '2024-03-01', None, 'Enrolled'),
    (19, 11, 1, '2023-07-15', '2024-02-28', 'Completed'),
    (20, 11, 4, '2023-08-01', None, 'Enrolled'),
    (21, 12, 2, '2024-03-20', None, 'Enrolled'),
    (22, 13, 1, '2023-10-15', '2024-01-20', 'Completed'),
    (23, 13, 6, '2024-02-01', None, 'Enrolled'),
    (24, 14, 3, '2024-01-10', None, 'Enrolled'),
    (25, 14, 2, '2024-01-15', '2024-03-10', 'Completed'),
    (26, 16, 6, '2024-04-15', None, 'Enrolled'),
    (27, 17, 1, '2024-02-25', '2024-03-30', 'Completed'),
    (28, 17, 3, '2024-03-01', None, 'Enrolled'),
    (29, 18, 5, '2023-12-05', None, 'Enrolled'),
    (30, 19, 1, '2023-10-01', '2024-03-01', 'Completed'),
    (31, 19, 4, '2023-10-15', None, 'Enrolled'),
    (32, 20, 2, '2024-03-30', None, 'Enrolled'),
]
cursor.executemany("INSERT INTO enrollments VALUES (?,?,?,?,?,?)", enrollments)

# ============================================================
# TABLE 4: CASE_NOTES
# ============================================================
cursor.execute("""
CREATE TABLE case_notes (
    note_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    program_id INTEGER,
    note_date TEXT,
    note_type TEXT,
    summary TEXT,
    created_by TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(client_id),
    FOREIGN KEY (program_id) REFERENCES programs(program_id)
)
""")

case_notes = [
    (1, 1, 1, '2024-01-25', 'Home Visit', 'Initial housing assessment completed. Client needs 2BR apartment, near bus line. Applied to 3 housing programs.', 'Maria_CHW'),
    (2, 1, 1, '2024-02-10', 'Follow-up', 'Housing application approved by Provider B. Move-in date set for March 1. Client expressed relief.', 'Maria_CHW'),
    (3, 1, 1, '2024-03-15', 'Completion', 'Client successfully moved into new apartment. Housing referral program completed. Stable housing confirmed.', 'Maria_CHW'),
    (4, 1, 3, '2024-02-05', 'Intake', 'Behavioral health intake completed. Client reports anxiety related to housing instability. Referred to counseling.', 'David_SW'),
    (5, 1, 3, '2024-03-01', 'Session', 'Second counseling session. Client reports reduced anxiety since housing placement. Continuing weekly sessions.', 'David_SW'),
    (6, 2, 2, '2024-02-10', 'Enrollment', 'Client enrolled in food assistance. Family of 4, income below 130% FPL. SNAP application submitted.', 'Sarah_CM'),
    (7, 2, 2, '2024-03-15', 'Follow-up', 'SNAP benefits approved. Client receiving $680/month. Connected to community food pantry for supplemental support.', 'Sarah_CM'),
    (8, 3, 1, '2023-09-20', 'Home Visit', 'Client currently in temporary shelter. Needs permanent housing with accessibility features. Mobility limitations noted.', 'Maria_CHW'),
    (9, 3, 4, '2023-10-05', 'Assessment', 'IDD assessment completed. Client qualifies for residential support services. Care plan initiated.', 'Jennifer_IDD'),
    (10, 5, 5, '2023-07-15', 'Intake', 'Chronic disease management intake. Client has Type 2 diabetes and hypertension. A1C at 8.2. Medication review completed.', 'Priya_RN'),
    (11, 5, 5, '2024-01-10', 'Follow-up', 'A1C improved to 7.1. Blood pressure stable. Client adhering to medication schedule. Continue quarterly monitoring.', 'Priya_RN'),
    (12, 9, 1, '2023-09-15', 'Home Visit', 'Client at risk of eviction. Arrears of $2,400. Emergency rental assistance application submitted.', 'Maria_CHW'),
    (13, 9, 1, '2024-01-30', 'Completion', 'Rental assistance approved and disbursed. Eviction prevented. Client stable in current housing.', 'Maria_CHW'),
    (14, 14, 3, '2024-01-15', 'Intake', 'Behavioral health intake. Client reports depression and isolation after recent immigration. Interpreter services arranged.', 'David_SW'),
    (15, 14, 3, '2024-03-01', 'Session', 'Progress noted. Client connected to Somali community group. Mood improved. Continuing biweekly sessions.', 'David_SW'),
]
cursor.executemany("INSERT INTO case_notes VALUES (?,?,?,?,?,?,?)", case_notes)

# ============================================================
# TABLE 5: ASSESSMENTS
# ============================================================
cursor.execute("""
CREATE TABLE assessments (
    assessment_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    assessment_type TEXT,
    assessment_date TEXT,
    score REAL,
    risk_flag TEXT,
    completed INTEGER DEFAULT 1,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
)
""")

assessments = [
    (1, 1, 'PHQ-9 Depression Screen', '2024-01-20', 12.0, 'Moderate', 1),
    (2, 1, 'Housing Stability Index', '2024-01-20', 3.0, 'Unstable', 1),
    (3, 1, 'PHQ-9 Depression Screen', '2024-03-15', 6.0, 'Mild', 1),
    (4, 1, 'Housing Stability Index', '2024-03-15', 8.0, 'Stable', 1),
    (5, 2, 'Food Security Screen', '2024-02-05', 2.0, 'Low Security', 1),
    (6, 3, 'Housing Stability Index', '2023-09-15', 2.0, 'Unstable', 1),
    (7, 3, 'ADL Assessment', '2023-10-05', 14.0, 'Needs Support', 1),
    (8, 5, 'HbA1c Lab Result', '2023-07-15', 8.2, 'Above Target', 1),
    (9, 5, 'HbA1c Lab Result', '2024-01-10', 7.1, 'Improving', 1),
    (10, 9, 'Housing Stability Index', '2023-09-01', 1.0, 'Critical', 1),
    (11, 9, 'Housing Stability Index', '2024-01-30', 7.0, 'Stable', 1),
    (12, 14, 'PHQ-9 Depression Screen', '2024-01-10', 18.0, 'Severe', 1),
    (13, 14, 'PHQ-9 Depression Screen', '2024-03-01', 10.0, 'Moderate', 1),
    # Missing assessments (completed = 0) for compliance demo
    (14, 4, 'Food Security Screen', '2024-04-01', None, None, 0),
    (15, 8, 'Food Security Screen', '2024-04-05', None, None, 0),
    (16, 12, 'PHQ-9 Depression Screen', '2024-04-01', None, None, 0),
    (17, 16, 'Employment Readiness', '2024-04-15', None, None, 0),
    (18, 20, 'Food Security Screen', '2024-04-01', None, None, 0),
]
cursor.executemany("INSERT INTO assessments VALUES (?,?,?,?,?,?,?)", assessments)

conn.commit()
conn.close()

print("=" * 50)
print("  DATABASE CREATED SUCCESSFULLY!")
print("  File: impowr_demo.db")
print("=" * 50)
print("\nTables created:")
print("  - clients (20 records)")
print("  - programs (6 records)")
print("  - enrollments (32 records)")
print("  - case_notes (15 records)")
print("  - assessments (18 records)")
print("\nSample queries to try in the demo:")
print('  "How many clients completed the housing referral program in Q1 2025?"')
print('  "Show me all high-risk clients"')
print('  "Which programs have the most enrollments?"')
print('  "Summarize Marcus Thompson\'s case history"')
print('  "Which assessments are incomplete?"')
