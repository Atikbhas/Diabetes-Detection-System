import os
import io
import base64
import pickle
import sqlite3
import numpy as np
import pandas as pd
import matplotlib  # type: ignore[import-not-found]
matplotlib.use('Agg')  # Non-interactive backend for server-side chart rendering
import matplotlib.pyplot as plt  # type: ignore[import-not-found]

from flask import (  # type: ignore[import-not-found]
    Flask, render_template, request, redirect, 
    url_for, flash, send_file, abort, session
)
from flask_login import (  # type: ignore[import-not-found]
    LoginManager, UserMixin, login_user, 
    logout_user, login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

# Import ReportLab modules for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Import medical data config
from data_config.medical_data import (
    FIELD_GUIDANCE, HEALTHY_MEDIANS, WEEKLY_DIET_PLAN, 
    LIFESTYLE_RECOMMENDATIONS, DOCTOR_ADVISORY
)
from model.train_model import train_and_save_model
from init_db import init_database

app = Flask(__name__)
app.secret_key = 'diabetes_detection_system_secret_key_2026'

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'diabetes_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'model', 'scaler.pkl')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# User Model for Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email, is_admin):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = bool(is_admin)

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user_row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user_row:
        return User(user_row['id'], user_row['username'], user_row['email'], user_row['is_admin'])
    return None

# Load ML Model & Scaler on Startup
def load_ml_components():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        print("ML model files missing. Training model automatically...")
        train_and_save_model()
        
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    return model, scaler

# Ensure DB and ML model exist
init_database()
ml_model, ml_scaler = load_ml_components()

# Chart Generator 1: Risk Probability Gauge / Bar
def generate_risk_chart(probability):
    fig, ax = plt.subplots(figsize=(6, 2.2), dpi=150)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f8f9fa')
    
    color = '#198754' if probability < 40 else ('#ffc107' if probability < 70 else '#dc3545')
    
    # Horizontal progress bar representation
    ax.barh([0], [100], color='#e9ecef', height=0.5, edgecolor='none')
    ax.barh([0], [probability], color=color, height=0.5, edgecolor='none')
    
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, 0.6)
    ax.axis('off')
    
    # Annotate risk level & score
    ax.text(probability / 2 if probability > 15 else probability + 3, 0, f"{probability:.1f}%", 
            va='center', ha='center' if probability > 15 else 'left', 
            color='white' if probability > 15 else '#212529', fontweight='bold', fontsize=12)
    
    risk_label = "LOW RISK" if probability < 40 else ("MODERATE RISK" if probability < 70 else "HIGH RISK")
    ax.text(50, 0.4, f"Predicted Risk Score: {probability:.1f}% ({risk_label})", 
            ha='center', va='center', fontweight='bold', fontsize=11, color='#212529')
    
    plt.tight_layout()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())
    buf.seek(0)
    base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    raw_bytes = buf.getvalue()
    plt.close(fig)
    return base64_img, raw_bytes

# Chart Generator 2: Parameter Comparison Chart vs Healthy Reference Baseline
def generate_comparison_chart(inputs):
    fig, ax = plt.subplots(figsize=(7, 3.5), dpi=150)
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    
    metrics = ['Glucose', 'Blood Press.', 'Insulin', 'BMI']
    patient_vals = [inputs['glucose'], inputs['blood_pressure'], inputs['insulin'], inputs['bmi']]
    reference_vals = [HEALTHY_MEDIANS['glucose'], HEALTHY_MEDIANS['blood_pressure'], HEALTHY_MEDIANS['insulin'], HEALTHY_MEDIANS['bmi']]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    rects1 = ax.bar(x - width/2, patient_vals, width, label='Patient Level', color='#0d6efd', alpha=0.9)
    rects2 = ax.bar(x + width/2, reference_vals, width, label='Healthy Baseline Median', color='#198754', alpha=0.7)
    
    ax.set_ylabel('Measured Values', fontsize=10, fontweight='bold')
    ax.set_title('Patient Parameters vs. Healthy Population Baselines', fontsize=12, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontweight='bold', fontsize=10)
    ax.legend(frameon=True, facecolor='#f8f9fa', edgecolor='none')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    
    # Value labels on top of bars
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    base64_img = base64.b64encode(buf.getvalue()).decode('utf-8')
    raw_bytes = buf.getvalue()
    plt.close(fig)
    return base64_img, raw_bytes

