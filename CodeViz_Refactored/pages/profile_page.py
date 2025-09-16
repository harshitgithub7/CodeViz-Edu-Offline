import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import json
from utils.session_manager import load_session_data
import os

PROFILE_FILE = "profile.json"

class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        self.data = load_session_data()
        self.profile_data = self.load_profile()
        self.build_ui()

    def build_ui(self):
        try:
            self.profile_img = ctk.CTkImage(Image.open("assets/user.png"), size=(100, 100))
        except:
            self.profile_img = None

        profile_frame = ctk.CTkFrame(self,   corner_radius=10)
        profile_frame.pack(pady=30, padx=40, fill="x")

        # Header
        ctk.CTkLabel(profile_frame, text="👤 Profile", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(20, 10))

        # Session Stats
        ctk.CTkLabel(profile_frame, text=f"🕓 Used: {self.data.get('last_used', 'N/A')}").pack(pady=5)
        ctk.CTkLabel(profile_frame, text=f"🕒 Duration: {self.data.get('last_duration', 'N/A')}").pack(pady=5)
        ctk.CTkLabel(profile_frame, text=f"📊 Total Sessions: {self.data.get('total_sessions', 0)}").pack(pady=5)

        # Profile Image
        if self.profile_img:
            ctk.CTkLabel(profile_frame, image=self.profile_img, text="").pack(pady=10)
        else:
            ctk.CTkLabel(profile_frame, text="(No Image)", font=ctk.CTkFont(size=14)).pack()

        # Form Frame
        form = ctk.CTkFrame(profile_frame, fg_color="transparent")
        form.pack(padx=20, pady=10, fill="x")

        # Name
        ctk.CTkLabel(form, text="Name:", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(form)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.name_entry.insert(0, self.profile_data.get("name", ""))

        # Role
        ctk.CTkLabel(form, text="Role:", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.role_optionmenu = ctk.CTkOptionMenu(form, values=["Student", "Educator", "Developer", "Enthusiast"])
        self.role_optionmenu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.role_optionmenu.set(self.profile_data.get("role", "Student"))

        # Bio
        ctk.CTkLabel(form, text="Tagline / Bio:", anchor="w").grid(row=2, column=0, sticky="nw", padx=10, pady=5)
        self.bio_text = ctk.CTkTextbox(form, height=60)
        self.bio_text.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.bio_text.insert("1.0", self.profile_data.get("bio", ""))

        # Location
        ctk.CTkLabel(form, text="Location:", anchor="w").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.location_entry = ctk.CTkEntry(form)
        self.location_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.location_entry.insert(0, self.profile_data.get("location", ""))

        # Make right column expandable
        form.grid_columnconfigure(1, weight=1)

        # Save Button
        ctk.CTkButton(profile_frame, text="💾 Save", command=self.save_profile).pack(pady=(10, 20))

        # Session History Title
        ctk.CTkLabel(self, text="📅 Recent Sessions (Last 10)", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 0))

        # Session Logs Scrollable Frame
        history_frame = ctk.CTkScrollableFrame(self, height=200)
        history_frame.pack(padx=20, pady=(5, 20), fill="x")

        history = self.data.get("history", [])
        if history:
            for i, session in enumerate(reversed(history), 1):
                label_text = f"{i}. 📅 {session['date']} 🕓 {session['start']} → {session['end']} ⏱️ {session['duration']}"
                ctk.CTkLabel(history_frame, text=label_text, anchor="w", font=ctk.CTkFont(size=13)).pack(anchor="w", pady=2)
        else:
            ctk.CTkLabel(history_frame, text="No recent session data", font=ctk.CTkFont(size=13, slant="italic")).pack(pady=10)


    def save_profile(self):
        profile_data = {
                      "name": self.name_entry.get(),
                      "role": self.role_optionmenu.get(),
                      "bio": self.bio_text.get("1.0", "end").strip(),
                      "location": self.location_entry.get()
        }
 
        print("Saving profile:", profile_data)  # 👈 Debug line
 
        try:
            with open(PROFILE_FILE, "w") as f:
               json.dump(profile_data, f, indent=4)
            print("✅ Profile saved successfully.")
            messagebox.showinfo("Saved", "Profile updated successfully!")
        except Exception as e:
            print("❌ Error:", e)  # 👈 Debug error
            messagebox.showerror("Error", f"Failed to save profile: {e}")

    def load_profile(self):
        if os.path.exists(PROFILE_FILE):
            try:
                with open(PROFILE_FILE, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def get_profile_data(self):
        return {
            "name": self.name_entry.get(),
            "role": self.role_optionmenu.get(),
            "bio": self.bio_text.get("1.0", "end").strip(),
            "location": self.location_entry.get()
        }

    def refresh_theme(self):
        self.configure(fg_color="transparent")
