import tkinter as tk
from tkinter import ttk

class MainView(tk.Tk):
    def __init__(self, dbManager):
        # Vista principal de la aplicación, muestra la calidad del agua y las actividades que se puedan hacer con ella
        super().__init__()
        self.__is_running = True
        self.title("AquaFlow System Device")
        self.geometry("500x800")

        self.dbManager = dbManager

        self.turbidiy_raw = ttk.Label(self, text="Turbidez (NTU): 0 NTU")
        self.turbidiy_raw.pack()

        self.tds_raw = ttk.Label(self, text="Total de Sólidos Disueltos (ppm): 0 ppm")
        self.tds_raw.pack()

        self.ph_raw = ttk.Label(self, text="pH: 7")
        self.ph_raw.pack()

        self.temp_raw = ttk.Label(self, text="Temperatura (C°): 0°")
        self.temp_raw.pack()

        self.activities_label = ttk.Label(self, text="Actividades recomendadas para su uso:")
        self.activities_label.pack(pady=(10, 0))

        self.activities_listbox = tk.Listbox(self, height=8, width=60)
        self.activities_listbox.pack(pady=5)

        self.sync_button = ttk.Button(self, text="Sincronizar usuario", command=self.open_sync_form)
        self.sync_button.pack(pady=10)

    # Método para mostrar mediciones en la vista   
    def showMeasurements(self, turbidity, tds, ph, temp):
        self.after(0, lambda: self.turbidiy_raw.config(text=f"Turbidez (NTU): {turbidity} NTU"))
        self.after(0, lambda: self.tds_raw.config(text=f"Total de Sólidos Disueltos (ppm): {tds} ppm"))
        self.after(0, lambda: self.ph_raw.config(text=f"pH: {ph}"))
        self.after(0, lambda: self.temp_raw.config(text=f"Temperatura (C°: {temp}°)"))
    
    # Método para mostrar actividades en la vista
    def showActivities(self, activities):
        def update_listbox():
            self.activities_listbox.delete(0, tk.END)  # Limpiar lista anterior
            for activity in activities["water_activities_list"]:
                formatted = f"{activity['water_activity']} - {activity['percentage']}%"
                self.activities_listbox.insert(tk.END, formatted)
        self.after(0, update_listbox)

    # Método para cerrar el programa (No usado)
    def __closeProgram(self):
        self.__is_running = False
    
    # Método para verificar ejecución
    def verifyRunning(self):
        return self.__is_running
    
    # Método para abrir vista de sincronización
    def open_sync_form(self):
        from src.ui.SinchronizeForm import SinchronizeForm
        SinchronizeForm(self, self.dbManager)
