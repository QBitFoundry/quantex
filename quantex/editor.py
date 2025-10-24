from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt6.QtGui import QFont, QColor
from languages_style import PythonStyles
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
        lexer = PythonStyles(font).get_styles()
        # lexer = PythonStyles().get()
        self.setLexer(lexer)

        # === Autocomplete ===
        api = QsciAPIs(lexer)
        api.add("print")
        api.add("range")
        api.add("len")
        api.add("sum")
        api.add("hello_world") # custom suggestion
        api.prepare()

        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionThreshold(1)

        # === Initial Text ===
        self.setText("# Custom Python Editor\n\ndef hello_world():\n    print('hello, world!')")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quantex Code Editor")
        self.setGeometry(200, 100, 800, 600)
        self.editor = CodeEditor()
        self.setCentralWidget(self.editor)
    
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