# PDF Generation Function
def create_pdf_report(user_name, user_email, pred_row, risk_chart_bytes, comp_chart_bytes):
    pdf_buf = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buf, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Palette PDF styles
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontSize=20, leading=24, 
        textColor=colors.HexColor('#0d6efd'), fontName='Helvetica-Bold', alignment=0
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'], fontSize=10, leading=14, 
        textColor=colors.HexColor('#6c757d'), fontName='Helvetica'
    )
    heading2_style = ParagraphStyle(
        'DocH2', parent=styles['Heading2'], fontSize=14, leading=18, 
        textColor=colors.HexColor('#198754'), fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DocBody', parent=styles['Normal'], fontSize=9, leading=13, textColor=colors.HexColor('#212529')
    )
    bold_style = ParagraphStyle(
        'DocBold', parent=styles['Normal'], fontSize=9, leading=13, fontName='Helvetica-Bold', textColor=colors.HexColor('#212529')
    )
    disclaimer_style = ParagraphStyle(
        'DocDisc', parent=styles['Italic'], fontSize=8, leading=11, textColor=colors.HexColor('#856404')
    )
    
    # Header Section
    story.append(Paragraph("DIABETES DETECTION SYSTEM — HEALTH REPORT", title_style))
    story.append(Paragraph(f"Patient Name: <b>{user_name}</b> ({user_email}) | Date: {pred_row['created_at']}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0d6efd'), spaceBefore=8, spaceAfter=12))
    
    # Summary Outcome Table
    res_color = colors.HexColor('#dc3545') if pred_row['result'] == 'Diabetic' else colors.HexColor('#198754')
    summary_data = [
        [Paragraph("Screening Result:", bold_style), Paragraph(f"<font color='{res_color.hexval()}'><b>{pred_row['result'].upper()}</b></font>", bold_style)],
        [Paragraph("Diabetes Probability Score:", bold_style), Paragraph(f"<b>{pred_row['probability']:.1f}%</b>", body_style)],
        [Paragraph("Evaluation Model:", bold_style), Paragraph("Scikit-Learn Random Forest Classifier (Pima Indians Dataset)", body_style)]
    ]
    summary_table = Table(summary_data, colWidths=[2.2*inch, 4.8*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8f9fa')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#dee2e6')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))
    
    # Patient Inputs Table
    story.append(Paragraph("Clinical Metrics Recorded", heading2_style))
    input_table_data = [
        [Paragraph("<b>Metric</b>", body_style), Paragraph("<b>Value Recorded</b>", body_style), Paragraph("<b>Normal Range Reference</b>", body_style)],
        [Paragraph("Glucose", body_style), Paragraph(f"{pred_row['glucose']} mg/dL", body_style), Paragraph(FIELD_GUIDANCE['glucose']['normal_range'], body_style)],
        [Paragraph("Blood Pressure", body_style), Paragraph(f"{pred_row['blood_pressure']} mm Hg", body_style), Paragraph(FIELD_GUIDANCE['blood_pressure']['normal_range'], body_style)],
        [Paragraph("BMI", body_style), Paragraph(f"{pred_row['bmi']} kg/m²", body_style), Paragraph(FIELD_GUIDANCE['bmi']['normal_range'], body_style)],
        [Paragraph("Insulin Level", body_style), Paragraph(f"{pred_row['insulin']} mu U/ml", body_style), Paragraph(FIELD_GUIDANCE['insulin']['normal_range'], body_style)],
        [Paragraph("Skin Thickness", body_style), Paragraph(f"{pred_row['skin_thickness']} mm", body_style), Paragraph(FIELD_GUIDANCE['skin_thickness']['normal_range'], body_style)],
        [Paragraph("Diabetes Pedigree", body_style), Paragraph(f"{pred_row['diabetes_pedigree']}", body_style), Paragraph(FIELD_GUIDANCE['diabetes_pedigree']['normal_range'], body_style)],
        [Paragraph("Pregnancies", body_style), Paragraph(f"{pred_row['pregnancies']}", body_style), Paragraph(FIELD_GUIDANCE['pregnancies']['normal_range'], body_style)],
        [Paragraph("Age", body_style), Paragraph(f"{pred_row['age']} years", body_style), Paragraph("21 - 80+ years", body_style)],
    ]
    inp_table = Table(input_table_data, colWidths=[2.3*inch, 2.3*inch, 2.4*inch])
    inp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e9ecef')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ced4da')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(inp_table)
    story.append(Spacer(1, 10))
    
    # Visualizations
    story.append(Paragraph("Risk & Metric Visualizations", heading2_style))
    img_risk = Image(io.BytesIO(risk_chart_bytes), width=5.5*inch, height=2.0*inch)
    img_comp = Image(io.BytesIO(comp_chart_bytes), width=5.8*inch, height=2.9*inch)
    story.append(img_risk)
    story.append(Spacer(1, 8))
    story.append(img_comp)
    story.append(Spacer(1, 10))
    
    # Diabetic Plan & Doctor Advisory (if diabetic)
    if pred_row['result'] == 'Diabetic':
        story.append(Paragraph("Doctor Consultation & Advisory", heading2_style))
        story.append(Paragraph(f"<b>Immediate Action:</b> {DOCTOR_ADVISORY['immediate_consultation']['description']}", body_style))
        story.append(Spacer(1, 4))
        story.append(Paragraph("<b>Recommended Diagnostic Tests:</b> " + ", ".join(DOCTOR_ADVISORY['diagnostic_tests_to_ask_for']), body_style))
        story.append(Spacer(1, 10))
        
        story.append(Paragraph("Recommended 7-Day Diabetes Management Meal Plan", heading2_style))
        diet_data = [[Paragraph("<b>Day</b>", body_style), Paragraph("<b>Breakfast</b>", body_style), Paragraph("<b>Lunch</b>", body_style), Paragraph("<b>Dinner</b>", body_style)]]
        for day in WEEKLY_DIET_PLAN:
            diet_data.append([
                Paragraph(f"<b>{day['day']}</b>", body_style),
                Paragraph(day['breakfast'], body_style),
                Paragraph(day['lunch'], body_style),
                Paragraph(day['dinner'], body_style)
            ])
        diet_table = Table(diet_data, colWidths=[1.1*inch, 2.0*inch, 2.0*inch, 1.9*inch])
        diet_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#d1e7dd')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#a3cfbb')),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(diet_table)
        story.append(Spacer(1, 10))
        
    # Medical Disclaimer Footer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#ffc107'), spaceBefore=8, spaceAfter=8))
    story.append(Paragraph(f"<b>Medical Disclaimer:</b> {DOCTOR_ADVISORY['disclaimer']}", disclaimer_style))
    
    doc.build(story)
    pdf_buf.seek(0)
    return pdf_buf

