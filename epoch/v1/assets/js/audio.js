/* ============================================================
   裂界纪 · audio.js
   真实音景播放器：assets/audio/bgm-epoch.wav（150s 无缝循环）
   失败时降级为 Web Audio 实时合成
   ============================================================ */
(function () {
  'use strict';

  var box = document.querySelector('.sound');
  if (!box) return;

  var btn = box.querySelector('.sound__btn');
  var label = box.querySelector('.sound__label');
  var SRC = 'assets/audio/bgm-epoch.wav';

  var audio = null;
  var on = false;
  var fadeTimer = null;
  var TARGET = 0.55;      /* 目标音量 */
  var FADE_MS = 1600;

  /* ---------- 创建 audio 元素 ---------- */
  function ensureAudio() {
    if (audio) return audio;
    audio = new Audio();
    audio.src = SRC;
    audio.loop = true;
    audio.preload = 'none';
    audio.volume = 0;
    audio.crossOrigin = 'anonymous';
    audio.addEventListener('error', function () {
      /* 音频不可用时降级到合成 */
      if (window.__riftSynth) {
        window.__riftSynth.start();
      }
    });
    return audio;
  }

  /* ---------- 音量渐变 ---------- */
  function fadeTo(target, done) {
    var a = ensureAudio();
    if (fadeTimer) { clearInterval(fadeTimer); fadeTimer = null; }
    var from = a.volume;
    var start = Date.now();
    fadeTimer = setInterval(function () {
      var k = Math.min(1, (Date.now() - start) / FADE_MS);
      /* easeOutCubic */
      var e = 1 - Math.pow(1 - k, 3);
      a.volume = Math.max(0, Math.min(1, from + (target - from) * e));
      if (k >= 1) {
        clearInterval(fadeTimer);
        fadeTimer = null;
        if (done) done();
      }
    }, 40);
  }

  /* ---------- 开关 ---------- */
  function turnOn() {
    var a = ensureAudio();
    var p = a.play();
    if (p && p.catch) {
      p.catch(function () {
        /* 自动播放被拦截或文件缺失 */
        if (window.__riftSynth) window.__riftSynth.start();
      });
    }
    fadeTo(TARGET);
    on = true;
    box.classList.add('is-on');
    btn.setAttribute('aria-pressed', 'true');
    if (label) label.textContent = 'Sound On';
  }

  function turnOff() {
    fadeTo(0, function () {
      if (audio) audio.pause();
    });
    on = false;
    box.classList.remove('is-on');
    btn.setAttribute('aria-pressed', 'false');
    if (label) label.textContent = 'Sound Off';
  }

  btn.addEventListener('click', function () {
    if (on) turnOff(); else turnOn();
  });

  /* ---------- 页面隐藏时暂停 ---------- */
  document.addEventListener('visibilitychange', function () {
    if (!audio) return;
    if (document.hidden && on) {
      audio.pause();
    } else if (!document.hidden && on) {
      var p = audio.play();
      if (p && p.catch) p.catch(function () {});
    }
  });

  /* ---------- 键盘可达 ---------- */
  box.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      btn.click();
    }
  });

  if (label) label.textContent = 'Sound Off';
})();


/* ============================================================
   降级合成器：WAV 不可用时用 Web Audio 实时生成
   ============================================================ */
(function () {
  'use strict';
  var AC = window.AudioContext || window.webkitAudioContext;
  if (!AC) return;

  var ctx = null, master = null, nodes = [], running = false, timer = null;

  function makeIR(seconds, decay) {
    var rate = ctx.sampleRate;
    var len = Math.floor(rate * seconds);
    var buf = ctx.createBuffer(2, len, rate);
    for (var ch = 0; ch < 2; ch++) {
      var data = buf.getChannelData(ch);
      for (var i = 0; i < len; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / len, decay);
      }
    }
    return buf;
  }

  function drone(freq, gain, detune) {
    var o = ctx.createOscillator();
    var g = ctx.createGain();
    o.type = 'sine';
    o.frequency.value = freq;
    o.detune.value = detune || 0;
    g.gain.value = 0;
    o.connect(g);
    g.connect(master);
    o.start();
    g.gain.setTargetAtTime(gain, ctx.currentTime, 2.4);
    nodes.push({ o: o, g: g });
    return g;
  }

  function start() {
    if (running) return;
    if (!ctx) {
      ctx = new AC();
      master = ctx.createGain();
      master.gain.value = 0.0;
      var conv = ctx.createConvolver();
      conv.buffer = makeIR(3.2, 2.6);
      var wet = ctx.createGain();
      wet.gain.value = 0.55;
      master.connect(ctx.destination);
      master.connect(conv);
      conv.connect(wet);
      wet.connect(ctx.destination);
    }
    if (ctx.state === 'suspended') ctx.resume();
    master.gain.setTargetAtTime(0.5, ctx.currentTime, 2.0);

    drone(38, 0.16, 0);
    drone(220, 0.05, -6);
    drone(880, 0.018, 4);
    drone(233.08, 0.03, 0);   /* 未解决音 */

    /* 稀疏五声音阶点缀 */
    var SCALE = [146.83, 164.81, 185.00, 220.00, 246.94, 293.66, 329.63];
    timer = setInterval(function () {
      if (!ctx || ctx.state !== 'running') return;
      var f = SCALE[Math.floor(Math.random() * SCALE.length)];
      var o = ctx.createOscillator();
      var g = ctx.createGain();
      o.type = 'triangle';
      o.frequency.value = f;
      g.gain.value = 0;
      o.connect(g);
      g.connect(master);
      var t = ctx.currentTime;
      g.gain.setValueAtTime(0, t);
      g.gain.linearRampToValueAtTime(0.05, t + 0.02);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 3.4);
      o.start(t);
      o.stop(t + 3.6);
    }, 2100);

    running = true;
  }

  window.__riftSynth = { start: start };
})();