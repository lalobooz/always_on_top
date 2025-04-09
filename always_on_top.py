import tkinter as tk
from tkinter import ttk
import win32gui
import win32con

class AlwaysOnTopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Always On Top")
        self.root.geometry("300x200")  # Tamaño pequeño
        self.root.resizable(False, False)  # No redimensionable
        self.root.configure(bg="#f5f5f5")  # Fondo gris claro

        # Lista de ventanas
        self.windows = []
        self.selected_hwnd = None

        # Estilo
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TLabel", background="#f5f5f5", font=("Arial", 12))
        style.configure("TListbox", font=("Arial", 10))

        # Etiqueta
        label = ttk.Label(root, text="Select a window:", style="TLabel")
        label.pack(pady=5)

        # Lista de ventanas
        self.listbox = tk.Listbox(root, height=5, font=("Arial", 10))
        self.listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Botones
        button_frame = ttk.Frame(root, style="TFrame")
        button_frame.pack(pady=5)

        self.set_top_button = ttk.Button(button_frame, text="Set On Top", command=self.set_always_on_top)
        self.set_top_button.pack(side=tk.LEFT, padx=5)

        self.unset_top_button = ttk.Button(button_frame, text="Unset", command=self.unset_always_on_top)
        self.unset_top_button.pack(side=tk.LEFT, padx=5)

        # Cargar la lista de ventanas
        self.refresh_windows()

    def refresh_windows(self):
        self.windows = []
        self.listbox.delete(0, tk.END)

        def enum_windows(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:  # Solo agregar ventanas con título
                    self.windows.append((hwnd, title))
                    self.listbox.insert(tk.END, title)

        win32gui.EnumWindows(enum_windows, None)

    def on_select(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.selected_hwnd = self.windows[index][0]

    def set_always_on_top(self):
        if self.selected_hwnd:
            # Establecer la ventana como "always on top"
            win32gui.SetWindowPos(self.selected_hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

    def unset_always_on_top(self):
        if self.selected_hwnd:
            # Quitar el estado "always on top"
            win32gui.SetWindowPos(self.selected_hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlwaysOnTopApp(root)
    root.mainloop()