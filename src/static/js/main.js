(function() {
  'use strict';
  document.addEventListener('DOMContentLoaded', function() {
    var nT = document.getElementById('navToggle');
    var nL = document.getElementById('navList');
    if (nT && nL) {
      nT.addEventListener('click', function(e) { e.stopPropagation(); nL.classList.toggle('active'); });
      document.addEventListener('click', function(e) { if (!nT.contains(e.target) && !nL.contains(e.target)) nL.classList.remove('active'); });
    }
    document.querySelectorAll('.nav-dropdown').forEach(function(dropdown) {
      var trigger = dropdown.querySelector('.dropdown-trigger');
      if (!trigger) return;
      trigger.addEventListener('click', function(e) {
        e.stopPropagation();
        var opening = !dropdown.classList.contains('open');
        document.querySelectorAll('.nav-dropdown.open').forEach(function(item) {
          item.classList.remove('open');
          var itemTrigger = item.querySelector('.dropdown-trigger');
          if (itemTrigger) itemTrigger.setAttribute('aria-expanded', 'false');
        });
        dropdown.classList.toggle('open', opening);
        trigger.setAttribute('aria-expanded', opening ? 'true' : 'false');
      });
    });
    document.addEventListener('click', function() {
      document.querySelectorAll('.nav-dropdown.open').forEach(function(item) {
        item.classList.remove('open');
        var trigger = item.querySelector('.dropdown-trigger');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
      });
    });
    document.querySelectorAll('.language-menu a').forEach(function(link) {
      var prefetched = false;
      function prefetchLanguage() {
        if (prefetched || link.classList.contains('active')) return;
        prefetched = true;
        var preload = document.createElement('link');
        preload.rel = 'prefetch';
        preload.href = link.href;
        preload.as = 'document';
        document.head.appendChild(preload);
      }
      link.addEventListener('pointerenter', prefetchLanguage, {once: true});
      link.addEventListener('focus', prefetchLanguage, {once: true});
      link.addEventListener('click', function(e) {
        if (link.classList.contains('active')) { e.preventDefault(); return; }
        e.preventDefault();
        document.body.classList.add('language-switching');
        window.setTimeout(function() { window.location.assign(link.href); }, 90);
      });
    });
    document.querySelectorAll('.faq-question').forEach(function(q) {
      q.addEventListener('click', function() {
        var item = q.parentElement;
        var active = item.classList.contains('active');
        item.parentElement.querySelectorAll('.faq-item').forEach(function(i) { i.classList.remove('active'); });
        if (!active) item.classList.add('active');
      });
    });
    var overlay = document.getElementById('searchOverlay');
    var sI = document.getElementById('searchInput');
    var sC = document.getElementById('searchClose');
    window.openSearch = function() {
      if (overlay) { overlay.classList.add('active'); document.body.style.overflow = 'hidden'; if (sI) setTimeout(function() { sI.focus(); }, 100); }
    };
    if (sC && overlay) {
      sC.addEventListener('click', function() { overlay.classList.remove('active'); document.body.style.overflow = ''; });
      overlay.addEventListener('click', function(e) { if (e.target === overlay) { overlay.classList.remove('active'); document.body.style.overflow = ''; } });
      document.addEventListener('keydown', function(e) { if (e.key === 'Escape') { overlay.classList.remove('active'); document.body.style.overflow = ''; } });
    }
    var vC = document.getElementById('videoCats');
    if (vC) {
      var btns = vC.querySelectorAll('.video-cat-btn');
      var cards = document.querySelectorAll('.video-card');
      btns.forEach(function(b) {
        b.addEventListener('click', function() {
          btns.forEach(function(x) { x.classList.remove('active'); });
          this.classList.add('active');
          var cat = this.dataset.cat;
          cards.forEach(function(c) { c.style.display = (cat === 'all' || c.dataset.cat === cat) ? '' : 'none'; });
        });
      });
    }
    var gC = document.getElementById('galleryCats');
    if (gC) {
      var btns = gC.querySelectorAll('.gallery-cat-btn');
      var items = document.querySelectorAll('.gallery-item');
      btns.forEach(function(b) {
        b.addEventListener('click', function() {
          btns.forEach(function(x) { x.classList.remove('active'); });
          this.classList.add('active');
          var cat = this.dataset.cat;
          items.forEach(function(i) { i.style.display = (cat === 'all' || i.dataset.cat === cat) ? '' : 'none'; });
        });
      });
    }
  });
})();
