from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os
from dotenv import load_dotenv


load_dotenv()


def attach_file(msg, filepath):
    with open(filepath, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())

    encoders.encode_base64(part)

    filename = os.path.basename(filepath)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')

    msg.attach(part)


def send_assignment_email(
        sender_name,
        github_repo_url,
        approach_summary,
        past_projects_links,
        screenshot_path='screenshots/confirmation.png',
        resume_path='attachments/resume.pdf'
):
    try:
        email_address = os.getenv("SENDER_EMAIL")
        email_password = os.getenv("SENDER_PASSWORD")

        if not email_address or not email_password:
            return False, "Email credentials not found"
        
        msg = MIMEMultipart()
        msg['From'] = email_address
        msg['To'] = "iamuchihadaniel236@gmail.com"
        msg['Cc'] = "iamuchihadaniel236@gmail.com"
        msg['Subject'] = f"Python (Selenium) Assignment - {sender_name}"

        if isinstance(past_projects_links, list):
            projects_text = '\n'.join(f"   - {link}" for link in past_projects_links)
        else:
            projects_text = f"  - {past_projects_links}"

        body = f"""Dear Hiring Team,
Please find my submission for the Python (Selenium) Assignment:

1. Screenshot of form filled via code: Attached (confirmation.png)

2. Source Code (GitHub Repository): 
   {github_repo_url}

3. Brief Documentation of Approach:
   {approach_summary}

4. Resume: Attached (resume.pdf)

5. Links to Past Projects/Work Samples:
{projects_text}

6. Availability Confirmation: 
   I confirm my availability to work full-time (10 AM to 7 PM) for the next 3-6 months.

Best regards,
{sender_name}
"""
        msg.attach(MIMEText(body, 'plain'))

        if os.path.exists(screenshot_path):
            attach_file(msg, screenshot_path)
        else:
            return False, f"Screenshot not found at {screenshot_path}"
        
        if os.path.exists(resume_path):
            attach_file(msg, resume_path)
        else:
            return False, f"Resume not found at {resume_path}"
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)

        recipients = ["iamuchihadaniel236@gmail.com", "iamuchihadaniel236@gmail.com"]
        server.send_message(msg)
        server.quit()

        return True, "Email sent successfully!"
    except FileNotFoundError as e:
        return False, f"File not found: {str(e)}"
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP Authentication failed. Check your email credentials."
    except Exception as e:
        return False, f"Error sending email: {str(e)}"