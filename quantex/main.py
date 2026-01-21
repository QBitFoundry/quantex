from editor import QApplication, MainWindow
import sys

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())