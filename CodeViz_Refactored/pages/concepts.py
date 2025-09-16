import customtkinter as ctk
from tkinter import Text, Scrollbar, RIGHT, Y
import re
import os

class ConceptsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=2)

        # 🔍 Search Entry
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search concepts...")
        self.search_entry.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.search_entry.bind("<KeyRelease>", self.search_topics)

        # 📚 Horizontal Scrollable Topic Button Bar
        self.topic_bar = ctk.CTkScrollableFrame(self, height=50, orientation="horizontal", fg_color="transparent")
        self.topic_bar.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        # 📜 Main Content Text (tk.Text instead of CTkTextbox)
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.concepts_content = Text(self.content_frame, wrap="word", font=("Consolas", 13), bg="#1e1e1e", fg="white", insertbackground="white")
        self.concepts_content.grid(row=0, column=0, sticky="nsew")

        # Add scrollbar
        scrollbar = Scrollbar(self.content_frame, command=self.concepts_content.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.concepts_content.config(yscrollcommand=scrollbar.set)

        # Internal state
        self.topic_offsets = {}
        self.topic_buttons = []
        self.topics = []

        self.load_theory_content()

    def load_theory_content(self):
        self.concepts_content.configure(state="normal")
        self.concepts_content.delete("1.0", "end")
        self.topic_offsets.clear()

        # ✅ Use relative path to read concepts_raw.txt from db/
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "concepts_raw.txt"))

        if not os.path.exists(file_path):
            self.concepts_content.insert("1.0", "❌ Error: db/concepts_raw.txt not found.")
            self.concepts_content.configure(state="disabled")
            return

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        blocks = re.split(r"-{10,}", text)
        start_idx = 0
        self.topics.clear()

        # Clear previous buttons
        for btn in self.topic_buttons:
            btn.destroy()
        self.topic_buttons.clear()

        for i, block in enumerate(blocks):
            block = block.strip()
            if not block:
                continue

            lines = block.splitlines()
            topic_title = lines[0].strip()
            topic_text = "\n".join(lines[1:]).strip()

            self.topics.append(topic_title)
            bg_color = "#1e1e1e" if i % 2 == 0 else "#2c2c2c"
            tag_header = f"header{i}"
            tag_body = f"body{i}"

            self.topic_offsets[topic_title] = f"1.0+{start_idx}c"

            header = f"{topic_title}\n"
            body = f"{topic_text}\n\n"

            self.concepts_content.insert("end", header, tag_header)
            self.concepts_content.insert("end", body, tag_body)

            start_idx += len(header + body)

            def make_jump(t=topic_title):
                return lambda: self.scroll_to(self.topic_offsets[t])

            btn = ctk.CTkButton(self.topic_bar, text=topic_title[:30], width=160, height=32, command=make_jump())
            btn.pack(side="left", padx=6)
            self.topic_buttons.append(btn)

            # Styling works now
            self.concepts_content.tag_configure(tag_header, background=bg_color, foreground="cyan", font=("Consolas", 14, "bold"))
            self.concepts_content.tag_configure(tag_body, background=bg_color, foreground="white")

        self.concepts_content.configure(state="disabled")

    def scroll_to(self, index):
        # Calculate fraction to move scroll position
        try:
         total_lines = int(self.concepts_content.index("end-1c").split('.')[0])
         target_line = int(self.concepts_content.index(index).split('.')[0])
         fraction = target_line / total_lines
         self.concepts_content.yview_moveto(fraction)
        except Exception as e:
         print(f"Scroll error: {e}")
         self.concepts_content.see(index)  # Fallback
    
    def search_topics(self, event=None):
        query = self.search_entry.get().lower()

        for btn, topic in zip(self.topic_buttons, self.topics):
            if query in topic.lower():
                btn.configure(fg_color="#3a3a3a")
                btn.pack(side="left", padx=6)
            else:
                btn.pack_forget()

        for topic in self.topics:
            if query in topic.lower():
                self.scroll_to(self.topic_offsets[topic])
                break
