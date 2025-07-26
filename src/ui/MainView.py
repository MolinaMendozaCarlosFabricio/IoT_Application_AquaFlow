import tkinter as tk
from tkinter import ttk

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.__is_running = True
        self.title("AquaFlow System Device")
        self.geometry("500x400")

        self.turbidiy_raw = ttk.Label(self, text="Turbidez (NTU): 0 NTU")
        self.turbidiy_raw.pack()

        self.tds_raw = ttk.Label(self, text="Total de Sólidos Disueltos (ppm): 0 ppm")
        self.tds_raw.pack()

        self.ph_raw = ttk.Label(self, text="pH: 7")
        self.ph_raw.pack()

        self.temp_raw = ttk.Label(self, text="Temperatura (C°): 0°")
        self.temp_raw.pack()

        self.boton = ttk.Button(self, text="Cerrar programa", command=self.__closeProgram)
        self.boton.pack(pady=20)
    
    def showMeasurements(self, turbidity, tds, ph, temp):
        self.after(0, lambda: self.turbidiy_raw.config(text=f"Turbidez (NTU): {turbidity} NTU"))
        self.after(0, lambda: self.tds_raw.config(text=f"Total de Sólidos Disueltos (ppm): {tds} ppm"))
        self.after(0, lambda: self.ph_raw.config(text=f"pH: {ph}"))
        self.after(0, lambda: self.temp_raw.config(text=f"Temperatura (C°: {temp}°)"))
    
    def __closeProgram(self):
        self.__is_running = False
    
    def verifyRunning(self):
        return self.__is_running