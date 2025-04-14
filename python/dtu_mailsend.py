# Send email from Python

#--------------------------------------
# Code printed the 2006-09-22
# DTU s060803
# The original version was in Python 2
# Converted to Python 3 2025-04-14
# Need an application-specific password
# https://myaccount.google.com/apppasswords
#--------------------------------------

import smtplib, socket
from email.message import EmailMessage

your_account_address = ''
destination = ''
application_specific_password = '' # without spaces

config = 2

if config == 1:
    smtp_server = 'pop.dtu.dk'
    smtp_port = 25
    smtp_auth = False
    smtp_tls = False
    smtp_login = '' # no need
    smtp_pass = '' # no need
elif config == 2:
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587 # 465 for SMTP_SLL object (Doesn't work anymore)
    smtp_auth = True
    smtp_tls = True
    smtp_login = your_account_address
    smtp_pass = application_specific_password
else:
    raise Exception("No config selected. Choose between one or two.")

msg = EmailMessage()
msg.set_content("Body of the message")
subject = 'Hello'
msg['Subject'] = f'The subject is {subject}'
msg['From'] = your_account_address
msg['To'] = destination

try:
    if smtp_auth or smtp_tls:
        # process to send an email via en securized smtp server
        server = smtplib.SMTP(smtp_server, smtp_port)
        #server.set_debuglevel(1) #very useful to debug
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_login, smtp_pass)
        result = server.send_message(msg)
        server.rset()
        try:
            server.quit()
        except (socket.sslerror):
            # gmail is badly closing the tls connection
            # nothing to worry about...
            # 2025 : the exception is not thrown anymore
            print("Little exception")
            pass
    else:
        # procss to send an email via anonymous smtp server
        server = smtplib.SMTP(smtp_server,smtp_port) # use valid SMTP server here! pop.dtu.dk
        result = server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
    if result:
        for r in result.keys():
            print("Error sending to", r)
            rt = result[r]
            print("Code", rt[0], ":", rt[1])
    else:
        print("Sent to all recipients without errors")
except (smtplib.SMTPException, socket.error) as arg:
    print("SMTP Server could not send mail", arg)
