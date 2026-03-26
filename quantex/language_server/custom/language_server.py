import sys
import json

# Global
documents = {}

def read_message():
    headers = {}

    while True:
        line = sys.stdin.readline()

        # Return None when line is EOF
        if not line:
            return None

        line = line.strip()
        if not line or line == "":
            break

        if ": " not in line:
            continue

        key, value = line.split(": ", 1)

        headers[key] = value

    content_length = int(headers.get("Content-Length", 0))

    body = sys.stdin.read(content_length)
    return json.loads(body)

def send_message(message):
    # Sends a JSON-RPC message to std out.
    body = json.dumps(message)

    body = body.encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8")

    sys.stdout.buffer.write(header +  body)
    sys.stdout.buffer.flush()

def handle_request(message):
    method = message.get("method")

    response = None

    # Initialize
    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": message["id"],
            "result": {
                "capabilities": {
                    "textDocumentSync": 1,
                    "completionProvider": {},
                },
            },
        }
    
    # Completion
    elif method == "textDocument/completion":
        response = {
            "jsonrpc": "2.0",
            "id": message["id"],
            "result": {
                "isComplete": True,
                "items": [
                    {"label": "Helloworld"},
                    {"label": "print"},
                    {"label": "ByeBye"},
                ],
            },
        }
    
    elif method == "textDocument/didOpen":
        uri =  message["params"]["textDocument"]["uri"]
        text = message["params"]["textDocument"]["text"]

        documents[uri] = text

    elif method == "textDocument/didChange":
        uri = message["params"]["textDocument"]["uri"]
        changes = message["params"]["contentChanges"]

        if changes:
            documents[uri] = changes[0]["text"]

    return response

def main():

    try:
        while True:
            message = read_message()

            if message is None:
                break

            if "id" not in message:
                continue

            response = handle_request(message)

            if response:
                send_message(response)
    
    except KeyboardInterrupt:
        print("Stopping the LSP ...\n", file=sys.stderr)

if __name__ == "__main__":
    print("Staring the LSP ...", file=sys.stderr)
    main()


# "textDocument/publishDiagnostics"
# "textDocument/hover"
# "textDocument/definition"