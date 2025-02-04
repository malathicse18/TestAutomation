import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient
from datetime import datetime

# Import database connection from your db file
from db import db  # Assuming you have a separate db file handling connection

def send_email(recipient, subject, message):
    sender_email = "your-email@example.com"  # Update with your email
    sender_password = "your-password"  # Update with your email password
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Update SMTP server details
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        return "Success"
    except Exception as e:
        return f"Failed: {str(e)}"

def fetch_scheduled_emails():
    schedules = db['greeting_schedules'].find()
    return schedules

def send_scheduled_emails():
    schedules = fetch_scheduled_emails()
    for schedule in schedules:
        current_time = datetime.now().strftime("%I:%M %p")
        if current_time == schedule['schedule_time']:
            for email in schedule['emails']:
                status = send_email(email, schedule['subject'], schedule['message'])
                log_email_status(email, schedule['subject'], schedule['message'], status)

def log_email_status(recipient, subject, message, status):
    log_entry = {
        "recipient": recipient,
        "subject": subject,
        "message": message,
        "sent_at": datetime.utcnow().isoformat(),
        "status": status
    }
    db['email_logs'].insert_one(log_entry)

# Schedule the job to run every minute
schedule.every(1).minutes.do(send_scheduled_emails)

if __name__ == "__main__":
    print("Email Automation Service Started...")
    while True:
        schedule.run_pending()
        time.sleep(60)
