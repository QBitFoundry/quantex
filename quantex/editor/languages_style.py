from PyQt6.Qsci import QsciLexerPython
from PyQt6.QtGui import QColor

class PythonStyles:
        
    def __init__(self, font, lexer):
        self.font = font
        self.lexer = lexer


    def get_styles(self):
        # === Syntax Highlighting (Python) ===
        self.lexer.setFont(self.font)
        self.lexer.setDefaultFont(self.font)
        # self.lexer.setPaper(QColor("#1b1b1b"))
        self.lexer.setColor(QColor("#FFD700"), QsciLexerPython.Keyword)
        self.lexer.setColor(QColor("#808080"), QsciLexerPython.Comment)
        self.lexer.setColor(QColor("#237FFF"), QsciLexerPython.FunctionMethodName)
        self.lexer.setColor(QColor("#FF8D23"), QsciLexerPython.ClassName)
        self.lexer.setColor(QColor("#2F9400"), QsciLexerPython.TripleDoubleQuotedString)
        self.lexer.setColor(QColor("#2F9400"), QsciLexerPython.TripleDoubleQuotedFString)
        self.lexer.setColor(QColor("#42D000"), QsciLexerPython.DoubleQuotedFString)
        self.lexer.setColor(QColor("#42D000"), QsciLexerPython.DoubleQuotedString)
        self.lexer.setColor(QColor("#42D000"), QsciLexerPython.SingleQuotedFString)
        self.lexer.setColor(QColor("#42D000"), QsciLexerPython.SingleQuotedString)
        self.lexer.setColor(QColor("#D04500"), QsciLexerPython.Number)
        return self.lexer
