import smtplib
import schedule
import time
from pymongo import MongoClient
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['file_management']

def configure_email():
    """Allows users to configure email settings and store them in MongoDB."""
    recipients = input("Enter recipient emails (comma-separated): ").split(',')
    subject = input("Enter email subject: ")
    message = input("Enter email message: ")
    schedule_time = input("Enter scheduled time (e.g., 09:00 AM): ")

    email_config = {
        "emails": [email.strip() for email in recipients],
        "subject": subject,
        "message": message,
        "schedule_time": schedule_time
    }

    db.greeting_schedules.insert_one(email_config)
    print("Email configuration saved successfully!")

def send_emails():
    """Fetch scheduled emails from MongoDB and send them using SMTP."""
    email_configs = db.greeting_schedules.find()
    
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your password

    for config in email_configs:
        for recipient in config['emails']:
            try:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = recipient
                msg['Subject'] = config['subject']
                msg.attach(MIMEText(config['message'], 'plain'))

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.sendmail(sender_email, recipient, msg.as_string())

                log_email(recipient, config['subject'], config['message'], "Success")
                print(f"Email sent successfully to {recipient}")

            except Exception as e:
                log_email(recipient, config['subject'], config['message'], f"Failed: {str(e)}")
                print(f"Failed to send email to {recipient}: {e}")

def log_email(recipient, subject, message, status):
    """Log sent emails to MongoDB."""
    log_entry = {
        "recipient": recipient,
        "subject": subject,
        "message": message,
        "sent_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "status": status
    }
    db.email_logs.insert_one(log_entry)

def schedule_email_sending():
    """Schedule email sending at the configured time."""
    schedules = db.greeting_schedules.find()
    for schedule_entry in schedules:
        schedule_time = schedule_entry['schedule_time']
import re

def is_valid_time_format(time_str):
    return re.match(r"^([01]\d|2[0-3]):([0-5]\d)(:[0-5]\d)?$", time_str)

def schedule_email_sending():
    while True:
        schedule_time = input("Enter the email schedule time (HH:MM, 24-hour format): ").strip()

        if not is_valid_time_format(schedule_time):
            print("❌ Invalid time format! Please enter time in HH:MM (24-hour format).")
            continue  # Ask again if the format is incorrect
        
        schedule.every().day.at(schedule_time).do(send_emails)
        print(f"✅ Emails scheduled daily at {schedule_time}.")
        break  # Exit loop after valid input

    while True:
        schedule.run_pending()
        time.sleep(60)
    

