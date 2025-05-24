
from flask import Flask, render_template, request
import smtplib
import google.generativeai as genai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Replace with your actual API key and email credentials
genai.configure(api_key="AIzaSyDV4PCJjnogJu2T96FSGx8JpfuyTzRzJk4")
EMAIL_ADDRESS = "arun120904@gmail.com"
EMAIL_PASSWORD = "oyeh jdvl waqm fuvl"  # Use an App Password for Gmail

# Generate email content
def generate_email(prompt, tone):
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    full_prompt = f"Write a {tone} email for the following: {prompt}"
    response = model.generate_content(full_prompt)
    return response.text

# Send the email
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    email_content = None
    if request.method == "POST":
        recipient = request.form["recipient"]
        subject = request.form["subject"]
        prompt = request.form["prompt"]
        tone = request.form["tone"]

        email_content = generate_email(prompt, tone)
        send_email(recipient, subject, email_content)

    return render_template("index.html", email_content=email_content)

if __name__ == "__main__":
    app.run(debug=True)

