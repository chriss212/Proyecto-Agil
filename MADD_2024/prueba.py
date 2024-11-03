import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import mariadb
import sys

class EmployeeEvaluationApp:
    def __init__(self, master):
        self.master = master
        master.title("Evaluación del Desempeño de Empleados")
        master.geometry("800x600")  # Ventana de tamaño 800x600

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

        tk.Label(self.master, text="Iniciar Sesión", font=("Arial", 16)).pack(pady=20)

        tk.Label(self.master, text="Usuario:").pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack(pady=5)

        tk.Label(self.master, text="Contraseña:").pack()
        self.password_entry = tk.Entry(self.master, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(self.master, text="Iniciar Sesión", command=self.login).pack(pady=20)

        tk.Button(self.master, text="Crear Cuenta", command=self.create_account).pack(pady=5)

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
        
        tk.Label(self.master, text="Bienvenido Gerente", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.master, text="Evaluar Empleado", command=self.manager_evaluation).pack(pady=5)
        tk.Button(self.master, text="Ver Evaluaciones Anteriores", command=self.view_previous_evaluations).pack(pady=5)
        tk.Button(self.master, text="Comparar Desempeño de Empleados", command=self.compare_performance).pack(pady=5)
        tk.Button(self.master, text="Generar Reporte de Desempeño", command=self.generate_report).pack(pady=5)
        tk.Button(self.master, text="Administrar Cuentas", command=self.manage_accounts).pack(pady=5)
        tk.Button(self.master, text="Ver Todas las Cuentas", command=self.view_accounts).pack(pady=5)

    def show_employee_interface(self):
        """Mostrar la interfaz del empleado."""
        self.clear_window()
        
        tk.Label(self.master, text="Bienvenido Empleado", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.master, text="Realizar Autoevaluación", command=self.self_evaluation).pack(pady=5)
        tk.Button(self.master, text="Ver Evaluaciones Anteriores", command=self.view_previous_evaluations).pack(pady=5)

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
            self.show_full_window("Autoevaluación", f"Categoría: {category}")  # Ventana completa
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
                autoeval_json = str(responses)

                self.cursor.execute("INSERT INTO evaluaciones (nombre_empleado, rol, autoevaluacion) VALUES (?, ?, ?)", 
                                    (employee_name, 'Empleado', autoeval_json))
                self.conn.commit()
                
                messagebox.showinfo("Resultados de Autoevaluación", f"Tu puntuación promedio es: {average_score:.2f}")
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo guardar la autoevaluación: {e}")
        else:
            messagebox.showwarning("Advertencia", "Nombre de empleado no ingresado.")

    def show_full_window(self, title, message):
        """Mostrar una ventana completa."""
        full_window = tk.Toplevel(self.master)
        full_window.title(title)
        full_window.geometry("800x600")  # Ajustar el tamaño de la ventana
        tk.Label(full_window, text=message, font=("Arial", 16)).pack(pady=20)

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
        self.clear_window()
        
        tk.Label(self.master, text="Evaluaciones Anteriores", font=("Arial", 16)).pack(pady=20)

        try:
            self.cursor.execute("SELECT nombre_empleado, autoevaluacion, evaluacion_gerente FROM evaluaciones")
            evaluations = self.cursor.fetchall()

            for emp_name, self_eval, mgr_eval in evaluations:
                tk.Label(self.master, text=f"Empleado: {emp_name}").pack()
                tk.Label(self.master, text=f"Autoevaluación: {self_eval}").pack()
                tk.Label(self.master, text=f"Evaluación del Gerente: {mgr_eval if mgr_eval else 'No disponible'}").pack()
                tk.Label(self.master, text="").pack()  # Espacio en blanco
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener las evaluaciones: {e}")

        tk.Button(self.master, text="Volver", command=self.login_screen).pack(pady=20)

    def compare_performance(self):
        # Lógica para comparar desempeño de empleados
        messagebox.showinfo("Comparar Desempeño", "Funcionalidad en desarrollo.")

    def generate_report(self):
        # Lógica para generar reportes
        messagebox.showinfo("Generar Reporte", "Funcionalidad en desarrollo.")

    def manage_accounts(self):
        self.clear_window()

        tk.Label(self.master, text="Administrar Cuentas", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.master, text="Crear Nueva Cuenta", command=self.create_account).pack(pady=5)
        tk.Button(self.master, text="Editar Cuenta Existente", command=self.edit_account).pack(pady=5)
        tk.Button(self.master, text="Ver Todas las Cuentas", command=self.view_accounts).pack(pady=5)

        tk.Button(self.master, text="Volver", command=self.login_screen).pack(pady=20)

    def create_account(self):
        new_username = simpledialog.askstring("Crear Cuenta", "Ingresa el nombre de usuario:")
        new_password = simpledialog.askstring("Crear Cuenta", "Ingresa la contraseña:", show='*')
        new_role = simpledialog.askstring("Crear Cuenta", "Ingresa el rol (gerente/empleado):")

        if new_username and new_password and new_role in ['gerente', 'empleado']:
            try:
                self.cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (?, ?, ?)", 
                                    (new_username, new_password, new_role))
                self.conn.commit()
                messagebox.showinfo("Éxito", f"Cuenta {new_username} creada exitosamente.")
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo crear la cuenta: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor ingresa todos los campos correctamente.")

    def edit_account(self):
        username_to_edit = simpledialog.askstring("Editar Cuenta", "Ingresa el nombre de usuario de la cuenta a editar:")
        
        if username_to_edit:
            new_password = simpledialog.askstring("Editar Cuenta", "Ingresa la nueva contraseña:", show='*')
            new_role = simpledialog.askstring("Editar Cuenta", "Ingresa el nuevo rol (gerente/empleado):")

            if new_password and new_role in ['gerente', 'empleado']:
                try:
                    self.cursor.execute("UPDATE usuarios SET contrasena=?, rol=? WHERE nombre_usuario=?", 
                                        (new_password, new_role, username_to_edit))
                    self.conn.commit()
                    messagebox.showinfo("Éxito", f"Cuenta {username_to_edit} editada exitosamente.")
                except mariadb.Error as e:
                    messagebox.showerror("Error", f"No se pudo editar la cuenta: {e}")
            else:
                messagebox.showwarning("Advertencia", "Por favor ingresa todos los campos correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Nombre de usuario no ingresado.")

    def view_accounts(self):
        """Mostrar todas las cuentas existentes."""
        self.clear_window()
        
        tk.Label(self.master, text="Cuentas Existentes", font=("Arial", 16)).pack(pady=20)

        try:
            self.cursor.execute("SELECT nombre_usuario, rol FROM usuarios")
            accounts = self.cursor.fetchall()

            if accounts:
                for username, role in accounts:
                    tk.Label(self.master, text=f"Usuario: {username}, Rol: {role}").pack()
            else:
                tk.Label(self.master, text="No hay cuentas registradas.").pack()
        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo obtener las cuentas: {e}")

        tk.Button(self.master, text="Volver", command=self.manage_accounts).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeEvaluationApp(root)
    root.mainloop()