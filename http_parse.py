#!/usr/bin/env python3
"""HTTP request/response parser. Zero dependencies."""

def parse_request(raw):
    lines = raw.split("\r\n") if "\r\n" in raw else raw.split("\n")
    method, path, version = lines[0].split(" ", 2)
    headers = {}; body = ""; in_body = False
    for line in lines[1:]:
        if in_body: body += line; continue
        if not line.strip(): in_body = True; continue
        key, val = line.split(":", 1)
        headers[key.strip().lower()] = val.strip()
    return {"method":method,"path":path,"version":version,"headers":headers,"body":body}

def parse_response(raw):
    lines = raw.split("\r\n") if "\r\n" in raw else raw.split("\n")
    parts = lines[0].split(" ", 2)
    version = parts[0]; status = int(parts[1]); reason = parts[2] if len(parts)>2 else ""
    headers = {}; body = ""; in_body = False
    for line in lines[1:]:
        if in_body: body += line + "\n"; continue
        if not line.strip(): in_body = True; continue
        key, val = line.split(":", 1)
        headers[key.strip().lower()] = val.strip()
    return {"version":version,"status":status,"reason":reason,"headers":headers,"body":body.rstrip("\n")}

def build_request(method, path, headers=None, body=""):
    h = headers or {}
    lines = [f"{method} {path} HTTP/1.1"]
    for k,v in h.items(): lines.append(f"{k}: {v}")
    if body: lines.append(f"Content-Length: {len(body)}")
    lines.append(""); lines.append(body)
    return "\r\n".join(lines)

def build_response(status, reason="OK", headers=None, body=""):
    h = headers or {}
    lines = [f"HTTP/1.1 {status} {reason}"]
    for k,v in h.items(): lines.append(f"{k}: {v}")
    if body: lines.append(f"Content-Length: {len(body)}")
    lines.append(""); lines.append(body)
    return "\r\n".join(lines)

def parse_query_string(qs):
    params = {}
    for pair in qs.split("&"):
        if "=" in pair:
            k, v = pair.split("=", 1); params[k] = v
        elif pair: params[pair] = ""
    return params

if __name__ == "__main__":
    req = build_request("GET", "/api/users", {"Host":"example.com"})
    print(req)
