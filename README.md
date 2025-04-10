# 5005CMDJUSTINTIME
# JustInTime – Manufacturing Management System

JustInTime is a Flask-based web application designed for FloatFry, a fictional frying pan manufacturing company. This system helps manage the production process efficiently through role-based access, task tracking, inventory control, and real-time machine monitoring.

---

## 🚀 Features

- 🔐 **User Roles & Authentication**
  - Customer registration & login
  - Company staff registration/login
  - Worker-specific logins (Stamper, Operative)
  
- 📦 **Inventory & Order Management**
  - Place, view, and manage customer orders
  - Admin approval workflow
  
- 🛠️ **Task Assignment**
  - Assign tasks to floor workers based on job roles

- 📊 **Reports & Monitoring**
  - Real-time machine tracking
  - PDF report generation for completed jobs

---

## 🖥️ System Requirements

- Python 3.8+
- Flask
- MySQL (via MAMP/XAMPP)
- phpMyAdmin
- ReportLab (for PDF generation)

---

## 🛠️ Setup Instructions

See `Project_Setup_Instructions.docx` for full setup guidance.

### 🔧 Quick Setup

#### 1. **Database Setup**
- Start MAMP/XAMPP and open phpMyAdmin.
- Create a new database (e.g., `project_db`).
- Import `final_queries.txt` into your database.

#### 2. **App Setup**
pip install flask
pip install reportlab
python app.py
Python Dependencies to Install
pip install flask
pip install flask-mysqldb
pip install reportlab
pip install werkzeug
pip install flask-session
pip install flask-login
pip install python-dotenv
pip install flask-debugtoolbar
pip install black
pip install pylint

## 🌐 App Access Links (Localhost)

### Customer:
- Register: `http://127.0.0.1:5000/customer/register`
- Login: `http://127.0.0.1:5000/customer/login`

### Admin/Manager:
- Register: `http://127.0.0.1:5000/register`
- Login: `http://127.0.0.1:5000/login`
- Dashboard: `http://127.0.0.1:5000/dashboard`

### Workers:
- Stamper Login: `http://127.0.0.1:5000/stamper_login`
- Operative Login: `http://127.0.0.1:5000/operative_login`
## 📝 License

This project is part of an academic software engineering module and is intended for learning purposes only.  

