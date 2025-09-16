import customtkinter as ctk
from tkinter import Text, filedialog
import subprocess
from pygments import lex
from pygments.lexers import CLexer
 
TOOLTIP_KEYWORDS = {
    "int": "Defines an integer variable or function return type.",
    "float": "Defines a floating-point variable or function return type.",
    "double": "Defines a double-precision floating-point variable or function return type.",
    "char": "Defines a character variable or function return type.",
    "void": "Specifies that a function does not return a value.",
    "return": "Exits a function and optionally returns a value.",
    "if": "Conditional statement for branching logic.",
    "else": "Alternative branch for an if statement.",
    "for": "Looping construct for iterating a set number of times.",
    "while": "Looping construct for repeating while a condition is true.",
    "do": "Used with while to create a do-while loop.",
    "switch": "Multi-way branch statement.",
    "case": "Defines a branch in a switch statement.",
    "break": "Exits from a loop or switch statement.",
    "continue": "Skips to the next iteration of a loop.",
    "struct": "Defines a structure type.",
    "typedef": "Creates a new type name (alias).",
    "const": "Declares a variable as constant (read-only).",
    "static": "Declares a variable with static storage duration.",
    "extern": "Declares a variable or function defined elsewhere.",
    "sizeof": "Returns the size of a variable or type.",
    "enum": "Defines an enumeration type.",
    "union": "Defines a union type.",
    "unsigned": "Specifies an unsigned integer type.",
    "signed": "Specifies a signed integer type.",
    "long": "Specifies a long integer type.",
    "short": "Specifies a short integer type.",
    "goto": "Jumps to a labeled statement.",
    "default": "Default branch in a switch statement.",
    "volatile": "Prevents compiler optimization of a variable.",
    "register": "Suggests storing a variable in a CPU register.",
    "auto": "Default storage class for local variables.",
    "inline": "Suggests inlining a function."
}


def get_compiler_frame(parent):
    frame = ctk.CTkFrame(parent, corner_radius=10)
    frame.pack_propagate(False)

    editor = Text(frame, height=20, width=80, font=("Consolas", 14),
                  bg="#1e1e1e", fg="white", insertbackground="white", wrap="none", borderwidth=0)
    editor.pack(fill="both", expand=True, padx=20, pady=(20, 10))

    tooltip_label = ctk.CTkLabel(frame, text="", fg_color="#2f2f2f", text_color="white",
                                 font=("Consolas", 12), corner_radius=6, padx=6, pady=2)
    tooltip_label.place_forget()

    output = ctk.CTkTextbox(frame, height=120, fg_color="#0f0f0f", text_color="lightgreen",
                            font=("Consolas", 13))
    output.pack(fill="x", padx=20, pady=(0, 10))
    output.configure(state="disabled")

    button_row = ctk.CTkFrame(frame, fg_color="transparent")
    button_row.pack(pady=5)

    def run_code():
        code = editor.get("1.0", "end-1c")
        with open("temp.c", "w", encoding="utf-8") as f:
            f.write(code)

        try:
            compile_result = subprocess.run(["gcc", "temp.c", "-o", "temp.exe"], capture_output=True, text=True)
            output.configure(state="normal")
            output.delete("1.0", "end")

            if compile_result.returncode != 0:
                output.insert("1.0", compile_result.stderr)
            else:
                run_result = subprocess.run(["temp.exe"], capture_output=True, text=True)
                output.insert("1.0", run_result.stdout)

        except Exception as e:
            output.configure(state="normal")
            output.insert("1.0", str(e))

        output.configure(state="disabled")

    def clear_all():
        editor.delete("1.0", "end")
        output.configure(state="normal")
        output.delete("1.0", "end")
        output.configure(state="disabled")

    def save_to_file():
        code = editor.get("1.0", "end-1c")
        filepath = filedialog.asksaveasfilename(defaultextension=".c", filetypes=[("C files", "*.c")])
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)

    def open_from_file():
        filepath = filedialog.askopenfilename(defaultextension=".c", filetypes=[("C files", "*.c")])
        if filepath:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
            editor.delete("1.0", "end")
            editor.insert("1.0", code)
            highlight_code()

     

    ctk.CTkButton(button_row, text="Run", command=run_code).pack(side="left", padx=10)
    ctk.CTkButton(button_row, text="Clear", command=clear_all).pack(side="left", padx=10)
    ctk.CTkButton(button_row, text="Save", command=save_to_file).pack(side="left", padx=10)
    ctk.CTkButton(button_row, text="Open", command=open_from_file).pack(side="left", padx=10)

    def highlight_code(event=None):
        code = editor.get("1.0", "end-1c")
        for tag in editor.tag_names():
            if tag != "sel":
                editor.tag_delete(tag)

        start_index = 0
        for token_type, token_str in lex(code, CLexer()):
            if token_str == "\n":
                start_index += 1
                continue

            start = f"1.0+{start_index}c"
            end = f"1.0+{start_index + len(token_str)}c"
            tag_name = str(token_type)
            editor.tag_add(tag_name, start, end)

            if tag_name == "Token.Keyword":
                editor.tag_config(tag_name, foreground="#82AAFF")
            elif tag_name == "Token.Literal.String":
                editor.tag_config(tag_name, foreground="#C3E88D")
            elif tag_name == "Token.Comment":
                editor.tag_config(tag_name, foreground="#546E7A")
            elif tag_name == "Token.Name.Function":
                editor.tag_config(tag_name, foreground="#F78C6C")
            elif tag_name == "Token.Operator":
                editor.tag_config(tag_name, foreground="#89DDFF")
            elif tag_name == "Token.Literal.Number":
                editor.tag_config(tag_name, foreground="#F78C6C")
            else:
                editor.tag_config(tag_name, foreground="#ECEFF1")

            if token_str in TOOLTIP_KEYWORDS:
                tooltip_tag = f"tooltip_{token_str}_{start_index}"
                editor.tag_add(tooltip_tag, start, end)

                def on_enter(e, word=token_str, pos=start):
                    tooltip_label.configure(text=TOOLTIP_KEYWORDS[word])
                    bbox = editor.bbox(pos)
                    if bbox:
                        x, y, width, height = bbox
                        tooltip_label.place(x=x + width + 15, y=y-10)

                def on_leave(e):
                    tooltip_label.place_forget()

                editor.tag_bind(tooltip_tag, "<Enter>", on_enter)
                editor.tag_bind(tooltip_tag, "<Leave>", on_leave)

            start_index += len(token_str)

    editor.bind("<KeyRelease>", highlight_code)

    editor.insert("1.0", """#include <stdio.h>\n\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}\n""")
    highlight_code()
    return frame
