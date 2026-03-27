from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QLabel, QHBoxLayout, QStatusBar
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt
import sys
# from PyQt6.QtCore import QTimer
# from language_server.client import Client
from editor.editor import CodeEditor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quantex Code Editor")
        self.setGeometry(200, 100, 800, 600)
        self.centerWindow()

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

        # === Language server status in top right menu bar ===
        statusbar = QStatusBar(self)
        self.setStatusBar(statusbar)
        statusbar.setSizeGripEnabled(False) # Disable the default size grip.

        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(8, 0, 16, 2)
        container_layout.setSpacing(6)

        self.lang_server_icon = QLabel()
        self.lang_server_text = QLabel()
        container_layout.addWidget(self.lang_server_icon)
        container_layout.addWidget(self.lang_server_text)
        statusbar.addPermanentWidget(container)

        self.lang_server_status_update("Language Server Error!", "../assets/icons/sync-error-svgrepo-com (1).png")
        # commented because language server has not been added yet.
        # self.lang_server_status_update("Language Server", "../assets/icons/sync-svgrepo-com (3).png")
        # self.lang_server_status_update("Python", "../assets/icons/check-circle-svgrepo-com.png")

        # self.lsp_client = Client([sys.executable, "language_server/language_server.py"], ".py")

        # === Editor ===
        # self.editor = CodeEditor(lsp_client=self.lsp_client)
        self.editor = CodeEditor()
        self.setCentralWidget(self.editor)
    

    def closeEvent(self, event):
        print("CLOSING WINDOW")
        self.editor.on_close()
        event.accept()
    

    def centerWindow(self):
        screen_size = QApplication.primaryScreen().availableSize()
        window_size = self.geometry();
        
        self.move(
            ((screen_size.width() - window_size.width()) // 2),
            ((screen_size.height() - window_size.height()) // 2)
        ) # used floor division because move() takes only int.

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

                # print(file_path)

            except:
                print("Fail to open!")
            
            # TODO: App freezes when installing LCP...
            self.editor.on_file_opened(file_path)
    
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
    
    def lang_server_status_update(self, text, icon_path):
        self.lang_server_text.setText(text)
        # Setting language server status icon.
        icon_pixel = QPixmap(icon_path).scaled(
            12, 12,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.lang_server_icon.setPixmap(icon_pixel)
