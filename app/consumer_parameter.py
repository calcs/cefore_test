import os, json, base64, cefpyco, random

# urlsafeなbase64エンコードでないと、/や+が入ってしまい名前に使えない・・気がする
def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

PREFIX = "ccnx:/api/param-test"
params = {"lang": "ja", "limit": 0}

blob = b64u(json.dumps(params, ensure_ascii=False).encode("utf-8"))
name = f"{PREFIX}/__p/{blob}"

with cefpyco.create_handle() as h:
    h.send_interest(name, 0)
    info = h.receive(timeout_ms=3000)
    print(info.payload.decode("utf-8", "ignore") if (info.is_data and info.name == name) else "timeout or error")
