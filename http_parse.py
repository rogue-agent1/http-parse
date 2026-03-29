#!/usr/bin/env python3
"""http_parse: HTTP request/response parser and builder."""
import sys

def parse_request(data):
    if isinstance(data, bytes): data = data.decode("utf-8", errors="replace")
    lines = data.split("\r\n")
    method, path, version = lines[0].split(" ", 2)
    headers = {}
    i = 1
    while i < len(lines) and lines[i]:
        key, val = lines[i].split(": ", 1)
        headers[key.lower()] = val
        i += 1
    body = "\r\n".join(lines[i+1:]) if i + 1 < len(lines) else ""
    return {"method": method, "path": path, "version": version, "headers": headers, "body": body}

def parse_response(data):
    if isinstance(data, bytes): data = data.decode("utf-8", errors="replace")
    lines = data.split("\r\n")
    parts = lines[0].split(" ", 2)
    version = parts[0]
    status = int(parts[1])
    reason = parts[2] if len(parts) > 2 else ""
    headers = {}
    i = 1
    while i < len(lines) and lines[i]:
        key, val = lines[i].split(": ", 1)
        headers[key.lower()] = val
        i += 1
    body = "\r\n".join(lines[i+1:]) if i + 1 < len(lines) else ""
    return {"version": version, "status": status, "reason": reason, "headers": headers, "body": body}

def build_request(method, path, headers=None, body="", version="HTTP/1.1"):
    headers = headers or {}
    if body and "content-length" not in {k.lower() for k in headers}:
        headers["Content-Length"] = str(len(body))
    lines = [f"{method} {path} {version}"]
    for k, v in headers.items():
        lines.append(f"{k}: {v}")
    lines.append("")
    lines.append(body)
    return "\r\n".join(lines)

def build_response(status, reason="OK", headers=None, body="", version="HTTP/1.1"):
    headers = headers or {}
    if body and "content-length" not in {k.lower() for k in headers}:
        headers["Content-Length"] = str(len(body))
    lines = [f"{version} {status} {reason}"]
    for k, v in headers.items():
        lines.append(f"{k}: {v}")
    lines.append("")
    lines.append(body)
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
    req = "GET /index.html HTTP/1.1\r\nHost: example.com\r\nAccept: text/html\r\n\r\n"
    r = parse_request(req)
    assert r["method"] == "GET"
    assert r["path"] == "/index.html"
    assert r["headers"]["host"] == "example.com"
    resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 5\r\n\r\nhello"
    p = parse_response(resp)
    assert p["status"] == 200
    assert p["body"] == "hello"
    assert p["headers"]["content-type"] == "text/html"
    # Build
    built = build_request("POST", "/api", {"Content-Type": "application/json"}, '{"a":1}')
    assert "POST /api HTTP/1.1" in built
    assert "Content-Length: 7" in built
    # Query string
    assert parse_query_string("a=1&b=2&c=hello") == {"a": "1", "b": "2", "c": "hello"}
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: http_parse.py test")
