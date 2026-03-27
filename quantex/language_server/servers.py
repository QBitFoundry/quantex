# Map file extensions to language server commands
# LSP_SERVERS = {
#     ".py": (["pyright-langserver", "--stdio"], "npm install -g pyright"),
#     ".js": (["typescript-language-server", "--stdio"], "npm install -g typescript typescript-language-server"),
#     ".ts": (["typescript-language-server", "--stdio"], "npm install -g typescript typescript-language-server"),
#     ".cpp": (["clangd"], "sudo apt install -y clangd"),
#     ".c": (["clangd"], "sudo apt install -y clangd"),
# }
# LSP_SERVERS = {
#     ".py": (("pyright-langserver", ["--stdio"]), ("npm", ["install", "pyright"])),
#     ".js": (("typescript-language-server", ["--stdio"]), ("npm", ["install", "typescript", "typescript-language-server"])),
#     ".ts": (("typescript-language-server", ["--stdio"]), ("npm", ["install", "typescript", "typescript-language-server"])),
#     # need OS support modification for the c families
#     ".cpp": (["clangd"], "sudo apt install -y clangd"),
#     ".c": (["clangd"], "sudo apt install -y clangd"),
# }

# lsp package will not be installed globally.
LSP_SERVERS = {
    ".py": (("pyright-langserver", ["--stdio"]), ["npm", "install", "pyright"]),
    ".js": (("typescript-language-server", ["--stdio"]), ["npm", "install", "typescript", "typescript-language-server"]),
    ".ts": (("typescript-language-server", ["--stdio"]), ["npm", "install", "typescript", "typescript-language-server"]),
    # need OS support modification for the c families
    ".cpp": (["clangd"], "sudo apt install -y clangd"),
    ".c": (["clangd"], "sudo apt install -y clangd"),
}

import subprocess
from PyQt6.QtCore import QProcess
from pathlib import Path
import shutil, sys, os
from PyQt6.QtCore import QCoreApplication, QTimer # just for tests


class PackageInstaller:
    def __init__(self, path: Path):
        super().__init__()
        # self.extension = ".py"
        self.extension = Path(path).suffix
        self.run_command = LSP_SERVERS[self.extension][0]
        self.install_command = LSP_SERVERS[self.extension][1]
        # self.packages_path = str(Path(__file__).parent.resolve()) + "\\ServersPackages\\"
        self.packages_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ServersPackages")

    def get_path(self):
        print(self.packages_path)

    def check_4_node(self) -> bool:
        if shutil.which("node") is None:
            print("Please Install node first ...")
            return False
        
        return True

    def install(self) -> bool:
        print("Installing", self.run_command[0], "...")
        
        install_path = os.path.join(self.packages_path, self.run_command[0])
        os.makedirs(install_path, exist_ok=True)

        try:
            if self.check_4_node():
                if self.install_command:
                    result = subprocess.run(self.install_command + ["--prefix", install_path], capture_output=True, text=True)
                    
                    if result.returncode != 0:
                        raise SystemError
                    
                    return True
        except:
            print(self.run_command[0], "Failed to install!")

        return False


class Server:
    def __init__(self):
        super().__init__()
        self.process = QProcess()
        self.extension = ".py"
        self.run_command = None
        # self.install_command = None
        if LSP_SERVERS.get(self.extension):
            self.run_command = LSP_SERVERS[self.extension][0]
            # self.install_command = LSP_SERVERS[self.extension][1]
    
        self.process.readyReadStandardOutput.connect(self.on_output)
        self.process.readyReadStandardError.connect(self.on_error)

    def setup(self, path: Path) -> bool:
        package_installer: PackageInstaller = PackageInstaller(path)
        package_installer.get_path()
        return package_installer.install()

    def initialize(self, path: Path) -> None:
        setup_successful: bool = self.setup(path)

        if setup_successful:
            self.start()
            return None
        
        print("Skipped due to setup error ...")

    def run(self):
        print("Starting LSP ...")
        # print(self.run_command[0], self.run_command[1])
        pyright_dir = os.path.join(os.getcwd(), "ServersPackages", self.run_command[0], "node_modules", "pyright")
        pyright_lsp = os.path.join(pyright_dir, "langserver.index.js")
        try:
            if self.run_command:
                self.process.start("node", [pyright_lsp, "--stdio"])
                # self.process.start(self.run_command[0], self.run_command[1])
        except FileNotFoundError:
            print(self.run_command[0], "not started!")
            self.install()

    def terminate(self, app):
        print("Stopping LSP ...")

        if self.process.state() != QProcess.ProcessState.NotRunning:
            self.process.terminate()
            if not self.process.waitForFinished(5000):
                print("Killing LSP process ...")
                self.process.kill()
                self.process.waitForFinished(3000)
        
        app.quit()
    
    def start(self):
        print("Starting LSP ...")
        # print(self.run_command[0], self.run_command[1])
        pyright_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ServersPackages", self.run_command[0], "node_modules", "pyright")
        pyright_lsp = os.path.join(pyright_dir, "langserver.index.js")
        try:
            if self.run_command:
                self.process.start("node", [pyright_lsp, "--stdio"])
                # self.process.start(self.run_command[0], self.run_command[1])
        except FileNotFoundError:
            print(self.run_command[0], "not started!")
            self.install()

    def stop(self):
        print("Stopping LSP ...")

        if self.process.state() != QProcess.ProcessState.NotRunning:
            self.process.terminate()
            if not self.process.waitForFinished(5000):
                print("Killing LSP process ...")
                self.process.kill()
                self.process.waitForFinished(3000)
        
        # app.quit()

        # super().stop(event) # fire it in CloseEvent

    def on_output(self):
        print("Server Output ...")
        print("Output: ", self.process.readAllStandardOutput().data().decode())

    def on_error(self):
        print("Server Error ...")
        print(self.process.readAllStandardError().data().decode())





def main() -> None:
    app = QCoreApplication([])

    server: Server = Server()
    setup_successful: bool = server.setup("test.py") # use a .py path name for test.
    
    if setup_successful:
        server.run()
        QTimer.singleShot(20000, lambda: server.terminate(app))
        app.exec()
        return None

    print("Skipped due to setup error ...")

if __name__ == "__main__":
    main()
