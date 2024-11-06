    def manager_evaluation(self):
        """Interfaz gráfica mejorada para la evaluación del empleado por el gerente."""
        self.clear_window()  # Limpiar la ventana actual

        # Crear el contenedor principal
        main_frame = tk.Frame(self.master, bg="#f0f0f0", padx=20, pady=20, relief="ridge", borderwidth=2)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Título de la evaluación
        title_label = tk.Label(main_frame, text="Evaluación de Desempeño del Empleado", font=("Arial", 26, "bold"),
                            fg="#4b2e83", bg="#f0f0f0")
        title_label.pack(pady=20)

        # Entrada para el nombre del empleado
        tk.Label(main_frame, text="Nombre del Empleado a Evaluar:", font=("Arial", 18), bg="#f0f0f0").pack(pady=(10, 5))
        employee_name_entry = tk.Entry(main_frame, font=("Arial", 16), width=40)
        employee_name_entry.pack(pady=5)

        # Crear un canvas para permitir el desplazamiento
        canvas = tk.Canvas(main_frame, bg="#ffffff")
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        questions_frame = tk.Frame(canvas, bg="#ffffff")

        questions_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=questions_frame, anchor="nw")

        # Configurar la barra de desplazamiento
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Lista de preguntas
        questions = [
            "1. ¿Cómo calificarías la calidad del trabajo del empleado?",
            "2. ¿Con qué frecuencia supera las expectativas en sus tareas asignadas?",
            "3. ¿Cómo evalúas su capacidad para resolver problemas?",
            "4. ¿Qué tan bien maneja las tareas bajo presión?",
            "5. ¿Cómo calificas su habilidad para trabajar en equipo?"
        ]

        response_scales = []
        for idx, question in enumerate(questions):
            # Etiqueta de la pregunta
            question_label = tk.Label(questions_frame, text=question, font=("Arial", 16), fg="#4b2e83", bg="#ffffff")
            question_label.pack(anchor="w", pady=(10 if idx > 0 else 0, 5))

            # Barra deslizante para la respuesta
            response_scale = tk.Scale(questions_frame, from_=1, to=5, orient="horizontal", length=400,
                                    font=("Arial", 14),
                                    bg="#ffffff", troughcolor="#d9d9d9", highlightthickness=0)
            response_scale.pack(pady=5)
            response_scales.append(response_scale)

        # Botón para guardar la evaluación
        submit_button = tk.Button(main_frame, text="Guardar Evaluación", font=("Arial", 18, "bold"), bg="#4b2e83",
                                fg="#ffffff",
                                padx=20, pady=10,
                                command=lambda: self.save_manager_evaluation(employee_name_entry.get(),
                                                                            response_scales))
        submit_button.pack(pady=20)

        # Botón para regresar a la interfaz principal del gerente
        back_button = tk.Button(main_frame, text="Volver", font=("Arial", 16), bg="#dddddd", fg="#333333",
                                command=self.show_manager_interface)
        back_button.pack(pady=10)

    def save_manager_evaluation(self, employee_name, response_scales):
        """Guardar la evaluación realizada por el gerente y enviar el reporte por correo."""
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
            
            # Mostrar el promedio en un mensaje con formato coherente
            messagebox.showinfo("Resultados de Evaluación",
                                f"La puntuación promedio del empleado {employee_name} es: "
                                f"{average_score:.2f}", icon='info')

            autoeval = responses  # Suponiendo que las respuestas son parte de la autoevaluación

            # Llamar a la función para generar PDF y enviar correo
            self.prompt_send_email(employee_name, autoeval, responses)

        except mariadb.Error as e:
            messagebox.showerror("Error", f"No se pudo guardar la evaluación del gerente: {e}")