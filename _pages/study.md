---
layout: default
title: Study
permalink: /study/
excerpt: "Học tri thức dạng flashcard — lật thẻ, xáo bài, đánh dấu đã thuộc."
image: /assets/img/the-flame.png
---

<section class="fc-study pt-20" aria-label="Flashcards">

  <header class="fc-head">
    <h1 class="header-title">Study.</h1>
    <p class="fc-sub">Lật thẻ để học. Đánh dấu <b>Đã thuộc</b> / <b>Cần ôn</b> — tiến độ lưu ngay trên trình duyệt của bạn.</p>
  </header>

  <!-- Card of the day -->
  <div class="fc-today" id="fc-today" hidden>
    <div class="fc-today-label">🔥 Thẻ hôm nay</div>
    <div id="fc-today-card"></div>
  </div>

  <!-- Deck picker -->
  <div class="fc-decks" id="fc-decks" role="tablist" aria-label="Chọn deck">
    <p class="fc-loading">Đang tải thẻ…</p>
  </div>

  <!-- Study session -->
  <div class="fc-session" id="fc-session" hidden>
    <div class="fc-progress">
      <div class="fc-progress-bar"><span id="fc-progress-fill"></span></div>
      <div class="fc-progress-meta">
        <span id="fc-progress-text">0 / 0</span>
        <span id="fc-known-count" class="fc-known-badge">✓ 0 đã thuộc</span>
      </div>
    </div>

    <div class="fc-stage" id="fc-stage" tabindex="0" aria-live="polite">
      <!-- flip card injected here -->
    </div>

    <div class="fc-controls">
      <button class="fc-btn" id="fc-prev" type="button" title="Trước (←)">‹ Trước</button>
      <button class="fc-btn fc-btn-review" id="fc-review" type="button" title="Cần ôn (1)">↺ Cần ôn</button>
      <button class="fc-btn fc-btn-known" id="fc-known" type="button" title="Đã thuộc (2)">✓ Đã thuộc</button>
      <button class="fc-btn" id="fc-next" type="button" title="Sau (→)">Sau ›</button>
    </div>

    <div class="fc-session-actions">
      <button class="fc-link" id="fc-shuffle" type="button">🔀 Xáo bài (S)</button>
      <button class="fc-link" id="fc-exit" type="button">← Đổi deck</button>
      <a class="fc-link" href="/stats/">📊 Thống kê</a>
      <button class="fc-link fc-danger" id="fc-reset" type="button">Reset tiến độ</button>
    </div>
    <p class="fc-hint">Phím tắt: <b>Space</b> lật thẻ · <b>←/→</b> chuyển thẻ · <b>1</b> = Cần ôn · <b>2</b> = Đã thuộc</p>
  </div>

  <noscript>
    <p class="fc-sub">Study mode cần JavaScript. Bạn vẫn có thể duyệt từng thẻ trong <a href="/archive/">Archive</a>.</p>
  </noscript>

</section>

<script src="/assets/js/flashcards.js" defer></script>
