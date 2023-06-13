import tkinter as tk
from tkinter import messagebox
import datetime
import webview

class CreadorAgendas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Creador de Agendas")
        self.geometry("800x600")

        self.titulo_agenda = None
        self.participantes = []
        self.apartados = []
        self.puntos = {}
        self.discusiones = {}
        

        self.etiqueta_titulo = tk.Label(self, text="Título de la Agenda:")
        self.etiqueta_titulo.pack()

        self.entrada_titulo = tk.Entry(self)
        self.entrada_titulo.pack()

        self.etiqueta_participantes = tk.Label(self, text="Participantes:")
        self.etiqueta_participantes.pack()

        self.lista_participantes = tk.Listbox(self, selectmode=tk.SINGLE)
        self.lista_participantes.pack()

        self.entrada_participante = tk.Entry(self)
        self.entrada_participante.pack()

        self.boton_agregar_participante = tk.Button(self, text="Agregar Participante", command=self.agregar_participante)
        self.boton_agregar_participante.pack()

        self.boton_eliminar_participante = tk.Button(self, text="Eliminar Participante", command=self.eliminar_participante)
        self.boton_eliminar_participante.pack()

        self.etiqueta_apartados = tk.Label(self, text="Apartados:")
        self.etiqueta_apartados.pack()

        self.entrada_apartado = tk.Entry(self)
        self.entrada_apartado.pack()

        self.boton_agregar_apartado = tk.Button(self, text="Agregar Apartado", command=self.agregar_apartado)
        self.boton_agregar_apartado.pack()

        self.boton_eliminar_apartado = tk.Button(self, text="Eliminar Apartado", command=self.eliminar_apartado)
        self.boton_eliminar_apartado.pack()

        self.etiqueta_puntos = tk.Label(self, text="Puntos:")
        self.etiqueta_puntos.pack()

        self.entrada_punto = tk.Entry(self)
        self.entrada_punto.pack()

        self.variable_apartado = tk.StringVar(self)
        self.variable_apartado.trace("w", self.actualizar_lista_puntos)
        self.menu_desplegable_apartado = tk.OptionMenu(self, self.variable_apartado, "")
        self.menu_desplegable_apartado.pack()

        self.variable_punto = tk.StringVar(self)
        self.menu_desplegable_punto = tk.OptionMenu(self, self.variable_punto, "")
        self.menu_desplegable_punto.pack()

        self.boton_agregar_punto = tk.Button(self, text="Agregar Punto", command=self.agregar_punto)
        self.boton_agregar_punto.pack()

        self.boton_eliminar_punto = tk.Button(self, text="Eliminar Punto", command=self.eliminar_punto)
        self.boton_eliminar_punto.pack()

        self.boton_agregar_discusion = tk.Button(self, text="Agregar Discusión", command=self.agregar_discusion)
        self.boton_agregar_discusion.pack()

        self.boton_imprimir_agenda = tk.Button(self, text="Imprimir Agenda", command=self.imprimir_agenda)
        self.boton_imprimir_agenda.pack()

        self.discusiones = {}  # Diccionario para almacenar las discusiones


        self.boton_generar_html = tk.Button(self, text="Generar HTML", command=self.generar_html)
        self.boton_generar_html.pack()

    def generar_html(self):
        self.titulo_agenda = self.entrada_titulo.get()
        if not self.titulo_agenda:
            tk.messagebox.showwarning("Advertencia", "Debes ingresar un título para la agenda.")
            return

        html = f"<!DOCTYPE html>\n<html>\n<head>\n<title>{self.titulo_agenda}</title>\n</head>\n<body>\n"
        html += f"<h1>{self.titulo_agenda}</h1>\n"
        html += f"<p>Fecha de creación: {datetime.datetime.now()}</p>\n"

        if self.participantes:
            html += "<h2>Participantes</h2>\n"
            html += "<ul>\n"
            for participante in self.participantes:
                html += f"<li>{participante}</li>\n"
            html += "</ul>\n"

        if self.apartados:
            html += "<h2>Apartados</h2>\n"
            html += "<ul>\n"
            for apartado in self.apartados:
                html += f"<li>{apartado}</li>\n"
                if apartado in self.puntos:
                    html += "<ol>\n"
                    for punto in self.puntos[apartado]:
                        html += f"<li>{punto}</li>\n"
                        if apartado in self.discusiones and punto in self.discusiones[apartado]:
                            html += "<ul>\n"
                            for discusion in self.discusiones[apartado][punto]:
                                persona = discusion["Persona"]
                                descripcion = discusion["Descripción"]
                                html += f"<li>{persona}: {descripcion}</li>\n"
                            html += "</ul>\n"
                    html += "</ol>\n"
            html += "</ul>\n"

        html += "</body>\n</html>"

        # Mostrar el HTML en un componente WebView
        webview.create_window("Agenda", html=html, width=800, height=600)
        webview.start()

    def agregar_participante(self):
        participante = self.entrada_participante.get()
        if participante:
            self.participantes.append(participante)
            self.lista_participantes.insert(tk.END, participante)
            self.entrada_participante.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Participante agregado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debes ingresar un participante.")

    def eliminar_participante(self):
        indice_seleccionado = self.lista_participantes.curselection()
        if indice_seleccionado:
            participante = self.lista_participantes.get(indice_seleccionado)
            confirmado = messagebox.askyesno("Confirmación", f"¿Estás seguro de eliminar al participante '{participante}'?")
            if confirmado:
                self.lista_participantes.delete(indice_seleccionado)
                self.participantes.remove(participante)
                messagebox.showinfo("Éxito", "Participante eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debes seleccionar un participante.")

    def agregar_apartado(self):
        apartado = self.entrada_apartado.get()
        if apartado:
            self.apartados.append(apartado)
            self.menu_desplegable_apartado['menu'].add_command(label=apartado, command=tk._setit(self.variable_apartado, apartado))
            self.entrada_apartado.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Apartado agregado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debes ingresar un apartado.")

    def eliminar_apartado(self):
        apartado_seleccionado = self.variable_apartado.get()
        if apartado_seleccionado:
            confirmado = messagebox.askyesno("Confirmación", f"¿Estás seguro de eliminar el apartado '{apartado_seleccionado}'?")
            if confirmado:
                self.menu_desplegable_apartado['menu'].delete(0, tk.END)
                self.apartados.remove(apartado_seleccionado)
                for apartado in self.apartados:
                    self.menu_desplegable_apartado['menu'].add_command(label=apartado, command=tk._setit(self.variable_apartado, apartado))
                self.variable_apartado.set("")
                self.menu_desplegable_punto['menu'].delete(0, tk.END)
                messagebox.showinfo("Éxito", "Apartado eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debes seleccionar un apartado.")

    def actualizar_lista_puntos(self, *args):
        apartado_seleccionado = self.variable_apartado.get()
        self.menu_desplegable_punto['menu'].delete(0, tk.END)
        if apartado_seleccionado in self.puntos:
            for punto in self.puntos[apartado_seleccionado]:
                self.menu_desplegable_punto['menu'].add_command(label=punto, command=tk._setit(self.variable_punto, punto))

    def agregar_punto(self):
        apartado = self.variable_apartado.get()
        punto = self.entrada_punto.get()
        if apartado and punto:
            if apartado not in self.puntos:
                self.puntos[apartado] = []
            self.puntos[apartado].append(punto)
            self.menu_desplegable_punto['menu'].add_command(label=punto, command=tk._setit(self.variable_punto, punto))
            self.entrada_punto.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Punto agregado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Debes seleccionar un apartado e ingresar un punto.")

    def eliminar_punto(self):
        punto_seleccionado = self.variable_punto.get()
        if punto_seleccionado:
            confirmado = messagebox.askyesno("Confirmación", f"¿Estás seguro de eliminar el punto '{punto_seleccionado}'?")
            if confirmado:
                for apartado in self.puntos:
                    if punto_seleccionado in self.puntos[apartado]:
                        self.puntos[apartado].remove(punto_seleccionado)
                        self.menu_desplegable_punto['menu'].delete(0, tk.END)
                        for punto in self.puntos[apartado]:
                            self.menu_desplegable_punto['menu'].add_command(label=punto, command=tk._setit(self.variable_punto, punto))
                        messagebox.showinfo("Éxito", "Punto eliminado correctamente.")
                        break
        else:
            messagebox.showwarning("Advertencia", "Debes seleccionar un punto.")

    def agregar_discusion(self):
        def actualizar_lista_puntos_discusion(*args):
            apartado = variable_apartado_discusion.get()
            menu_desplegable_punto_discusion['menu'].delete(0, tk.END)
            if apartado in self.puntos:
                for punto in self.puntos[apartado]:
                    menu_desplegable_punto_discusion['menu'].add_command(label=punto, command=tk._setit(variable_punto_discusion, punto))

        discusion = tk.Toplevel(self)
        discusion.title("Agregar Discusión")
        discusion.geometry("400x300")

        etiqueta_apartado_discusion = tk.Label(discusion, text="Apartado:")
        etiqueta_apartado_discusion.pack()

        variable_apartado_discusion = tk.StringVar(discusion)
        variable_apartado_discusion.set(self.apartados[0] if self.apartados else "")
        menu_desplegable_apartado_discusion = tk.OptionMenu(discusion, variable_apartado_discusion, *self.apartados, command=actualizar_lista_puntos_discusion)
        menu_desplegable_apartado_discusion.pack()

        etiqueta_punto_discusion = tk.Label(discusion, text="Punto:")
        etiqueta_punto_discusion.pack()

        variable_punto_discusion = tk.StringVar(discusion)
        menu_desplegable_punto_discusion = tk.OptionMenu(discusion, variable_punto_discusion, "")
        menu_desplegable_punto_discusion.pack()

        etiqueta_persona_discusion = tk.Label(discusion, text="Persona:")
        etiqueta_persona_discusion.pack()

        variable_persona_discusion = tk.StringVar(discusion)
        menu_desplegable_persona_discusion = tk.OptionMenu(discusion, variable_persona_discusion, *self.participantes)
        menu_desplegable_persona_discusion.pack()

        etiqueta_descripcion_discusion = tk.Label(discusion, text="Descripción:")
        etiqueta_descripcion_discusion.pack()

        texto_descripcion_discusion = tk.Text(discusion)
        texto_descripcion_discusion.pack()

        def guardar_discusion():
            apartado = variable_apartado_discusion.get()
            punto = variable_punto_discusion.get()
            persona = variable_persona_discusion.get()
            descripcion = texto_descripcion_discusion.get("1.0", tk.END).strip()
            if apartado and punto and descripcion and persona:
                if apartado not in self.discusiones:
                    self.discusiones[apartado] = {}
                if punto not in self.discusiones[apartado]:
                    self.discusiones[apartado][punto] = []
                self.discusiones[apartado][punto].append({"Persona": persona, "Descripción": descripcion})
                discusion.destroy()
                messagebox.showinfo("Éxito", "Discusión agregada correctamente.")
            else:
                messagebox.showwarning("Advertencia", "Debes llenar todos los campos.")

        boton_guardar_discusion = tk.Button(discusion, text="Guardar Discusión", command=guardar_discusion)
        boton_guardar_discusion.pack()

    def imprimir_agenda(self):
        self.titulo_agenda = self.entrada_titulo.get()
        if not self.titulo_agenda:
            messagebox.showwarning("Advertencia", "Debes ingresar un título para la agenda.")
            return
        agenda = f"Título de la Agenda: {self.titulo_agenda}\n\n"

        if self.participantes:
            agenda += "Participantes:\n"
            for participante in self.participantes:
                agenda += f"- {participante}\n"
            agenda += "\n"

        if self.apartados:
            agenda += "Apartados:\n"
            for apartado in self.apartados:
                agenda += f"- {apartado}\n"
                if apartado in self.puntos:
                    agenda += "  Puntos:\n"
                    for punto in self.puntos[apartado]:
                        agenda += f"  - {punto}\n"
                        if apartado in self.discusiones and punto in self.discusiones[apartado]:
                            agenda += "    Discusiones:\n"
                            for discusion in self.discusiones[apartado][punto]:
                                persona = discusion["Persona"]
                                descripcion = discusion["Descripción"]
                                agenda += f"    - {persona}: {descripcion}\n"
            agenda += "\n"

        messagebox.showinfo("Agenda", agenda)

    def imprimir_agenda_terminal(self):
        
        for section in self.discusiones:
            print(f"Apartado: {section}")
            for point in self.discusiones[section]:
                print(f"Punto: {point}")
                for discussion in self.discusiones[section][point]:
                    print(f"Discusión: {discussion}")
            print()

if __name__ == "__main__":
    app = CreadorAgendas()
    app.mainloop()

    app.imprimir_agenda_terminal()
