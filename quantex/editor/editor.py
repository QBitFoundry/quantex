from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QLabel, QHBoxLayout, QStatusBar
from PyQt6.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt6.QtGui import QFont, QColor, QAction, QPixmap
from PyQt6.QtCore import Qt
from editor.languages_style import PythonStyles
from languages_support.python import Python
import sys

# from language_server.client import Client
from editor.theme import get_theme

class CodeEditor(QsciScintilla):
    def __init__(self):
        super().__init__()
        # self.lsp_client = lsp_client

        # === Basic Editor Configuration ===
        self.setUtf8(True)
        self.setMarginLineNumbers(0, True)
        
        theme_data = get_theme()
        self.set_config(theme_data)

        # Set the scroll to active only when text overflow horizontally.
        self.setScrollWidthTracking(True)
        self.setScrollWidth(1)

        # === Set Editor EOL type to UNIX(To solve newlines issue in windows) ===
        self.setEolMode(QsciScintilla.EolMode.EolUnix)

        # === Variable that store file changes data ===
        self.file_changes = {}

        # # === Syntax Highlighting (Python) ===
        # lexer = QsciLexerPython(self)
        # PythonStyles(font, lexer).get_styles()
        # self.setLexer(lexer)

        # # === Autocomplete ===
        # api = QsciAPIs(lexer)
        # Python(api)

        # Language server on text change
        self.textChanged.connect(self.on_text_change)

        # api.prepare()
        # lexer.setAPIs(api)

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

        # === Horizontal scroll reset ===
        def on_line_updated():
            self.setScrollWidth(1)
            
        self.SCN_MODIFIED.connect(on_line_updated)

        # === Line number width responsive ===
        def on_line_num_changed():
            margin_width = str(max(1, self.lines()))
            self.setMarginWidth(0, f'0${margin_width}')
        on_line_num_changed() # sets the line number correct spacing when editor is opened.
        self.linesChanged.connect(on_line_num_changed)

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
    

    def on_text_change(self):
        
        text_changed = self.text() or ""
    
    
    def set_config(self, theme_data):
        self.setMarginsBackgroundColor(theme_data["marginBgColor"])
        self.setMarginsForegroundColor(theme_data["marginFgColor"])
        
        if theme_data["braceMatching"]["active"]:
            if theme_data["braceMatching"]["type"] == "Strict":
                self.setBraceMatching(QsciScintilla.BraceMatch.StrictBraceMatch)
            elif theme_data["braceMatching"]["type"] == "Sloppy":
                self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
            else:
                self.setBraceMatching(QsciScintilla.BraceMatch.NoBraceMatch)

            self.setMatchedBraceBackgroundColor(theme_data["braceMatching"]["matched"]["bgColor"])
            self.setMatchedBraceForegroundColor(theme_data["braceMatching"]["matched"]["fgColor"])
            self.setUnmatchedBraceBackgroundColor(theme_data["braceMatching"]["unmatched"]["bgColor"])
            self.setUnmatchedBraceForegroundColor(theme_data["braceMatching"]["unmatched"]["fgColor"])
        
        self.setCaretLineVisible(theme_data["caretLine"]["visible"])
        self.setCaretLineBackgroundColor(theme_data["caretLine"]["bgColor"])
        self.setCaretForegroundColor(theme_data["caretLine"]["fgColor"])

        # === Font ===
        font = QFont(theme_data["font"]["family"], theme_data["font"]["size"])

        self.setFont(font)
        self.setMarginsFont(font)

        # === Syntax Highlighting (Python) ===
        lexer = QsciLexerPython(self)
        PythonStyles(font, lexer).get_styles()
        self.setLexer(lexer)

        # === Autocomplete ===
        api = QsciAPIs(lexer)
        Python(api)

        # Language server on text change
        # self.textChanged.connect(self.on_text_change)

        # api.prepare()
        # lexer.setAPIs(api)
