#!/usr/bin/env python3
"""HTTP request/response parser."""

def parse_request(raw: str) -> dict:
    lines = raw.split("\r\n")
    method, path, version = lines[0].split(" ", 2)
    headers = {}
    body_start = 1
    for i in range(1, len(lines)):
        if lines[i] == "":
            body_start = i + 1
            break
        k, v = lines[i].split(": ", 1)
        headers[k.lower()] = v
    body = "\r\n".join(lines[body_start:]) if body_start < len(lines) else ""
    return {"method": method, "path": path, "version": version, "headers": headers, "body": body}

def parse_response(raw: str) -> dict:
    lines = raw.split("\r\n")
    parts = lines[0].split(" ", 2)
    version = parts[0]
    status = int(parts[1])
    reason = parts[2] if len(parts) > 2 else ""
    headers = {}
    body_start = 1
    for i in range(1, len(lines)):
        if lines[i] == "":
            body_start = i + 1
            break
        k, v = lines[i].split(": ", 1)
        headers[k.lower()] = v
    body = "\r\n".join(lines[body_start:]) if body_start < len(lines) else ""
    return {"version": version, "status": status, "reason": reason, "headers": headers, "body": body}

def build_request(method: str, path: str, headers: dict = None, body: str = "") -> str:
    lines = [f"{method} {path} HTTP/1.1"]
    for k, v in (headers or {}).items():
        lines.append(f"{k}: {v}")
    if body:
        lines.append(f"Content-Length: {len(body)}")
    lines.append("")
    lines.append(body)
    return "\r\n".join(lines)

def test():
    req = "GET /index.html HTTP/1.1\r\nHost: example.com\r\nAccept: text/html\r\n\r\n"
    r = parse_request(req)
    assert r["method"] == "GET"
    assert r["path"] == "/index.html"
    assert r["headers"]["host"] == "example.com"
    resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html></html>"
    p = parse_response(resp)
    assert p["status"] == 200
    assert p["body"] == "<html></html>"
    built = build_request("POST", "/api", {"Host": "api.com"}, "data")
    r2 = parse_request(built)
    assert r2["method"] == "POST" and r2["body"] == "data"
    print("  http_parse: ALL TESTS PASSED")

if __name__ == "__main__":
    test()
