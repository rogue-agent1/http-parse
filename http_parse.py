#!/usr/bin/env python3
"""http_parse - HTTP request/response parser and builder."""
import sys

class HTTPRequest:
    def __init__(self, method="GET", path="/", headers=None, body="", version="HTTP/1.1"):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body
        self.version = version

    @staticmethod
    def parse(raw):
        lines = raw.split("\r\n")
        method, path, version = lines[0].split(" ", 2)
        headers = {}
        i = 1
        while i < len(lines) and lines[i]:
            key, val = lines[i].split(": ", 1)
            headers[key] = val
            i += 1
        body = "\r\n".join(lines[i+1:]) if i + 1 < len(lines) else ""
        return HTTPRequest(method, path, headers, body, version)

    def to_bytes(self):
        lines = [f"{self.method} {self.path} {self.version}"]
        for k, v in self.headers.items():
            lines.append(f"{k}: {v}")
        lines.append("")
        lines.append(self.body)
        return "\r\n".join(lines)

class HTTPResponse:
    def __init__(self, status=200, reason="OK", headers=None, body="", version="HTTP/1.1"):
        self.status = status
        self.reason = reason
        self.headers = headers or {}
        self.body = body
        self.version = version

    @staticmethod
    def parse(raw):
        lines = raw.split("\r\n")
        parts = lines[0].split(" ", 2)
        version = parts[0]
        status = int(parts[1])
        reason = parts[2] if len(parts) > 2 else ""
        headers = {}
        i = 1
        while i < len(lines) and lines[i]:
            key, val = lines[i].split(": ", 1)
            headers[key] = val
            i += 1
        body = "\r\n".join(lines[i+1:]) if i + 1 < len(lines) else ""
        return HTTPResponse(status, reason, headers, body, version)

    def to_bytes(self):
        lines = [f"{self.version} {self.status} {self.reason}"]
        for k, v in self.headers.items():
            lines.append(f"{k}: {v}")
        lines.append("")
        lines.append(self.body)
        return "\r\n".join(lines)

def test():
    raw = "GET /index.html HTTP/1.1\r\nHost: example.com\r\nAccept: text/html\r\n\r\n"
    req = HTTPRequest.parse(raw)
    assert req.method == "GET"
    assert req.path == "/index.html"
    assert req.headers["Host"] == "example.com"
    rebuilt = req.to_bytes()
    assert "GET /index.html HTTP/1.1" in rebuilt
    raw_resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 5\r\n\r\nhello"
    resp = HTTPResponse.parse(raw_resp)
    assert resp.status == 200
    assert resp.reason == "OK"
    assert resp.headers["Content-Type"] == "text/html"
    assert resp.body == "hello"
    post = HTTPRequest("POST", "/api", {"Content-Type": "application/json"}, '{"key":"val"}')
    s = post.to_bytes()
    assert "POST /api" in s
    assert '{"key":"val"}' in s
    r404 = HTTPResponse(404, "Not Found", {"Server": "test"}, "not found")
    assert "404 Not Found" in r404.to_bytes()
    print("All tests passed!")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("http_parse: HTTP parser. Use --test")
