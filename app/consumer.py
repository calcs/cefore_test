import os, cefpyco
name="ccnx:/api/httpbin/get"; port=int(os.getenv("CEF_PORT","9896"))

with cefpyco.create_handle(ceforedir="/usr/local/cefore", portnum=port) as h:
    h.send_interest(name, 0)
    info=h.receive(timeout_ms=3000)
    print(info.payload.decode("utf-8","ignore") if info.is_data else "timeout or error")
