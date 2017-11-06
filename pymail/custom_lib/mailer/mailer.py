import smtplib
import time 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import custom_lib.log as l

def sendEmail(data, account, queque):
    
    fromAddr = "\"%s\" <%s>" % (account.get('name'), account.get('email'))
    toAddr = []
    
    for i in data['recieve']['to']:
        if i['name'] is not None:
            #toAddr = "%s, \"%s\" <%s>" % (toAddr, i['name'], i['email'])
            toAddr.append("%s <%s>" % (i['name'], i['email']))
        else:
            #toAddr = "%s, %s" % (toAddr, i['email'])
            toAddr.append("%s" % i['email'])
        
    ccAddr = ""
    if 'cc' in data['recieve']:
        for i in data['recieve']['cc']:
            ccAddr = "%s, \"%s\" <%s>" % (ccAddr, i['name'], i['email'])
            
        ccAddr = ccAddr[2:].strip()
        
    bccAddr = ""
    if 'bcc' in data['recieve']:
        for i in data['recieve']['bcc']:
            bccAddr = "%s, \"%s\" <%s>" % (bccAddr, i['name'], i['email'])
            
        bccAddr = bccAddr[2:].strip()
        
    subject = data['subject']
    body = data['body']
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject 
    msg['From'] = fromAddr 
    msg['To'] = ", ".join(toAddr)
    if ccAddr != '':
        msg['CC'] = ccAddr 
    
    if bccAddr != '':
        msg['BCC'] = bccAddr
        
    body = body.replace('\n', '<br/>')
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    if 'attach' in data:
        import base64
        for att in data['attach']:
            try :
                aname = att['name']
                acontent = base64.b64decode(att['content'])
                part = MIMEApplication(acontent, Name=aname)
                part['Content-Disposition'] = 'attachment; filename="%s"' % aname
                msg.attach(part)
            except Exception, e :
                l.error("Unable to add attachement")
                l.error(str(e))
                    
    try :
        l.info("Send email")
        l.info(str({
            "Subject": subject, 
            "From": fromAddr, 
            "To": toAddr, 
            "CC": ccAddr, 
            "BCC": bccAddr
        }))
        s = smtplib.SMTP(account.get('host'), int(account.get('port')))
        s.ehlo()
        if account.get('tls') == 1:
            s.starttls()
        s.login(account.get('username'), account.get('password'))
        s.sendmail(account.get('email'), toAddr, msg.as_string().encode('ascii'))
        s.quit()
        
        queque.set('done', time.strftime('%Y-%m-%d %H:%M:%S'))
        
        queque.update();
        
    except Exception, e:
        queque.set('error', str(e))
        queque.update()
        l.error(e)

        
