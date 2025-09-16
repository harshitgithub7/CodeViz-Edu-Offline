import customtkinter as ctk
from controller import AppController
from pages.home import HomePage
from pages.concepts import ConceptsPage
from pages.learning_module import LearningModulePage
from pages.applications import ApplicationsPage
from pages.settings_page import SettingsPage
from pages.user_manual import UserManualPage
from pages.profile_page import ProfilePage
from utils.session_manager import save_session_data
from datetime import datetime
 
import json

session_start_time = datetime.now()

class CodeVizApp(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.controller.screen_manager = self
        self.timer_label = None

        self.title("CodeViz - Offline Coding App")
        self.geometry("1400x800")
        self.minsize(1000, 600)
        self.protocol("WM_DELETE_WINDOW", self.on_app_close)

        # Configure master grid layout
        self.grid_rowconfigure(0, weight=0)   # Header row
        self.grid_rowconfigure(1, weight=1)   # Main content row
        self.grid_columnconfigure(0, weight=0)  # Sidebar column
        self.grid_columnconfigure(1, weight=1)  # Main area column

        # ========== Sidebar ==========
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        ctk.CTkLabel(self.sidebar, text="CodeViz", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        self.menu_items = [
            ("\U0001F3E0", "Home"),
            ("\U0001F4BB", "Compiler"),
            ("\U0001F4DA", "Concepts"),
            ("\U0001F4D2", "Learning Module"),
            ("\U0001F4CA", "Applications"),
            

             
        ]

        for icon, label in self.menu_items:
            def make_callback(name=label):
                return lambda: self.show_screen(name)
            ctk.CTkButton(self.sidebar, text=f"{icon}  {label}", anchor="w",
                          width=180, height=40, command=make_callback()).pack(pady=5, padx=10)

        # Bottom Sidebar Buttons
        ctk.CTkButton(self.sidebar, text="⚙️ Settings",
                      command=lambda: self.show_screen("Settings"), width=180).pack(side="bottom", pady=(10, 0))
        ctk.CTkButton(self.sidebar, text="📖 Manual",
                      command=lambda: self.show_screen("User Manual"), width=180).pack(side="bottom", pady=(10, 0))
        ctk.CTkButton(self.sidebar, text="\U0001F319 Toggle Theme",
                      command=self.toggle_theme, width=180).pack(side="bottom", pady=(10, 20))

        # ========== Header ==========
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.grid(row=0, column=1, sticky="new")
        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.header, text="Home", font=ctk.CTkFont(size=22, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.profile_icon = ctk.CTkButton(self.header, text="\U0001F464", width=40, height=40,
                                          corner_radius=20, fg_color="#2f2f2f",
                                          command=lambda: self.show_screen("Profile"))
        self.profile_icon.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        # ========== Main Area ==========
        self.main_area = ctk.CTkFrame(self)
        self.main_area.grid(row=1, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        # ========== Screens ==========
        self.frames = {
            "Home": HomePage(self.main_area, self.controller),
            "Concepts": ConceptsPage(self.main_area),
            "Learning Module": LearningModulePage(self.main_area),
            "Applications": ApplicationsPage(self.main_area),
            "Settings": SettingsPage(self.main_area),
            "User Manual": UserManualPage(self.main_area),
            "Profile": ProfilePage(self.main_area),
           
            "Compiler": None  # Lazy loaded
            
        }

        for key, frame in self.frames.items():
            if frame is not None:
                frame.grid(row=0, column=0, sticky="nsew")

        self.show_screen("Home")

    def on_app_close(self):
        try:
            profile_page = self.frames.get("Profile")
            if profile_page:
               profile_data = profile_page.get_profile_data()
            with open("profile.json", "w") as f:
                json.dump(profile_data, f, indent=4)
        except Exception as e:
         print("Error saving profile:", e)
    
        self.destroy()


    def show_screen(self, name):
        self.title_label.configure(text=name)

        # Track session
        self.last_opened_tab = name
        self.controller.save_session_data(name)

        for frame in self.frames.values():
            if frame is not None:
                frame.grid_remove()
        if name == "Compiler":
            from pages.compiler_internal import get_compiler_frame
            compiler_frame = get_compiler_frame(self.main_area)
            self.frames["Compiler"] = compiler_frame
            compiler_frame.grid(row=0, column=0, sticky="nsew")
        elif name in self.frames and self.frames[name]:
            self.frames[name].grid(row=0, column=0, sticky="nsew")
        elif name == "Profile":
            self.frames["Profile"].refresh_theme()
            self.frames["Profile"].grid()

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        ctk.set_appearance_mode("Light" if current == "Dark" else "Dark")

        home = self.frames.get("Home")
        if home:
            home.refresh_footer_theme()

  

import atexit
atexit.register(lambda: save_session_data(session_start_time))
# Save session data on exit
        
if __name__ == "__main__":
    controller = AppController()
    app = CodeVizApp(controller)
    app.mainloop()