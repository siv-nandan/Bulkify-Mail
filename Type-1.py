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


# Function to send an email
def send_email(entry):
    sender = entry["Email Id"]
    password = entry["Password"]
    receiver = entry["receiverid"]

    try:
        # Create email content
        message = MIMEMultipart("alternative")
        message["Subject"] = "***SUBJECT FOR E-MAIL***"
        message["From"] = sender
        message["To"] = receiver
        #Type your Email content
        html_content = f"""
        <html>
        <body>
            <p>***INTRODUCTION***</p> 
            <p>***BODY***</p>
            <p>***CONCLUTION***</p>
        </body>
        </html>
        """
        message.attach(MIMEText(html_content, "html"))

        
        with smtplib.SMTP("smtp.gmail.com", 587) as email:
            email.starttls()
            email.login(sender, password)
            email.sendmail(sender, receiver, message.as_string())
            print(f"Email sent to {receiver} from {sender}!")
    except Exception as e:
        print(f"Failed to send email to {receiver} from {sender}: {e}")


def schedule_emails():
    send_time = dt.datetime(2025, 6, 1, 10, 59, 57)  # YYYY,MM,DD,HR,MIN,SEC.  <-Format and no leading zeros
    time_to_wait = (send_time - dt.datetime.now()).total_seconds()
    print(f"Time to wait: {time_to_wait} seconds")

    if time_to_wait > 0:
        time.sleep(time_to_wait)

    
    with ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(send_email, data)


if __name__ == "__main__":
    schedule_emails()