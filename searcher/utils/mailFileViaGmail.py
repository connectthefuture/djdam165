#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os


def send_gmail(to, subject, text, attach):
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attach, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
    msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

################# RUN ##################
def main(toaddrs=None, msgsubj=None, bodyfile=None, attachfile=None, gmail_pwd=None):

    import re,os,sys

    gmail_user  =   'john.bragato@gmail.com'
    gmail_pwd   =   ''

    if not toaddrs:
        toaddrs =   'john.bragato@bluefly.com'

    if bodyfile:
        msgbody         =   open(bodyfile, 'rb').read()
        msgsubj = "File: {0} was attached ByPython".format(os.path.basename(bodyfile))
    else:
        msgbody = "File: was attached By Python"
        if not msgsubj:
            msgsubj =   msgbody[:15]


    if os.path.isfile(attachfile):
        send_gmail(toaddrs, msgsubj, msgbody, attachfile)

    elif os.path.isfile(bodyfile):
        send_gmail(toaddrs, msgsubj, msgbody, bodyfile)

    else:
        send_gmail(toaddrs, msgsubj, msgbody, "NotAfile")
    #for arg in sys.argv[1]:
    #    print arg
    #    toaddrs_list = []
    #    pattern_email = re.compile(r'.+[@].+[.].+')
    #    to_emailargs = re.findall(pattern_email, arg)
    #    if to_emailargs:
    #        for line in to_emailargs:
    #            toaddrs_list.append(line)
    #    else:
    #        print "Fail"
    #

if __name__ == "__main__":
    main()

