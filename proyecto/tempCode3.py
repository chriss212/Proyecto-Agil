def prompt_send_email(self, employee_name, autoeval, to_email):
    """Generar PDF y enviar la evaluación al correo del empleado."""
    
    pdf_filename = self.generate_pdf(employee_name, autoeval)
    
    if to_email:
        self.send_email(to_email, pdf_filename)
    else:
        messagebox.showwarning("Advertencia", "Por favor ingresa un correo electrónico.")

def generate_pdf(self, employee_name, autoeval):
    """Generar un PDF con los resultados de la evaluación."""
    
    pdf_filename = f"{employee_name}_evaluacion.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    
    c.drawString(100, 750, f"Evaluación de Desempeño de {employee_name}")
    c.drawString(100, 730, "Autoevaluación y Evaluación por Gerente:")

    # Lista de preguntas
    questions = [
        "1. ¿Cómo calificarías la calidad del trabajo del empleado?",
        "2. ¿Con qué frecuencia supera las expectativas en sus tareas asignadas?",
        "3. ¿Cómo evalúas su capacidad para resolver problemas?",
        "4. ¿Qué tan bien maneja las tareas bajo presión?",
        "5. ¿Cómo calificas su habilidad para trabajar en equipo?"
    ]
    
    y_position = 710
    
    for i, (question, score) in enumerate(zip(questions, autoeval), start=1):
        c.drawString(100, y_position, f"{question} Respuesta: {score}")
        y_position -= 20

    c.save()
    return pdf_filename

def send_email(self, to_email, pdf_filename):
    """Enviar el correo electrónico con el PDF adjunto usando SMTP_SSL y reintento en caso de error."""
    
    from_email = "evaluaciondesempenoesen@gmail.com"
    password = "yegz pbdh bkpt gpxl"  # Contraseña de aplicación del correo

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Evaluación de Desempeño Completa"
    
    body = "Por este medio te adjunto el PDF con los resultados de tu evaluación de desempeño. Un saludo."
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={pdf_filename}")
        msg.attach(part)

    # Intentar enviar el correo hasta 3 veces en caso de error
    for attempt in range(3):
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(from_email, password)
                server.send_message(msg)
            
            messagebox.showinfo("Correo Enviado", "El correo ha sido enviado exitosamente.")
            break
        except Exception as e:
            if attempt == 2:  # Después de 3 intentos, mostrar el error
                messagebox.showerror("Error al Enviar Correo", f"No se pudo enviar el correo: {e}")
    
    finally:
        os.remove(pdf_filename)  # Eliminar el archivo PDF después de enviarlo
