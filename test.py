from http_parse import parse_request, parse_response, build_request, build_response, parse_query_string
req = parse_request("GET /index.html HTTP/1.1\r\nHost: example.com\r\n\r\n")
assert req["method"] == "GET" and req["path"] == "/index.html"
assert req["headers"]["host"] == "example.com"
resp = parse_response("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello")
assert resp["status"] == 200 and resp["body"] == "Hello"
built = build_request("POST", "/api", {"Host":"x.com"}, "data")
assert "POST /api HTTP/1.1" in built
bresp = build_response(404, "Not Found")
assert "404 Not Found" in bresp
qs = parse_query_string("name=alice&age=30&flag")
assert qs == {"name":"alice","age":"30","flag":""}
print("http_parse tests passed")
