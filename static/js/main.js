/* ───────────────────────────────────────────────────────────
   Personalized Learning System – frontend JS
   ─────────────────────────────────────────────────────────── */

const API = "";                      // same-origin; no prefix needed
const LIKED_KEY = "pls_liked_posts"; // localStorage key

// ── State ──────────────────────────────────────────────────
let state = {
  posts: [],
  categories: [],
  selectedCategory: null,
  selectedDifficulty: null,
  likedPosts: new Set(JSON.parse(localStorage.getItem(LIKED_KEY) || "[]")),
};

// ── Helpers ────────────────────────────────────────────────
function saveLiked() {
  localStorage.setItem(LIKED_KEY, JSON.stringify([...state.likedPosts]));
}

function difficultyBadgeClass(d) {
  return d === "进阶" ? "badge-hard" : d === "中级" ? "badge-mid" : "badge-easy";
}

// ── API calls ──────────────────────────────────────────────
async function fetchJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function loadCategories() {
  state.categories = await fetchJSON(`${API}/api/categories`);
}

async function loadPosts() {
  const params = new URLSearchParams();
  if (state.selectedCategory) params.set("category_id", state.selectedCategory);
  if (state.selectedDifficulty) params.set("difficulty", state.selectedDifficulty);
  state.posts = await fetchJSON(`${API}/api/posts?${params}`);
}

// ── Like toggle ────────────────────────────────────────────
async function toggleLike(postId, event) {
  event.stopPropagation(); // don't open modal when clicking like

  const btn = event.currentTarget;
  const wasLiked = state.likedPosts.has(postId);

  // Optimistic UI
  const countSpan = btn.querySelector(".like-count");
  let count = parseInt(countSpan.textContent, 10);
  if (wasLiked) {
    btn.classList.remove("liked");
    count = Math.max(0, count - 1);
    state.likedPosts.delete(postId);
  } else {
    btn.classList.add("liked");
    count += 1;
    state.likedPosts.add(postId);
  }
  countSpan.textContent = count;
  saveLiked();

  // Sync with server
  try {
    const res = await fetch(`${API}/api/posts/${postId}/like`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ liked: wasLiked }),
    });
    if (!res.ok) throw new Error("server error");
    const data = await res.json();
    countSpan.textContent = data.like_count;

    // Keep all like buttons for this post in sync
    document
      .querySelectorAll(`.like-btn[data-id="${postId}"] .like-count`)
      .forEach(el => { el.textContent = data.like_count; });
  } catch {
    // Revert optimistic update on failure
    if (wasLiked) {
      btn.classList.add("liked");
      state.likedPosts.add(postId);
    } else {
      btn.classList.remove("liked");
      state.likedPosts.delete(postId);
    }
    countSpan.textContent = wasLiked ? count + 1 : count - 1;
    saveLiked();
  }
}

// ── Build DOM elements ─────────────────────────────────────
function buildLikeBtn(post) {
  const liked = state.likedPosts.has(post.id);
  const btn = document.createElement("button");
  btn.className = `like-btn${liked ? " liked" : ""}`;
  btn.setAttribute("data-id", post.id);
  btn.setAttribute("aria-label", liked ? "取消点赞" : "点赞");
  btn.setAttribute("aria-pressed", liked ? "true" : "false");
  btn.innerHTML = `<span class="heart">❤</span><span class="like-count">${post.like_count}</span>`;
  btn.addEventListener("click", e => toggleLike(post.id, e));
  return btn;
}

function buildCard(post) {
  const card = document.createElement("article");
  card.className = "post-card";
  card.setAttribute("tabindex", "0");
  card.setAttribute("role", "button");
  card.setAttribute("aria-label", `打开课程：${post.title}`);

  const cat = post.category || { icon: "📚", name: "其他" };
  const badgeClass = difficultyBadgeClass(post.difficulty);

  card.innerHTML = `
    <div class="card-body">
      <div class="card-meta">
        <span class="badge badge-category">${cat.icon} ${cat.name}</span>
        <span class="badge ${badgeClass}">${post.difficulty}</span>
      </div>
      <h2 class="card-title">${escapeHtml(post.title)}</h2>
      <p class="card-summary">${escapeHtml(post.summary)}</p>
    </div>
    <div class="card-footer">
      <div class="card-info">
        <span>✍ ${escapeHtml(post.author)}</span>
        <span>⏱ ${post.duration} 分钟</span>
        <span>👁 ${post.view_count}</span>
      </div>
    </div>`;

  // Append like button into footer
  card.querySelector(".card-footer").prepend(buildLikeBtn(post));

  card.addEventListener("click", () => openModal(post.id));
  card.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") openModal(post.id); });

  return card;
}

