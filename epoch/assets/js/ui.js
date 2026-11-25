/* ============================================================
   裂界纪 · ui.js
   导航 / 滚动揭示 / 逐字 / 视差
   ============================================================ */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 导航 ---------- */
  var nav = document.querySelector('.nav');
  var links = document.querySelector('.nav__links');
  var toggle = document.querySelector('.nav__toggle');

  if (toggle && links) {
    toggle.addEventListener('click', function () {
      links.classList.toggle('is-open');
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') links.classList.remove('is-open');
    });
  }

  var lastY = 0;
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (nav) {
      if (y > 40) nav.classList.add('is-solid');
      else nav.classList.remove('is-solid');
    }
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- 滚动揭示 ---------- */
  var revealEls = [].slice.call(document.querySelectorAll('[data-reveal]'));

  if (reduce || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('is-in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ---------- 逐字揭示 ---------- */
  [].slice.call(document.querySelectorAll('.reveal-chars')).forEach(function (el) {
    var text = el.textContent;
    el.textContent = '';
    var frag = document.createDocumentFragment();
    for (var i = 0; i < text.length; i++) {
      var s = document.createElement('span');
      s.textContent = text[i];
      s.style.animationDelay = (i * 0.055) + 's';
      frag.appendChild(s);
    }
    el.appendChild(frag);
  });

  /* ---------- 轻视差 ---------- */
  if (!reduce) {
    var pxEls = [].slice.call(document.querySelectorAll('[data-parallax]'));
    if (pxEls.length) {
      var ticking = false;
      window.addEventListener('scroll', function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () {
          var vh = window.innerHeight;
          pxEls.forEach(function (el) {
            var r = el.getBoundingClientRect();
            if (r.bottom < -200 || r.top > vh + 200) return;
            var speed = parseFloat(el.getAttribute('data-parallax')) || 0.08;
            var offset = (r.top + r.height / 2 - vh / 2) * speed;
            el.style.transform = 'translate3d(0,' + offset.toFixed(2) + 'px,0)';
          });
          ticking = false;
        });
      }, { passive: true });
    }
  }

  /* ---------- 当前页高亮 ---------- */
  var path = location.pathname.split('/').pop() || 'index.html';
  [].slice.call(document.querySelectorAll('.nav__links a')).forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === path) a.classList.add('is-active');
  });
})();