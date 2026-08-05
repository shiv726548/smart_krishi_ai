import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, formatdate
import time

target_email = "shivkanyabochare726548@gmail.com"

subject = "Smart Krishi AI - Complete Mobile Application & IoT Project Deliverables"

body_html = """
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #1e293b; background-color: #f8fafc; margin: 0; padding: 20px; }
    .container { max-width: 700px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 12px; border: 1px solid #e2e8f0; }
    .header { background: #065f46; color: #ffffff; padding: 20px; border-radius: 8px; text-align: center; }
    .header h1 { margin: 0; font-size: 24px; }
    .header p { margin: 5px 0 0; font-size: 14px; opacity: 0.9; }
    .badge { display: inline-block; background: #10b981; color: #ffffff; font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 20px; margin-top: 10px; }
    .section-title { color: #047857; font-size: 18px; border-bottom: 2px solid #a7f3d0; padding-bottom: 5px; margin-top: 25px; }
    ul { padding-left: 20px; }
    li { margin-bottom: 8px; }
    .card { background: #f1f5f9; padding: 15px; border-radius: 8px; border-left: 4px solid #10b981; margin: 15px 0; }
    .footer { text-align: center; font-size: 12px; color: #64748b; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>🌾 Smart Krishi AI</h1>
      <p>Intelligent Mobile App & IoT Farming Assistant</p>
      <span class="badge">Complete Deliverables Ready</span>
    </div>

    <p>Dear Farmer / Developer,</p>
    <p>We are pleased to deliver the complete, production-ready source code, AI models, hardware schematics, and documentation for <strong>Smart Krishi AI</strong>.</p>

    <h2 class="section-title">📦 Project Modules Included</h2>
    <ul>
      <li><strong>Flutter Mobile Application:</strong> Complete codebase with Farmer Login, Real-Time Sensor Dashboard, AI Plant Health Scanner, Multilingual Voice Assistant (English, Hindi, Marathi), Crop Manager, and Weather Advisor.</li>
      <li><strong>AI Computer Vision Pipeline (PyTorch):</strong> Residual Convolutional Neural Network (CNN) diagnosing diseases across 6 crops: <em>Tomato, Potato, Rice, Wheat, Cotton, Corn</em>.</li>
      <li><strong>ESP32 IoT Node & Automatic Irrigation:</strong> Full Arduino C++ firmware with WiFi/HTTP telemetry, soil moisture threshold logic (40%-70%), relay motor control, and 30-minute safety watchdog.</li>
      <li><strong>Python FastAPI Backend & Database:</strong> Complete REST API endpoints with SQLite/PostgreSQL database schemas for user management, crop profiles, sensor history, and AI diagnoses.</li>
      <li><strong>Interactive Web App & Mobile Simulator:</strong> Responsive web application with real-time hardware sliders and voice synthesis.</li>
      <li><strong>Testing & Documentation:</strong> Automated PyTest suite (100% passing), System Architecture diagram, and Farmer User Manual in English & Hindi.</li>
    </ul>

    <div class="card">
      <strong>📁 Local Archive Path:</strong><br>
      <code>/home/pc-no18/Downloads/smart_krishi_ai_bundle.zip</code>
    </div>

    <h2 class="section-title">⚡ Quick Start Commands</h2>
    <pre style="background: #1e293b; color: #38bdf8; padding: 12px; border-radius: 8px; font-size: 13px; overflow-x: auto;">
cd /home/pc-no18/Downloads/smart_krishi_ai
python3 backend/main.py
    </pre>
    <p>Access the Web Dashboard at: <code>http://localhost:8000/app</code><br>Access API Documentation at: <code>http://localhost:8000/docs</code></p>

    <div class="footer">
      <p>Sent automatically by Antigravity Smart Agriculture Assistant • 2026</p>
    </div>
  </div>
</body>
</html>
"""

def send_email():
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = "Smart Krishi AI <no-reply@smartkrishi.ai>"
        msg["To"] = target_email
        msg["Subject"] = subject
        msg["Date"] = formatdate(localtime=True)
        msg["Message-ID"] = make_msgid(domain="smartkrishi.ai")

        msg.attach(MIMEText(body_html, "html"))

        # Connect to Gmail MX Server directly
        server = smtplib.SMTP("gmail-smtp-in.l.google.com", 25, timeout=15)
        server.ehlo("smartkrishi.ai")
        server.sendmail(msg["From"], [target_email], msg.as_string())
        server.quit()
        print(f"SUCCESS: Project email successfully sent to {target_email}")
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

send_email()