# Prediction Execution & DB Helper
def process_prediction_and_save(user_id, form_dict):
    pregnancies = int(form_dict.get('pregnancies', 0))
    glucose = float(form_dict.get('glucose', 0.0))
    blood_pressure = float(form_dict.get('blood_pressure', 0.0))
    skin_thickness = float(form_dict.get('skin_thickness', 0.0))
    insulin = float(form_dict.get('insulin', 0.0))
    bmi = float(form_dict.get('bmi', 0.0))
    diabetes_pedigree = float(form_dict.get('diabetes_pedigree', 0.0))
    age = int(form_dict.get('age', 0))
    
    input_features = np.array([[
        pregnancies, glucose, blood_pressure, 
        skin_thickness, insulin, bmi, 
        diabetes_pedigree, age
    ]])
    
    scaled_features = ml_scaler.transform(input_features)
    pred_class = ml_model.predict(scaled_features)[0]
    pred_proba = ml_model.predict_proba(scaled_features)[0][1] * 100.0
    
    result_str = 'Diabetic' if pred_class == 1 else 'Not Diabetic'
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (user_id, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age, result, probability)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age, result_str, round(pred_proba, 2)))
    pred_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return pred_id

# ROUTES

@app.route('/')
def home():
    return render_template('home.html', guidance=FIELD_GUIDANCE)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject', 'General Inquiry')
        message = request.form.get('message')
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO contact_submissions (name, email, subject, message)
            VALUES (?, ?, ?, ?)
        ''', (name, email, subject, message))
        conn.commit()
        conn.close()
        
        flash('Thank you for contacting us! Your message has been received.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('predict'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('signup.html')
            
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html')
            
        pwd_hash = generate_password_hash(password)
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO users (username, email, password_hash, is_admin)
                VALUES (?, ?, ?, 0)
            ''', (username, email, pwd_hash))
            conn.commit()
            
            user_row = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            conn.close()
            
            user_obj = User(user_row['id'], user_row['username'], user_row['email'], user_row['is_admin'])
            login_user(user_obj)
            flash('Account created successfully! Welcome to Diabetes Detection System.', 'success')
            
            # Auto-process pending prediction if guest filled form prior to signup
            pending_pred = session.pop('pending_prediction', None)
            if pending_pred:
                try:
                    pred_id = process_prediction_and_save(user_obj.id, pending_pred)
                    flash('Your risk assessment report has been generated successfully!', 'success')
                    return redirect(url_for('result', pred_id=pred_id))
                except Exception as e:
                    flash(f'Error processing your saved assessment: {str(e)}', 'danger')
                    
            return redirect(url_for('predict'))
        except sqlite3.IntegrityError:
            conn.close()
            flash('Username or email already registered.', 'danger')
            return render_template('signup.html')
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('predict'))
        
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password')
        
        conn = get_db_connection()
        user_row = conn.execute(
            'SELECT * FROM users WHERE username = ? OR email = ?', (identifier, identifier.lower())
        ).fetchone()
        conn.close()
        
        if user_row and check_password_hash(user_row['password_hash'], password):
            user_obj = User(user_row['id'], user_row['username'], user_row['email'], user_row['is_admin'])
            login_user(user_obj)
            flash(f'Welcome back, {user_obj.username}!', 'success')
            
            # Auto-process pending prediction if guest filled form prior to login
            pending_pred = session.pop('pending_prediction', None)
            if pending_pred:
                try:
                    pred_id = process_prediction_and_save(user_obj.id, pending_pred)
                    flash('Your risk assessment report has been generated successfully!', 'success')
                    return redirect(url_for('result', pred_id=pred_id))
                except Exception as e:
                    flash(f'Error processing your saved assessment: {str(e)}', 'danger')

            next_page = request.args.get('next')
            if user_obj.is_admin and not next_page:
                return redirect(url_for('admin_dashboard'))
            return redirect(next_page or url_for('predict'))
        else:
            flash('Invalid username/email or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            form_data = {
                'pregnancies': request.form.get('pregnancies', 0),
                'glucose': request.form.get('glucose', 0.0),
                'blood_pressure': request.form.get('blood_pressure', 0.0),
                'skin_thickness': request.form.get('skin_thickness', 0.0),
                'insulin': request.form.get('insulin', 0.0),
                'bmi': request.form.get('bmi', 0.0),
                'diabetes_pedigree': request.form.get('diabetes_pedigree', 0.0),
                'age': request.form.get('age', 0)
            }
            
            if not current_user.is_authenticated:
                session['pending_prediction'] = form_data
                flash('Please log in or sign up to view your personalized risk assessment report.', 'warning')
                return redirect(url_for('login'))
                
            pred_id = process_prediction_and_save(current_user.id, form_data)
            return redirect(url_for('result', pred_id=pred_id))
            
        except Exception as e:
            flash(f'Error processing prediction input: {str(e)}', 'danger')
            return redirect(url_for('predict'))
            
    return render_template('predict.html', guidance=FIELD_GUIDANCE)

