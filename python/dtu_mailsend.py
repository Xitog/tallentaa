# Send email from Python

#--------------------------------------
# Code printed the 2006-09-22
# DTU s060803
# The original version was in Python 2
#--------------------------------------

#smtp_server = 'pop.dtu.dk'
#smtp_port = 25

config = 2

if config == 1:
    smtp_server = 'pop.dtu.dk'
    smtp_port = 25
    smtp_auth = False
    smtp_tls = False
    smtp_login = '' # no need
    smtp_pass = '' # no need
else:
    smtp_server = 'smpt.gmail.com'
    smtp_port = 587
    smtp_auth = True
    smtp_tls = True
    smtp_login = ''
    smtp_pass = ''

import smtplib, socket
fromaddr = "testdtu"
toaddrs = ["testdtu@gmail.com", "testdtu@gmail.com"]
msg = open("mailmsg.txt", "r").read()
try:
    if smtp_auth or smtp_tls:
        # process to send an email via en securized smtp server
        server = smtplib.SMTP(smtp_server, smtp_port)
        #server.set_debuglevel(1) #very useful to debug
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_login, smtp_pass)
        result = server.sendmail(fromaddr, toaddrs, msg)
        sever.rset()
        try:
            server.quit()
        except (socket.sslerror):
            # gmail is badly closing the tls connection
            # nothing to worry about...
            pass
    else:
        # procss to send an email via anonymous smtp server
        server = smtplib.SMTP(smtp_server,smtp_port) # use valid SMTP server here! pop.dtu.dk
        result = server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
    if result:
        for r in result.keys():
            print "Error sending to", r
            rt = result[r]
            print "Code", rt[0], ":", rt[1]
    else:
        print "Sent to all recipients without errors"
except (smptlib.SMTPException, socket.error), arg:
    print "SMTP Server could not send mail", arg
