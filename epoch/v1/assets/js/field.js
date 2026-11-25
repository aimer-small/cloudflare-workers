/* ============================================================
   裂界纪 · field.js
   背景场：粒子 + 界痕扰动
   ============================================================ */
(function () {
  'use strict';

  var canvas = document.getElementById('field');
  if (!canvas) return;

  var ctx = canvas.getContext('2d', { alpha: true });
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var W = 0, H = 0, DPR = 1;
  var particles = [];
  var mouse = { x: -9999, y: -9999, active: false };
  var t = 0;
  var raf = null;
  var running = true;

  var JADE = '111,191,168';
  var BRASS = '176,141,79';

  function resize() {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = Math.floor(W * DPR);
    canvas.height = Math.floor(H * DPR);
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    build();
  }

  /* 界痕：一条纵向的扰动曲线，x = 中心 + 双正弦叠加 */
  function riftX(y) {
    var base = W * 0.5;
    var a = Math.sin(y * 0.0042 + t * 0.00042) * (W * 0.055);
    var b = Math.sin(y * 0.0113 - t * 0.00071) * (W * 0.018);
    var c = Math.sin(y * 0.0021 + t * 0.00019) * (W * 0.032);
    return base + a + b + c;
  }

  function build() {
    var target = Math.round(Math.min(150, Math.max(46, (W * H) / 15000)));
    particles = [];
    for (var i = 0; i < target; i++) {
      particles.push(spawn(true));
    }
  }

  function spawn(anywhere) {
    var side = Math.random() < 0.5 ? -1 : 1;
    var x = Math.random() * W;
    var y = anywhere ? Math.random() * H : (Math.random() < 0.5 ? -20 : H + 20);
    return {
      x: x,
      y: y,
      vx: (Math.random() - 0.5) * 0.16,
      vy: (Math.random() - 0.5) * 0.16 - 0.05,
      r: Math.random() * 1.5 + 0.35,
      side: side,
      a: Math.random() * 0.5 + 0.12,
      ph: Math.random() * Math.PI * 2,
      sp: Math.random() * 0.0016 + 0.0004
    };
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);

    /* --- 界痕光带 --- */
    var steps = 26;
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    for (var s = 0; s < steps; s++) {
      var y0 = (H / steps) * s;
      var y1 = (H / steps) * (s + 1);
      var x0 = riftX(y0);
      var x1 = riftX(y1);
      var g = ctx.createLinearGradient(x0, y0, x1, y1);
      var pulse = 0.5 + 0.5 * Math.sin(t * 0.0009 + s * 0.42);
      g.addColorStop(0, 'rgba(' + JADE + ',' + (0.05 + pulse * 0.05) + ')');
      g.addColorStop(0.5, 'rgba(' + BRASS + ',' + (0.03 + pulse * 0.04) + ')');
      g.addColorStop(1, 'rgba(' + JADE + ',' + (0.05 + pulse * 0.05) + ')');
      ctx.strokeStyle = g;
      ctx.lineWidth = 1.1;
      ctx.beginPath();
      ctx.moveTo(x0, y0);
      ctx.lineTo(x1, y1);
      ctx.stroke();
    }
    /* 界痕外晕 */
    ctx.globalCompositeOperation = 'lighter';
    for (var k = 0; k < 3; k++) {
      ctx.beginPath();
      for (var yy = 0; yy <= H; yy += 18) {
        var xx = riftX(yy);
        if (yy === 0) ctx.moveTo(xx, yy);
        else ctx.lineTo(xx, yy);
      }
      ctx.strokeStyle = 'rgba(' + JADE + ',' + (0.028 - k * 0.008) + ')';
      ctx.lineWidth = 8 + k * 14;
      ctx.stroke();
    }
    ctx.restore();

    /* --- 粒子 --- */
    for (var i = 0; i < particles.length; i++) {
      var p = particles[i];

      if (!reduce) {
        p.x += p.vx;
        p.y += p.vy;
        p.ph += p.sp;
      }

      /* 界痕排斥：粒子被推离裂缝 */
      var rx = riftX(p.y);
      var dx = p.x - rx;
      var dist = Math.abs(dx);
      var force = Math.max(0, 1 - dist / 190);
      if (force > 0) {
        p.x += (dx > 0 ? 1 : -1) * force * 0.55;
      }

      /* 鼠标斥力 */
      if (mouse.active) {
        var mdx = p.x - mouse.x;
        var mdy = p.y - mouse.y;
        var md = Math.sqrt(mdx * mdx + mdy * mdy);
        if (md < 130 && md > 0.1) {
          var mf = (1 - md / 130) * 0.9;
          p.x += (mdx / md) * mf;
          p.y += (mdy / md) * mf;
        }
      }

      /* 环绕 */
      if (!reduce) {
        p.x += Math.sin(p.ph) * 0.12;
        p.y += Math.cos(p.ph * 0.7) * 0.1;
      }

      /* 边界回收 */
      if (p.y < -30) { p.y = H + 20; p.x = Math.random() * W; }
      if (p.y > H + 30) { p.y = -20; p.x = Math.random() * W; }
      if (p.x < -30) p.x = W + 20;
      if (p.x > W + 30) p.x = -20;

      var alpha = p.a * (0.55 + 0.45 * Math.sin(p.ph * 1.6));
      var col = p.side < 0 ? JADE : BRASS;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(' + col + ',' + alpha.toFixed(3) + ')';
      ctx.fill();

      /* 近界痕的粒子加光晕 */
      if (dist < 120) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r * 3.4, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(' + col + ',' + (alpha * 0.1).toFixed(3) + ')';
        ctx.fill();
      }
    }

    t += 16;
    if (running) raf = requestAnimationFrame(draw);
  }

  /* --- 事件 --- */
  var resizeTimer = null;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(resize, 180);
  });

  window.addEventListener('pointermove', function (e) {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    mouse.active = true;
  }, { passive: true });

  window.addEventListener('pointerleave', function () {
    mouse.active = false;
  });

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) {
      running = false;
      if (raf) cancelAnimationFrame(raf);
    } else {
      if (!running) {
        running = true;
        raf = requestAnimationFrame(draw);
      }
    }
  });

  resize();
  if (reduce) {
    draw();
    running = false;
  } else {
    raf = requestAnimationFrame(draw);
  }
})();