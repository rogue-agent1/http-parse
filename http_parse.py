#!/usr/bin/env python3
"""http_parse - HTTP/1.1 request and response parser."""
import sys

class HttpRequest:
    def __init__(self, method, path, version, headers, body=""):
        self.method, self.path, self.version = method, path, version
        self.headers, self.body = headers, body

class HttpResponse:
    def __init__(self, version, status, reason, headers, body=""):
        self.version, self.status, self.reason = version, status, reason
        self.headers, self.body = headers, body

def parse_request(raw):
    parts = raw.split("\r\n\r\n", 1)
    head = parts[0]
    body = parts[1] if len(parts) > 1 else ""
    lines = head.split("\r\n")
    method, path, version = lines[0].split(" ", 2)
    headers = {}
    for line in lines[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            headers[k.lower()] = v
    return HttpRequest(method, path, version, headers, body)

def parse_response(raw):
    parts = raw.split("\r\n\r\n", 1)
    head = parts[0]
    body = parts[1] if len(parts) > 1 else ""
    lines = head.split("\r\n")
    version, status, reason = lines[0].split(" ", 2)
    headers = {}
    for line in lines[1:]:
        if ": " in line:
            k, v = line.split(": ", 1)
            headers[k.lower()] = v
    return HttpResponse(version, int(status), reason, headers, body)

def build_request(method, path, headers=None, body=""):
    headers = headers or {}
    lines = [f"{method} {path} HTTP/1.1"]
    for k, v in headers.items():
        lines.append(f"{k}: {v}")
    if body:
        lines.append(f"Content-Length: {len(body)}")
    return "\r\n".join(lines) + "\r\n\r\n" + body

def test():
    raw = "GET /index.html HTTP/1.1\r\nHost: example.com\r\nAccept: text/html\r\n\r\n"
    req = parse_request(raw)
    assert req.method == "GET"
    assert req.path == "/index.html"
    assert req.headers["host"] == "example.com"
    raw_resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hi</h1>"
    resp = parse_response(raw_resp)
    assert resp.status == 200
    assert resp.body == "<h1>Hi</h1>"
    built = build_request("POST", "/api", {"Host": "x.com"}, "data")
    req2 = parse_request(built)
    assert req2.method == "POST" and req2.body == "data"
    assert req2.headers["content-length"] == "4"
    print("http_parse: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: http_parse.py --test")
