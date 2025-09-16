import customtkinter as ctk
from .compiler_internal import get_compiler_frame
from datetime import datetime
from utils.session_manager import load_session_data

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()

    def update_timer(self):
        elapsed = datetime.now() - self.start_time
        self.timer_label.configure(text=f"Session: {str(elapsed).split('.')[0]}")
        self.after(1000, self.update_timer)

    def build_ui(self):
        # Header
        ctk.CTkLabel(self, text="👋 Welcome to CodeViz", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(40, 10))
        ctk.CTkLabel(self, text="Your personal offline C programming buddy", font=ctk.CTkFont(size=16)).pack(pady=(0, 30))

        # Button Grid
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        button_data = [
            ("📒 Learning Module", lambda: self.master.master.show_screen("Learning Module")),
            ("💻 Compiler", lambda: self.master.master.show_screen("Compiler")),
            ("📚 Concepts", lambda: self.master.master.show_screen("Concepts")),
            ("📊 Applications", lambda: self.master.master.show_screen("Applications")),
        ]

        for i, (label, command) in enumerate(button_data):
            btn = ctk.CTkButton(button_frame, text=label, width=240, height=50, font=ctk.CTkFont(size=15), command=command)
            btn.grid(row=i//2, column=i%2, padx=20, pady=10)

        self.start_time = datetime.now()

        # Footer Frame
        self.footer = ctk.CTkFrame(self, height=60, fg_color="#000000", corner_radius=0)
        self.footer.pack(fill="x", side="bottom", pady=(200, 10))

        self.footer.grid_columnconfigure(0, weight=1)
        self.footer.grid_columnconfigure(1, weight=2)
        self.footer.grid_columnconfigure(2, weight=1)

        # Labels
        self.timer_label = ctk.CTkLabel(self.footer, text="Session: 00:00:00")
        self.timer_label.grid(row=0, column=0, padx=20, sticky="w")

        self.quote_label = ctk.CTkLabel(
            self.footer,
            text="“The only way to learn to code is by coding.”",
            font=ctk.CTkFont(size=14, slant="italic")
        )
        self.quote_label.grid(row=0, column=1, padx=20, sticky="n")

        self.copyright_label = ctk.CTkLabel(
            self.footer,
            text="© Harshit Sharma • Terms • Privacy",
            font=ctk.CTkFont(size=12)
        )
        self.copyright_label.grid(row=0, column=2, padx=20, sticky="e")

        self.update_timer()
        self.refresh_footer_theme()  # Initial theme sync

    def refresh_footer_theme(self):
        theme = ctk.get_appearance_mode()
        if theme == "Dark":
            text_color = "#FFFFFF"
            footer_color = "#000000"
        else:
            text_color = "#000000"
            footer_color = "#F5F5F5"

        self.footer.configure(fg_color=footer_color)
        self.timer_label.configure(text_color=text_color)
        self.quote_label.configure(text_color=text_color)
        self.copyright_label.configure(text_color=text_color)
