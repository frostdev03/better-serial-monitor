import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import serial
import serial.tools.list_ports
import threading
from datetime import datetime
import os
import sys

def resource_path(relative_path):
    """ Mengambil path absolut ke resource, berfungsi untuk dev dan PyInstaller """
    try:
        # PyInstaller membuat folder sementara dan menyimpan path-nya di _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SerialMonitorApp:
    def __init__(self, root):
        self.root = root
        # self.root.wm_iconbitmap("app_icon.ico")
        self.root.wm_iconbitmap(resource_path("app_icon.ico"))
        self.root.title("Simple Serial Monitor v1.0")
        self.root.geometry("800x500") # Sedikit lebih tinggi untuk menampung tombol baru
        
        self.serial_conn = None
        self.is_reading = False

        # --- Layout Utama ---
        self.left_frame = tk.Frame(root, width=220, padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.right_frame = tk.Frame(root, padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- Sisi Kiri: Konfigurasi ---
        tk.Label(self.left_frame, text="Config", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))

        # Dropdown Serial Port
        tk.Label(self.left_frame, text="Serial Port:").pack(anchor=tk.W)
        self.port_cb = ttk.Combobox(self.left_frame, values=self.get_ports(), state="readonly")
        self.port_cb.pack(fill=tk.X, pady=(0, 5))
        
        self.btn_refresh = tk.Button(self.left_frame, text="Refresh Ports", command=self.refresh_ports, font=("Arial", 8))
        self.btn_refresh.pack(fill=tk.X, pady=(0, 10))
        
        # Dropdown Baud Rate
        tk.Label(self.left_frame, text="Baud Rate:").pack(anchor=tk.W)
        self.baud_cb = ttk.Combobox(self.left_frame, values=["9600", "115200", "921600"], state="readonly")
        self.baud_cb.set("115200") 
        self.baud_cb.pack(fill=tk.X, pady=(0, 10))

        # Checkbox Options
        self.show_timestamp = tk.BooleanVar(value=False)
        tk.Checkbutton(self.left_frame, text="Show Timestamp", variable=self.show_timestamp).pack(anchor=tk.W)

        self.auto_scroll = tk.BooleanVar(value=True)
        tk.Checkbutton(self.left_frame, text="Auto Scroll", variable=self.auto_scroll).pack(anchor=tk.W, pady=(0, 15))

        # Action Buttons
        self.btn_connect = tk.Button(self.left_frame, text="Connect", command=self.connect, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.btn_connect.pack(fill=tk.X, pady=3)

        self.btn_disconnect = tk.Button(self.left_frame, text="Disconnect", command=self.disconnect, bg="#f44336", fg="white", font=("Arial", 10, "bold"), state=tk.DISABLED)
        self.btn_disconnect.pack(fill=tk.X, pady=3)

        # FITUR BARU: Tombol Export
        self.btn_export = tk.Button(self.left_frame, text="Export to .txt", command=self.export_to_txt, bg="#2196F3", fg="white")
        self.btn_export.pack(fill=tk.X, pady=(15, 3))

        self.btn_clear = tk.Button(self.left_frame, text="Clear Monitor", command=self.clear_text)
        self.btn_clear.pack(fill=tk.X, pady=3)

        # --- Sisi Kanan: Serial Monitor ---
        self.text_area = tk.Text(self.right_frame, wrap=tk.WORD, state=tk.DISABLED, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
        self.scrollbar = tk.Scrollbar(self.right_frame, command=self.text_area.yview)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def get_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]
        
    def refresh_ports(self):
        self.port_cb['values'] = self.get_ports()

    def connect(self):
        port = self.port_cb.get()
        baud = self.baud_cb.get()
        if not port:
            messagebox.showerror("Error", "Pilih Serial Port terlebih dahulu!")
            return
        try:
            self.serial_conn = serial.Serial(port, int(baud), timeout=1)
            self.is_reading = True
            self.btn_connect.config(state=tk.DISABLED)
            self.btn_disconnect.config(state=tk.NORMAL)
            self.port_cb.config(state=tk.DISABLED)
            self.thread = threading.Thread(target=self.read_data, daemon=True)
            self.thread.start()
            self.log_text(f"--- Connected to {port} ---\n")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal: {e}")

    def disconnect(self):
        self.is_reading = False
        if self.serial_conn: self.serial_conn.close()
        self.btn_connect.config(state=tk.NORMAL)
        self.btn_disconnect.config(state=tk.DISABLED)
        self.port_cb.config(state="readonly")
        self.log_text("--- Disconnected ---\n")

    def read_data(self):
        while self.is_reading and self.serial_conn.is_open:
            try:
                if self.serial_conn.in_waiting > 0:
                    data = self.serial_conn.readline().decode('utf-8', errors='replace')
                    if self.show_timestamp.get():
                        data = f"[{datetime.now().strftime('%H:%M:%S')}] {data}"
                    self.log_text(data)
            except: break

    def log_text(self, text):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text)
        if self.auto_scroll.get(): self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def clear_text(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)

    # LOGIKA BARU: Fungsi Export
    def export_to_txt(self):
        # Mengambil semua teks dari text_area
        content = self.text_area.get(1.0, tk.END).strip()
        
        if not content:
            messagebox.showwarning("Export", "Monitor masih kosong, tidak ada data untuk di-export.")
            return

        # Membuka dialog simpan file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Simpan Log Serial"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Berhasil", f"Data berhasil disimpan ke:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialMonitorApp(root)
    root.mainloop()