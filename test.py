import http.client
import time
import ssl

CHUNK_SIZE = 1024

with open("sample-3s.wav", "rb") as f:
    data = f.read()

if __name__ == "__main__":
    conn = http.client.HTTPConnection('localhost', port=8000)
    conn.connect()
    conn.putrequest('POST', '/uploadfile')
    conn.putheader('Transfer-Encoding', 'chunked')
    conn.putheader('Content-Type', 'audio/raw; encoding=signed-integer; bits=16; rate=16000; endian=little')
    conn.putheader('file', 'sample-3s.wav')
    conn.putheader('user_id' , '1234')
    conn.endheaders()

    # Send the data in chunks
    chunk_size = 1024
    while data:
        chunk = data[:chunk_size]
        data = data[chunk_size:]

        conn.send(b"%x\r\n" % len(chunk))
        conn.send(chunk)
        conn.send(b"\r\n")

        # time.sleep(0.1)

    # Last chunk
    conn.send(b"0\r\n\r\n")

    r = conn.getresponse()
    print(r.status, r.reason, r.read())
    conn.close()