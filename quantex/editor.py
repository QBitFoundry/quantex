from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt6.QtGui import QFont, QColor
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