@app.route('/result/<int:pred_id>')
@login_required
def result(pred_id):
    conn = get_db_connection()
    pred_row = conn.execute('SELECT * FROM predictions WHERE id = ?', (pred_id,)).fetchone()
    conn.close()
    
    if not pred_row:
        flash('Prediction record not found.', 'danger')
        return redirect(url_for('history'))
        
    # Security check: User can view their own predictions or Admin can view any
    if pred_row['user_id'] != current_user.id and not current_user.is_admin:
        abort(403)
        
    inputs = {
        'glucose': pred_row['glucose'],
        'blood_pressure': pred_row['blood_pressure'],
        'insulin': pred_row['insulin'],
        'bmi': pred_row['bmi'],
        'skin_thickness': pred_row['skin_thickness'],
        'pregnancies': pred_row['pregnancies'],
        'diabetes_pedigree': pred_row['diabetes_pedigree'],
        'age': pred_row['age']
    }
    
    risk_img_base64, _ = generate_risk_chart(pred_row['probability'])
    comp_img_base64, _ = generate_comparison_chart(inputs)
    
    return render_template(
        'result.html', 
        pred=pred_row, 
        risk_img=risk_img_base64, 
        comp_img=comp_img_base64,
        diet_plan=WEEKLY_DIET_PLAN,
        lifestyle=LIFESTYLE_RECOMMENDATIONS,
        advisory=DOCTOR_ADVISORY
    )

