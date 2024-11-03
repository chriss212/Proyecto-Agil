    if username and password and role in ['empleado', 'gerente']:
            try:
                self.cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena, rol) VALUES (?, ?, ?)", (username, password, role))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Cuenta creada exitosamente.")
            except mariadb.Error as e:
                messagebox.showerror("Error", f"No se pudo crear la cuenta: {e}")
        else:
            messagebox.showwarning("Advertencia", "Nombre de usuario, contraseña y rol son requeridos. El rol debe ser 'empleado' o 'gerente'.")