import tkinter as tk
from tkinter import messagebox
from src.services.SynchronizeUser import SynchronizeUser

class SinchronizeForm(tk.Toplevel):
    def __init__(self, dbManager):
        super().__init__()
        self.title("Sinchronize User Form - AquaFlow")
        self.geometry("300x400")

        self.db_manager = dbManager

        tk.Label(self, text="ID de usuario:").grid(row=2, column=0, padx=5, pady=5)
        self.user_id = tk.Entry(self)
        self.user_id.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self, text="Enviar", command=self.send_uid).grid(row=3, column=0, columnspan=2, pady=10)

    def send_uid(self):
        SynchronizeUser(self.db_manager, self.user_id.get())
        messagebox.showinfo("Sincronizado", f"Sincronizado con el usuari: {self.user_id.get()}")
        self.destroy()