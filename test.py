from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib

attachment = 'Anna Kupfer average per week.png'

msg = MIMEMultipart()
msg["To"] = ''
msg["From"] = 'me'
msg["Subject"] = 'ProjektManagement Testing'

body = 'Hello, Anna Kupfer!'

#msgText = MIMEText('<b>%s</b><br><img src="cid:%s"><br>' % (body, attachment), 'html')
#msg.attach(msgText)   # Added, and edited the previous line

html = """\
<html>
<head>
</head>
<body>

<div>
    <div style="padding: 10px; border: 1px solid black">
        <b> Konstantin Hopf</b>
        <div> Customer Id: 1077</div>
    </div>
    <div>
         <img src="cid:regnitzLogo.png">
    </div>
</div>

</body>
</html>
"""

fp = open(attachment, 'rb')
img = MIMEImage(fp.read())
fp.close()

img.add_header('Content-ID', '<regnitzLogo>')
msg.attach(img)
# img.add_header('Content-ID', '<{}>'.format(attachment))
# msg.attach(img)

#part1 = MIMEText(body, 'plain')
part2 = MIMEText(html, 'html')

#msg.attach(part1)
msg.attach(part2)

server = smtplib.SMTP('smtp.gmail.com:587')
#server = smtplib.SMTP('127.0.0.1')
#server.ehlo()
server.starttls()
server.login("d@gmail.com","zzzz")
server.sendmail(msg["From"], [msg["To"]], msg.as_string())
server.quit()