@app.route('/download_report/<int:pred_id>')
@login_required
def download_report(pred_id):
    conn = get_db_connection()
    pred_row = conn.execute('SELECT * FROM predictions WHERE id = ?', (pred_id,)).fetchone()
    user_row = conn.execute('SELECT username, email FROM users WHERE id = ?', (pred_row['user_id'],)).fetchone() if pred_row else None
    conn.close()
    
    if not pred_row or not user_row:
        flash('Prediction record not found.', 'danger')
        return redirect(url_for('history'))
        
    if pred_row['user_id'] != current_user.id and not current_user.is_admin:
        abort(403)
        
    inputs = {
        'glucose': pred_row['glucose'],
        'blood_pressure': pred_row['blood_pressure'],
        'insulin': pred_row['insulin'],
        'bmi': pred_row['bmi']
    }
    
    _, risk_bytes = generate_risk_chart(pred_row['probability'])
    _, comp_bytes = generate_comparison_chart(inputs)
    
    pdf_buffer = create_pdf_report(
        user_row['username'], user_row['email'], pred_row, risk_bytes, comp_bytes
    )
    
    return send_file(
        pdf_buffer, 
        as_attachment=True, 
        download_name=f"DDS_Diabetes_Report_{user_row['username']}_{pred_id}.pdf",
        mimetype='application/pdf'
    )

@app.route('/history')
@login_required
def history():
    conn = get_db_connection()
    search = request.args.get('search', '').strip()
    result_filter = request.args.get('result_filter', '').strip()
    
    query = 'SELECT * FROM predictions WHERE user_id = ?'
    params = [current_user.id]
    
    if result_filter:
        query += ' AND result = ?'
        params.append(result_filter)
        
    query += ' ORDER BY created_at DESC'
    predictions = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('history.html', predictions=predictions, result_filter=result_filter)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        rating = int(request.form.get('rating', 5))
        message = request.form.get('message', '').strip()
        
        if not name or not email or not message:
            flash('Name, email, and feedback message are required.', 'danger')
            return render_template('feedback.html')
            
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO feedback (name, email, rating, message)
            VALUES (?, ?, ?, ?)
        ''', (name, email, rating, message))
        conn.commit()
        conn.close()
        
        flash('Thank you for your valuable feedback!', 'success')
        return redirect(url_for('feedback'))
        
    return render_template('feedback.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Administrator privileges required.', 'danger')
        return redirect(url_for('home'))
        
    user_filter = request.args.get('user_id', '')
    result_filter = request.args.get('result_filter', '')
    
    conn = get_db_connection()
    
    # Query summary counts
    total_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    total_preds = conn.execute('SELECT COUNT(*) FROM predictions').fetchone()[0]
    diabetic_count = conn.execute('SELECT COUNT(*) FROM predictions WHERE result = "Diabetic"').fetchone()[0]
    feedback_count = conn.execute('SELECT COUNT(*) FROM feedback').fetchone()[0]
    
    # Build predictions query
    pred_query = '''
        SELECT p.*, u.username, u.email 
        FROM predictions p 
        JOIN users u ON p.user_id = u.id 
        WHERE 1=1
    '''
    pred_params = []
    
    if user_filter:
        pred_query += ' AND p.user_id = ?'
        pred_params.append(user_filter)
        
    if result_filter:
        pred_query += ' AND p.result = ?'
        pred_params.append(result_filter)
        
    pred_query += ' ORDER BY p.created_at DESC'
    
    all_predictions = conn.execute(pred_query, pred_params).fetchall()
    all_users = conn.execute('SELECT id, username, email, is_admin, created_at FROM users ORDER BY created_at DESC').fetchall()
    all_feedback = conn.execute('SELECT * FROM feedback ORDER BY created_at DESC').fetchall()
    conn.close()
    
    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_preds=total_preds,
        diabetic_count=diabetic_count,
        feedback_count=feedback_count,
        predictions=all_predictions,
        users=all_users,
        feedbacks=all_feedback,
        selected_user=user_filter,
        selected_result=result_filter
    )

if __name__ == '__main__':
    print("Starting Diabetes Detection System Flask Application...")
    app.run(host='0.0.0.0', port=5000, debug=True)
