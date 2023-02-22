from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import uuid

PORT = 8000

class TestHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        audio_id = str(uuid.uuid4())
        path = f"records/{audio_id}.wav"
        path = self.translate_path(path)
        self.log_message("Recieving the file")
        self.log_message("Current path is: %s", path)

        if "Content-Length" in self.headers:
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            with open(path, "wb") as out_file:
                out_file.write(body)
        elif "chunked" in self.headers.get("Transfer-Encoding", ""):
            with open(path, "wb") as out_file:
                while True:
                    line = self.rfile.readline().strip()
                    self.log_message("Received chunck len: %s", line)
                    chunk_length = int(line, 16)

                    if chunk_length != 0:
                        chunk = self.rfile.read(chunk_length)
                        # self.log_message("Received chunk: %s", chunk)
                        out_file.write(chunk)

                    # Each chunk is followed by an additional empty newline
                    # that we have to consume.
                    self.rfile.readline()

                    # Finally, a chunk size of 0 is an end indication
                    if chunk_length == 0:
                        break

            self.log_message("File received successfully")
                
            # self.saveAudioToDisk(path, body)
            response_message = json.dumps({"message": "File saved successfully"})
            self.wfile.write(response_message.encode())

httpd = HTTPServer(("", PORT), TestHTTPRequestHandler)

print("Serving at port:", httpd.server_port)
httpd.serve_forever()