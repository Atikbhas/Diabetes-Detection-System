# 🩺 Diabetes Detection System (DDS)

An AI-driven full-stack web application built with **Python Flask**, **Scikit-Learn Machine Learning**, **SQLite**, **Matplotlib**, **ReportLab**, and **Bootstrap 5**.

The system predicts diabetes risk based on 8 clinical physiological parameters, provides pre-prediction medical guidance, renders visual risk gauge charts, constructs customized 7-day meal plans and doctor advisories, generates downloadable PDF reports, and features a dedicated role-based Admin Panel.

---

## ✨ Features

- **Machine Learning Screening**: RandomForest Classifier trained on the Pima Indians Diabetes Dataset.
- **Pre-Prediction Guidance & BMI Calculator**: "Don't know your numbers?" guidance for each field + interactive BMI calculator widget that auto-fills the form.
- **Visual Risk Analytics**: Server-side Matplotlib risk gauge charts and patient vs. healthy baseline comparison charts.
- **Dietary & Doctor Consultation Advisory**: 7-day diabetes management meal plan, lifestyle tips, immediate/routine consultation guidance, recommended specialists, and HbA1c test notes.
- **Downloadable PDF Reports**: Full report export using ReportLab with embedded charts and advisories.
- **User Authentication & History**: Password hashing (`werkzeug.security`), session management (`Flask-Login`), and prediction history log.
- **Role-Based Admin Panel**: Protected `/admin` route showing system stats, all user prediction logs with filters, user accounts, and feedback submissions.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask, Flask-Login, Werkzeug
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Visualizations**: Matplotlib, Seaborn
- **PDF Generation**: ReportLab
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons

---

## 🔑 Pre-Configured Demo Credentials

| Role | Username | Email | Password |
| :--- | :--- | :--- | :--- |
| **Admin** | `Jay` | `jay@dds.com` | `admin123` |
| **Admin** | `Atik` | `atik@dds.com` | `admin123` |
| **Patient** | `demo_patient` | `patient@dds.com` | `user123` |

---

## 🚀 Quick Start Guide

### 1. Clone & Navigate
```bash
git clone https://github.com/Atikbhas/Diabetes-Detection-System.git
cd Diabetes-Detection-System
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```
Open **`http://127.0.0.1:5000/`** in your browser.

---

## 📂 Project Structure

```
.
├── app.py                      # Main Flask application & routes
├── requirements.txt            # Dependency manifest
├── database.db                 # SQLite database (auto-generated)
├── init_db.py                  # Database setup & seed script
├── data/
│   └── diabetes.csv            # Pima Indians Diabetes Dataset
├── model/
│   ├── train_model.py          # ML training script
│   ├── diabetes_model.pkl      # Saved trained model
│   └── scaler.pkl              # Saved feature scaler
├── data_config/
│   └── medical_data.py         # Static guidance text, meal plans & advisories
├── static/
│   ├── css/style.css           # Custom medical styling
│   └── js/main.js              # Interactive BMI calculator script
└── templates/
    ├── base.html               # Shared layout & navbar
    ├── home.html               # Landing page with embedded assessment form
    ├── stats.html              # Global & India diabetes statistics page
    ├── predict.html            # Dedicated assessment form
    ├── result.html             # Outcome, charts, diet plan & doctor advisory
    ├── history.html            # User history log
    ├── feedback.html           # User feedback page
    ├── components/
    │   └── assessment_form.html# Reusable form component
    └── admin/
        └── dashboard.html      # Protected Admin Dashboard
```

---

## ⚠️ Medical Disclaimer
This software is intended strictly as an educational screening tool and does not provide formal medical diagnosis or treatment. Always consult a licensed healthcare professional for clinical evaluations.
