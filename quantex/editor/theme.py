from PyQt6.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
from PyQt6.QtGui import QFont, QColor

def set_theme():
    # save theme
    pass

def get_theme():
    # self.setUtf8(True)
    # self.setMarginLineNumbers(0, True)
    # # self.setMarginWidth(0, "0000") # fixed line num margin
    # self.setMarginsBackgroundColor(QColor("#3D3D3D"))
    # self.setMarginsForegroundColor(QColor("#dedede"))
    # self.setBraceMatching(QsciScintilla.BraceMatch.StrictBraceMatch)
    # self.setCaretLineVisible(True)
    # self.setCaretLineBackgroundColor(QColor("#393939"))
    # self.setCaretForegroundColor(QColor("#ffffff"))

    # # === Font ===
    # # font = QFont("Consolas", 12)
    # # font = QFont("JetBrains Mono", 12)
    # # font = QFont("Fira Code", 12)
    # font = QFont("Cascadia Code", 12)
    # # font = QFont("Ubuntu Mono", 12)
    # # font = QFont("Monaspace", 12)

    # self.setFont(font)
    # self.setMarginsFont(font)

    data = {
        "marginBgColor": QColor("#3D3D3D"),
        "marginFgColor": QColor("#dedede"),
        "braceMatching": {
            "active": False, # QColor doesn't accept alpha value.
            "type": "Strict", # NoBraceMatch, SloppyBraceMatch, StrictBraceMatch
            "matched": {
                "bgColor": QColor("#59FF3F"),
                "fgColor": QColor(0, 0, 0)
            },
            "unmatched": {
                "bgColor": QColor("#FF3F3F"),
                "fgColor": QColor(255, 255, 255)
            }
        },
        "caretLine": {
            "visible": True,
            "bgColor": QColor("#393939"),
            "fgColor": QColor("#ffffff"),
        },
        "font": {
            "family": "Cascadia Code",
            "size": 12
        }
    }

    return data