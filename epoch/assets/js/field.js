/* ============================================================
   裂界纪 2.0 · 界气（Field）
   全屏动态壁纸：暖纸基底 + 缓慢漂移的柔光团 + 玉青/黄铜气旋 + 纸面颗粒
   明亮系，非纯白；低对比，只做"呼吸"，不抢正文
   ============================================================ */
(function () {
  'use strict';

  var canvas = document.getElementById('bgField');
  if (!canvas) return;
  var ctx = canvas.getContext('2d', { alpha: false });
  if (!ctx) return;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var W = 0, H = 0, S = 1;
  var base = document.createElement('canvas');
  var bctx = base.getContext('2d');
  var noisePat = null;

  /* ------------- 纸面颗粒纹理（128 像素平铺） ------------- */
  function buildNoise() {
    var n = document.createElement('canvas');
    n.width = n.height = 128;
    var nc = n.getContext('2d');
    var img = nc.createImageData(128, 128);
    var d = img.data;
    for (var i = 0; i < d.length; i += 4) {
      var v = 120 + Math.random() * 120;
      d[i] = v; d[i + 1] = v * 0.96; d[i + 2] = v * 0.86; d[i + 3] = 26;
    }
    nc.putImageData(img, 0, 0);
    noisePat = ctx.createPattern(n, 'repeat');
  }

  /* ------------- 静态基底：暖色径向渐变 + 颗粒，只在 resize 时重绘 ------------- */
  function paintBase() {
    base.width = Math.max(1, Math.floor(W * S));
    base.height = Math.max(1, Math.floor(H * S));
    var b = bctx;
    b.setTransform(S, 0, 0, S, 0, 0);

    // 底色：中心暖米 → 边缘浅陶，整体明亮但不刺白
    var g = b.createRadialGradient(W * 0.44, H * 0.30, 0, W * 0.44, H * 0.30, Math.max(W, H) * 0.92);
    g.addColorStop(0.00, '#FBF3E2');
    g.addColorStop(0.42, '#F7EFDF');
    g.addColorStop(0.72, '#F1E6D1');
    g.addColorStop(1.00, '#E8DBC3');
    b.fillStyle = g;
    b.fillRect(0, 0, W, H);

    // 斜向暖光带，给画面一点方向感
    var lg = b.createLinearGradient(0, 0, W, H);
    lg.addColorStop(0.00, 'rgba(255,246,226,0)');
    lg.addColorStop(0.38, 'rgba(255,247,229,0.55)');
    lg.addColorStop(0.55, 'rgba(255,250,236,0.20)');
    lg.addColorStop(0.78, 'rgba(233,222,199,0.30)');
    lg.addColorStop(1.00, 'rgba(226,213,186,0)');
    b.fillStyle = lg;
    b.fillRect(0, 0, W, H);

    // 颗粒
    if (noisePat) {
      b.globalAlpha = 0.55;
      b.fillStyle = noisePat;
      b.fillRect(0, 0, W, H);
      b.globalAlpha = 1;
    }

    // 四角轻微压暗，收住视线
    var vg = b.createRadialGradient(W * 0.5, H * 0.5, Math.min(W, H) * 0.28, W * 0.5, H * 0.5, Math.max(W, H) * 0.80);
    vg.addColorStop(0, 'rgba(200,183,152,0)');
    vg.addColorStop(1, 'rgba(196,178,146,0.26)');
    b.fillStyle = vg;
    b.fillRect(0, 0, W, H);
  }

  /* ------------- 漂移光团 ------------- */
  // color: 暖杏 / 玉青 / 黄铜 / 纸白，全部低饱和高明度
  var BLOTS = [
    { r: 0.68, rgb: '238,220,184', a0: 0.30, a1: 0.10, ax: 0.16, ay: 0.10, sx: 0.000043, sy: 0.000061, px: 0.0, py: 1.7, sp: 0.000031 },
    { r: 0.54, rgb: '198,226,215', a0: 0.26, a1: 0.08, ax: 0.20, ay: 0.13, sx: 0.000037, sy: 0.000049, px: 2.1, py: 0.4, sp: 0.000026 },
    { r: 0.48, rgb: '230,212,175', a0: 0.28, a1: 0.09, ax: 0.26, ay: 0.16, sx: 0.000052, sy: 0.000044, px: 4.0, py: 2.9, sp: 0.000035 },
    { r: 0.36, rgb: '255,250,235', a0: 0.12, a1: 0.03, bm: 'lighter', ax: 0.24, ay: 0.18, sx: 0.000061, sy: 0.000057, px: 1.2, py: 5.1, sp: 0.000041 },
    { r: 0.34, rgb: '186,216,205', a0: 0.12, a1: 0.03, ax: 0.28, ay: 0.20, sx: 0.000044, sy: 0.000063, px: 3.4, py: 3.6, sp: 0.000029 }
  ];

  var t0 = Date.now();

  function draw(now) {
    var t = now - t0;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    // 静态底（已按 S 缩放绘好，直接铺一层）
    ctx.drawImage(base, 0, 0, W, H);
    ctx.setTransform(S, 0, 0, S, 0, 0);

    var m = Math.max(W, H);
    // 染色气流：暖陶 / 玉青 / 黄铜低饱和雾团缓慢漂移
    for (var i = 0; i < BLOTS.length; i++) {
      var b = BLOTS[i];
      var cx = W * 0.5 + Math.sin(t * b.sx + b.px) * W * b.ax + Math.cos(t * b.sp + b.px) * W * 0.03;
      var cy = H * 0.5 + Math.cos(t * b.sy + b.py) * H * b.ay + Math.sin(t * b.sp + b.py) * H * 0.03;
      var rad = m * b.r * (1 + 0.06 * Math.sin(t * 0.00007 + b.px));
      var g = ctx.createRadialGradient(cx, cy, 0, cx, cy, rad);
      g.addColorStop(0.00, 'rgba(' + b.rgb + ',' + b.a0 + ')');
      g.addColorStop(0.52, 'rgba(' + b.rgb + ',' + b.a1 + ')');
      g.addColorStop(1.00, 'rgba(' + b.rgb + ',0)');
      ctx.globalCompositeOperation = b.bm || 'source-over';
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(cx, cy, rad, 0, 6.2832);
      ctx.fill();
    }
    ctx.globalCompositeOperation = 'source-over';

    // 缓慢横扫的界痕光丝
    var sweep = (t * 0.000026) % 1;
    var sx = -W * 0.35 + sweep * W * 1.7;
    var sg = ctx.createLinearGradient(sx - W * 0.22, 0, sx + W * 0.22, 0);
    sg.addColorStop(0.00, 'rgba(255,250,235,0)');
    sg.addColorStop(0.50, 'rgba(255,252,242,0.11)');
    sg.addColorStop(1.00, 'rgba(255,250,235,0)');
    ctx.fillStyle = sg;
    ctx.fillRect(sx - W * 0.22, 0, W * 0.44, H);

    if (!reduce) requestAnimationFrame(draw);
  }

  function resize() {
    var dpr = window.devicePixelRatio || 1;
    S = Math.min(dpr, 1.6);
    W = canvas.clientWidth || window.innerWidth;
    H = canvas.clientHeight || window.innerHeight;
    canvas.width = Math.max(1, Math.floor(W * S));
    canvas.height = Math.max(1, Math.floor(H * S));
    paintBase();
    if (reduce) draw(t0);
  }

  buildNoise();
  resize();

  var rt = null;
  window.addEventListener('resize', function () {
    clearTimeout(rt);
    rt = setTimeout(resize, 180);
  }, { passive: true });

  if (reduce) {
    draw(t0);
  } else {
    requestAnimationFrame(draw);
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) requestAnimationFrame(draw);
    });
  }
})();