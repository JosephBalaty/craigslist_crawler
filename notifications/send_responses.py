import os
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib


def sendEmail(listings, query, receiver_email):

    email_sender = "test.cl.emails@gmail.com"
    email_password = "qbnekcyfzzmqplcq"
    email_receiver = receiver_email

    subject = f'Craigslit Notifications: {query}'

    em = MIMEMultipart("alternative")
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject



    text = """Here are the results:\n"""
    for idx in range(len(listings['Title'])):
        text += f""" 
         Listing {idx + 1}:
         
         Title: {listings["Title"][idx]} 
         
         
         
         Price: {listings["Price"][idx]} 
         Location: {listings["Location"][idx]} 
         Hyperlink: {listings["link"][idx]}\n
         """



    html = f"""
        <html>
          <body>
            <p>Here are the results:<br>
        """
    for idx in range(len(listings['Title'])):
        html += f""" 
         Listing {idx + 1}:<br>
         Title: {listings["Title"][idx]} <br>

        <img src="{listings["Image"][idx]}"> <br>

         Price: {listings["Price"][idx]} <br>
         Location: {listings["Location"][idx]} <br>
         Hyperlink: {listings["link"][idx]}<br><br>
         """
    html += f"""
            </p>
          </body>
        </html>
     """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    em.attach(part1)
    em.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        try:
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        except:
            print("Error delivering mail to the recipient!")