from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from datetime import datetime
from email.utils import formatdate
import smtplib

class Correo:

    current_date = datetime.today().strftime('%Y-%m-%d')

    def send_mail(self,ruta, destinatarios, title):
        print("Ingresa a Enviar Correo!!!!!")

        server = smtplib.SMTP(host='correo.mct.com.co',port=25)
        msg = MIMEMultipart()
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(ruta, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="Informe_Tiempos_Polar.xlsx"')
        msg.attach(part)

        password = "temporal_2015"
        msg['From'] = "notificaciones@mct.com.co"
        msg['To'] = ",".join(destinatarios)
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = title


        mail_body = self.set_mail_body(title)
        server.starttls()
        server.login(msg['From'], password)
        msg.attach(mail_body)
        server.sendmail(msg['From'], destinatarios, msg.as_string())
        server.quit()

        print("Correo enviado con exito %s:" % (msg['To']))

    def set_mail_body(sef, title):
        body_html = f"""\
                <html>
                  <head></head>
                  <body>
                    <p>Buen día,
                    <br>
                    <br>
                    A continuacion, se relaciona {title} de la fecha {sef.current_date}
                    <br>
                    <br>
                    Cordialmente,
                    <br>
                    sistemas@mct.com.co
                    </p>
                  </body>
                </html>
                """
        part = MIMEText(body_html, 'html')
        return part
