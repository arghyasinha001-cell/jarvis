import customtkinter as ctk
import threading
from jarvis import start_jarvis, shutdown_system

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class JarvisGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("JARVIS AI SYSTEM")
        self.geometry("600x500")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header
        self.header = ctk.CTkFrame(self, corner_radius=10)
        self.header.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(self.header, text="J.A.R.V.I.S.", font=("Roboto Medium", 24, "bold"), text_color="#00E5FF").pack(side="left", padx=20, pady=10)
        self.status = ctk.CTkLabel(self.header, text="OFFLINE", font=("Roboto", 14), text_color="gray")
        self.status.pack(side="right", padx=20)

        # Console
        self.console = ctk.CTkTextbox(self, font=("Consolas", 12), text_color="#00FF00", fg_color="black")
        self.console.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.console.insert("0.0", "System Initialized...\n")
        self.console.configure(state="disabled")

        # Buttons
        self.btn_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.start_btn = ctk.CTkButton(self.btn_frame, text="INITIALIZE", command=self.start_thread, font=("Roboto", 14, "bold"), fg_color="#00E5FF", text_color="black")
        self.start_btn.pack(side="left", expand=True, fill="x", padx=10)

        self.stop_btn = ctk.CTkButton(self.btn_frame, text="TERMINATE", command=self.stop_process, font=("Roboto", 14, "bold"), fg_color="#FF3D00")
        self.stop_btn.pack(side="right", expand=True, fill="x", padx=10)
        
        self.thread = None

    def log(self, msg):
        self.console.configure(state="normal")
        self.console.insert("end", str(msg) + "\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def start_thread(self):
        if self.thread and self.thread.is_alive(): return
        self.status.configure(text="SYSTEM ONLINE", text_color="#00FF00")
        self.start_btn.configure(state="disabled")
        self.thread = threading.Thread(target=start_jarvis, args=(self.log,), daemon=True)
        self.thread.start()

    def stop_process(self):
        self.log("Shutting down...")
        self.status.configure(text="OFFLINE", text_color="red")
        shutdown_system()
        self.destroy()

if __name__ == "__main__":
    app = JarvisGUI()
    app.mainloop()
    