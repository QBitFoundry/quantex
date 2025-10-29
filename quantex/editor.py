from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt6.QtGui import QFont, QColor, QAction
from languages_style import PythonStyles
from languages_support.python import Python
import sys

class CodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__()

        # === Basic Editor Configuration ===
        self.setUtf8(True)
        self.setMarginLineNumbers(0, True)
        self.setMarginWidth(0, "00000000")
        self.setMarginsBackgroundColor(QColor("#3D3D3D"))
        self.setMarginsForegroundColor(QColor("#dedede"))
        self.setBraceMatching(QsciScintilla.BraceMatch.StrictBraceMatch)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#393939"))
        self.setCaretForegroundColor(QColor("#ffffff"))

        # === Set Editor EOL type to UNIX(To solve newlines issue in windows) ===
        self.setEolMode(QsciScintilla.EolMode.EolUnix)

        # === Variable that store file changes data ===
        self.file_changes = {}
        

        # === Font ===
        # font = QFont("Consolas", 12)
        # font = QFont("JetBrains Mono", 12)
        # font = QFont("Fira Code", 12)
        font = QFont("Cascadia Code", 12)
        # font = QFont("Ubuntu Mono", 12)
        # font = QFont("Monaspace", 12)

        self.setFont(font)
        self.setMarginsFont(font)

        # === Syntax Highlighting (Python) ===
        lexer = QsciLexerPython(self)
        PythonStyles(font, lexer).get_styles()
        self.setLexer(lexer)

        # === Autocomplete ===
        api = QsciAPIs(lexer)
        Python(api)

        api.prepare()
        lexer.setAPIs(api)

        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionFillupsEnabled(True)
        self.setAutoCompletionShowSingle(True)

        # === Initial Text ===
        # self.setText("# Custom Python Editor\n\ndef hello_world():\n    print('hello, world!')")
        self.setText("")

        # === Hover Explanations ===
        self.word_explanations = {
            "print": "Built-in function: Outputs text to console.",
            "range": "Built-in function: generates a sequence of numbers.",
            "len": "Built-in function: returns length of an object.",
        }

    def mouseMoveEvent(self, e):
        """Override mouseMoveEvent to handle hover over specific words."""
        # Get the word at the current mouse position
        word = self.wordAtPoint(e.pos())

        if word in self.word_explanations:
            # Show the tooltip if the word has an explanation
            position = self.positionFromLineIndex(e.pos().x(), e.pos().y())
            if position >= 0:
                self.SendScintilla(self.SCI_CALLTIPSHOW, position, (self.word_explanations[word]).encode("utf-8"))
        else:
            # Hide the tooltip if no explanation is found
            self.SendScintilla(self.SCI_CALLTIPCANCEL)

        super().mouseMoveEvent(e)

    
    def show_tooltip(self, pos, x, y):
        word = self.wordAtPoint(pos)
        if word in self.word_explanations:
            self.callTipShow(x, y, self.word_explanation[word])
    
    def hide_tooltip(self, pos, x, y):
        self.callTipCancel()

    def keyPressEvent(self, event):
        cursor_line, cursor_index = self.getCursorPosition()
        key = event.text()

        # Only track printable characters / deletes
        if key:
            if cursor_line not in self.file_changes:
                self.file_changes[cursor_line] = set()
            self.file_changes[cursor_line].add(cursor_index)
        super().keyPressEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quantex Code Editor")
        self.setGeometry(200, 100, 800, 600)

        # === Class Variables ===
        self.file_paths = []
        self.file_names = []
        self.active_file_index = None
        
        # === Menu Bar ===
        menubar = self.menuBar()
        file_menu = menubar.addMenu("&File")

        open_file_action = QAction("&Open File", self)
        open_file_action.setStatusTip("Opens a File")
        open_file_action.triggered.connect(self.open_file)
        
        open_folder_action = QAction("Open &Folder", self)
        open_folder_action.setStatusTip("Opens a Folder (Project)")
        # open_folder_action.triggered.connect(self.open_folder)

        safe_save_file_action = QAction("Safe Sa&ve", self)
        safe_save_file_action.setStatusTip("Save the current active file changes(recommended for ssd)")
        safe_save_file_action.triggered.connect(self.safe_save_file)
        
        save_file_action = QAction("&Save", self)
        save_file_action.setStatusTip("Save the current active file")
        save_file_action.triggered.connect(self.save_file)
        
        save_file_as_action = QAction("Save &As", self)
        save_file_as_action.setStatusTip("Save as the current active file")
        save_file_as_action.triggered.connect(self.save_as_file)

        save_all_action = QAction("Save Al&l", self)
        save_all_action.setStatusTip("Save all the files")

        exit_action = QAction('&Exit', self)
        exit_action.setStatusTip('Exit the application')
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_file_action)
        file_menu.addAction(open_folder_action)
        file_menu.addAction(safe_save_file_action)
        file_menu.addAction(save_file_action)
        file_menu.addAction(save_file_as_action)
        file_menu.addAction(save_all_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("&Edit")
        run_menu = menubar.addMenu("&Run")
        help_menu = menubar.addMenu("&Help")

        # === Editor ===
        self.editor = CodeEditor()
        self.setCentralWidget(self.editor)
    

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            "All Files (*);;Text Files (*.txt);;Python Files (*.py)"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    # code = file.read()
                    self.editor.setText(file.read())
                self.file_paths.append(file_path)
            except:
                print("Fail to open!")
    
    def safe_save_file(self):
        if len(self.file_paths) == 0:
            self.save_as_file()
        else:
            file_path = self.file_paths[0]

            # Build initial byte offset table
            self.line_offsets = {}
            offset = 0
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
            for i, line in enumerate(lines):
                self.line_offsets[i] = offset
                offset += len(line.encode("utf-8"))
            
            if file_path:
                try:
                    with open(file_path, "r+", encoding="utf-8") as file:
                        for line_num in self.editor.file_changes:
                            code_line = self.editor.text(line_num)
                            byte_offset = self.line_offsets[line_num]
                            file.seek(byte_offset)
                            file.write(code_line)

                except:
                    print("Fail to save!")

    def save_file(self):
        if len(self.file_paths) == 0:
            self.save_as_file()
        else:
            file_path = self.file_paths[0]
            
            if file_path:
                try:
                    code = self.editor.text()
                    with open(file_path, "w", encoding="utf-8", newline='\n') as file:
                        file.write(code)

                except:
                    print("Fail to save!")
    
    def save_as_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File As",
            "untitled.txt"
            "",
            "All Files (*)"
        )
        if file_path:
            try:
                code = self.editor.text()
                with open(file_path, "w", encoding="utf-8", newline='\n') as file:
                    file.write(code)
            except:
                print("Fail to save as!")
    
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
