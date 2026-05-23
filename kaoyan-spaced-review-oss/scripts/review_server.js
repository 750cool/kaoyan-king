const http = require("http");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const appDir = path.join(root, "data", "review_app");
const statePath = path.join(root, "data", "review_app", "review_state.json");

const mime = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".md": "text/markdown; charset=utf-8"
};

function ensureState() {
  if (!fs.existsSync(statePath)) {
    fs.mkdirSync(path.dirname(statePath), { recursive: true });
    fs.writeFileSync(statePath, JSON.stringify({ reviews: [], schedule: {} }, null, 2), "utf8");
  }
}

function send(res, status, body, type = "application/json; charset=utf-8") {
  res.writeHead(status, { "Content-Type": type, "Access-Control-Allow-Origin": "*" });
  res.end(body);
}

function safeJoin(base, reqPath) {
  const decoded = decodeURIComponent(reqPath.split("?")[0]);
  const target = path.normalize(path.join(base, decoded));
  if (!target.startsWith(base)) return null;
  return target;
}

function nextDue(card, grade) {
  const now = new Date();
  const prior = Number(card.intervalDays || 0);
  let interval = 1;
  if (grade === "know") interval = prior <= 1 ? 3 : Math.min(Math.round(prior * 2.3), 30);
  if (grade === "unknown") interval = 1;
  const due = new Date(now);
  due.setDate(now.getDate() + interval);
  return { interval, due: due.toISOString().slice(0, 10) };
}

ensureState();

const server = http.createServer((req, res) => {
  if (req.method === "OPTIONS") return send(res, 204, "");

  if (req.url === "/api/state" && req.method === "GET") {
    ensureState();
    return send(res, 200, fs.readFileSync(statePath, "utf8"));
  }

  if (req.url === "/api/review" && req.method === "POST") {
    let body = "";
    req.on("data", chunk => (body += chunk));
    req.on("end", () => {
      try {
        ensureState();
        const payload = JSON.parse(body || "{}");
        const state = JSON.parse(fs.readFileSync(statePath, "utf8"));
        const result = nextDue(payload.card || {}, payload.grade);
        const event = {
          cardId: payload.card?.id,
          grade: payload.grade,
          answer: payload.answer || "",
          reviewedAt: new Date().toISOString(),
          nextDue: result.due,
          intervalDays: result.interval
        };
        state.reviews.push(event);
        state.schedule[payload.card?.id] = {
          nextDue: result.due,
          intervalDays: result.interval,
          lastGrade: payload.grade
        };
        fs.writeFileSync(statePath, JSON.stringify(state, null, 2), "utf8");
        return send(res, 200, JSON.stringify(event));
      } catch (err) {
        return send(res, 400, JSON.stringify({ error: String(err.message || err) }));
      }
    });
    return;
  }

  const reqPath = req.url === "/" ? "/data/review_app/index.html" : req.url;
  const file = safeJoin(root, reqPath);
  if (!file || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    return send(res, 404, "Not found", "text/plain; charset=utf-8");
  }
  const ext = path.extname(file).toLowerCase();
  send(res, 200, fs.readFileSync(file), mime[ext] || "application/octet-stream");
});

const port = Number(process.env.REVIEW_PORT || 8765);
server.listen(port, "127.0.0.1", () => {
  console.log(`Review app running at http://127.0.0.1:${port}/data/review_app/index.html`);
});
