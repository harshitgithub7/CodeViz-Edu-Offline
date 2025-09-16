import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.selected_mode = ctk.StringVar(value="Dark")

        # 🌙 Theme Label
        ctk.CTkLabel(self, text="🌙 App Appearance", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(30, 10))

        # ⬇️ Light/Dark Toggle
        ctk.CTkOptionMenu(self, values=["Light", "Dark"], variable=self.selected_mode).pack(pady=10)

        # ✅ Apply Button
        ctk.CTkButton(self, text="Apply Theme", command=self.apply_theme).pack(pady=30)

        # Feedback Label
        self.feedback = ctk.CTkLabel(self, text="", text_color="lightgreen")
        self.feedback.pack()

    def apply_theme(self):
        mode = self.selected_mode.get()
        ctk.set_appearance_mode(mode)

        self.feedback.configure(text=f"Switched to {mode} Mode ✅", text_color="#2ECC71")
        self.after(2500, lambda: self.feedback.configure(text=""))  
        
        # Refresh theme-aware pages
        if hasattr(self.master.master, "frames"):
            for frame in self.master.master.frames.values():
                if hasattr(frame, "refresh_theme"):
                    frame.refresh_theme()