function renderPosts() {
  const grid = document.getElementById("posts-grid");
  grid.innerHTML = "";

  if (state.posts.length === 0) {
    grid.innerHTML = `<p class="loading-spinner">暂无相关内容，换个筛选条件试试吧～</p>`;
    return;
  }

  const frag = document.createDocumentFragment();
  state.posts.forEach(p => frag.appendChild(buildCard(p)));
  grid.appendChild(frag);
}

// ── Categories filter chips ────────────────────────────────
function renderCategoryChips() {
  const container = document.getElementById("category-filters");
  state.categories.forEach(cat => {
    const btn = document.createElement("button");
    btn.className = "chip";
    btn.dataset.category = cat.id;
    btn.textContent = `${cat.icon} ${cat.name}`;
    container.appendChild(btn);
  });
}

// ── Modal ──────────────────────────────────────────────────
async function openModal(postId) {
  try {
    const post = await fetchJSON(`${API}/api/posts/${postId}`);
    const overlay = document.getElementById("modal-overlay");
    const body = document.getElementById("modal-body");
    const cat = post.category || { icon: "📚", name: "其他" };
    const badgeClass = difficultyBadgeClass(post.difficulty);

    body.innerHTML = `
      <div class="modal-meta">
        <span class="badge badge-category">${cat.icon} ${cat.name}</span>
        <span class="badge ${badgeClass}">${post.difficulty}</span>
      </div>
      <h2 class="modal-title" id="modal-title">${escapeHtml(post.title)}</h2>
      <p class="modal-summary">${escapeHtml(post.summary)}</p>
      <hr class="modal-divider" />
      <p style="line-height:1.8;color:#374151">${escapeHtml(post.content)}</p>
      <div class="modal-footer">
        <div class="card-info">
          <span>✍ ${escapeHtml(post.author)}</span>
          <span>⏱ ${post.duration} 分钟</span>
          <span>👁 ${post.view_count}</span>
        </div>
      </div>`;

    body.querySelector(".modal-footer").prepend(buildLikeBtn(post));
    overlay.hidden = false;
    document.getElementById("modal-close").focus();
  } catch (e) {
    console.error("Failed to load post", e);
  }
}

function closeModal() {
  document.getElementById("modal-overlay").hidden = true;
}

// ── Filter wiring ──────────────────────────────────────────
function wireFilters() {
  document.addEventListener("click", async e => {
    const chip = e.target.closest(".chip");
    if (!chip) return;

    if ("category" in chip.dataset) {
      document
        .querySelectorAll("#category-filters .chip")
        .forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      state.selectedCategory = chip.dataset.category || null;
    }

    if ("difficulty" in chip.dataset) {
      document
        .querySelectorAll("[data-difficulty]")
        .forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      state.selectedDifficulty = chip.dataset.difficulty || null;
    }

    await loadPosts();
    renderPosts();
  });
}

// ── Modal close ────────────────────────────────────────────
function wireModal() {
  document.getElementById("modal-close").addEventListener("click", closeModal);
  document.getElementById("modal-overlay").addEventListener("click", e => {
    if (e.target === e.currentTarget) closeModal();
  });
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") closeModal();
  });
}

// ── Tiny XSS guard ─────────────────────────────────────────
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ── Boot ───────────────────────────────────────────────────
async function main() {
  try {
    await Promise.all([loadCategories(), loadPosts()]);
    renderCategoryChips();
    renderPosts();
    wireFilters();
    wireModal();
  } catch (e) {
    document.getElementById("posts-grid").innerHTML =
      `<p class="loading-spinner">加载失败，请刷新页面重试。</p>`;
    console.error(e);
  }
}

main();
