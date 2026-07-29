/* The Stuff Unseen — Flashcard stats (trang /stats/)
 * Đọc tiến độ từ localStorage (su_flashcards_v1) + decks.json để hiển thị.
 * Không backend. Chỉ đọc, không ghi (trừ nút Reset).
 */
(function () {
  "use strict";

  var FEED = "/assets/decks.json";
  var LS_KEY = "su_flashcards_v1";

  var root = document.getElementById("fc-stats");
  if (!root) return;

  var store = loadStore();

  fetch(FEED, { cache: "no-cache" })
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var all = (data || []).filter(function (c) { return c && c.title; });
      all.forEach(function (c) { if (!c.slug) c.slug = slugify(c.title); });
      render(all);
    })
    .catch(function () {
      root.innerHTML = '<p class="fc-loading">Không tải được dữ liệu thẻ.</p>';
    });

  function loadStore() {
    try {
      var raw = localStorage.getItem(LS_KEY);
      if (raw) { var s = JSON.parse(raw); s.cards = s.cards || {}; s.history = s.history || {}; return s; }
    } catch (e) {}
    return { cards: {}, history: {} };
  }

  function render(all) {
    var total = all.length;
    var known = 0, review = 0, seen = 0, dueToday = 0, reps = 0;
    var now = Date.now();
    all.forEach(function (c) {
      var s = store.cards[c.slug];
      if (!s) return;
      if (s.seen) seen++;
      if (s.box === "known") known++;
      if (s.box === "review") review++;
      if (s.due && s.due <= now) dueToday++;
      reps += s.reps || 0;
    });
    var mastery = total ? Math.round(known / total * 100) : 0;
    var streak = calcStreak(store.history);
    var studyDays = Object.keys(store.history).length;

    // per-category
    var cat = {};
    all.forEach(function (c) {
      var k = c.category || "Uncategorized";
      if (!cat[k]) cat[k] = { total: 0, known: 0 };
      cat[k].total++;
      var s = store.cards[c.slug];
      if (s && s.box === "known") cat[k].known++;
    });

    var empty = seen === 0;

    var html = "";
    // KPI cards
    html += '<div class="fc-kpis">' +
      kpi("🔥", streak, "ngày streak") +
      kpi("✓", known, "đã thuộc") +
      kpi("%", mastery + "%", "mastery") +
      kpi("⏰", dueToday, "cần ôn hôm nay") +
      kpi("👁", seen + "/" + total, "đã xem") +
      kpi("📅", studyDays, "ngày đã học") +
      "</div>";

    // overall bar
    html += '<div class="fc-stats-block">' +
      '<div class="fc-stats-row"><span>Tiến độ tổng</span><span>' + known + " / " + total + "</span></div>" +
      bar(mastery) + "</div>";

    // per category
    html += '<div class="fc-stats-block"><h3 class="fc-stats-h">Theo chủ đề</h3>';
    Object.keys(cat).sort().forEach(function (k) {
      var c = cat[k];
      var pct = c.total ? Math.round(c.known / c.total * 100) : 0;
      html += '<div class="fc-stats-row"><span>' + esc(k) + '</span><span>' + c.known + " / " + c.total + " (" + pct + "%)</span></div>" + bar(pct);
    });
    html += "</div>";

    // 14-day activity
    html += '<div class="fc-stats-block"><h3 class="fc-stats-h">14 ngày gần đây</h3>' + heatmap(store.history) + "</div>";

    // actions
    html += '<div class="fc-stats-actions">' +
      '<a class="fc-btn fc-btn-known" href="/study/">Học tiếp →</a>' +
      '<button class="fc-link fc-danger" id="fc-stats-reset" type="button">Reset tiến độ</button></div>';

    if (empty) {
      html = '<div class="fc-empty"><p class="fc-done-emoji">🌱</p>' +
        '<h3>Chưa có dữ liệu học</h3><p>Bắt đầu ở <a href="/study/">/study/</a>, thống kê sẽ hiện ở đây.</p></div>' + html;
    }

    root.innerHTML = html;

    var rb = document.getElementById("fc-stats-reset");
    if (rb) rb.addEventListener("click", function () {
      if (!window.confirm("Xoá toàn bộ tiến độ học?")) return;
      try { localStorage.removeItem(LS_KEY); } catch (e) {}
      store = { cards: {}, history: {} };
      render(all);
    });
  }

  function kpi(icon, val, label) {
    return '<div class="fc-kpi"><div class="fc-kpi-icon">' + icon + '</div>' +
      '<div class="fc-kpi-val">' + esc(val) + '</div>' +
      '<div class="fc-kpi-label">' + esc(label) + '</div></div>';
  }
  function bar(pct) {
    return '<div class="fc-progress-bar"><span style="width:' + pct + '%"></span></div>';
  }

  function heatmap(history) {
    var cells = "";
    for (var i = 13; i >= 0; i--) {
      var d = new Date(); d.setDate(d.getDate() - i);
      var key = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
      var n = history[key] || 0;
      var lvl = n === 0 ? 0 : n < 3 ? 1 : n < 8 ? 2 : 3;
      cells += '<span class="fc-cell lvl' + lvl + '" title="' + key + ": " + n + ' thẻ"></span>';
    }
    return '<div class="fc-heatmap">' + cells + "</div>";
  }

  function calcStreak(history) {
    var d = new Date();
    function key(dt) { return dt.getFullYear() + "-" + String(dt.getMonth() + 1).padStart(2, "0") + "-" + String(dt.getDate()).padStart(2, "0"); }
    // streak tính đến hôm nay hoặc hôm qua
    if (!history[key(d)]) {
      d.setDate(d.getDate() - 1);
      if (!history[key(d)]) return 0;
    }
    var streak = 0;
    while (history[key(d)]) { streak++; d.setDate(d.getDate() - 1); }
    return streak;
  }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function slugify(s) {
    return String(s).toLowerCase().trim()
      .replace(/[^\w\s-]/g, "").replace(/[\s_-]+/g, "-").replace(/^-+|-+$/g, "");
  }
})();
