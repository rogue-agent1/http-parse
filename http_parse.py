#!/usr/bin/env python3
"""HTTP request/response parser."""
import sys

class HttpRequest:
    def __init__(self, method="GET", path="/", headers=None, body=""):
        self.method, self.path, self.body = method, path, body
        self.headers = headers or {}
        self.version = "HTTP/1.1"
    @classmethod
    def parse(cls, raw):
        lines = raw.split("\r\n")
        method, path, version = lines[0].split(" ", 2)
        headers = {}
        i = 1
        while i < len(lines) and lines[i]:
            key, val = lines[i].split(": ", 1)
            headers[key.lower()] = val
            i += 1
        body = "\r\n".join(lines[i+1:]) if i+1 < len(lines) else ""
        req = cls(method, path, headers, body)
        req.version = version
        return req
    def serialize(self):
        lines = [f"{self.method} {self.path} {self.version}"]
        for k, v in self.headers.items():
            lines.append(f"{k}: {v}")
        lines.append("")
        lines.append(self.body)
        return "\r\n".join(lines)

class HttpResponse:
    def __init__(self, status=200, reason="OK", headers=None, body=""):
        self.status, self.reason, self.body = status, reason, body
        self.headers = headers or {}
        self.version = "HTTP/1.1"
    @classmethod
    def parse(cls, raw):
        lines = raw.split("\r\n")
        parts = lines[0].split(" ", 2)
        version, status = parts[0], int(parts[1])
        reason = parts[2] if len(parts) > 2 else ""
        headers = {}
        i = 1
        while i < len(lines) and lines[i]:
            key, val = lines[i].split(": ", 1)
            headers[key.lower()] = val
            i += 1
        body = "\r\n".join(lines[i+1:]) if i+1 < len(lines) else ""
        resp = cls(status, reason, headers, body)
        resp.version = version
        return resp
    def serialize(self):
        lines = [f"{self.version} {self.status} {self.reason}"]
        for k, v in self.headers.items():
            lines.append(f"{k}: {v}")
        lines.append("")
        lines.append(self.body)
        return "\r\n".join(lines)

def parse_query_string(qs):
    params = {}
    for pair in qs.split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1)
            params[k] = v
        elif pair:
            params[pair] = ""
    return params

def test():
    raw = "GET /api?key=val HTTP/1.1\r\nHost: example.com\r\nAccept: */*\r\n\r\n"
    req = HttpRequest.parse(raw)
    assert req.method == "GET"
    assert req.path == "/api?key=val"
    assert req.headers["host"] == "example.com"
    raw_resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hi</h1>"
    resp = HttpResponse.parse(raw_resp)
    assert resp.status == 200
    assert resp.body == "<h1>Hi</h1>"
    assert parse_query_string("a=1&b=2&c") == {"a": "1", "b": "2", "c": ""}
    assert req.serialize().startswith("GET /api")
    print("  http_parse: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("HTTP request/response parser")
