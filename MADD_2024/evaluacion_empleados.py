import tkinter as tk
from tkinter import messagebox
import mariadb
import sys
from tkinter import simpledialog, scrolledtext

class EmployeeEvaluationApp:
    def __init__(self, master):
        self.master = master
        master.title("Evaluación del Desempeño de Empleados")
        master.geometry("800x600")  # Ajustar el tamaño de la ventana para mostrar el diseño completo
        master.configure(bg="#f0f4f7")

        # Conexión a la base de datos
        self.connect_db()

        # Pantalla de inicio de sesión
        self.login_screen()

    def connect_db(self):
        """Conectar a la base de datos MariaDB."""
        try:
            self.conn = mariadb.connect(
                user="root",
                password="suser",
                host="127.0.0.1",
                port=3306,
                database="evaluaciones"
            )
            self.cursor = self.conn.cursor()
            print("Conexión exitosa a la base de datos.")
        except mariadb.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            sys.exit(1)

    def clear_window(self):
        """Limpiar la ventana actual."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def login_screen(self):
        """Crear la pantalla de inicio de sesión."""
        self.clear_window()
        
        # Establecer un fondo claro para toda la ventana
        self.master.configure(bg="#FFFFFF")

        # Frame principal para centrar todo el contenido
        main_frame = tk.Frame(self.master, bg="#FFFFFF")
        main_frame.pack(expand=True, pady=(20, 80))

        # Título
        title_label = tk.Label(main_frame, text="¡Bienvenido!", font=("Arial", 28, "bold"), bg="#FFFFFF", fg="#1c0d02")
        title_label.pack(pady=(20, 15))

        # Frame para los campos de entrada
        frame = tk.Frame(main_frame, bg="#ffffdf", bd=5, relief=tk.RAISED)
        frame.pack(pady=10, padx=20)

        # Etiqueta y entrada para el usuario
        tk.Label(frame, text="Usuario:", font=("Arial", 14), bg="#ffffdf", fg="#1c0d02").grid(row=0, column=0, sticky='w', padx=(0, 10))
        self.username_entry = tk.Entry(frame, font=("Arial", 12), bg="#ffffff", fg="#000000", width=20, bd=2, relief=tk.FLAT)
        self.username_entry.grid(row=0, column=1)
        self.username_entry.bind("<FocusIn>", lambda e: self.username_entry.configure(bg="#e0f7fa"))
        self.username_entry.bind("<FocusOut>", lambda e: self.username_entry.configure(bg="#ffffff"))

        # Etiqueta y entrada para la contraseña
        tk.Label(frame, text="Contraseña:", font=("Arial", 14), bg="#ffffdf", fg="#1c0d02").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(10, 0))
        self.password_entry = tk.Entry(frame, show='*', font=("Arial", 12), bg="#ffffff", fg="#000000", width=20, bd=2, relief=tk.FLAT)
        self.password_entry.grid(row=1, column=1, pady=(10, 0))
        self.password_entry.bind("<FocusIn>", lambda e: self.password_entry.configure(bg="#e0f7fa"))
        self.password_entry.bind("<FocusOut>", lambda e: self.password_entry.configure(bg="#ffffff"))

        # Botón de inicio de sesión con efecto hover
        login_button = tk.Button(main_frame, text="Iniciar Sesión", command=self.login,
                                bg="#47176b", fg="white", font=("Arial", 14, "bold"), 
                                bd=0, activebackground="#9c27b0", activeforeground="white")
        login_button.pack(pady=(15, 0)) 

        # Efecto hover para el botón
        login_button.bind("<Enter>", lambda e: login_button.configure(bg="#9c27b0"))  
        login_button.bind("<Leave>", lambda e: login_button.configure(bg="#8e24aa"))

        # Botón para crear cuenta
        create_account_button = tk.Button(main_frame, text="Crear Cuenta", command=self.create_account,
                            bg="#47176b", fg="white", font=("Arial", 14, "bold"), 
                            bd=0, activebackground="#9c27b0", activeforeground="white")
        create_account_button.pack(pady=(15, 0))

        create_account_button.bind("<Enter>", lambda e: create_account_button.configure(bg="#9c27b0"))  
        create_account_button.bind("<Leave>", lambda e: create_account_button.configure(bg="#8e24aa"))

    def login(self):
        """Verificar credenciales y mostrar la interfaz correspondiente."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.cursor.execute("SELECT rol FROM usuarios WHERE nombre_usuario=? AND contrasena=?", (username, password))
            result = self.cursor.fetchone()
            if result:
                role = result[0]
                if role == "gerente":
                    self.show_manager_interface()
                else:
                    self.show_employee_interface()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas. Intenta nuevamente.")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo verificar las credenciales: {e}")

    def create_account(self):
        """Crear una nueva cuenta de usuario."""
        username = simpledialog.askstring("Crear Cuenta", "Ingresa un nombre de usuario:")
        password = simpledialog.askstring("Crear Cuenta", "Ingresa una contraseña:", show='*')
        # Preguntar por el rol del usuario
        role = simpledialog.askstring("Seleccionar Rol", "Ingresa el rol (empleado/gerente):").lower()
        
        if username and password and role in ['empleado', 'gerente']:
            try:
                self.cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (?, ?, ?)", (username, password, role))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Cuenta creada exitosamente.")
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo crear la cuenta: {e}")
        else:
            messagebox.showwarning("Advertencia", "Nombre de usuario, contraseña y rol son requeridos. El rol debe ser 'empleado' o 'gerente'.")

    def show_manager_interface(self):
        """Mostrar la interfaz del gerente."""
        self.clear_window()
        
        tk.Label(self.master, text="Bienvenido Gerente", font=("Arial", 18), bg="#f0f4f7").pack(pady=20)
        
        tk.Button(self.master, text="Evaluar Empleado", command=self.manager_evaluation, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Ver Evaluaciones Anteriores", command=self.view_previous_evaluations, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Comparar Desempeño de Empleados", command=self.compare_performance, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Generar Reporte de Desempeño", command=self.generate_report, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Añadir Feedback", command=self.add_feedback, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)

        
        tk.Button(self.master, text="Regresar a Iniciar Sesión", command=self.login_screen, bg="#f0ad4e", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Cerrar Aplicación", command=sys.exit, bg="#d9534f", fg="white", font=("Arial", 12)).pack(pady=10)

    def show_employee_interface(self):
        """Mostrar la interfaz del empleado con barra lateral y tarjetas."""
        self.clear_window()
        
        tk.Label(self.master, text="Bienvenido Empleado", font=("Arial", 18), bg="#f0f4f7").pack(pady=20)
        
        tk.Button(self.master, text="Realizar Autoevaluación", command=self.self_evaluation, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Ver Evaluaciones Anteriores", command=self.view_previous_evaluations, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Ver Feedback", command=self.view_feedback, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)

        
        tk.Button(self.master, text="Regresar a Iniciar Sesión", command=self.login_screen, bg="#f0ad4e", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Cerrar Aplicación", command=sys.exit, bg="#d9534f", fg="white", font=("Arial", 12)).pack(pady=10)

        # Barra lateral
        sidebar = tk.Frame(self.master, bg="#4A148C", width=200)
        sidebar.pack(side="left", fill="y")

        # Título del sistema
        tk.Label(sidebar, text="See", font=("Arial", 24, "bold"), bg="#4A148C", fg="white").pack(pady=(50, 5))  # Aumenté el padding superior a 30
        tk.Label(sidebar, text="Sistema de Evaluación de Desempeño", font=("Arial", 10), bg="#4A148C", fg="white").pack(pady=(0, 100))  # Agregué un padding inferior de 15

        # Botones de la barra lateral
        buttons = [("Home", "🏠"), ("Mis resultados", "📊"), ("Mi historial", "📁")]
        for text, icon in buttons:
            button = tk.Button(sidebar, text=f"{icon}  {text}", font=("Arial", 12), bg="#4A148C", fg="white", borderwidth=0)
            button.pack(fill="x", pady=20, padx=20)  # Aumenté pady a 10 para más separació

        # Botón de cerrar sesión
        tk.Button(sidebar, text="Log out", font=("Arial", 12, "bold"), bg="#A4A4A4", fg="white", borderwidth=0,
                  command=self.login_screen).pack(side="bottom", pady=20, padx=10)  # Se añadió el comando para cerrar sesión

        # Frame principal de la interfaz
        main_frame = tk.Frame(self.master, bg="#f0f4f7")
        main_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        # Saludo al usuario con emoji de bienvenida
        tk.Label(main_frame, text="Bienvenido, empleado 👋 ", font=("Arial", 14), bg="#f0f4f7", fg="#4A148C").pack(anchor="ne")

        # Tarjetas de evaluación
        card_data = [
            ("Realizar autoevaluación", "Autoevaluación de Desempeño", "Evalúa tu desempeño en tres áreas clave: habilidades, productividad y colaboración.", self.self_evaluation),
            ("Evaluar pares", "Evaluación de Desempeño de Pares", "Evalúa el desempeño de tus compañeros en tres áreas clave.", self.view_previous_evaluations),
            ("Ver evaluaciones anteriores", "Historial de Evaluaciones", "Revisa el historial de tus evaluaciones anteriores en esta sección.", self.view_previous_evaluations)
        ]

        for title, subtitle, description, command in card_data:
            card = tk.Frame(main_frame, bg="white", bd=1, relief="solid")
            card.pack(pady=10, fill="x", padx=10, ipadx=10, ipady=10)
            tk.Label(card, text="📝", font=("Arial", 18, "bold"), bg="white", fg="#4A148C").grid(row=0, column=0, padx=10, pady=5)
            tk.Label(card, text=title, font=("Arial", 16, "bold"), bg="white", fg="#4A148C").grid(row=0, column=1, sticky="w", pady=5)
            tk.Label(card, text=subtitle, font=("Arial", 12), bg="white", fg="#757575").grid(row=1, column=1, sticky="w")
            tk.Label(card, text=description, font=("Arial", 10), bg="white", fg="#757575").grid(row=2, column=1, sticky="w", padx=10, pady=(5, 10))
            tk.Button(card, text="Comenzar", command=command, bg="#4A148C", fg="white", font=("Arial", 12, "bold"), relief="flat").grid(row=3, column=1, pady=(10, 5), sticky="e")

    def self_evaluation(self):
        questions = {
            "Puntualidad": [
                "1. ¿Con qué frecuencia llegas a tiempo a tu lugar de trabajo?",
                "2. ¿Cumples con los plazos establecidos para la entrega de tareas?",
                "3. ¿Cómo calificas tu capacidad para asistir a reuniones programadas puntualmente?",
                "4. ¿Te consideras una persona que respeta el horario laboral establecido?",
                "5. ¿Cómo evalúas tu compromiso con la puntualidad en el trabajo?"
            ],
            "Desempeño": [
                "1. ¿Cómo calificarías la calidad de tu trabajo en general?",
                "2. ¿Con qué frecuencia superas las expectativas en tus tareas asignadas?",
                "3. ¿Cómo evalúas tu capacidad para resolver problemas de manera efectiva?",
                "4. ¿Qué tan bien manejas las tareas bajo presión o en situaciones de estrés?",
                "5. ¿Cómo calificas tu habilidad para aprender y aplicar nuevos conocimientos o habilidades en tu trabajo?"
            ],
            "Trabajo en Equipo": [
                "1. ¿Cómo calificarías tu habilidad para colaborar con otros miembros del equipo?",
                "2. ¿Con qué frecuencia ofreces ayuda a tus compañeros cuando lo necesitan?",
                "3. ¿Cómo evalúas tu capacidad para comunicarte efectivamente con el equipo?",
                "4. ¿Qué tan bien manejas los conflictos dentro del equipo?",
                "5. ¿Cómo calificas tu disposición para aceptar críticas constructivas de tus compañeros?"
            ]
        }

        responses = []

        for category, qs in questions.items():
            messagebox.showinfo("Autoevaluación", f"Categoría: {category}")
            for question in qs:
                response = simpledialog.askinteger("Autoevaluación",
                                                    f"{question}\n(1: Malo, 5: Excelente)",
                                                    minvalue=1,
                                                    maxvalue=5)
                if response is not None:
                    responses.append(response)

        if not responses:
            messagebox.showwarning("Advertencia",
                                    "No se realizaron respuestas a la autoevaluación.")
            return

        average_score = sum(responses) / len(responses)
        
        employee_name = simpledialog.askstring("Nombre del Empleado",
                                                "Ingresa tu nombre:")
        
        if employee_name:
            try:
                autoeval_json = str(responses)
                
                self.cursor.execute(
                    "INSERT INTO evaluaciones (nombre_empleado, rol, autoevaluacion) VALUES (?, ?, ?)",
                    (employee_name, 'Empleado', autoeval_json))
                
                self.conn.commit()
                
                messagebox.showinfo("Resultados de Autoevaluación",
                                    f"Tu puntuación promedio es: {average_score:.2f}")
                
            except mariadb.Error as e:
                messagebox.showerror("Error",
                                     f"No se pudo guardar la autoevaluación: {e}")
                
        else:
            messagebox.showwarning("Advertencia",
                                   "Nombre de empleado no ingresado.")

    def manager_evaluation(self):
        employee_name = simpledialog.askstring("Nombre del Empleado",
                                                "Ingresa el nombre del empleado a evaluar:")
        
        if employee_name:
            responses = []
            
            questions = [
                "1. ¿Cómo calificarías la calidad del trabajo del empleado?",
                "2. ¿Con qué frecuencia supera las expectativas en sus tareas asignadas?",
                "3. ¿Cómo evalúas su capacidad para resolver problemas?",
                "4. ¿Qué tan bien maneja las tareas bajo presión?",
                "5. ¿Cómo calificas su habilidad para trabajar en equipo?"
            ]

            for question in questions:
                response = simpledialog.askinteger("Evaluación del Empleado",
                                                    f"{question}\n(1: Malo, 5: Excelente)",
                                                    minvalue=1,
                                                    maxvalue=5)
                
                if response is not None:
                    responses.append(response)

            if not responses:
                messagebox.showwarning("Advertencia",
                                        "No se realizaron respuestas a la evaluación del empleado.")
                return

            average_score = sum(responses) / len(responses)

            try:
                manager_eval_json = str(responses)

                self.cursor.execute(
                    "UPDATE evaluaciones SET evaluacion_gerente=? WHERE nombre_empleado=?",
                    (manager_eval_json, employee_name))
                
                self.conn.commit()

                messagebox.showinfo("Resultados de Evaluación",
                                    f"La puntuación promedio del empleado {employee_name} es: {average_score:.2f}")

            except mariadb.Error as e:
                messagebox.showerror("Error",
                                     f"No se pudo guardar la evaluación del gerente: {e}")
                
        else:
            messagebox.showwarning("Advertencia",
                                   "Nombre de empleado no ingresado.")

    def view_previous_evaluations(self):
        employee_name = simpledialog.askstring("Nombre del Empleado",
                                                "Ingresa tu nombre:")
        
        if employee_name:
            try:
                self.cursor.execute(
                    "SELECT autoevaluacion, evaluacion_gerente FROM evaluaciones WHERE nombre_empleado=?",
                    (employee_name,))
                
                result = self.cursor.fetchone()

                if result:
                    autoeval = eval(result[0])
                    manager_eval = eval(result[1]) if result[1] else []

                    evaluations_text = f"Evaluaciones anteriores para {employee_name}:\n\n"
                    
                    evaluations_text += "Autoevaluación:\n"
                    for i, score in enumerate(autoeval, 1):
                        evaluations_text += f"{i}. Pregunta {i}: {score}\n"

                    evaluations_text += "\nEvaluación por Gerente:\n"
                    for i, score in enumerate(manager_eval, 1):
                        evaluations_text += f"{i}. Pregunta {i}: {score}\n"

                    messagebox.showinfo("Evaluaciones Anteriores",
                                        evaluations_text.strip())
                    
                else:
                    messagebox.showinfo("Evaluaciones Anteriores",
                                        f"No se encontraron evaluaciones para {employee_name}.")

            except mariadb.Error as e:
                messagebox.showerror("Error",
                                     f"No se pudieron recuperar las evaluaciones: {e}")

    def compare_performance(self):
        employees_to_compare = simpledialog.askstring(
            "Comparar Desempeño",
            "Ingresa los nombres de los empleados separados por comas:")
        
        if employees_to_compare:
            employee_list = [name.strip() for name in employees_to_compare.split(',')]
            
            report_text = "Comparativa de Desempeño:\n\n"
            
            overall_scores = {}

            for employee in employee_list:
                
                try:
                    self.cursor.execute(
                        "SELECT autoevaluacion FROM evaluaciones WHERE nombre_empleado=?",
                        (employee,))
                    
                    result = self.cursor.fetchone()

                    if result:
                        autoeval = eval(result[0]) # Convertir JSON a lista
                        report_text += f"Empleado: {employee}\n"
                        report_text += "Autoevaluación:\n"
                        
                        for i, score in enumerate(autoeval, 1):
                            report_text += f" Pregunta {i}: {score}\n"

                        # Calcular y almacenar el promedio
                        average_score = sum(autoeval) / len(autoeval)
                        report_text += f" Promedio Autoevaluación: {average_score:.2f}\n"
                        
                        overall_scores[employee] = average_score
                    else:
                        report_text += f"Empleado: {employee} no encontrado.\n\n"

                except mariadb.Error as e:
                    messagebox.showerror("Error",
                                         f"No se pudo recuperar las evaluaciones para {employee}: {e}")

            compare_window = tk.Toplevel(self.master)
            
            compare_window.title("Comparativa de Desempeño")
            
            compare_window.focus_force()
            
            compare_text_area = scrolledtext.ScrolledText(compare_window,
                                                           width=70,
                                                           height=20)
            
            compare_text_area.insert(tk.END,
                                     report_text.strip())
            
            compare_text_area.pack(padx=10,
                                   pady=10)

            if overall_scores:
                
                sorted_scores = sorted(overall_scores.items(),
                                       key=lambda x: x[1],
                                       reverse=True)

                compare_text_area.insert(tk.END,
                                         "\nRanking de Empleados:\n")

                for rank, (emp, score) in enumerate(sorted_scores,
                                         start=1):
                    
                    compare_text_area.insert(tk.END,
                                             f"{rank}. {emp}: {score:.2f}\n")

            tk.Button(compare_window,
                       text="Cerrar",
                       command=compare_window.destroy).pack(pady=5)

    def generate_report(self):
         report_text = "Reporte de Desempeño General:\n\n"
         
         try:
             self.cursor.execute(
                "SELECT nombre_empleado, autoevaluacion, evaluacion_gerente FROM evaluaciones")
             
             for row in self.cursor.fetchall():
                 report_text += f"Empleado: {row[0]}\n"
                 # Procesar autoevaluación
                 autoeval = eval(row[1]) # Convertir JSON a lista
                 report_text += "Autoevaluación:\n"
                 
                 for i, score in enumerate(autoeval,1):
                    report_text += f" Pregunta {i}: {score}\n"

                 # Procesar evaluación por gerente
                 if row[2]:
                     manager_eval = eval(row[2])
                     report_text += "Evaluación por Gerente:\n"
                     
                     for i, score in enumerate(manager_eval, 1):
                         report_text += f" Pregunta {i}: {score}\n"
                 else:
                     report_text += \
                         "Evaluación por Gerente: No disponible\n"

                 # Calcular y agregar puntajes promedio
                 average_auto = sum(autoeval) / len(autoeval) if autoeval else 0
                 average_manager = sum(manager_eval) / len(manager_eval) if manager_eval else 0

                 report_text += \
                     f" Promedio Autoevaluación: {average_auto:.2f}\n"
                 report_text += \
                     f" Promedio Evaluación Gerente: {average_manager:.2f}\n"

                 report_text += "-" * 50 + "\n" # Separator for better readability

             # Mostrar reporte en una ventana nueva
             report_window = tk.Toplevel(self.master)

             report_window.title("Reporte de Desempeño")

             #Color de la ventana
             report_window.configure(bg="#432c81")
             
             report_window.focus_force()

             report_text_area = scrolledtext.ScrolledText(report_window,
                                            width=70,
                                            height=20)

             report_text_area.insert(tk.END,
                                     report_text.strip())
             
             report_text_area.pack(padx=10,
                                   pady=10)

             # Add a button to close the report window
             tk.Button(report_window,
                       text="Cerrar",
                       command=report_window.destroy,
                       bg="#625b71",  # Color de fondo del botón
                       fg="#ffffff"
                       ).pack(pady=5)

         except mariadb.Error as e:
             messagebox.showerror("Error",
                                  f"No se pudo generar el reporte: {e}")

    def add_feedback(self):
        """Función para añadir comentarios de feedback para un empleado."""
        employee_name = simpledialog.askstring("Feedback", "Ingresa el nombre del empleado para darle feedback:")
        if employee_name:
            feedback = simpledialog.askstring("Feedback", "Escribe tus comentarios:")
            if feedback:
                try:
                    # Verificar si el empleado existe en la tabla evaluaciones
                    self.cursor.execute("SELECT id FROM evaluaciones WHERE nombre_empleado=?", (employee_name,))
                    result = self.cursor.fetchone()
                    
                    if result:
                        employee_id = result[0]
                        # Insertar o actualizar feedback en la base de datos
                        self.cursor.execute("UPDATE evaluaciones SET feedback=? WHERE id=?", (feedback, employee_id))
                        self.conn.commit()
                        messagebox.showinfo("Feedback", f"Feedback agregado para {employee_name}.")
                    else:
                        messagebox.showwarning("Advertencia", f"No se encontró un empleado con el nombre: {employee_name}.")
                    
                except mariadb.Error as e:
                    messagebox.showerror("Error", f"No se pudo añadir el feedback: {e}")
            else:
                messagebox.showwarning("Advertencia", "El campo de feedback está vacío.")
        else:
            messagebox.showwarning("Advertencia", "No se ingresó el nombre del empleado.")

    def view_feedback(self):
        """Función para que los empleados vean su feedback."""
        employee_name = simpledialog.askstring("Ver Feedback", "Ingresa tu nombre:")
        
        if employee_name:
            try:
                # Buscar el feedback del empleado en la base de datos
                self.cursor.execute("SELECT feedback FROM evaluaciones WHERE nombre_empleado=?", (employee_name,))
                result = self.cursor.fetchone()
                
                if result and result[0]:
                    feedback = result[0]
                    messagebox.showinfo("Feedback", f"Feedback para {employee_name}:\n\n{feedback}")
                else:
                    messagebox.showinfo("Feedback", f"No se encontró feedback para el empleado: {employee_name}.")
                    
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo recuperar el feedback: {e}")
        else:
            messagebox.showwarning("Advertencia", "No se ingresó el nombre del empleado.")
    

if __name__ == "__main__":
    root = tk.Tk()

    app = EmployeeEvaluationApp(root)

    root.mainloop()