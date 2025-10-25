from flask import Flask, jsonify
from email_utils import send_assignment_email


app = Flask(__name__)


@app.route('/send-email')
def trigger_email():
    success, message =  send_assignment_email(
        sender_name="Daniel Popoola",
        github_repo_url="https://github.com/yourusername/selenium-form-automation",
        approach_summary=(
            "Used Selenium WebDriver to automate Google Form submission. "
            "Implemented explicit waits for dynamic elements, handled date fields "
            "using JavaScript execution, and captured confirmation screenshot. "
            "Email automation implemented using Flask and smtplib."
        ),
        past_projects_links=[
            "https://github.com/DanielPopoola/job_scraper",
            "https://github.com/DanielPopoola/digital-wallet-system",
            "https://github.com/DanielPopoola/currency_converter",
        ],
        screenshot_path="screenshots/confirmation.png",
        resume_path="attachments/resume.pdf"
    )

    if success:
        return jsonify({"status": "success", "message": message}), 200
    else:
        return jsonify({"status": "error", "message": message}), 500
    

@app.route('/')
def home():
    return """
    <h1>Assignment Submission Email Sender</h1>
    <p>Visit <a href="/send-email">/send-email</a> to send the submission email.</p>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)