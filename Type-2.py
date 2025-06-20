import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime as dt
import time
from concurrent.futures import ThreadPoolExecutor
import csv

data = [] 

#Your csv should contain senders id,receivers id,password(App Password )
#check for example csv in files
with open('filename.csv', mode ='r') as file:    
       csvFile = csv.DictReader(file)
       for lines in csvFile:
           data.append(lines)


# Your csv should contain the heading row (key) and correcsonding values
def generate_html_table(entry):
    # Filter out sensitive fields
    filtered_entry = {k: v for k, v in entry.items() if k not in ["receiverid", "Password"]}
    
    # Start table
    html = "<table border='1' style='border-collapse: collapse; width: 100%;'>"
    
    # First row - all keys
    html += "<tr>"
    for key in filtered_entry:
        html += f"<th style='padding: 8px; text-align: left;'>{key}</th>"
    html += "</tr>"
    
    # Second row - all values
    html += "<tr>"
    for value in filtered_entry.values():
        html += f"<td style='padding: 8px; text-align: left;'>{value}</td>"
    html += "</tr>"
    
    html += "</table>"
    return html


# Function to send an email
def send_email(entry):
    sender = entry["Email Id"]
    password = entry["Password"]
    receiver = entry["receiverid"]

    try:
        # Create email content with table
        message = MIMEMultipart("alternative")
        message["Subject"] = "***SUBJECT***"
        message["From"] = sender
        message["To"] = receiver

        html_content = f"""
        <html>
        <body>
            <p>****INTRODUCTION***</p>

            <p>***BODY***</p>

            {generate_html_table(entry)} 
           
            <p>CONCLUTION</p>
        </body>
        </html>
        """
        message.attach(MIMEText(html_content, "html"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as email:
            email.starttls()
            email.login(sender, password)
            email.sendmail(sender, receiver, message.as_string())
            print(f"Email sent to {receiver} from {sender}!")
    except Exception as e:
        print(f"Failed to send email to {receiver} from {sender}: {e}")

# Schedule emails
def schedule_emails():
    send_time = dt.datetime(2025, 6, 1, 10, 59, 57)  # YYYY,MM,DD,HR,MIN,SEC.  <-Format and no leading zeros
    time_to_wait = (send_time - dt.datetime.now()).total_seconds()
    print(f"Time to wait: {time_to_wait} seconds")

    if time_to_wait > 0:
        time.sleep(time_to_wait)

    # Use ThreadPoolExecutor to send emails concurrently
    with ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(send_email, data)

# Run the scheduling function
if __name__ == "__main__":
    schedule_emails()