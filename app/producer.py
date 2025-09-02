import os, cefpyco, requests

PREFIX     = "ccnx:/api"
PORT       = int(os.getenv("CEF_PORT", "9896"))
CEFOREDIR  = "/usr/local/cefore"

def handle_interest(name: str) -> bytes:
    if name.startswith(f"{PREFIX}/httpbin/get"):
        r = requests.get("https://httpbin.org/get", timeout=5)
        return r.content
    return b'{"error":"unsupported"}'

with cefpyco.create_handle(ceforedir=CEFOREDIR, portnum=PORT) as h:
    h.register(PREFIX)
    print(f"[producer] Registered: {PREFIX} on port {PORT}. Waiting...")
    while True:
        info = h.receive(timeout_ms=200)
        if not info.is_succeeded:
            continue
        if info.is_interest and info.name.startswith(PREFIX):
            try:
                payload = handle_interest(info.name)
            except Exception as e:
                payload = f'{{"error":"{e}"}}'.encode()
            h.send_data(info.name, payload, info.chunk_num, cache_time=0)
