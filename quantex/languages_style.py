from PyQt6.Qsci import QsciLexerPython
from PyQt6.QtGui import QFont, QColor

class PythonStyles:
        
    def __init__(self, font):
        self.font = font


    def get_styles(self):
        # === Syntax Highlighting (Python) ===
        lexer = QsciLexerPython()
        lexer.setFont(self.font)
        lexer.setDefaultFont(self.font)
        # self.lexer.setPaper(QColor("#1b1b1b"))
        lexer.setColor(QColor("#FFD700"), QsciLexerPython.Keyword)
        lexer.setColor(QColor("#808080"), QsciLexerPython.Comment)
        lexer.setColor(QColor("#237FFF"), QsciLexerPython.FunctionMethodName)
        lexer.setColor(QColor("#FF8D23"), QsciLexerPython.ClassName)
        lexer.setColor(QColor("#2F9400"), QsciLexerPython.TripleDoubleQuotedString)
        lexer.setColor(QColor("#2F9400"), QsciLexerPython.TripleDoubleQuotedFString)
        lexer.setColor(QColor("#42D000"), QsciLexerPython.DoubleQuotedFString)
        lexer.setColor(QColor("#42D000"), QsciLexerPython.DoubleQuotedString)
        lexer.setColor(QColor("#42D000"), QsciLexerPython.SingleQuotedFString)
        lexer.setColor(QColor("#42D000"), QsciLexerPython.SingleQuotedString)
        lexer.setColor(QColor("#D04500"), QsciLexerPython.Number)
        return lexer
