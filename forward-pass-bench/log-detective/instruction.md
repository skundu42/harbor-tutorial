`/app/server.log` is a web server access log. Each line looks like:

    2026-11-11T09:00:01Z 10.0.0.4 GET /api/users 200 87ms

Answer three questions and write them to `/app/answer.json`:

- `errors`: how many requests returned a 5xx status code
- `top_ip`: the client IP that made the most requests
- `slowest_path`: the path of the single slowest request

Example format: `{"errors": 1, "top_ip": "10.0.0.9", "slowest_path": "/login"}`
