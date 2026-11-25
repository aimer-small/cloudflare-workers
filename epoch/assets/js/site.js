/* 裂界纪 2.0 · 双轨纪 —— 交互 */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 滚动揭示 ---------- */
  var items = document.querySelectorAll('[data-reveal]');

  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-in');
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });

    items.forEach(function (el) { io.observe(el); });
  }

  /* ---------- 顶栏：下滚隐藏，上滚出现 ---------- */
  var bar = document.getElementById('topbar');
  var lastY = window.scrollY;
  var ticking = false;

  function onScroll() {
    var y = window.scrollY;
    if (bar) {
      if (y > 160 && y > lastY + 6) {
        bar.classList.add('is-hidden');
      } else if (y < lastY - 6 || y < 160) {
        bar.classList.remove('is-hidden');
      }
    }
    lastY = y;
    ticking = false;
  }

  window.addEventListener('scroll', function () {
    if (!ticking) {
      window.requestAnimationFrame(onScroll);
      ticking = true;
    }
  }, { passive: true });

  /* ---------- 导航当前章节高亮 ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
  var targets = links.map(function (a) {
    return document.querySelector(a.getAttribute('href'));
  }).filter(Boolean);

  if (targets.length && 'IntersectionObserver' in window) {
    var navIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) {
          var on = a.getAttribute('href') === '#' + e.target.id;
          a.style.color = on ? 'var(--ink)' : '';
          a.style.borderBottomColor = on ? 'var(--line)' : '';
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    targets.forEach(function (t) { navIo.observe(t); });
  }

  /* ---------- 图片加载失败兜底 ---------- */
  document.querySelectorAll('img').forEach(function (img) {
    img.addEventListener('error', function () {
      img.style.background = 'var(--paper-2)';
      img.style.minHeight = '12rem';
      img.alt = (img.alt || '') + '（图像未能加载）';
    });
  });
})();