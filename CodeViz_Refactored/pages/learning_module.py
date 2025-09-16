import customtkinter as ctk
from tkinter import Text, Scrollbar, RIGHT, Y, LEFT, BOTH
from pygments import lex
from pygments.lexers import CLexer
from pygments.token import Token
import json
import os 
from tkinter import messagebox

# Tooltips dictionary for C keywords
TOOLTIP_KEYWORDS = {
    # 🟩 Data Types
    "int": "Defines an integer variable.",
    "float": "Defines a floating-point variable.",
    "double": "Defines a double-precision floating-point variable.",
    "char": "Defines a character variable.",
    "void": "Specifies that a function returns no value.",

    # 🔁 Control Structures
    "for": "Loop that repeats a block a fixed number of times.",
    "while": "Loop that runs as long as a condition is true.",
    "do": "Used with while to create a do-while loop.",
    "if": "Executes a block if a condition is true.",
    "else": "Executes when the if condition is false.",
    "switch": "Selects one of many code blocks to execute.",
    "case": "Defines a block inside a switch.",
    "break": "Exits the current loop or switch block.",
    "continue": "Skips the rest of the loop and starts the next iteration.",
    "goto": "Jumps to a labeled statement (use with caution).",
    "default": "Executed when no case in switch matches.",

    # 📦 Operators & Storage
    "sizeof": "Returns the size of a data type or variable.",
    "static": "Preserves variable value between function calls.",
    "const": "Defines a variable whose value cannot be changed.",
    "extern": "Declares a variable or function defined elsewhere.",
    "register": "Suggests variable be stored in CPU register.",
    "volatile": "Tells compiler variable may be changed externally.",

    # 🔣 Standard Library Functions
    "scanf": "Reads input from the user.",
    "printf": "Prints output to the console.",
    "gets": "Reads a line from stdin (unsafe, avoid).",
    "puts": "Writes a string to stdout.",
    "strlen": "Returns the length of a string.",
    "strcpy": "Copies one string into another.",
    "strcat": "Concatenates two strings.",
    "strcmp": "Compares two strings.",
    "fopen": "Opens a file.",
    "fclose": "Closes an open file.",
    "fgets": "Reads a line from a file.",
    "fputs": "Writes a string to a file.",
    "fprintf": "Writes formatted output to a file.",
    "fscanf": "Reads formatted input from a file.",
    "malloc": "Allocates memory dynamically.",
    "calloc": "Allocates memory and initializes to zero.",
    "realloc": "Resizes previously allocated memory.",
    "free": "Frees dynamically allocated memory.",
    "exit": "Terminates the program.",

    # 🎯 Function & Program Structure
    "main": "The entry point of a C program.",
    "return": "Exits a function and optionally returns a value.",
    "include": "Includes a header file.",
    "define": "Defines macros or constants.",
    "typedef": "Defines a new data type name.",
    "struct": "Groups variables of different types.",
    "enum": "Defines a set of named integer constants.",
    "union": "Defines variables sharing the same memory location.",

    # 📊 Math & Misc
    "abs": "Returns absolute value.",
    "pow": "Raises a number to a power.",
    "sqrt": "Returns square root.",
    "rand": "Returns a random number.",
    "time": "Returns current time.",
}


class LearningModulePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent )

        self.code_panel = None
        self.line_numbers = None
        self.output_sidebar = None
        self.examples = self.load_examples()

        self.build_ui()
        self.populate_examples()

    def build_ui(self):
        # Header
        ctk.CTkLabel(self, text="Learning Module", font=ctk.CTkFont(size=22, weight="bold"), anchor="w").pack(pady=(20, 10), padx=20, anchor="w")


        # Layout: left (editor), right (examples)
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Editor Frame
        editor_frame = ctk.CTkFrame(body_frame, fg_color="#1e1e1e")
        editor_frame.pack(side=LEFT, fill="both", expand=True, padx=(0, 10))

        self.line_numbers = Text(editor_frame, width=4, padx=4, font=("JetBrains Mono", 14),
                                 bg="#2c2c2c", fg="#888", bd=0, state="disabled")
        self.line_numbers.pack(side=LEFT, fill=Y)

        self.code_panel = Text(editor_frame, font=("JetBrains Mono", 14), bg="#1e1e1e", fg="white",
                               insertbackground="white", bd=0, wrap="none")
        self.code_panel.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(editor_frame, command=lambda *args: (
            self.code_panel.yview(*args), self.line_numbers.yview(*args)))
        scrollbar.pack(side=RIGHT, fill=Y)
        self.code_panel.config(yscrollcommand=scrollbar.set)
        self.line_numbers.config(yscrollcommand=scrollbar.set)

        # Output Sidebar for buttons
        self.output_sidebar = ctk.CTkScrollableFrame(body_frame, width=300, label_text="Syntax Examples")
        self.output_sidebar.pack(side=RIGHT, fill="y", padx=(10, 0))

    def populate_examples(self):
        for example in self.examples:
            btn = ctk.CTkButton(
                self.output_sidebar,
                text=example.get("title", "Untitled"),
                command=lambda ex=example: self.load_code(ex["code"])
            )
            btn.pack(pady=5, padx=10, anchor="w")

    def load_examples(self):
        # Safely resolve JSON path relative to this file
        json_path = os.path.join(os.path.dirname(__file__), "..", "assets", "c_code_examples_extended.json")
        json_path = os.path.abspath(json_path)

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading examples: {e}")
            return [{
                "title": "Hello World",
                "code": "#include <stdio.h>\nint main() {\n    printf(\"Hello, World!\");\n    return 0;\n}"
            }]

    def load_code(self, code_text):
        self.code_panel.configure(state="normal")
        self.code_panel.delete("1.0", "end")
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")

        self.code_panel.insert("1.0", code_text)

        lines = code_text.split("\n")
        for i in range(1, len(lines) + 1):
            self.line_numbers.insert("end", f"{i}\n")

        self.define_tags()

        start_index = 0
        for token_type, token_str in lex(code_text, CLexer()):
            if token_str == "\n":
                start_index += 1
                continue
            pos = f"1.0+{start_index}c"
            end_pos = f"1.0+{start_index + len(token_str)}c"
            tag_name = str(token_type)
            if tag_name.startswith("Token"):
                self.code_panel.tag_add(tag_name, pos, end_pos)
            start_index += len(token_str)

        self.code_panel.configure(state="disabled")
        self.line_numbers.configure(state="disabled")

    def define_tags(self):
        self.code_panel.tag_configure("Token.Keyword", foreground="#82AAFF")
        self.code_panel.tag_configure("Token.Name.Builtin", foreground="#FFCB6B")
        self.code_panel.tag_configure("Token.Literal.String", foreground="#C3E88D")
        self.code_panel.tag_configure("Token.Comment", foreground="#546E7A")
        self.code_panel.tag_configure("Token.Name.Function", foreground="#F78C6C")
        self.code_panel.tag_configure("Token.Operator", foreground="#89DDFF")
        self.code_panel.tag_configure("Token.Punctuation", foreground="#D0D0D0")
        self.code_panel.tag_configure("Token.Literal.Number", foreground="#F78C6C")
        self.code_panel.tag_configure("Token.Text", foreground="#ECEFF1")

