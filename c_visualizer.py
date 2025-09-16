# C Code Visualizer Application
import tkinter as tk
from tkinter import scrolledtext, messagebox
import json

class VisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("C Code Visualizer")
        self.original_code = ""

        # Load example codes
        try:
            with open("c_code_examples_extended.json", "r") as f:
                self.examples = json.load(f)
        except FileNotFoundError:
            self.examples = []
            messagebox.showwarning("Warning", "c_code_examples_extended.json not found")

        # GUI Components
        tk.Label(root, text="Select Example or Enter C Code:").pack()
        self.example_var = tk.StringVar()
        self.example_menu = tk.OptionMenu(root, self.example_var, *[ex["title"] for ex in self.examples], command=self.load_example)
        self.example_menu.pack()
        self.code_text = scrolledtext.ScrolledText(root, height=10, width=80)
        self.code_text.pack()

        tk.Label(root, text="Enter Input Values (one per line):").pack()
        self.input_text = scrolledtext.ScrolledText(root, height=3, width=80)
        self.input_text.pack()

        tk.Label(root, text="Code Visualization").pack()
        self.display_panel = scrolledtext.ScrolledText(root, height=20, width=80)
        self.display_panel.pack()

        # Control Buttons
        tk.Button(root, text="Run", command=self.run).pack()
        tk.Button(root, text="Step Forward", command=self.step_forward).pack(side=tk.LEFT)
        tk.Button(root, text="Step Backward", command=self.step_backward).pack(side=tk.LEFT)
        tk.Button(root, text="Play", command=self.play).pack(side=tk.LEFT)
        tk.Button(root, text="Pause", command=self.pause).pack(side=tk.LEFT)

    def load_example(self, *args):
        selected = self.example_var.get()
        for example in self.examples:
            if example["title"] == selected:
                self.code_text.delete("1.0", tk.END)
                self.code_text.insert(tk.END, example["code"])
                self.display_panel.delete("1.0", tk.END)
                self.display_panel.insert(tk.END, example["code"])
                self.original_code = example["code"]
                break

    def run(self):
        self.original_code = self.code_text.get("1.0", tk.END).strip()
        self.display_panel.delete("1.0", tk.END)
        self.display_panel.insert(tk.END, self.original_code)

    def step_forward(self):
        pass  # Placeholder for Phase 2

    def step_backward(self):
        pass  # Placeholder for Phase 2

    def play(self):
        pass  # Placeholder for Phase 3

    def pause(self):
        pass  # Placeholder for Phase 3

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualizerApp(root)
    root.mainloop()
