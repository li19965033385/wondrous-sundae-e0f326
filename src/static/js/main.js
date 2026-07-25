/**
 * AI Tools Hub v3 — Main JavaScript
 * Premium interactions, smooth animations, mobile nav
 */
(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {
    /* ── Intersection Observer for scroll animations ──── */
    const animateEls = document.querySelectorAll('.fade-in, .fade-in-left, .fade-in-right, .fade-in-scale');
    if (animateEls.length) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
      animateEls.forEach(el => observer.observe(el));
    }

    /* ── Mobile Navigation ────────────────────────────── */
    const navToggle = document.getElementById('navToggle');
    const navList = document.getElementById('navList');
    if (navToggle && navList) {
      navToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        navList.classList.toggle('active');
      });
      document.addEventListener('click', function(e) {
        if (!navToggle.contains(e.target) && !navList.contains(e.target)) {
          navList.classList.remove('active');
        }
      });
    }

    /* ── FAQ Accordion ────────────────────────────────── */
    document.querySelectorAll('.faq-question').forEach(function(q) {
      q.addEventListener('click', function() {
        const item = q.parentElement;
        const isActive = item.classList.contains('active');
        // Close all
        item.parentElement.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
        if (!isActive) item.classList.add('active');
      });
    });

    /* ── Search Overlay ───────────────────────────────── */
    const overlay = document.getElementById('searchOverlay');
    const searchInput = document.getElementById('searchInput');
    const searchClose = document.getElementById('searchClose');

    window.openSearch = function() {
      if (overlay) {
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
        if (searchInput) setTimeout(function() { searchInput.focus(); }, 150);
      }
    };

    if (searchClose && overlay) {
      searchClose.addEventListener('click', function() {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      });
      overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
          overlay.classList.remove('active');
          document.body.style.overflow = '';
        }
      });
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          overlay.classList.remove('active');
          document.body.style.overflow = '';
        }
      });
    }

    /* ── Smooth Scroll for TOC ────────────────────────── */
    document.addEventListener('click', function(e) {
      const tocLink = e.target.closest('#tocList a');
      if (tocLink) {
        e.preventDefault();
        const target = document.querySelector(tocLink.getAttribute('href'));
        if (target) {
          const offset = 100;
          const top = target.getBoundingClientRect().top + window.scrollY - offset;
          window.scrollTo({ top, behavior: 'smooth' });
          history.pushState(null, '', tocLink.href);
        }
      }
    });

    /* ── AdSense ──────────────────────────────────────── */
    if (typeof adsbygoogle !== 'undefined') {
      try {
        (adsbygoogle = window.adsbygoogle || []).push({});
      } catch (e) {
        // AdSense may not be available
      }
    }

    /* ── Video Category Filter ────────────────────────── */
    const videoCats = document.getElementById('videoCats');
    if (videoCats) {
      const btns = videoCats.querySelectorAll('.video-cat-btn');
      const cards = document.querySelectorAll('.video-card');
      btns.forEach(btn => {
        btn.addEventListener('click', function() {
          btns.forEach(b => b.classList.remove('active'));
          this.classList.add('active');
          const cat = this.dataset.cat;
          cards.forEach(card => {
            card.style.display = (cat === 'all' || card.dataset.cat === cat) ? '' : 'none';
          });
        });
      });
    }

    /* ── Gallery Category Filter ──────────────────────── */
    const galleryCats = document.getElementById('galleryCats');
    if (galleryCats) {
      const btns = galleryCats.querySelectorAll('.gallery-cat-btn');
      const items = document.querySelectorAll('.gallery-item');
      btns.forEach(btn => {
        btn.addEventListener('click', function() {
          btns.forEach(b => b.classList.remove('active'));
          this.classList.add('active');
          const cat = this.dataset.cat;
          items.forEach(item => {
            item.style.display = (cat === 'all' || item.dataset.cat === cat) ? '' : 'none';
          });
        });
      });
    }

    console.log('AI Tools Hub v3 initialized');
  });
})();
