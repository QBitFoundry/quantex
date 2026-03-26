import subprocess
import json

def send(process, message):
    body = json.dumps(message)
    body = body.encode("utf-8")
    
    request = f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8") + body

    process.stdin.write(request)
    process.stdin.flush()

def read(process):
    headers = {}

    while True:
        line = process.stdout.readline().decode()

        if not line:
            return None
        
        line =  line.strip()
        if not line or line == "":
            break

        if ": " not in line:
            continue

        key, value = line.split(": ", 1)
        headers[key] = value

    length = int(headers.get("Content-Length", "0"))
    body = read_exact(process, length).decode()

    return json.loads(body)
    
def read_exact(process, n):
    data = b""
    while len(data) < n:
        chunk = process.stdout.read(n - len(data))
        if not chunk:
            raise EOFError
        
        data += chunk

    return data
    
# Start server
process = subprocess.Popen(
    ["python", "language_server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE
)

# Send Initialize
send(process, {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {}
})

print("Initialize response: ")
print(read(process))

# Send Completion response
send(process, {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "textDocument/completion",
    "params": {}
})

print("\n Completion response: ")
print(read(process))