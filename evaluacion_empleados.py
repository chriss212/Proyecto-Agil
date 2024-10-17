import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import mariadb
import sys

class EmployeeEvaluationApp:
    def __init__(self, master):
        self.master = master
        master.title("Evaluación del Desempeño de Empleados")

        # Conexión a la base de datos
        self.connect_db()

        # Pantalla de inicio de sesión
        self.login_screen()

    def connect_db(self):
        """Conectar a la base de datos MariaDB."""
        try:
            # Cambia estos valores por tus credenciales
            self.conn = mariadb.connect(
                user="root",
                password="suser",
                host="localhost",
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

        tk.Label(self.master, text="Iniciar Sesión").pack()

        tk.Label(self.master, text="Usuario:").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        tk.Label(self.master, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self.master, show='*')
        self.password_entry.pack()

        tk.Button(self.master, text="Iniciar Sesión", command=self.login).pack()

    def clear_window(self):
        """Limpiar la ventana actual."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def login(self):
        """Verificar credenciales y mostrar la interfaz correspondiente."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            # Consultar las credenciales desde la base de datos
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
        
        tk.Label(self.master, text="Bienvenido Gerente").pack()

        self.manager_evaluation_button = tk.Button(self.master, text="Evaluar Empleado", command=self.manager_evaluation)
        self.manager_evaluation_button.pack()

        self.previous_evaluations_button = tk.Button(self.master, text="Ver Evaluaciones Anteriores", command=self.view_previous_evaluations)
        self.previous_evaluations_button.pack()

        self.compare_performance_button = tk.Button(self.master, text="Comparar Desempeño de Empleados", command=self.compare_performance)
        self.compare_performance_button.pack()

        self.report_button = tk.Button(self.master, text="Generar Reporte de Desempeño", command=self.generate_report)
        self.report_button.pack()

    def show_employee_interface(self):
        """Mostrar la interfaz del empleado."""
        self.clear_window()
        
        tk.Label(self.master, text="Bienvenido Empleado").pack()

        self.self_evaluation_button = tk.Button(self.master, text="Realizar Autoevaluación", command=self.self_evaluation)
        self.self_evaluation_button.pack()

        self.previous_evaluations_button = tk.Button(self.master, text="Ver Evaluaciones Anteriores", command=self.view_previous_evaluations)
        self.previous_evaluations_button.pack()

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
                if response is not None:  # Verifica que el usuario no cancele
                    responses.append(response)

        if not responses:
            messagebox.showwarning("Advertencia", "No se realizaron respuestas a la autoevaluación.")
            return

        average_score = sum(responses) / len(responses)
        
        employee_name = simpledialog.askstring("Nombre del Empleado", "Ingresa tu nombre:")
        
        if employee_name:
            try:
                # Guardar autoevaluación en formato JSON
                autoeval_json = str(responses)

                # Insertar autoevaluación en la base de datos
                self.cursor.execute("INSERT INTO evaluaciones (nombre_empleado, rol, autoevaluacion) VALUES (?, ?, ?)", 
                                    (employee_name, 'Empleado', autoeval_json))
                
                # Commit a la base de datos
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
                if response is not None:  # Verifica que el usuario no cancele
                    responses.append(response)

            if not responses:
                messagebox.showwarning("Advertencia", "No se realizaron respuestas a la evaluación del empleado.")
                return

            average_score = sum(responses) / len(responses)

            try:
                # Guardar evaluación del gerente en formato JSON
                manager_eval_json = str(responses)

                # Insertar evaluación del gerente en la base de datos
                self.cursor.execute("UPDATE evaluaciones SET evaluacion_gerente=? WHERE nombre_empleado=?", 
                                    (manager_eval_json, employee_name))
                
                # Commit a la base de datos
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
                # Consultar evaluaciones anteriores desde la base de datos
                self.cursor.execute("SELECT autoevaluacion, evaluacion_gerente FROM evaluaciones WHERE nombre_empleado=?", (employee_name,))
                
                result = self.cursor.fetchone()
                
                if result:
                    evaluations_text = f"Evaluaciones anteriores para {employee_name}:\n\n"
                    evaluations_text += f"Autoevaluación: {result[0]}\n"
                    evaluations_text += f"Evaluación por Gerente: {result[1]}\n"
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
            
            for employee in employee_list:
                try:
                    # Consultar las evaluaciones desde la base de datos
                    self.cursor.execute("SELECT autoevaluacion FROM evaluaciones WHERE nombre_empleado=?", (employee,))
                    result = self.cursor.fetchone()
                    
                    if result:
                        report_text += f"Empleado: {employee}\nAutoevaluación: {result[0]}\n\n"
                    else:
                        report_text += f"Empleado: {employee} no encontrado.\n\n"
                except mariadb.Error as e:
                    messagebox.showerror("Error", f"No se pudo recuperar las evaluaciones para {employee}: {e}")

            # Mostrar comparativa en una ventana nueva
            compare_window = tk.Toplevel(self.master)
            compare_window.title("Comparativa de Desempeño")
            compare_window.focus_force()  # Hacer que esta ventana esté activa

            compare_text_area = scrolledtext.ScrolledText(compare_window, width=50, height=20)
            compare_text_area.insert(tk.END, report_text.strip())
            compare_text_area.pack()

    def generate_report(self):
        report_text = "Reporte de Desempeño General:\n\n"
        
        try:
            # Consultar todas las evaluaciones desde la base de datos
            self.cursor.execute("SELECT nombre_empleado, autoevaluacion, evaluacion_gerente FROM evaluaciones")
            
            for row in self.cursor.fetchall():
                report_text += f"Empleado: {row[0]}\n"
                report_text += f"Autoevaluación: {row[1]}\n"
                report_text += f"Evaluación por Gerente: {row[2]}\n\n"

            # Mostrar reporte en una ventana nueva
            report_window = tk.Toplevel(self.master)
            report_window.title("Reporte de Desempeño")
            report_window.focus_force()  # Hacer que esta ventana esté activa

            report_text_area = scrolledtext.ScrolledText(report_window, width=50, height=20)
            report_text_area.insert(tk.END, report_text.strip())
            report_text_area.pack()
          
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeEvaluationApp(root)
    root.mainloop()