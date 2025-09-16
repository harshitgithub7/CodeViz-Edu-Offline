import customtkinter as ctk

# 📚 Application Data
APPLICATION_DATA = [
    {
        "title": "📦 Arrays",
        "category": "Basics",
        "difficulty": "Beginner",
        "use": "Used in shopping carts, sensor data tracking, and image processing.",
        "why": "To store multiple elements of the same type in contiguous memory.",
        "helpful": "Efficient for indexing, traversing, sorting, and searching.",
        "project": "Create a Mini Inventory Tracker for a grocery shop."
    },
    {
        "title": "🔁 Loops",
        "category": " Control Flow",
        "difficulty": "Beginner",
        "use": "Used in loading animations, simulation programs, and menu-based apps.",
        "why": "To execute a set of statements repeatedly based on a condition.",
        "helpful": "Reduces code repetition, improves control and logic building.",
        "project": "Create a Pattern Printer or a Number Guessing Game."
    },
    {
        "title": "🧮 Functions",
        "category": "Basics",
        "difficulty": "Beginner",
        "use": "Used in calculators, banking systems, and modular programs.",
        "why": "Breaks down complex logic into manageable chunks.",
        "helpful": "Increases reusability, readability, and debugging ease.",
        "project": "Build a Scientific Calculator with multiple operations."
    },
    {
        "title": "📂 File Handling",
        "category": "Memory",
        "difficulty": "Intermediate",
        "use": "Used in text editors, log systems, and saving game progress.",
        "why": "Allows data persistence beyond runtime.",
        "helpful": "You can store and retrieve user-generated data easily.",
        "project": "Create a File-based To-Do List or Student Record System."
    },
    {
        "title": "🎯 Conditionals",
        "category": "Control Flow",
        "difficulty": "Beginner",
        "use": "Used in authentication systems, sorting logic, and decision apps.",
        "why": "Controls flow of execution based on conditions.",
        "helpful": "Essential for logic branching and decision-making.",
        "project": "Build a Login System or a Menu-Driven Calculator."
    },
    {
        "title": "🧵 Pointers",
        "category": "Memory",
        "difficulty": "Advanced",
        "use": "Used in memory managers, linked lists, and system-level programs.",
        "why": "Allows direct memory access and dynamic memory allocation.",
        "helpful": "Used to build flexible data structures like trees and graphs.",
        "project": "Create a Custom String Manipulator using pointers."
    },
    {
        "title": "🧱 Structures",
        "category": " Data Structures",
        "difficulty": "Intermediate",
        "use": "Used in student databases, employee records, and gaming profiles.",
        "why": "To group related variables (data of different types) together.",
        "helpful": "Enables object-like data modeling.",
        "project": "Design a Resume Builder or Employee Management System."
    },
    {
        "title": "📶 Recursion",
        "category": "Advanced",
        "difficulty": "Advanced",
        "use": "Used in problem-solving (factorials, Fibonacci, backtracking).",
        "why": "Solves problems by breaking them into smaller sub-problems.",
        "helpful": "Ideal for tree traversal, mathematical algorithms, etc.",
        "project": "Create a Tower of Hanoi simulator or Maze Solver."
    },
    {
        "title": "🔍 Searching",
        "category": "Basics",
        "difficulty": "Intermediate",
        "use": "Used in search engines, contact lookup, and inventory checks.",
        "why": "Helps find data efficiently in a large dataset.",
        "helpful": "Binary search is fast for sorted data; linear for unsorted.",
        "project": "Build a Library Book Finder using search logic."
    },
    {
        "title": "📊 Sorting",
        "category": "Basics",
        "difficulty": "Intermediate",
        "use": "Used in leaderboards, billing systems, and analytics.",
        "why": "Sorts data to make search and analysis easier.",
        "helpful": "Fundamental in data processing and organization.",
        "project": "Create a Student Marks Sorter (bubble, selection, quick sort)."
    },
    {
        "title": "📈 Dynamic Memory",
        "category": "Memory",
        "difficulty": "Advanced",
        "use": "Used in real-time systems with uncertain memory size.",
        "why": "Allocates memory during runtime as needed.",
        "helpful": "Avoids wastage and handles variable-size data.",
        "project": "Create a Dynamic Array or Memory Usage Visualizer."
    },
    {
        "title": "🔗 Linked Lists",
        "category": "Data Structures",
        "difficulty": "Intermediate",
        "use": "Used in undo features, browser history, and playlist queues.",
        "why": "Allows dynamic memory use and easier insertion/deletion.",
        "helpful": "More flexible than arrays in data insertion/removal.",
        "project": "Build a Singly Linked List App with add/delete/search."
    }
]


class ApplicationsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.filtered_data = APPLICATION_DATA.copy()
        self.build_ui()
        self.render_cards()

    def build_ui(self):
        ctk.CTkLabel(self, text="💡 Applications of C Programming", font=ctk.CTkFont(size=22, weight="bold"))\
            .pack(pady=(20, 10))

        self.category_filter = ctk.CTkOptionMenu(self, values=[
            "All", "Basics", "Control Flow", "Data Structures", "Memory", "Advanced"
        ], command=self.apply_filter)
        self.category_filter.pack(pady=(0, 20))
        self.category_filter.set("All")

        self.card_area = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.card_area.pack(fill="both", expand=True, padx=30, pady=10)

    def apply_filter(self, category):
        if category == "All":
            self.filtered_data = APPLICATION_DATA.copy()
        else:
            self.filtered_data = [item for item in APPLICATION_DATA if item["category"].strip() == category]
        self.render_cards()

    def get_theme_colors(self):
        mode = ctk.get_appearance_mode()
        return {
            "card_bg": "#1e1e1e" if mode == "Dark" else "#f2f2f2",
            "card_hover": "#2a2a2a" if mode == "Dark" else "#e0e0e0",
            "text": "white" if mode == "Dark" else "#222222",
            "project": "#89f089" if mode == "Dark" else "#228B22"
        }

    def render_cards(self):
        for widget in self.card_area.winfo_children():
            widget.destroy()

        colors = self.get_theme_colors()

        for item in self.filtered_data:
            card = ctk.CTkFrame(self.card_area, corner_radius=12, fg_color=colors["card_bg"])
            card.pack(padx=10, pady=10, fill="x")

            card.bind("<Enter>", lambda e, c=card: c.configure(fg_color=colors["card_hover"]))
            card.bind("<Leave>", lambda e, c=card: c.configure(fg_color=colors["card_bg"]))

            ctk.CTkLabel(card, text=item["title"], font=ctk.CTkFont(size=18, weight="bold"), anchor="w",
                         text_color=colors["text"]).pack(anchor="w", padx=20, pady=(10, 0))

            badge = ctk.CTkLabel(
                card, text=item["difficulty"],
                font=ctk.CTkFont(size=12),
                fg_color=self.get_badge_color(item["difficulty"]),
                text_color="black", corner_radius=6, padx=10
            )
            badge.pack(anchor="ne", padx=20, pady=(0, 5))

            for key in ["use", "why", "helpful"]:
                label = ctk.CTkLabel(card, text=f"{key.capitalize()}: {item[key]}", wraplength=1100,
                                     anchor="w", font=ctk.CTkFont(size=13), text_color=colors["text"])
                label.pack(anchor="w", padx=20, pady=2)

            ctk.CTkLabel(card, text=f"Project: {item['project']}", wraplength=1100,
                         anchor="w", text_color=colors["project"], font=ctk.CTkFont(size=13, weight="bold"))\
                .pack(anchor="w", padx=20, pady=(5, 10))

            ctk.CTkButton(card, text="Try in Compiler", width=140,
                          command=lambda: self.master.master.show_screen("Compiler"))\
                .pack(anchor="e", padx=20, pady=(0, 10))

    def get_badge_color(self, level):
        return {
            "Beginner": "#C3E88D",
            "Intermediate": "#FFCB6B",
            "Advanced": "#F78C6C"
        }.get(level, "gray")

    def refresh_theme(self):
        self.render_cards()