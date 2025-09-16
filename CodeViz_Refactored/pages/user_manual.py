import customtkinter as ctk

manual_data = {
    "Home": "Overview of the app, motivation, and quick navigation.",
    "Concepts": "Theoretical content with quick jump buttons and search.",
    "Learning Module": "Code examples and real-time explanation area.",
    "Compiler": "Write, run and debug your C code.",
    "Applications": "Real-world C applications, ideas and project tips.",
    "Settings": "Toggle appearance and theme options.",
    "Profile": "Customize your name and role for personalization."
}

class UserManualPage(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(parent )

        ctk.CTkLabel(self, text="📖 User Manual", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 10))

        for section, description in manual_data.items():
            accordion = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=6)
            accordion.pack(fill="x", pady=8, padx=20)
            ctk.CTkLabel(accordion, text=f"📌 {section}", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(accordion, text=description, wraplength=800).pack(anchor="w", padx=10, pady=(2, 10))
