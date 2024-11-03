class Styles:
    def __init__(self, root):
        # Definir estilos para el login
        style = ttk.Style(root)

        # Estilo para las etiquetas
        style.configure('TLabel', font=('Arial', 12), padding=10, background="#f0f4f7")  # Establecer fondo
        style.configure('TButton', font=('Arial', 12), padding=5, background="#5cb85c", foreground="white")  # Estilo para el botón
        style.configure('TEntry', font=('Arial', 12), padding=5)

        # Estilo adicional para el botón cuando está en estado activo
        style.map('TButton',
                  background=[('active', '#4cae4f')])  # Color cuando el botón está activo



