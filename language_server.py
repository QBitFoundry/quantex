import subprocess
import threading
import json

class Client:
    def __init__(self, command):
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )
        
        print("Started LSP process:", self.process.pid)
        print("Process running:", self.process.poll() is None)

        self._response = {}
        self._start_reader_thread()
        self._id=1

        # Initializing the server.
        self.send_request("initialize", {
            "processId": None,
            "rootUri": None,
            "capabilities": {}
        })

    def _start_reader_thread(self):
        def reader():
            while True:
                header = {}
                while True:
                    line = self.process.stdout.readline().strip()
                    if line == "":
                        break
                    if ":" in line:
                        key, value = line.split(":", 1)
                        header[key.strip()] = value.strip()
                
                if not header:
                    continue

                length = int(header.get("content-length", 0))
                body = self.process.stdout.read(length)
                message = json.loads(body)
                if "id" in message:
                    self._response[message["id"]] = message
                elif "method" in message:
                    # Handles notification (Diagnostic)
                    print("Notification", message)
                print("Message: ", message)
        
        # print(self.process.stderr.read())
        threading.Thread(target=reader, daemon=True).start()
    
    def send_request(self, method, params):
        self._id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self._id,
            "method": method,
            "params": params
        }
        self._send_message(request)

        return self._id
    
    def send_notification(self, method, params):
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        self._send_message(request)

    def _send_message(self, message):
        message_bytes = json.dumps(message)
        header = f"Content-Length: {len(message_bytes)}\r\n\r\n"
        self.process.stdin.write(header + message_bytes)
        self.process.stdin.flush()


# if __name__ == "__main__":
#     server = Client()
    # server.run()