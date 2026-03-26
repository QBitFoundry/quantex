from editor.editor import QApplication
# from language_server.client import Client
import sys
from frames.mainframe import MainWindow

# client = Client([sys.executable, "language_server/language_server.py"])

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())