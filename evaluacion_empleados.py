import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import mariadb
import sys
from tkinter import ttk

class EmployeeEvaluationApp:
    def __init__(self, master):
        self.master = master
        master.title("Evaluación del Desempeño de Empleados")
        master.geometry("800x600")
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
                password="28marzo2005",
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
        self.master.configure(bg="#FFFFFF")

        main_frame = tk.Frame(self.master, bg="#FFFFFF")
        main_frame.pack(expand=True, pady=(20, 80))

        title_label = tk.Label(main_frame, text="¡Bienvenido!", font=("Arial", 28, "bold"), bg="#FFFFFF", fg="#1c0d02")
        title_label.pack(pady=(20, 15))

        frame = tk.Frame(main_frame, bg="#ffffdf", bd=5, relief=tk.RAISED)
        frame.pack(pady=10, padx=20)

        tk.Label(frame, text="Usuario:", font=("Arial", 14), bg="#ffffdf", fg="#1c0d02").grid(row=0, column=0,
                                                                                              sticky='w', padx=(0, 10))
        self.username_entry = tk.Entry(frame, font=("Arial", 12), bg="#ffffff", fg="#000000", width=20, bd=2,
                                       relief=tk.FLAT)
        self.username_entry.grid(row=0, column=1)

        tk.Label(frame, text="Contraseña:", font=("Arial", 14), bg="#ffffdf", fg="#1c0d02").grid(row=1, column=0,
                                                                                                 sticky='w',
                                                                                                 padx=(0, 10),
                                                                                                 pady=(10, 0))
        self.password_entry = tk.Entry(frame, show='*', font=("Arial", 12), bg="#ffffff", fg="#000000", width=20, bd=2,
                                       relief=tk.FLAT)
        self.password_entry.grid(row=1, column=1, pady=(10, 0))

        login_button = tk.Button(main_frame, text="Iniciar Sesión", command=self.login,
                                 bg="#47176b", fg="white", font=("Arial", 14, "bold"),
                                 bd=0, activebackground="#9c27b0", activeforeground="white")
        login_button.pack(pady=(15, 0))

        create_account_button = tk.Button(main_frame, text="Crear Cuenta", command=self.create_account,
                                          bg="#47176b", fg="white", font=("Arial", 14, "bold"),
                                          bd=0, activebackground="#9c27b0", activeforeground="white")
        create_account_button.pack(pady=(15, 0))

    def login(self):
        """Verificar credenciales y mostrar la interfaz correspondiente."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Usuario ingresado: {username}, Contraseña ingresada: {password}")  # Depuración

        try:
            self.cursor.execute("SELECT rol FROM usuarios WHERE nombre_usuario=? AND contrasena=?",
                                (username, password))
            result = self.cursor.fetchone()
            print("Resultado de la consulta:", result)  # Depuración
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
        role = simpledialog.askstring("Seleccionar Rol", "Ingresa el rol (empleado/gerente):").lower()

        if username and password and role in ['empleado', 'gerente']:
            try:
                self.cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (?, ?, ?)",
                                    (username, password, role))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Cuenta creada exitosamente.")
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo crear la cuenta: {e}")
        else:
            messagebox.showwarning("Advertencia",
                                   "Nombre de usuario, contraseña y rol son requeridos. El rol debe ser 'empleado' o 'gerente'.")

    def show_manager_interface(self):
        """Mostrar la interfaz del gerente sin scroll y con barra lateral completa."""
        self.clear_window()

        main_container = tk.Frame(self.master)
        main_container.pack(fill="both", expand=True)

        sidebar = tk.Frame(main_container, bg="#4A148C", width=200, height=self.master.winfo_height())
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="SED", font=("Arial", 24, "bold"), bg="#4A148C", fg="white").pack(pady=(50, 5))
        tk.Label(sidebar, text="Sistema de Evaluación de Desempeño", font=("Arial", 10), bg="#4A148C", fg="white").pack(
            pady=(0, 100))

        buttons = [("Home", "🏠"), ("Mis resultados", "📊"), ("Mi historial", "📁")]
        for text, icon in buttons:
            button = tk.Button(sidebar, text=f"{icon}  {text}", font=("Arial", 12), bg="#4A148C", fg="white",
                               borderwidth=0)
            button.pack(fill="x", pady=20, padx=20)

        tk.Button(sidebar, text="Log out", font=("Arial", 12, "bold"), bg="#A4A4A4", fg="white", borderwidth=0,
                  command=self.login_screen).pack(side="bottom", pady=20, padx=10)

        content_frame = tk.Frame(main_container, bg="#f0f4f7")
        content_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        tk.Label(content_frame, text="Bienvenido, gerente 👔", font=("Arial", 14), bg="#f0f4f7", fg="#4A148C").pack(
            anchor="ne")

        card_titles = [
            ("Evaluar empleado", self.manager_evaluation),
            ("Ver evaluaciones anteriores", self.view_previous_evaluations),
            ("Comparar desempeño de empleados", self.compare_performance),
            ("Generar reporte de desempeño", self.generate_report),
            ("Añadir feedback", self.add_feedback)
        ]

        for title, command in card_titles:
            card = tk.Frame(content_frame, bg="white", bd=1, relief="solid", width=600, height=100)
            card.pack(pady=10, fill="x")
            card.pack_propagate(False)

            tk.Label(card, text=title, font=("Arial", 14, "bold"), bg="white", fg="#4A148C").pack(anchor="w", padx=10,
                                                                                                  pady=5)
            tk.Button(card, text="Comenzar", bg="#4A148C", fg="white", font=("Arial", 10, "bold"), relief="flat",
                      command=command).pack(anchor="e", padx=10, pady=5)

    def show_employee_interface(self):
        """Mostrar la interfaz del empleado con el mismo tamaño de tarjetas que las de gerente, conservando títulos específicos."""
        self.clear_window()

        main_container = tk.Frame(self.master)
        main_container.pack(fill="both", expand=True)

        sidebar = tk.Frame(main_container, bg="#4A148C", width=200, height=self.master.winfo_height())
        sidebar.pack(side="left", fill="y")

        tk.Label(sidebar, text="SED", font=("Arial", 24, "bold"), bg="#4A148C", fg="white").pack(pady=(50, 5))
        tk.Label(sidebar, text="Sistema de Evaluación de Desempeño", font=("Arial", 10), bg="#4A148C", fg="white").pack(
            pady=(0, 100))

        buttons = [("Home", "🏠"), ("Mis resultados", "📊"), ("Mi historial", "📁")]
        for text, icon in buttons:
            button = tk.Button(sidebar, text=f"{icon}  {text}", font=("Arial", 12), bg="#4A148C", fg="white",
                               borderwidth=0)
            button.pack(fill="x", pady=20, padx=20)

        tk.Button(sidebar, text="Log out", font=("Arial", 12, "bold"), bg="#A4A4A4", fg="white", borderwidth=0,
                  command=self.login_screen).pack(side="bottom", pady=20, padx=10)

        content_frame = tk.Frame(main_container, bg="#f0f4f7")
        content_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)

        tk.Label(content_frame, text="Bienvenido, empleado 👔", font=("Arial", 14), bg="#f0f4f7", fg="#4A148C").pack(
            anchor="ne")

        card_titles = [
            ("Autoevaluación", self.self_evaluation),
            ("Ver evaluaciones anteriores", self.view_previous_evaluations),
            ("Ver feedback recibido", self.view_feedback),
        ]

        for title, command in card_titles:
            card = tk.Frame(content_frame, bg="white", bd=1, relief="solid", width=600, height=100)
            card.pack(pady=10, fill="x")
            card.pack_propagate(False)

            tk.Label(card, text=title, font=("Arial", 14, "bold"), bg="white", fg="#4A148C").pack(anchor="w", padx=10,
                                                                                                  pady=5)
            tk.Button(card, text="Comenzar", bg="#4A148C", fg="white", font=("Arial", 10, "bold"), relief="flat",
                      command=command).pack(anchor="e", padx=10, pady=5)

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
        """Interfaz gráfica mejorada para la evaluación del empleado por el gerente."""
        self.clear_window()  # Limpiar la ventana actual

        # Crear el contenedor principal
        main_frame = tk.Frame(self.master, bg="#f0f0f0", padx=20, pady=20, relief="ridge", borderwidth=2)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título de la evaluación, más grande que el resto del texto
        title_label = tk.Label(main_frame, text="Evaluación de Desempeño del Empleado", font=("Arial", 26, "bold"),
                               fg="#4b2e83", bg="#f0f0f0")
        title_label.pack(pady=20)

        # Entrada para el nombre del empleado
        tk.Label(main_frame, text="Nombre del Empleado a Evaluar:", font=("Arial", 18), bg="#f0f0f0").pack(pady=(10, 5))
        employee_name_entry = tk.Entry(main_frame, font=("Arial", 16), width=40)
        employee_name_entry.pack(pady=5)

        # Preguntas de evaluación en un marco con estilo "tarjeta"
        questions_frame = tk.Frame(main_frame, bg="#ffffff", padx=10, pady=10, relief="groove", borderwidth=1)
        questions_frame.pack(pady=(20, 10), fill="x")

        # Lista de preguntas
        questions = [
            "1. ¿Cómo calificarías la calidad del trabajo del empleado?",
            "2. ¿Con qué frecuencia supera las expectativas en sus tareas asignadas?",
            "3. ¿Cómo evalúas su capacidad para resolver problemas?",
            "4. ¿Qué tan bien maneja las tareas bajo presión?",
            "5. ¿Cómo calificas su habilidad para trabajar en equipo?"
        ]

        response_scales = []
        for idx, question in enumerate(questions, start=1):
            # Etiqueta de la pregunta con fuente más grande
            question_label = tk.Label(questions_frame, text=question, font=("Arial", 16), fg="#4b2e83", bg="#ffffff")
            question_label.pack(anchor="w", pady=(10 if idx > 1 else 0, 5))  # Separación entre preguntas

            # Barra deslizante para la respuesta, con fuente más grande para los números
            response_scale = tk.Scale(questions_frame, from_=1, to=5, orient="horizontal", length=400,
                                      font=("Arial", 14),
                                      bg="#ffffff", troughcolor="#d9d9d9", highlightthickness=0)
            response_scale.pack(pady=5)
            response_scales.append(response_scale)

        # Botón para guardar la evaluación, con fuente más grande
        submit_button = tk.Button(main_frame, text="Guardar Evaluación", font=("Arial", 18, "bold"), bg="#4b2e83",
                                  fg="#ffffff",
                                  padx=20, pady=10,
                                  command=lambda: self.save_manager_evaluation(employee_name_entry.get(),
                                                                               response_scales))
        submit_button.pack(pady=20)

        # Botón para regresar a la interfaz principal del gerente, también con fuente más grande
        back_button = tk.Button(main_frame, text="Volver", font=("Arial", 16), bg="#dddddd", fg="#333333",
                                command=self.show_manager_interface)
        back_button.pack(pady=10)

    def save_manager_evaluation(self, employee_name, response_scales):
        """Guardar la evaluación realizada por el gerente."""
        if not employee_name:
            messagebox.showwarning("Advertencia", "Por favor ingresa el nombre del empleado.")
            return

        # Obtener las respuestas de las barras deslizantes
        responses = [scale.get() for scale in response_scales]
        if not any(responses):
            messagebox.showwarning("Advertencia", "Por favor responde todas las preguntas antes de guardar.")
            return

        # Calcular el promedio
        average_score = sum(responses) / len(responses)

        try:
            manager_eval_json = str(responses)
            self.cursor.execute(
                "UPDATE evaluaciones SET evaluacion_gerente=? WHERE nombre_empleado=?",
                (manager_eval_json, employee_name)
            )
            self.conn.commit()
            messagebox.showinfo("Resultados de Evaluación",
                                f"La puntuación promedio del empleado {employee_name} es: {average_score:.2f}")
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar la evaluación del gerente: {e}")

    from tkinter import ttk

    def view_previous_evaluations(self):
        # Mejoras en el cuadro de diálogo para ingresar el nombre del empleado
        name_window = tk.Toplevel(self.master)
        name_window.title("Nombre del Empleado")
        name_window.geometry("400x150")
        name_window.configure(bg="#f7f7f7")

        tk.Label(name_window, text="Ingresa el nombre del empleado:", font=("Arial", 16), bg="#f7f7f7").pack(pady=20)

        employee_name_entry = tk.Entry(name_window, font=("Arial", 14), width=30)
        employee_name_entry.pack(pady=5)

        def submit_name():
            employee_name = employee_name_entry.get()
            if employee_name:
                name_window.destroy()
                self.display_evaluations(employee_name)
            else:
                messagebox.showwarning("Advertencia", "Por favor ingresa el nombre del empleado.")

        tk.Button(name_window, text="OK", font=("Arial", 14), command=submit_name).pack(pady=10)

    def display_evaluations(self, employee_name):
        try:
            self.cursor.execute(
                "SELECT autoevaluacion, evaluacion_gerente FROM evaluaciones WHERE nombre_empleado=?",
                (employee_name,))
            result = self.cursor.fetchone()

            if result:
                autoeval = eval(result[0]) if result[0] else []
                manager_eval = eval(result[1]) if result[1] else []

                # Calcular promedios
                autoeval_avg = sum(autoeval) / len(autoeval) if autoeval else 0
                manager_eval_avg = sum(manager_eval) / len(manager_eval) if manager_eval else 0

                # Crear una nueva ventana para mostrar las evaluaciones
                eval_window = tk.Toplevel(self.master)
                eval_window.title(f"Evaluaciones de {employee_name}")
                eval_window.geometry("1000x800")  # Ajuste del tamaño de la ventana
                eval_window.configure(bg="#f7f7f7")

                # Botón para volver a la página principal en la esquina superior izquierda
                back_button = tk.Button(eval_window, text="Volver", font=("Arial", 14), bg="#4b2e83", fg="white",
                                        command=self.show_manager_interface)
                back_button.place(x=20, y=20)  # Posición en la esquina superior izquierda

                # Título de la ventana
                title_label = tk.Label(eval_window, text=f"Evaluaciones anteriores para {employee_name}",
                                       font=("Arial", 24, "bold"), fg="#4b2e83", bg="#f7f7f7")
                title_label.pack(pady=60)  # Separación para que el título quede debajo del botón "Volver"

                # Tabla de Autoevaluación
                autoeval_label = tk.Label(eval_window, text="Autoevaluación", font=("Arial", 20, "bold"),
                                          fg="#4b2e83", bg="#f7f7f7")
                autoeval_label.pack(pady=10)

                autoeval_table = ttk.Treeview(eval_window, columns=("Pregunta", "Puntaje"), show="headings", height=8)
                autoeval_table.heading("Pregunta", text="Pregunta", anchor="center")
                autoeval_table.heading("Puntaje", text="Puntaje", anchor="center")
                autoeval_table.column("Pregunta", anchor="center", width=600)
                autoeval_table.column("Puntaje", anchor="center", width=200)
                autoeval_table.pack(pady=5, padx=20, fill="x", expand=False)

                # Estilos
                style = ttk.Style()
                style.configure("Treeview", font=("Arial", 16), rowheight=30)
                style.configure("Treeview.Heading", font=("Arial", 18, "bold"))

                # Insertar filas de autoevaluación y promedio
                for i, score in enumerate(autoeval, 1):
                    autoeval_table.insert("", "end", values=(f"Pregunta {i}", score))
                autoeval_table.insert("", "end", values=("Promedio", f"{autoeval_avg:.2f}"))

                # Tabla de Evaluación por Gerente
                manager_eval_label = tk.Label(eval_window, text="Evaluación por Gerente", font=("Arial", 20, "bold"),
                                              fg="#4b2e83", bg="#f7f7f7")
                manager_eval_label.pack(pady=20)

                manager_eval_table = ttk.Treeview(eval_window, columns=("Pregunta", "Puntaje"), show="headings",
                                                  height=8)
                manager_eval_table.heading("Pregunta", text="Pregunta", anchor="center")
                manager_eval_table.heading("Puntaje", text="Puntaje", anchor="center")
                manager_eval_table.column("Pregunta", anchor="center", width=600)
                manager_eval_table.column("Puntaje", anchor="center", width=200)
                manager_eval_table.pack(pady=5, padx=20, fill="x", expand=False)

                # Insertar filas de evaluación por gerente y promedio
                for i, score in enumerate(manager_eval, 1):
                    manager_eval_table.insert("", "end", values=(f"Pregunta {i}", score))
                manager_eval_table.insert("", "end", values=("Promedio", f"{manager_eval_avg:.2f}"))

            else:
                messagebox.showinfo("Evaluaciones Anteriores", f"No se encontraron evaluaciones para {employee_name}.")

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudieron recuperar las evaluaciones: {e}")

    def compare_performance(self):
        employees_to_compare = simpledialog.askstring(
            "Comparar Desempeño",
            "Ingresa los nombres de los empleados separados por comas:"
        )

        if employees_to_compare:
            employee_list = [name.strip() for name in employees_to_compare.split(',')]
            overall_scores = {}

            # Crear la ventana de comparación de desempeño
            compare_window = tk.Toplevel(self.master)
            compare_window.title("Comparativa de Desempeño")
            compare_window.geometry("1400x850")  # Tamaño ajustado para más espacio
            compare_window.configure(bg="#f0f4f7")

            # Botón para regresar a la página principal
            back_button = tk.Button(
                compare_window, text="Volver", font=("Arial", 16, "bold"), bg="#4b2e83", fg="white",
                command=self.show_manager_interface, relief="flat", padx=20, pady=10
            )
            back_button.place(x=20, y=20)

            # Título principal ajustado más abajo
            title_label = tk.Label(
                compare_window, text="Comparativa de Desempeño",
                font=("Arial", 28, "bold"), fg="#4b2e83", bg="#f0f4f7"
            )
            title_label.pack(pady=(60, 20))  # Ajuste de padding para bajar el título

            # Crear marco principal centrado
            main_frame = tk.Frame(compare_window, bg="#f0f4f7")
            main_frame.pack(expand=True)

            # Frame superior para las tablas de desempeño de cada empleado (una al lado de la otra)
            tables_frame = tk.Frame(main_frame, bg="#f0f4f7")
            tables_frame.pack(side="top", pady=20)

            # Obtener y mostrar los resultados de cada empleado en una tabla separada
            for idx, employee in enumerate(employee_list, start=1):
                try:
                    self.cursor.execute(
                        "SELECT autoevaluacion FROM evaluaciones WHERE nombre_empleado=?",
                        (employee,)
                    )
                    result = self.cursor.fetchone()

                    if result:
                        autoeval = eval(result[0])  # Convertir JSON a lista

                        # Crear un marco para cada empleado y colocarlos uno al lado del otro
                        employee_frame = tk.Frame(tables_frame, bg="#ffffff", padx=10, pady=10, relief="ridge",
                                                  borderwidth=1)
                        employee_frame.grid(row=0, column=idx - 1, padx=20, sticky="n")

                        # Etiqueta de título para el empleado en grande
                        employee_label = tk.Label(
                            employee_frame,
                            text=f"Empleado {idx}: {employee}",
                            font=("Arial", 18, "bold"),
                            fg="#4b2e83",
                            bg="#ffffff"
                        )
                        employee_label.pack(anchor="w", pady=(10, 5))

                        # Crear la tabla para mostrar preguntas y puntajes
                        eval_table = ttk.Treeview(employee_frame, columns=("Pregunta", "Puntaje"), show="headings",
                                                  height=10)
                        eval_table.heading("Pregunta", text="Pregunta", anchor="center")
                        eval_table.heading("Puntaje", text="Puntaje", anchor="center")
                        eval_table.column("Pregunta", anchor="center", width=350)  # Ajustar el ancho de columna
                        eval_table.column("Puntaje", anchor="center", width=150)
                        eval_table.pack(pady=5, padx=20, fill="x")

                        # Ajuste de estilo para aumentar el tamaño de fuente de las celdas y encabezados
                        style = ttk.Style()
                        style.configure("Treeview", font=("Arial", 14), rowheight=40)
                        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

                        # Insertar las respuestas en la tabla
                        for i, score in enumerate(autoeval, 1):
                            eval_table.insert("", "end", values=(f"Pregunta {i}", score))

                        # Calcular y mostrar el promedio
                        average_score = sum(autoeval) / len(autoeval) if autoeval else 0
                        eval_table.insert("", "end", values=("Promedio", f"{average_score:.2f}"))

                        # Guardar el promedio en el diccionario para el ranking
                        overall_scores[employee] = average_score
                    else:
                        messagebox.showinfo("Info", f"No se encontró autoevaluación para el empleado: {employee}")
                except mariadb.Error as e:
                    messagebox.showerror("Error", f"No se pudo recuperar las evaluaciones para {employee}: {e}")

            # Frame inferior para el ranking de empleados, centrado
            ranking_frame = tk.Frame(main_frame, bg="#f0f4f7")
            ranking_frame.pack(side="top", pady=30)

            # Mostrar el ranking de empleados
            if overall_scores:
                ranking_title = tk.Label(
                    ranking_frame, text="Ranking de Empleados",
                    font=("Arial", 24, "bold"), fg="#4b2e83", bg="#f0f4f7"
                )
                ranking_title.pack(pady=(10, 20))

                sorted_scores = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
                for rank, (emp, score) in enumerate(sorted_scores, start=1):
                    rank_label = tk.Label(
                        ranking_frame,
                        text=f"{rank}. {emp}: {score:.2f}",
                        font=("Arial", 20), fg="#333333", bg="#f0f4f7"
                    )
                    rank_label.pack(anchor="w", pady=10)  # Mayor separación entre cada empleado en el ranking

    def generate_report(self):
        report_text = "Reporte de Desempeño General:\n\n"

        try:
            self.cursor.execute(
                "SELECT nombre_empleado, autoevaluacion, evaluacion_gerente FROM evaluaciones")

            for row in self.cursor.fetchall():
                report_text += f"Empleado: {row[0]}\n"
                # Procesar autoevaluación
                autoeval = eval(row[1])  # Convertir JSON a lista
                report_text += "Autoevaluación:\n"

                for i, score in enumerate(autoeval, 1):
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

                report_text += "-" * 50 + "\n"  # Separator for better readability

            # Mostrar reporte en una ventana nueva
            report_window = tk.Toplevel(self.master)

            report_window.title("Reporte de Desempeño")

            # Color de la ventana
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
                        messagebox.showwarning("Advertencia",
                                               f"No se encontró un empleado con el nombre: {employee_name}.")

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