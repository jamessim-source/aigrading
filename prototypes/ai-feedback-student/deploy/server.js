/* Static server for the AI Feedback student prototype. No dependencies —
   node standard library only, so Railway needs no install step.
   Setting both AUTH_USER and AUTH_PASS turns on Basic auth. */

const http = require("http");
const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "public");
const PORT = process.env.PORT || 3000;
const USER = process.env.AUTH_USER;
const PASS = process.env.AUTH_PASS;
const PROTECTED = Boolean(USER && PASS);

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
};

/* Compare in constant time, so response timing says nothing about the secret. */
function sameSecret(a, b) {
  const x = Buffer.from(String(a));
  const y = Buffer.from(String(b));
  if (x.length !== y.length) return false;
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

function authorized(req) {
  if (!PROTECTED) return true;
  const header = req.headers.authorization || "";
  if (!header.startsWith("Basic ")) return false;
  const [user, pass] = Buffer.from(header.slice(6), "base64").toString().split(":");
  return sameSecret(user, USER) && sameSecret(pass, PASS);
}

const server = http.createServer((req, res) => {
  if (!authorized(req)) {
    res.writeHead(401, { "WWW-Authenticate": 'Basic realm="prototype"' });
    res.end("Authentication required");
    return;
  }

  let url;
  try {
    url = decodeURIComponent(req.url.split("?")[0]);
  } catch (e) {
    res.writeHead(400).end("400");
    return;
  }

  let rel = url === "/" ? "index.html" : url.replace(/^\/+/, "");
  if (!path.extname(rel)) rel += ".html"; // /M-Crop also works
  const file = path.join(ROOT, rel);

  /* Refuse anything that climbs out of public/ */
  if (file !== ROOT && !file.startsWith(ROOT + path.sep)) {
    res.writeHead(403).end("403");
    return;
  }

  fs.readFile(file, (err, body) => {
    if (err) {
      res.writeHead(404, { "content-type": "text/html; charset=utf-8" });
      res.end('<meta charset="utf-8"><p>Not found. <a href="/">All screens</a>');
      return;
    }
    res.writeHead(200, {
      "content-type": TYPES[path.extname(file)] || "application/octet-stream",
      "cache-control": "no-cache",
    });
    res.end(body);
  });
});

server.listen(PORT, () => {
  console.log(`listening on ${PORT}${PROTECTED ? " (Basic auth on)" : " (no auth)"}`);
});
