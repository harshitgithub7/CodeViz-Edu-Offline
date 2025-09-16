import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QTextEdit, QToolBar, QAction, QFileDialog, QComboBox, QInputDialog
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, QSize
import subprocess
import re
import uuid


class MultiLanguageHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, language="C"):
        super().__init__(parent)
        self.language = language
        self.highlighting_rules = []

        # Define formats
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))
        keyword_format.setFontWeight(QFont.Bold)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))

        # Language-specific keywords
        language_keywords = {
            "C": ['int', 'return', 'void', 'if', 'else', 'while', 'for', 'char', 'float', 'double', 'struct'],
            "C++": ['int', 'return', 'void', 'if', 'else', 'while', 'for', 'char', 'float', 'double', 'class', 'public', 'private', 'namespace', 'using'],
            "Python": ['def', 'return', 'if', 'else', 'elif', 'while', 'for', 'class', 'import', 'from', 'as'],
            "Java": ['public', 'private', 'class', 'static', 'void', 'int', 'double', 'if', 'else', 'while', 'for', 'return']
        }

            # Language-specific patterns
        if language in language_keywords:
            for word in language_keywords[language]:
                pattern = r'\b' + word + r'\b'
                self.highlighting_rules.append((re.compile(pattern), keyword_format))

        # Comments (single-line and multi-line)
        if language in ["C", "C++", "Java"]:
            self.highlighting_rules.append((re.compile(r'//.*'), comment_format))
            self.highlighting_rules.append((re.compile(r'/\*[\s\S]*?\*/'), comment_format))
        elif language == "Python":
            self.highlighting_rules.append((re.compile(r'#.*'), comment_format))

        # Strings
        self.highlighting_rules.append((re.compile(r'"[^"]*"'), string_format))
        self.highlighting_rules.append((re.compile(r"'[^']*'"), string_format))

        # Numbers
        self.highlighting_rules.append((re.compile(r'\b[0-9]+\b'), number_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in pattern.finditer(text):
                start, end = match.start(), match.end()
                self.setFormat(start, end - start, format)

class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Language Code Editor")
        self.setGeometry(100, 100, 1200, 800)
        self.current_language = "C"
        self.temp_file_name = str(uuid.uuid4())
        # Use absolute path based on script location
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Output")

        # Create Output directory structure for all languages at startup
        for lang in ["C", "C++", "Python", "Java"]:
            lang_path = os.path.join(self.output_dir, lang)
            try:
                os.makedirs(lang_path, exist_ok=True)
                print(f"Created/Verified folder: {lang_path}")
            except PermissionError:
                print(f"Permission denied creating folder: {lang_path}")
            except Exception as e:
                print(f"Error creating folder {lang_path}: {e}")

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Toolbar 
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Function to tint icons
        def tint_icon(icon, color):
            pixmap = icon.pixmap(QSize(24, 24))
            image = pixmap.toImage()
            for x in range(image.width()):
                for y in range(image.height()):
                    if image.pixelColor(x, y).alpha() > 0:  # Only tint non-transparent pixels
                        image.setPixelColor(x, y, QColor(color))
            return QIcon(QPixmap.fromImage(image))

        # Toolbar actions with elegantly colored icons and visible text
        open_action = QAction(tint_icon(QIcon.fromTheme("document-open"), "#56B6C2"), "Open File", self)  # Cyan
        open_action.setToolTip("Open File (Ctrl+O)")
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        save_action = QAction(tint_icon(QIcon.fromTheme("document-save"), "#E5C07B"), "Save File", self)  # Gold
        save_action.setToolTip("Save File (Ctrl+S)")
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        compile_action = QAction(tint_icon(QIcon.fromTheme("system-run"), "#61AFEF"), "Compile", self)  # Blue
        compile_action.setToolTip("Compile Code (F5)")
        compile_action.triggered.connect(self.compile_code)
        toolbar.addAction(compile_action)

        run_action = QAction(tint_icon(QIcon.fromTheme("media-playback-start"), "#98C379"), "Run", self)  # Green
        run_action.setToolTip("Run Code (Ctrl+F5)")
        run_action.triggered.connect(self.run_code)
        self.run_action = run_action
        toolbar.addAction(run_action)

        # Language selector
        self.language_combo = QComboBox()
        self.language_combo.addItems(["C", "C++", "Python", "Java"])
        self.language_combo.currentTextChanged.connect(self.change_language)
        toolbar.addWidget(self.language_combo)

        # Apply toolbar and combo box styles with visible text
        toolbar.setStyleSheet("""
            QToolBar { 
                background-color: #1E1E1E; 
                border: none;
                padding: 5px;
                spacing: 10px;
            }
            QToolButton {
                color: #D4D4D4; /* Visible text color for fallback */
                background-color: transparent;
                border: none;
                padding: 2px 8px;
            }
            QToolButton:hover {
                background-color: #3C3C3C;
                border-radius: 4px;
            }
            QComboBox {
                background-color: #2D2D2D;
                color: #D4D4D4;
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 5px;
                font-family: 'Segoe UI';
                font-size: 12px;
            }
            QComboBox:hover {
                background-color: #3C3C3C;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)

        # Editor area
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Fira Code", 12))
        layout.addWidget(self.editor)

        # Apply syntax highlighter
        self.highlighter = MultiLanguageHighlighter(self.editor.document(), self.current_language)

        # Output display
        self.output = QTextEdit()
        self.output.setFont(QFont("Fira Code", 12))
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        # Status bar with line counter
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #1E1E1E;
                color: #D4D4D4;
                font-family: 'Segoe UI';
                font-size: 12px;
                border-top: 1px solid #3C3C3C;
            }
        """)
        self.statusBar().showMessage("Ready | Line: 1 | Total Lines: 0")

        # Initialize variables
        self.executable = None
        self.current_file = None
        self.run_action.setEnabled(False)

        # Connect editor signals for line counter
        self.editor.cursorPositionChanged.connect(self.update_line_counter)
        self.editor.textChanged.connect(self.update_line_counter)
        self.update_line_counter()

        #Ddark theme
        self.setStyleSheet("""
            QMainWindow { 
                background-color: #1E1E1E; 
                border: none;
            }
            QPlainTextEdit { 
                background-color: #252526; 
                color: #D4D4D4; 
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Fira Code';
                font-size: 12px;
            }
            QTextEdit { 
                background-color: #252526; 
                color: #D4D4D4; 
                border: 1px solid #3C3C3C;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Fira Code';
                font-size: 12px;
            }
        """)

    def update_line_counter(self):
        cursor = self.editor.textCursor()
        current_line = cursor.blockNumber() + 1
        total_lines = self.editor.document().blockCount()
        self.statusBar().showMessage(f"Ready | Line: {current_line} | Total Lines: {total_lines}")

    def change_language(self, language):
        self.current_language = language
        self.highlighter = MultiLanguageHighlighter(self.editor.document(), self.current_language)
        self.editor.document().setDocumentMargin(10)
        lang_path = os.path.join(self.output_dir, self.current_language)
        try:
            os.makedirs(lang_path, exist_ok=True)
            print(f"Verified/Created folder for {self.current_language}: {lang_path}")
        except PermissionError:
            print(f"Permission denied creating folder for {self.current_language}: {lang_path}")
        except Exception as e:
            print(f"Error creating folder for {self.current_language}: {e}")
        self.update_line_counter()
        self.statusBar().showMessage(f"Language changed to {language} | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")

    def open_file(self):
        file_extensions = {
            "C": "C Files (*.c);;All Files (*)",
            "C++": "C++ Files (*.cpp *.cxx *.cc);;All Files (*)",
            "Python": "Python Files (*.py);;All Files (*)",
            "Java": "Java Files (*.java);;All Files (*)"
        }
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", file_extensions[self.current_language])
        if file_name:
            try:
                with open(file_name, "r") as f:
                    self.editor.setPlainText(f.read())
                self.current_file = file_name
                self.update_line_counter()
                self.statusBar().showMessage(f"Opened {file_name} | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")
            except Exception as e:
                self.output.setText(f"Failed to open file: {str(e)}")

    def save_file(self):
        if not self.current_file:
            file_extensions = {
                "C": ".c",
                "C++": ".cpp",
                "Python": ".py",
                "Java": ".java"
            }
            file_ext = file_extensions[self.current_language]
            file_name, ok = QInputDialog.getText(self, "Save File", f"Enter filename (will be saved as .{file_ext}):")
            if ok and file_name:
                save_path = os.path.join(self.output_dir, self.current_language, f"{file_name}{file_ext}")
                try:
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    with open(save_path, "w") as f:
                        f.write(self.editor.toPlainText())
                    self.current_file = save_path
                    self.update_line_counter()
                    self.statusBar().showMessage(f"Saved {save_path} | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")
                except Exception as e:
                    self.output.setText(f"Failed to save file: {str(e)}")
        else:
            try:
                with open(self.current_file, "w") as f:
                    f.write(self.editor.toPlainText())
                self.update_line_counter()
                self.statusBar().showMessage(f"Saved {self.current_file} | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")
            except Exception as e:
                self.output.setText(f"Failed to save file: {str(e)}")

    def compile_code(self):
        code = self.editor.toPlainText()
        if not code.strip():
            self.output.setText("Error: No code to compile.")
            return

        # Create language-specific folder
        lang_path = os.path.join(self.output_dir, self.current_language)
        try:
            os.makedirs(lang_path, exist_ok=True)
            print(f"Verified/Created folder for compilation: {lang_path}")
        except PermissionError:
            self.output.setText(f"Permission denied creating folder: {lang_path}")
            return
        except Exception as e:
            self.output.setText(f"Error creating folder: {e}")
            return

        ext = {"C": ".c", "C++": ".cpp", "Python": ".py", "Java": ".java"}
        temp_file = os.path.join(lang_path, f"{self.temp_file_name}{ext[self.current_language]}")
        with open(temp_file, "w") as f:
            f.write(code)

        try:
            if self.current_language == "C":
                compiler_cmd = ["gcc", "-o", os.path.join(lang_path, self.temp_file_name), temp_file]
                result = subprocess.run(compiler_cmd, capture_output=True, text=True)
                self.executable = os.path.join(lang_path, self.temp_file_name) if sys.platform != "win32" else os.path.join(lang_path, f"{self.temp_file_name}.exe")
            elif self.current_language == "C++":
                compiler_cmd = ["g++", "-o", os.path.join(lang_path, self.temp_file_name), temp_file]
                result = subprocess.run(compiler_cmd, capture_output=True, text=True)
                self.executable = os.path.join(lang_path, self.temp_file_name) if sys.platform != "win32" else os.path.join(lang_path, f"{self.temp_file_name}.exe")
            elif self.current_language == "Python":
                self.executable = ["python", temp_file]
                result = subprocess.run(["python", "--version"], capture_output=True, text=True)
                if result.returncode != 0:
                    raise FileNotFoundError("Python not found")
            elif self.current_language == "Java":
                compiler_cmd = ["javac", temp_file]
                result = subprocess.run(compiler_cmd, capture_output=True, text=True)
                self.executable = ["java", "-cp", lang_path, os.path.splitext(os.path.basename(temp_file))[0]]

            if self.current_language != "Python" and result.returncode == 0:
                self.output.setHtml('<span style="color: #98C379;">Compilation successful!</span>')
                self.run_action.setEnabled(True)
                self.statusBar().showMessage(f"Compilation successful | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")
            elif self.current_language == "Python":
                self.output.setHtml('<span style="color: #98C379;">Python ready to run!</span>')
                self.run_action.setEnabled(True)
                self.statusBar().showMessage(f"Python ready | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")
            else:
                self.output.setHtml(f'<span style="color: #D16969;">Compilation failed:</span><br>{result.stderr}')
                self.run_action.setEnabled(False)
                self.statusBar().showMessage(f"Compilation failed | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")
        except FileNotFoundError as e:
            self.output.setHtml(f'<span style="color: #D16969;">Compilation failed: {str(e)}. Please install the required compiler.</span>')
            self.run_action.setEnabled(False)
            self.statusBar().showMessage(f"Compiler not found | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")
        except Exception as e:
            self.output.setHtml(f'<span style="color: #D16969;">Compilation failed: {str(e)}</span>')
            self.run_action.setEnabled(False)
            self.statusBar().showMessage(f"Compilation error | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")

    def run_code(self):
        if self.executable:
            try:
                result = subprocess.run(self.executable, capture_output=True, text=True, cwd=os.path.join(self.output_dir, self.current_language))
                output_text = (result.stdout or "") + (result.stderr or "")
                if not output_text:
                    output_text = "No output"
                self.output.setHtml(f'<pre style="color: #D4D4D4;">{output_text}</pre>')
                self.statusBar().showMessage(f"Program executed | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")
            except Exception as e:
                self.output.setHtml(f'<pre style="color: #D16969;">Execution failed: {str(e)}</pre>')
                self.statusBar().showMessage(f"Execution error | Line: {self.editor.textCursor().blockNumber() + 1} | Total Lines: {self.editor.document().blockCount()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CodeEditor()
    window.show()
    sys.exit(app.exec_())


