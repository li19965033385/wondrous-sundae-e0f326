/**
 * AI Tools Hub - Main JavaScript
 * Navigation, mobile menu, FAQ accordion, search overlay
 */
(function() {
  'use strict';

  // DOM Ready
  document.addEventListener('DOMContentLoaded', function() {

    // ── Mobile Navigation Toggle ──────────────────────────
    const navToggle = document.getElementById('navToggle');
    const navList = document.getElementById('navList');
    if (navToggle && navList) {
      navToggle.addEventListener('click', function() {
        navList.classList.toggle('active');
        navToggle.classList.toggle('active');
      });
      // Close on outside click
      document.addEventListener('click', function(e) {
        if (!navToggle.contains(e.target) && !navList.contains(e.target)) {
          navList.classList.remove('active');
          navToggle.classList.remove('active');
        }
      });
    }

    // ── FAQ Accordion ─────────────────────────────────────
    document.querySelectorAll('.faq-question').forEach(function(q) {
      q.addEventListener('click', function() {
        const item = q.parentElement;
        item.classList.toggle('active');
      });
    });

    // ── Search Overlay ────────────────────────────────────
    const overlay = document.getElementById('searchOverlay');
    const searchInput = document.getElementById('searchInput');
    const searchClose = document.getElementById('searchClose');

    window.openSearch = function() {
      if (overlay) {
        overlay.classList.add('active');
        if (searchInput) setTimeout(function() { searchInput.focus(); }, 100);
      }
    };

    if (searchClose && overlay) {
      searchClose.addEventListener('click', function() {
        overlay.classList.remove('active');
      });
      overlay.addEventListener('click', function(e) {
        if (e.target === overlay) overlay.classList.remove('active');
      });
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') overlay.classList.remove('active');
      });
    }

    // Hero search button
    const heroSearchBtn = document.querySelector('.hero-search-btn');
    if (heroSearchBtn) {
      heroSearchBtn.addEventListener('click', window.openSearch);
    }
    const heroSearchInput = document.querySelector('.hero-search-input');
    if (heroSearchInput) {
      heroSearchInput.addEventListener('focus', window.openSearch);
    }

    // ── Smooth Scroll for TOC ─────────────────────────────
    document.addEventListener('click', function(e) {
      if (e.target.matches('#tocList a')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.pushState(null, '', e.target.href);
        }
      }
    });

    // ── Lazy Load Adsense ─────────────────────────────────
    if (typeof adsbygoogle !== 'undefined') {
      try {
        (adsbygoogle = window.adsbygoogle || []).push({});
      } catch (e) {
        console.log('AdSense not ready yet');
      }
    }

    console.log('AI Tools Hub initialized');
  });
})();
