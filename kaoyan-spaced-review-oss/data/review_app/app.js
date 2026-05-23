const cardsEl = document.querySelector("#cards");
const template = document.querySelector("#cardTemplate");
const totalCount = document.querySelector("#totalCount");
const doneCount = document.querySelector("#doneCount");
const scheduleList = document.querySelector("#scheduleList");
const filters = document.querySelectorAll(".filter");

let state = { reviews: [], schedule: {} };
let currentFilter = "all";

function localKey() {
  return "kaoyan-review-state";
}

async function loadState() {
  try {
    const res = await fetch("/api/state");
    if (res.ok) {
      state = await res.json();
      localStorage.setItem(localKey(), JSON.stringify(state));
      return;
    }
  } catch (_) {
    const cached = localStorage.getItem(localKey());
    if (cached) state = JSON.parse(cached);
  }
}

function saveLocal() {
  localStorage.setItem(localKey(), JSON.stringify(state));
}

function nextDue(card, grade) {
  const prior = state.schedule[card.id]?.intervalDays || 0;
  const interval = grade === "know" ? (prior <= 1 ? 3 : Math.min(Math.round(prior * 2.3), 30)) : 1;
  const due = new Date();
  due.setDate(due.getDate() + interval);
  return { intervalDays: interval, nextDue: due.toISOString().slice(0, 10) };
}

async function submitReview(card, grade, answer) {
  const fallback = nextDue(card, grade);
  const event = { cardId: card.id, grade, answer, reviewedAt: new Date().toISOString(), ...fallback };
  try {
    const res = await fetch("/api/review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ card, grade, answer })
    });
    if (res.ok) Object.assign(event, await res.json());
  } catch (_) {}

  state.reviews.push(event);
  state.schedule[card.id] = {
    nextDue: event.nextDue,
    intervalDays: event.intervalDays,
    lastGrade: grade
  };
  saveLocal();
  render();
}

function cardStatus(card) {
  return state.schedule[card.id]?.lastGrade;
}

function shouldShow(card) {
  const status = cardStatus(card);
  if (currentFilter === "known") return status === "know";
  if (currentFilter === "unknown") return status === "unknown";
  return true;
}

function renderCard(card) {
  const node = template.content.firstElementChild.cloneNode(true);
  const status = cardStatus(card);
  node.dataset.cardId = card.id;
  if (status === "know") node.classList.add("known");
  if (status === "unknown") node.classList.add("unknown-mark");
  node.querySelector(".page").textContent = card.page;
  node.querySelector(".topic").textContent = card.topic;
  node.querySelector(".prompt").textContent = card.prompt;
  node.querySelector(".answer").textContent = card.answer;
  const textarea = node.querySelector("textarea");
  node.querySelector(".know").addEventListener("click", () => submitReview(card, "know", textarea.value));
  node.querySelector(".unknown").addEventListener("click", () => submitReview(card, "unknown", textarea.value));
  node.querySelector(".image-toggle").addEventListener("click", () => {
    const fig = node.querySelector(".page-image");
    const img = fig.querySelector("img");
    img.src = card.image;
    fig.querySelector("figcaption").textContent = `${card.page} · ${card.source}`;
    fig.classList.toggle("hidden");
  });
  return node;
}

function renderSchedule() {
  const items = Object.entries(state.schedule)
    .map(([id, item]) => ({ id, ...item }))
    .sort((a, b) => String(a.nextDue).localeCompare(String(b.nextDue)))
    .slice(0, 8);
  scheduleList.innerHTML = "";
  if (!items.length) {
    scheduleList.innerHTML = "<div>还没有记录。点“知道/不知道”后会生成。</div>";
    return;
  }
  for (const item of items) {
    const card = window.REVIEW_CARDS.find(c => c.id === item.id);
    const div = document.createElement("div");
    div.textContent = `${item.nextDue} · ${card?.topic || item.id} · ${item.lastGrade === "know" ? "知道" : "不知道"}`;
    scheduleList.appendChild(div);
  }
}

function render() {
  totalCount.textContent = window.REVIEW_CARDS.length;
  doneCount.textContent = Object.keys(state.schedule).length;
  cardsEl.innerHTML = "";
  window.REVIEW_CARDS.filter(shouldShow).forEach(card => cardsEl.appendChild(renderCard(card)));
  renderSchedule();
}

filters.forEach(button => {
  button.addEventListener("click", () => {
    filters.forEach(b => b.classList.remove("active"));
    button.classList.add("active");
    currentFilter = button.dataset.filter;
    render();
  });
});

loadState().then(render);
