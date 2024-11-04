from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
#Agregar a la clase EmployeeEvaluationApp
def generate_pdf(self, employee_name, autoeval, manager_eval):
    """Generar un PDF con los resultados de la evaluación."""
    pdf_filename = f"{employee_name}_evaluacion.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.drawString(100, 750, f"Evaluación de Desempeño de {employee_name}")
    c.drawString(100, 730, "Autoevaluación:")
    
    
    y_position = 710
    for i, score in enumerate(autoeval, 1):
        c.drawString(100, y_position, f"Pregunta {i}: {score}")
        y_position -= 20

    c.drawString(100, y_position, "Evaluación por Gerente:")
    y_position -= 20
    for i, score in enumerate(manager_eval, 1):
        c.drawString(100, y_position, f"Pregunta {i}: {score}")
        y_position -= 20

    # Guardar el PDF
    c.save()
    return pdf_filename

def send_email(self, to_email, pdf_filename):
    """Enviar el correo electrónico con el PDF adjunto."""
    from_email = "evluaciondesempenoesen@gmail.com"
    password = "yegz pbdh bkpt gpxl"  # Contraseña de aplicación del correo

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Evaluación de Desempeño Completa"
    body = "Por este medio, te adjunto el PDF con los resultados de tu evaluación de desempeño. Un saludo, el gerente"
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {pdf_filename}")
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        messagebox.showinfo("Correo Enviado", "El correo ha sido enviado exitosamente.")
    except Exception as e:
        messagebox.showerror("Error al Enviar Correo", f"No se pudo enviar el correo: {e}")
    finally:
        os.remove(pdf_filename)  

def prompt_send_email(self, employee_name, autoeval, manager_eval):
    """Generar PDF y preguntar por el correo del empleado para enviar la evaluación."""
    pdf_filename = self.generate_pdf(employee_name, autoeval, manager_eval)
    to_email = simpledialog.askstring("Enviar Correo", "Ingresa el correo electrónico del empleado:")
    if to_email:
        self.send_email(to_email, pdf_filename)
