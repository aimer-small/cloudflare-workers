# -*- coding: utf-8 -*-
"""
裂界纪 · SVG 概念图生成器 · 公共工具
所有图形为纯矢量，无位图依赖，任意分辨率清晰
"""
import math
import random

# ---------- 调色 ----------
INK      = "#070C0E"
INK2     = "#0B1215"
INK3     = "#101A1E"
BONE     = "#E6EDE9"
JADE     = "#6FBFA8"
JADE_D   = "#2E6B5C"
JADE_DD  = "#16332C"
BRASS    = "#B08D4F"
BRASS_D  = "#6B5228"
BRASS_DD = "#2E2415"
CINNABAR = "#A63D2F"


def lerp(a, b, t):
    return a + (b - a) * t


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(c1, c2, t):
    a, b = hex2rgb(c1), hex2rgb(c2)
    return "#%02X%02X%02X" % tuple(int(round(lerp(a[i], b[i], t))) for i in range(3))


def rgba(h, a):
    r, g, b = hex2rgb(h)
    return "rgba(%d,%d,%d,%.3f)" % (r, g, b, a)


# ---------- 山脊生成 ----------
def ridge(width, base_y, amp, freq, seed, octaves=4, roughness=0.55, step=14):
    """生成一条山脊折线点列（正弦叠加 + 分形扰动）"""
    rnd = random.Random(seed)
    pts = []
    x = -40
    while x <= width + 40:
        y = base_y
        a = amp
        f = freq
        for o in range(octaves):
            phase = rnd.uniform(0, math.tau)
            y += math.sin(x / width * math.tau * f + phase) * a
            a *= roughness
            f *= 2.1
        # 尖峰感：局部抬升
        y -= abs(math.sin(x / width * math.tau * freq * 0.5 + seed)) * amp * 0.35
        pts.append((x, y))
        x += step
    return pts


def ridge_path(pts, width, bottom, close=True):
    d = "M %.1f %.1f" % pts[0]
    for i in range(1, len(pts)):
        px, py = pts[i - 1]
        cx, cy = pts[i]
        mx = (px + cx) / 2
        d += " Q %.1f %.1f %.1f %.1f" % (px, py, mx, (py + cy) / 2)
    if close:
        d += " L %.1f %.1f L %.1f %.1f Z" % (width + 40, bottom, -40, bottom)
    return d


def smooth_path(pts, close_to=None):
    """平滑曲线（Catmull-Rom 近似）"""
    if len(pts) < 2:
        return ""
    d = "M %.1f %.1f" % pts[0]
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1x = p1[0] + (p2[0] - p0[0]) / 6.0
        c1y = p1[1] + (p2[1] - p0[1]) / 6.0
        c2x = p2[0] - (p3[0] - p1[0]) / 6.0
        c2y = p2[1] - (p3[1] - p1[1]) / 6.0
        d += " C %.1f %.1f %.1f %.1f %.1f %.1f" % (c1x, c1y, c2x, c2y, p2[0], p2[1])
    if close_to:
        d += " L %.1f %.1f Z" % close_to
    return d


# ---------- 通用片段 ----------
def defs_common(prefix=""):
    """通用渐变与滤镜"""
    return f"""
  <defs>
    <filter id="{prefix}soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="18"/>
    </filter>
    <filter id="{prefix}soft2" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="42"/>
    </filter>
    <filter id="{prefix}soft6" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6"/>
    </filter>
    <filter id="{prefix}soft3" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3"/>
    </filter>
    <filter id="{prefix}grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" seed="7" result="n"/>
      <feColorMatrix in="n" type="saturate" values="0"/>
      <feComponentTransfer><feFuncA type="linear" slope="0.055"/></feComponentTransfer>
    </filter>
    <filter id="{prefix}cloud" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.006 0.014" numOctaves="5" seed="11" result="t"/>
      <feDisplacementMap in="SourceGraphic" in2="t" scale="46" xChannelSelector="R" yChannelSelector="G"/>
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <filter id="{prefix}mist" x="-20%" y="-20%" width="140%" height="140%">
      <feTurbulence type="fractalNoise" baseFrequency="0.004 0.02" numOctaves="4" seed="3" result="t"/>
      <feDisplacementMap in="SourceGraphic" in2="t" scale="70" xChannelSelector="R" yChannelSelector="G"/>
      <feGaussianBlur stdDeviation="14"/>
    </filter>
  </defs>"""


def stars(w, h, n, seed, color=BONE, ymax=None, rmin=0.4, rmax=1.5, amin=0.15, amax=0.75):
    rnd = random.Random(seed)
    ymax = ymax or h * 0.7
    out = []
    for _ in range(n):
        x = rnd.uniform(0, w)
        y = rnd.uniform(0, ymax)
        r = rnd.uniform(rmin, rmax)
        a = rnd.uniform(amin, amax)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{color}" opacity="{a:.2f}"/>')
    return "\n    ".join(out)


def glow(cx, cy, r, color, a=0.5, fid="soft2"):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{color}" opacity="{a}" filter="url(#{fid})"/>'


def svg_open(w, h, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" preserveAspectRatio="xMidYMid slice" {extra}>')


def grain_rect(w, h, fid="grain", op=1.0):
    return f'<rect width="{w}" height="{h}" filter="url(#{fid})" opacity="{op}"/>'