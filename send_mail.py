import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromaddr = "dest@visian.com"
toaddr = ["dest@dest.fr", "dest@visian.fr", "dest@visian.fr", "dest@visian.fr"]

subject = sys.argv[1]
subject += " "
subject += sys.argv[2]

corp = "DATE : "
corp += sys.argv[3]
corp += " \n"
corp += "HEURE : "
corp += sys.argv[4]
corp += " \n \n"
corp += "Operateur : "
corp += sys.argv[5]
corp += " \n"
corp += "Eolienne : "
corp += sys.argv[6]
corp += " \n"
corp += "Intervention : "
corp += sys.argv[7]
corp += "\n \n \n"
corp += "Le Token "
corp += sys.argv[2]
if (int(sys.argv[8]) == 1):
    corp += " vient d etre utilise pendant sa periode de validite."
    corp += "\n \n"
    corp += "L acces a l eolienne est confirme"
else :
    corp += "utilise n est pas valide."
    corp += "\n \n"
    corp += "L acces a l eolienne est refuse"

msg = MIMEMultipart()

msg['From'] = "Team Visian"
#msg['To'] = toaddr
msg['To'] = ", ".join(toaddr)
msg['Subject'] = subject

body = corp

msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "Password")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
