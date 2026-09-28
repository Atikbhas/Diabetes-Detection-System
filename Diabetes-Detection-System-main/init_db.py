# ==============================================================================
# DIABETES DETECTION SYSTEM — DATABASE INITIALIZATION SCRIPT
# ==============================================================================
# Initializes SQLite database schema (users, predictions, feedback, contact).
# Aa script SQLite database initialize kare chhe, badha tables banave chhe,
# ane pre-seeded admin/user demo accounts create kare chhe.
# ==============================================================================

import sqlite3
import os
from werkzeug.security import generate_password_hash

def init_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'database.db')
    
    print(f"Initializing SQLite database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # --------------------------------------------------------------------------
    # TABLE 1: USERS TABLE (User authentication & role storage)
    # Users no table - jema username, email, password hash ane admin flag save thase.
    # --------------------------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # --------------------------------------------------------------------------
    # TABLE 2: PREDICTIONS TABLE (Patient clinical metric log & ML results)
    # Patient na assessment results ane 8 clinical metrics save karva mate.
    # --------------------------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            pregnancies INTEGER,
            glucose REAL,
            blood_pressure REAL,
            skin_thickness REAL,
            insulin REAL,
            bmi REAL,
            diabetes_pedigree REAL,
            age INTEGER,
            result TEXT NOT NULL,
            probability REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # --------------------------------------------------------------------------
    # TABLE 3: FEEDBACK TABLE (User rating & review collection)
    # User feedback ane ratings store karva mate.
    # --------------------------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # --------------------------------------------------------------------------
    # TABLE 4: CONTACT SUBMISSIONS TABLE (Support form submissions)
    # Contact page par thi aavela inquiry messages store thase.
    # --------------------------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # --------------------------------------------------------------------------
    # SEED DATA: ADMIN & DEMO PATIENT ACCOUNTS
    # Default demo accounts: Jay Sitapara (Admin), Atik Bhas (Admin), demo_patient
    # --------------------------------------------------------------------------
    preseeded_users = [
        ('Jay Sitapara', 'jay.sitapara@dds.com', generate_password_hash('admin123'), 1),
        ('Atik Bhas', 'atik.bhas@dds.com', generate_password_hash('admin123'), 1),
        ('demo_patient', 'patient@dds.com', generate_password_hash('user123'), 0)
    ]
    
    for username, email, pwd_hash, is_admin in preseeded_users:
        cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
        row = cursor.fetchone()
        if not row:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, is_admin)
                VALUES (?, ?, ?, ?)
            ''', (username, email, pwd_hash, is_admin))
            print(f"Created preseeded user: {username} (Admin: {is_admin})")
        else:
            # Ensure names and emails are updated
            cursor.execute('''
                UPDATE users SET username = ?, email = ?, is_admin = ? WHERE id = ?
            ''', (username, email, is_admin, row[0]))
            
    # Get user ids for sample prediction mapping
    cursor.execute('SELECT id FROM users WHERE username IN ("demo_patient", "Jay Sitapara")')
    patient_row = cursor.fetchone()
    patient_id = patient_row[0] if patient_row else 3

    cursor.execute('SELECT id FROM users WHERE username = "Jay Sitapara"')
    jay_row = cursor.fetchone()
    jay_id = jay_row[0] if jay_row else 1

    # --------------------------------------------------------------------------
    # SEED DATA: SAMPLE PREDICTIONS LOGS
    # Demo history test karva mate sample records insert thay chhe.
    # --------------------------------------------------------------------------
    cursor.execute('SELECT COUNT(*) FROM predictions')
    if cursor.fetchone()[0] == 0:
        sample_preds = [
            (patient_id, 2, 148.0, 72.0, 35.0, 160.0, 33.6, 0.627, 50, 'Diabetic', 78.5, '2026-09-10 10:15:00'),
            (patient_id, 1, 85.0, 66.0, 29.0, 70.0, 26.6, 0.351, 31, 'Not Diabetic', 14.2, '2026-09-12 14:30:00'),
            (jay_id, 0, 175.0, 80.0, 28.0, 210.0, 31.2, 0.750, 42, 'Diabetic', 84.0, '2026-09-14 09:45:00'),
            (patient_id, 1, 110.0, 70.0, 22.0, 80.0, 23.4, 0.250, 28, 'Not Diabetic', 22.0, '2026-09-15 16:20:00')
        ]
        cursor.executemany('''
            INSERT INTO predictions (user_id, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age, result, probability, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_preds)
        print("Preseeded sample prediction records.")
        
    # --------------------------------------------------------------------------
    # SEED DATA: SAMPLE FEEDBACK ENTRIES
    # Initial user reviews ane testimonials insert karva mate.
    # --------------------------------------------------------------------------
    cursor.execute('SELECT COUNT(*) FROM feedback')
    if cursor.fetchone()[0] == 0:
        sample_feedback = [
            ('Jay Sitapara', 'jay.sitapara@dds.com', 5, 'Extremely helpful tool! The BMI calculator and guidance notes were very easy to follow.', '2026-09-11 11:20:00'),
            ('Atik Bhas', 'atik.bhas@dds.com', 5, 'Great visualization charts and instant PDF download. Really appreciate the 7-day diet suggestions.', '2026-09-13 15:45:00')
        ]
        cursor.executemany('''
            INSERT INTO feedback (name, email, rating, message, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', sample_feedback)
        print("Preseeded sample feedback submissions.")

    conn.commit()
    conn.close()
    print("Database initialization complete.")

if __name__ == '__main__':
    init_database()
