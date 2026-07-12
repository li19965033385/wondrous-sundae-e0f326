/**
 * AI Tools Hub - Client-Side Search
 * Loads search-index.json and provides instant search
 */
(function() {
  'use strict';

  let searchIndex = [];
  let searchLoaded = false;

  // Load search index
  function loadSearchIndex() {
    if (searchLoaded) return Promise.resolve(searchIndex);
    return fetch('/search-index.json')
      .then(function(r) { return r.json(); })
      .then(function(data) {
        searchIndex = data;
        searchLoaded = true;
        return searchIndex;
      })
      .catch(function(err) {
        console.error('Search index load failed:', err);
        return [];
      });
  }

  // Search function
  function search(query) {
    if (!query || query.length < 1) return [];
    var q = query.toLowerCase();
    var results = [];
    var seen = new Set();

    searchIndex.forEach(function(item) {
      var score = 0;
      var titleMatch = item.title.toLowerCase().includes(q);
      var titleCnMatch = item.title_cn && item.title_cn.toLowerCase().includes(q);
      var descMatch = item.description && item.description.toLowerCase().includes(q);
      var descCnMatch = item.description_cn && item.description_cn.toLowerCase().includes(q);
      var bodyMatch = item.body && item.body.toLowerCase().includes(q);
      var tagMatch = item.tags && item.tags.some(function(t) { return t.toLowerCase().includes(q); });

      if (titleMatch || titleCnMatch) score += 10;
      if (descMatch || descCnMatch) score += 5;
      if (tagMatch) score += 3;
      if (bodyMatch) score += 1;

      if (score > 0 && !seen.has(item.slug)) {
        seen.add(item.slug);
        results.push({ item: item, score: score });
      }
    });

    results.sort(function(a, b) { return b.score - a.score; });
    return results.slice(0, 20).map(function(r) { return r.item; });
  }

  // Render results
  function renderResults(results, container) {
    if (results.length === 0) {
      container.innerHTML = '<div style="padding:20px;text-align:center;color:var(--text-muted)">未找到相关文章</div>';
      return;
    }

    var html = '';
    results.forEach(function(item) {
      html += '<a href="' + item.url + '" class="search-result-item" onclick="document.getElementById(\'searchOverlay\').classList.remove(\'active\')">';
      html += '<div class="search-result-title">' + (item.title_cn || item.title) + '</div>';
      html += '<div class="search-result-desc">' + (item.description_cn || item.description) + '</div>';
      html += '<div class="search-result-meta">' + item.date + ' · ' + (item.category || '') + '</div>';
      html += '</a>';
    });
    container.innerHTML = html;
  }

  // Initialize search
  document.addEventListener('DOMContentLoaded', function() {
    var searchInput = document.getElementById('searchInput');
    var searchResults = document.getElementById('searchResults');
    if (!searchInput || !searchResults) return;

    // Load index on focus
    var indexLoaded = false;
    searchInput.addEventListener('focus', function() {
      if (!indexLoaded) {
        loadSearchIndex();
        indexLoaded = true;
      }
    });

    // Search on input
    var debounceTimer;
    searchInput.addEventListener('input', function() {
      clearTimeout(debounceTimer);
      var query = searchInput.value.trim();
      if (query.length < 2) {
        searchResults.innerHTML = '<div style="padding:20px;text-align:center;color:var(--text-muted)">输入关键词搜索（至少2个字符）</div>';
        return;
      }
      debounceTimer = setTimeout(function() {
        if (!searchLoaded) {
          loadSearchIndex().then(function() {
            renderResults(search(query), searchResults);
          });
        } else {
          renderResults(search(query), searchResults);
        }
      }, 200);
    });
  });
})();
