/* The Stuff Unseen — Flashcard layer (Hướng A)
 * Client-side study mode: flip, shuffle, keyboard nav, Leitner/SM-2-lite SRS.
 * State persisted in localStorage. No backend.
 */
(function () {
  "use strict";

  var FEED = "/assets/decks.json";
  var LS_KEY = "su_flashcards_v1";

  // ---- state ----
  var ALL = [];          // all cards from feed
  var DECK = [];         // current session cards
  var idx = 0;           // current index in DECK
  var store = load();    // persisted progress

  // ---- dom ----
  var $ = function (id) { return document.getElementById(id); };
  var elDecks = $("fc-decks");
  var elSession = $("fc-session");
  var elStage = $("fc-stage");
  var elToday = $("fc-today");
  var elTodayCard = $("fc-today-card");

  if (!elDecks) return; // not on study page

  // ---- boot ----
  fetch(FEED, { cache: "no-cache" })
    .then(function (r) { return r.json(); })
    .then(function (data) {
      ALL = (data || []).filter(function (c) { return c && c.title; });
      ALL.forEach(function (c) { if (!c.slug) c.slug = slugify(c.title); });
      renderDecks();
      renderToday();
      bindGlobalKeys();
    })
    .catch(function () {
      elDecks.innerHTML = '<p class="fc-loading">Không tải được thẻ. Kiểm tra /assets/decks.json.</p>';
    });

  // ---- persistence ----
  function load() {
    try {
      var raw = localStorage.getItem(LS_KEY);
      if (raw) {
        var s = JSON.parse(raw);
        if (!s.history) s.history = {};
        return s;
      }
    } catch (e) {}
    return { cards: {}, lastDeck: null, history: {}, updatedAt: Date.now() };
  }
  function todayKey() {
    var d = new Date();
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  }
  function recordDay() {
    if (!store.history) store.history = {};
    var k = todayKey();
    store.history[k] = (store.history[k] || 0) + 1;
  }
  function save() {
    store.updatedAt = Date.now();
    try { localStorage.setItem(LS_KEY, JSON.stringify(store)); } catch (e) {}
  }
  function cardState(slug) {
    return store.cards[slug] || { box: null, ease: 2.5, interval: 0, due: 0, reps: 0, seen: false };
  }

  // ---- deck picker ----
  function decksList() {
    var byCat = {};
    ALL.forEach(function (c) { byCat[c.category] = (byCat[c.category] || 0) + 1; });
    var out = [{ id: "all", label: "Tất cả", count: ALL.length }];
    Object.keys(byCat).sort().forEach(function (cat) {
      out.push({ id: "cat:" + cat, label: cat, count: byCat[cat] });
    });
    // Ôn hôm nay (SRS due)
    var due = ALL.filter(function (c) {
      var s = store.cards[c.slug];
      return s && s.due && s.due <= Date.now();
    }).length;
    if (due > 0) out.splice(1, 0, { id: "due", label: "⏰ Cần ôn hôm nay", count: due });
    return out;
  }

  function renderDecks() {
    var known = countKnown();
    var html = decksList().map(function (d) {
      return '<button class="fc-deck" type="button" data-deck="' + esc(d.id) + '">' +
        '<span class="fc-deck-label">' + esc(d.label) + '</span>' +
        '<span class="fc-deck-count">' + d.count + ' thẻ</span></button>';
    }).join("");
    elDecks.innerHTML =
      '<div class="fc-decks-summary">Bạn đã thuộc <b>' + known + '</b> / ' + ALL.length + ' thẻ.</div>' +
      '<div class="fc-decks-grid">' + html + "</div>";
    Array.prototype.forEach.call(elDecks.querySelectorAll(".fc-deck"), function (b) {
      b.addEventListener("click", function () { startDeck(b.getAttribute("data-deck")); });
    });
  }

  function countKnown() {
    var n = 0;
    Object.keys(store.cards).forEach(function (k) { if (store.cards[k].box === "known") n++; });
    return n;
  }

  // ---- session ----
  function startDeck(id) {
    store.lastDeck = id;
    if (id === "all") DECK = ALL.slice();
    else if (id === "due") DECK = ALL.filter(function (c) {
      var s = store.cards[c.slug]; return s && s.due && s.due <= Date.now();
    });
    else { var cat = id.slice(4); DECK = ALL.filter(function (c) { return c.category === cat; }); }
    // ưu tiên thẻ khó / chưa thuộc trước
    DECK.sort(function (a, b) {
      var ka = cardState(a.slug).box === "known" ? 1 : 0;
      var kb = cardState(b.slug).box === "known" ? 1 : 0;
      if (ka !== kb) return ka - kb;
      return (b.difficulty || 2) - (a.difficulty || 2);
    });
    if (!DECK.length) return;
    idx = 0;
    save();
    elDecks.hidden = true;
    if (elToday) elToday.hidden = true;
    elSession.hidden = false;
    renderCard();
    elStage.focus();
  }

  function renderCard() {
    var c = DECK[idx];
    if (!c) return;
    elStage.innerHTML = cardHTML(c);
    var card = elStage.querySelector(".fc-card");
    card.addEventListener("click", function (e) {
      if (e.target.closest("a")) return; // don't flip when clicking links
      card.classList.toggle("is-flipped");
    });
    // connected links
    Array.prototype.forEach.call(elStage.querySelectorAll("[data-goto]"), function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        gotoTitle(a.getAttribute("data-goto"), a.getAttribute("href"));
      });
    });
    // mark seen
    var st = cardState(c.slug); st.seen = true; store.cards[c.slug] = st; save();
    updateProgress();
  }

  function cardHTML(c) {
    var conn = (c.connected || []).map(function (t) {
      var tgt = ALL.filter(function (x) { return x.title === t; })[0];
      var href = tgt ? tgt.url : "#";
      return '<a class="fc-chip" data-goto="' + esc(t) + '" href="' + esc(href) + '">' + esc(t) + "</a>";
    }).join("");
    var st = cardState(c.slug);
    var flipped = st.box === "known" ? "" : "";
    return '' +
      '<div class="fc-card ' + flipped + '">' +
        '<div class="fc-card-inner">' +
          '<div class="fc-face fc-front">' +
            '<span class="fc-cat">' + esc(c.category || "") + '</span>' +
            '<p class="fc-front-text">' + esc(c.front || c.title) + '</p>' +
            '<span class="fc-flip-hint">Nhấn để lật ↻</span>' +
          '</div>' +
          '<div class="fc-face fc-back">' +
            '<h3 class="fc-back-title">' + esc(c.title) + '</h3>' +
            '<p class="fc-back-text">' + esc(c.back || "") + '</p>' +
            (c.strategy ? '<p class="fc-strategy"><b>Áp dụng:</b> ' + esc(c.strategy) + '</p>' : "") +
            (conn ? '<div class="fc-connected"><span class="fc-connected-label">Liên quan</span>' + conn + "</div>" : "") +
            (c.source ? '<a class="fc-source" href="' + esc(c.source) + '" target="_blank" rel="noopener">Nguồn ↗</a>' : "") +
            (c.url ? '<a class="fc-source" href="' + esc(c.url) + '">Trang chi tiết →</a>' : "") +
          '</div>' +
        '</div>' +
      '</div>';
  }

  function updateProgress() {
    var total = DECK.length;
    var pos = idx + 1;
    var knownInDeck = DECK.filter(function (c) { return cardState(c.slug).box === "known"; }).length;
    var fill = $("fc-progress-fill");
    if (fill) fill.style.width = (pos / total * 100) + "%";
    var t = $("fc-progress-text"); if (t) t.textContent = pos + " / " + total;
    var k = $("fc-known-count"); if (k) k.textContent = "✓ " + knownInDeck + " đã thuộc";
  }

  // ---- grading (SM-2 lite) ----
  function grade(good) {
    var c = DECK[idx]; if (!c) return;
    var s = cardState(c.slug);
    var DAY = 86400000;
    if (good) {
      s.box = "known"; s.reps = (s.reps || 0) + 1;
      s.interval = s.reps === 1 ? 1 : s.reps === 2 ? 3 : Math.round((s.interval || 1) * (s.ease || 2.5));
      s.due = Date.now() + s.interval * DAY;
    } else {
      s.box = "review"; s.reps = 0; s.interval = 0;
      s.ease = Math.max(1.3, (s.ease || 2.5) - 0.2);
      s.due = Date.now();
    }
    s.seen = true;
    store.cards[c.slug] = s; recordDay(); save();
    next();
  }

  function next() {
    if (idx < DECK.length - 1) { idx++; renderCard(); }
    else finish();
  }
  function prev() { if (idx > 0) { idx--; renderCard(); } }

  function finish() {
    var known = DECK.filter(function (c) { return cardState(c.slug).box === "known"; }).length;
    elStage.innerHTML = '<div class="fc-done">' +
      '<p class="fc-done-emoji">🔥</p>' +
      '<h3>Xong deck!</h3>' +
      '<p>Bạn đã thuộc ' + known + ' / ' + DECK.length + ' thẻ trong deck này.</p>' +
      '<button class="fc-btn fc-btn-known" id="fc-again" type="button">Học lại</button></div>';
    var again = $("fc-again");
    if (again) again.addEventListener("click", function () { idx = 0; renderCard(); });
  }

  function shuffle() {
    for (var i = DECK.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = DECK[i]; DECK[i] = DECK[j]; DECK[j] = tmp;
    }
    idx = 0; renderCard();
  }

  function gotoTitle(title, href) {
    var inDeck = -1;
    for (var i = 0; i < DECK.length; i++) { if (DECK[i].title === title) { inDeck = i; break; } }
    if (inDeck >= 0) { idx = inDeck; renderCard(); }
    else if (href && href !== "#") window.location.href = href;
  }

  function exitSession() {
    elSession.hidden = true;
    elDecks.hidden = false;
    if (elToday) elToday.hidden = false;
    renderDecks();
  }

  function resetProgress() {
    if (!window.confirm("Xoá toàn bộ tiến độ học?")) return;
    store = { cards: {}, lastDeck: null, history: {}, updatedAt: Date.now() };
    save();
    exitSession();
    renderToday();
  }

  // ---- card of the day ----
  function renderToday() {
    if (!elToday || !ALL.length) return;
    var day = new Date();
    var seed = day.getFullYear() * 10000 + (day.getMonth() + 1) * 100 + day.getDate();
    var c = ALL[seed % ALL.length];
    elTodayCard.innerHTML = cardHTML(c);
    elToday.hidden = false;
    var card = elTodayCard.querySelector(".fc-card");
    card.addEventListener("click", function (e) {
      if (e.target.closest("a")) return;
      card.classList.toggle("is-flipped");
    });
    Array.prototype.forEach.call(elTodayCard.querySelectorAll("[data-goto]"), function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        window.location.href = a.getAttribute("href");
      });
    });
  }

  // ---- controls & keys ----
  function bindGlobalKeys() {
    on("fc-next", next); on("fc-prev", prev);
    on("fc-known", function () { grade(true); });
    on("fc-review", function () { grade(false); });
    on("fc-shuffle", shuffle);
    on("fc-exit", exitSession);
    on("fc-reset", resetProgress);

    document.addEventListener("keydown", function (e) {
      if (elSession.hidden) return;
      var card = elStage.querySelector(".fc-card");
      switch (e.key) {
        case " ": case "Enter":
          if (card) { e.preventDefault(); card.classList.toggle("is-flipped"); } break;
        case "ArrowRight": next(); break;
        case "ArrowLeft": prev(); break;
        case "1": grade(false); break;
        case "2": grade(true); break;
        case "s": case "S": shuffle(); break;
      }
    });
  }
  function on(id, fn) { var el = $(id); if (el) el.addEventListener("click", fn); }

  // ---- utils ----
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
