import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import mariadb
import sys

class EmployeeEvaluationApp:
    def __init__(self, master):
        self.master = master
        master.title("Evaluación del Desempeño de Empleados")
        master.geometry("400x400")
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

    def login_screen(self):
        """Crear la pantalla de inicio de sesión."""
        self.clear_window()

        tk.Label(self.master, text="Iniciar Sesión", font=("Arial", 18), bg="#f0f4f7").pack(pady=20)

        tk.Label(self.master, text="Usuario:", font=("Arial", 12), bg="#f0f4f7").pack()
        self.username_entry = tk.Entry(self.master, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Label(self.master, text="Contraseña:", font=("Arial", 12), bg="#f0f4f7").pack()
        self.password_entry = tk.Entry(self.master, show='*', font=("Arial", 12))
        self.password_entry.pack(pady=5)

        tk.Button(self.master, text="Iniciar Sesión", command=self.login, bg="#5cb85c", fg="white", font=("Arial", 12)).pack(pady=20)

    def clear_window(self):
        """Limpiar la ventana actual."""
        for widget in self.master.winfo_children():
            widget.destroy()

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

    def show_manager_interface(self):
        """Mostrar la interfaz del gerente."""
        self.clear_window()
        
        tk.Label(self.master, text="Bienvenido Gerente", font=("Arial", 18), bg="#f0f4f7").pack(pady=20)

        tk.Button(self.master, text="Evaluar Empleado", command=self.manager_evaluation, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Ver Evaluaciones Anteriores", command=self.view_previous_evaluations, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Comparar Desempeño de Empleados", command=self.compare_performance, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Generar Reporte de Desempeño", command=self.generate_report, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.master, text="Regresar a Iniciar Sesión", command=self.login_screen, bg="#f0ad4e", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Cerrar Aplicación", command=sys.exit, bg="#d9534f", fg="white", font=("Arial", 12)).pack(pady=10)


    def show_employee_interface(self):
        """Mostrar la interfaz del empleado."""
        self.clear_window()
        
        tk.Label(self.master, text="Bienvenido Empleado", font=("Arial", 18), bg="#f0f4f7").pack(pady=20)

        tk.Button(self.master, text="Realizar Autoevaluación", command=self.self_evaluation, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Ver Evaluaciones Anteriores", command=self.view_previous_evaluations, bg="#5bc0de", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.master, text="Regresar a Iniciar Sesión", command=self.login_screen, bg="#f0ad4e", font=("Arial", 12)).pack(pady=10)
        tk.Button(self.master, text="Cerrar Aplicación", command=sys.exit, bg="#d9534f", fg="white", font=("Arial", 12)).pack(pady=10)


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
                response = simpledialog.askinteger("Autoevaluación", f"{question}\n(1: Malo, 5: Excelente)", minvalue=1, maxvalue=5)
                if response is not None:
                    responses.append(response)

        if not responses:
            messagebox.showwarning("Advertencia", "No se realizaron respuestas a la autoevaluación.")
            return

        average_score = sum(responses) / len(responses)
        
        employee_name = simpledialog.askstring("Nombre del Empleado", "Ingresa tu nombre:")
        
        if employee_name:
            try:
                autoeval_json = str(responses)

                self.cursor.execute("INSERT INTO evaluaciones (nombre_empleado, rol, autoevaluacion) VALUES (?, ?, ?)", 
                                    (employee_name, 'Empleado', autoeval_json))
                
                self.conn.commit()
                
                messagebox.showinfo("Resultados de Autoevaluación", f"Tu puntuación promedio es: {average_score:.2f}")
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo guardar la autoevaluación: {e}")
        else:
            messagebox.showwarning("Advertencia", "Nombre de empleado no ingresado.")

    def manager_evaluation(self):
        employee_name = simpledialog.askstring("Nombre del Empleado", "Ingresa el nombre del empleado a evaluar:")
        
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
                response = simpledialog.askinteger("Evaluación del Empleado", f"{question}\n(1: Malo, 5: Excelente)", minvalue=1, maxvalue=5)
                if response is not None:
                    responses.append(response)

            if not responses:
                messagebox.showwarning("Advertencia", "No se realizaron respuestas a la evaluación del empleado.")
                return

            average_score = sum(responses) / len(responses)

            try:
                manager_eval_json = str(responses)

                self.cursor.execute("UPDATE evaluaciones SET evaluacion_gerente=? WHERE nombre_empleado=?", 
                                    (manager_eval_json, employee_name))
                
                self.conn.commit()
                
                messagebox.showinfo("Resultados de Evaluación", f"La puntuación promedio del empleado {employee_name} es: {average_score:.2f}")
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo guardar la evaluación del gerente: {e}")
        else:
            messagebox.showwarning("Advertencia", "Nombre de empleado no ingresado.")

    def view_previous_evaluations(self):
        employee_name = simpledialog.askstring("Nombre del Empleado", "Ingresa tu nombre:")
        
        if employee_name:
            try:
                self.cursor.execute("SELECT autoevaluacion, evaluacion_gerente FROM evaluaciones WHERE nombre_empleado=?", (employee_name,))
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
                    
                    messagebox.showinfo("Evaluaciones Anteriores", evaluations_text.strip())
                else:
                    messagebox.showinfo("Evaluaciones Anteriores", f"No se encontraron evaluaciones para {employee_name}.")
                
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudieron recuperar las evaluaciones: {e}")

    def compare_performance(self):
        employees_to_compare = simpledialog.askstring("Comparar Desempeño", 
                                                    "Ingresa los nombres de los empleados separados por comas:")
        
        if employees_to_compare:
            employee_list = [name.strip() for name in employees_to_compare.split(',')]
            
            report_text = "Comparativa de Desempeño:\n\n"
            overall_scores = {}

            for employee in employee_list:
                try:
                    self.cursor.execute("SELECT autoevaluacion FROM evaluaciones WHERE nombre_empleado=?", (employee,))
                    result = self.cursor.fetchone()
                    
                    if result:
                        autoeval = eval(result[0])  # Convertir JSON a lista
                        report_text += f"Empleado: {employee}\n"
                        report_text += "Autoevaluación:\n"
                        for i, score in enumerate(autoeval, 1):
                            report_text += f"  Pregunta {i}: {score}\n"
                        
                        # Calcular y almacenar el promedio
                        average_score = sum(autoeval) / len(autoeval)
                        report_text += f"  Promedio Autoevaluación: {average_score:.2f}\n"
                        overall_scores[employee] = average_score
                    else:
                        report_text += f"Empleado: {employee} no encontrado.\n\n"
                    
                except mariadb.Error as e:
                    messagebox.showerror("Error", f"No se pudo recuperar las evaluaciones para {employee}: {e}")
            
            compare_window = tk.Toplevel(self.master)
            compare_window.title("Comparativa de Desempeño")
            compare_window.focus_force()

            compare_text_area = scrolledtext.ScrolledText(compare_window, width=70, height=20)
            compare_text_area.insert(tk.END, report_text.strip())
            compare_text_area.pack(padx=10, pady=10)

            if overall_scores:
                sorted_scores = sorted(overall_scores.items(), key=lambda x: x[1], reverse=True)
                compare_text_area.insert(tk.END, "\nRanking de Empleados:\n")
                for rank, (emp, score) in enumerate(sorted_scores, start=1):
                    compare_text_area.insert(tk.END, f"{rank}. {emp}: {score:.2f}\n")

            tk.Button(compare_window, text="Cerrar", command=compare_window.destroy).pack(pady=5)

    def generate_report(self):
        report_text = "Reporte de Desempeño General:\n\n"
        
        try:
            self.cursor.execute("SELECT nombre_empleado, autoevaluacion, evaluacion_gerente FROM evaluaciones")
            
            for row in self.cursor.fetchall():
                report_text += f"Empleado: {row[0]}\n"
                
                # Procesar autoevaluación
                autoeval = eval(row[1])  # Convertir JSON a lista
                report_text += "Autoevaluación:\n"
                for i, score in enumerate(autoeval, 1):
                    report_text += f"  Pregunta {i}: {score}\n"
                    
                # Procesar evaluación por gerente
                if row[2]:
                    manager_eval = eval(row[2])
                    report_text += "Evaluación por Gerente:\n"
                    for i, score in enumerate(manager_eval, 1):
                        report_text += f"  Pregunta {i}: {score}\n"
                else:
                    report_text += "Evaluación por Gerente: No disponible\n"
                
                # Calcular y agregar puntajes promedio
                average_auto = sum(autoeval) / len(autoeval) if autoeval else 0
                average_manager = sum(manager_eval) / len(manager_eval) if manager_eval else 0
                
                report_text += f"  Promedio Autoevaluación: {average_auto:.2f}\n"
                report_text += f"  Promedio Evaluación Gerente: {average_manager:.2f}\n"
                report_text += "-" * 50 + "\n"  # Separator for better readability

            # Mostrar reporte en una ventana nueva
            report_window = tk.Toplevel(self.master)
            report_window.title("Reporte de Desempeño")
            report_window.focus_force()

            report_text_area = scrolledtext.ScrolledText(report_window, width=70, height=20)
            report_text_area.insert(tk.END, report_text.strip())
            report_text_area.pack(padx=10, pady=10)
            
            # Add a button to close the report window
            tk.Button(report_window, text="Cerrar", command=report_window.destroy).pack(pady=5)
        
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeEvaluationApp(root)
    root.mainloop()