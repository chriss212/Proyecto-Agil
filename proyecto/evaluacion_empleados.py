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

        self.label = tk.Label(master, text="Sistema de Evaluación")
        self.label.pack()

        self.role_entry = tk.Entry(master)
        self.role_entry.insert(0, "Ingrese el rol del empleado")
        self.role_entry.pack()

        self.criteria_entry = tk.Entry(master)
        self.criteria_entry.insert(0, "Ingrese criterios (separados por coma)")
        self.criteria_entry.pack()

        self.submit_criteria_button = tk.Button(master, text="Guardar Criterios", command=self.save_criteria)
        self.submit_criteria_button.pack()

        self.self_evaluation_button = tk.Button(master, text="Realizar Autoevaluación", command=self.self_evaluation)
        self.self_evaluation_button.pack()

        self.manager_evaluation_button = tk.Button(master, text="Evaluar Empleado", command=self.manager_evaluation)
        self.manager_evaluation_button.pack()

        self.previous_evaluations_button = tk.Button(master, text="Ver Evaluaciones Anteriores", command=self.view_previous_evaluations)
        self.previous_evaluations_button.pack()

        self.report_button = tk.Button(master, text="Generar Reporte de Desempeño", command=self.generate_report)
        self.report_button.pack()

    def connect_db(self):
        """Conectar a la base de datos MariaDB."""
        try:
            # Cambia estos valores por tus credenciales
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

    def save_criteria(self):
        role = self.role_entry.get()
        criteria = self.criteria_entry.get().split(',')

        if role and criteria:
            criteria_str = ', '.join(criteria)
            try:
                # Inserta los criterios en la tabla
                self.cursor.execute("INSERT INTO evaluaciones (rol, criterios) VALUES (?, ?)", (role, criteria_str))
                self.conn.commit()
                messagebox.showinfo("Criterios Guardados", f"Criterios para {role}: {criteria_str}")
                # Limpiar entradas después de guardar
                self.role_entry.delete(0, tk.END)
                self.criteria_entry.delete(0, tk.END)
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudieron guardar los criterios: {e}")

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
                responses.append(response)

        average_score = sum(responses) / len(responses)
        
        employee_name = simpledialog.askstring("Nombre del Empleado", "Ingresa tu nombre:")
        
        if employee_name:
            try:
                # Guardar autoevaluación en formato JSON
                autoeval_json = str(responses)

                # Insertar autoevaluación en la base de datos
                self.cursor.execute("UPDATE evaluaciones SET autoevaluacion=? WHERE nombre_empleado=?", (autoeval_json, employee_name))
                
                # Commit a la base de datos
                self.conn.commit()
                
                messagebox.showinfo("Resultados de Autoevaluación", f"Tu puntuación promedio es: {average_score:.2f}")
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo guardar la autoevaluación: {e}")

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
                responses.append(response)

            average_score = sum(responses) / len(responses)

            try:
                # Guardar evaluación del gerente en formato JSON
                manager_eval_json = str(responses)

                # Insertar evaluación del gerente en la base de datos
                self.cursor.execute("UPDATE evaluaciones SET evaluacion_gerente=? WHERE nombre_empleado=?", (manager_eval_json, employee_name))
                
                # Commit a la base de datos
                self.conn.commit()
                
                messagebox.showinfo("Resultados de Evaluación", f"La puntuación promedio del empleado {employee_name} es: {average_score:.2f}")
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo guardar la evaluación del gerente: {e}")

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
                    return
                
            except mariadb.Error as e:
               messagebox.showerror("Error", f"No se pudieron recuperar las evaluaciones: {e}")

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
          
            report_text_area = scrolledtext.ScrolledText(report_window, width=50, height=20)
            report_text_area.insert(tk.END, report_text.strip())
          
            report_text_area.pack()
          
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo generar el reporte: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeEvaluationApp(root)
    root.mainloop()