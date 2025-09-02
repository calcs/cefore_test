import os, cefpyco, requests, base64, json

PREFIX     = "ccnx:/api"
PORT       = int(os.getenv("CEF_PORT", "9896"))
CEFOREDIR  = "/usr/local/cefore"

def parse_params_from_name(name: str) -> dict:
    # __pが含まれる場合、それ以降をパースして辞書で返す
    parts = name.split("/")
    for i in range(len(parts)-1):
        if parts[i] == "__p":
            b64 = parts[i+1]
            padded = b64 + "=" * ((4 - len(b64) % 4) % 4)
            return json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
    return {}

def handle_interest(name: str) -> bytes:
    params = parse_params_from_name(name)
    if name.startswith(f"{PREFIX}/httpbin/get"):
        r = requests.get("https://httpbin.org/get", timeout=5)
        return r.content
    elif name.startswith(f"{PREFIX}/param-test/"):
        params["limit"] += 50;  # ちょっと弄ってみる
        r = json.dumps(params).encode("utf-8")
        return r
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
