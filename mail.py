import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = "codecombatjuit@gmail.com"
PASSWORD = "clashofcoders"

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()

s.login(MY_ADDRESS, PASSWORD)

msg = MIMEMultipart()

message = '''message'''

msg['From']=MY_ADDRESS
msg['To']="geetansh2k1@gmail.com"
msg['Subject'] = "Coders Arena"

msg.attach(MIMEText(message, 'plain'))

s.send_message(msg)

del msg