import sqlite3
import os
from werkzeug.security import generate_password_hash

def init_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, 'database.db')
    
    print(f"Initializing SQLite database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
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
    
    # Create predictions table
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
    
    # Create feedback table
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
    
    # Create contact_submissions table
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
    
    # Pre-seed Admin and User accounts
    preseeded_users = [
        ('Jay', 'jay@dds.com', generate_password_hash('admin123'), 1),
        ('Atik', 'atik@dds.com', generate_password_hash('admin123'), 1),
        ('demo_patient', 'patient@dds.com', generate_password_hash('user123'), 0)
    ]
    
    for username, email, pwd_hash, is_admin in preseeded_users:
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, is_admin)
                VALUES (?, ?, ?, ?)
            ''', (username, email, pwd_hash, is_admin))
            print(f"Created preseeded user: {username} (Admin: {is_admin})")
            
    # Get user ids
    cursor.execute('SELECT id FROM users WHERE username = "demo_patient"')
    patient_row = cursor.fetchone()
    patient_id = patient_row[0] if patient_row else 3

    cursor.execute('SELECT id FROM users WHERE username = "Jay"')
    jay_row = cursor.fetchone()
    jay_id = jay_row[0] if jay_row else 1

    # Pre-seed sample predictions if empty
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
        
    # Pre-seed sample feedback if empty
    cursor.execute('SELECT COUNT(*) FROM feedback')
    if cursor.fetchone()[0] == 0:
        sample_feedback = [
            ('Sarah Jenkins', 'sarah@example.com', 5, 'Extremely helpful tool! The BMI calculator and guidance notes were very easy to follow.', '2026-09-11 11:20:00'),
            ('Robert Chen', 'robert@example.com', 4, 'Great visualization charts and instant PDF download. Really appreciate the 7-day diet suggestions.', '2026-09-13 15:45:00')
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
