# -*- coding: utf-8 -*-
"""景物概念图：昆仑之巅 / 奥瑞恩巨城 / 界痕特写 / 首页背景"""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_common import *

W, H = 1600, 900
OUT = os.path.dirname(os.path.abspath(__file__))


def save(name, body):
    svg = svg_open(W, H) + body + "</svg>"
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("  ->", name, len(svg), "bytes")


# ============================================================
# 1. 昆仑之巅
# ============================================================
def cloud_bank(cx, cy, spread, count, seed, c_hi, c_lo, op_base, blur):
    """云团簇：多个重叠椭圆构成翻涌云海"""
    rnd = random.Random(seed)
    out = [f'<g filter="url(#kcloud{blur})">']
    for i in range(count):
        x = cx + rnd.uniform(-spread, spread)
        y = cy + rnd.uniform(-spread * 0.22, spread * 0.22)
        rx = rnd.uniform(spread * 0.16, spread * 0.42)
        ry = rx * rnd.uniform(0.26, 0.44)
        col = mix(c_hi, c_lo, rnd.random())
        op = op_base * rnd.uniform(0.55, 1.0)
        out.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{col}" opacity="{op:.2f}"/>')
    out.append('</g>')
    return "".join(out)


def kunlun():
    p = "k"
    s = [defs_common(p)]
    s.append(f"""
  <defs>
    <linearGradient id="{p}sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#03070A"/>
      <stop offset="0.22" stop-color="#071417"/>
      <stop offset="0.44" stop-color="#0F2A2C"/>
      <stop offset="0.62" stop-color="#1D4A47"/>
      <stop offset="0.74" stop-color="#2A5F58"/>
      <stop offset="0.86" stop-color="#12292B"/>
      <stop offset="1" stop-color="#060C0E"/>
    </linearGradient>
    <radialGradient id="{p}aurora" cx="0.5" cy="0.24" r="0.7">
      <stop offset="0" stop-color="{JADE}" stop-opacity="0.30"/>
      <stop offset="0.4" stop-color="{JADE_D}" stop-opacity="0.13"/>
      <stop offset="1" stop-color="{JADE_DD}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="{p}moon" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#DDF3EA" stop-opacity="0.30"/>
      <stop offset="0.62" stop-color="#9FD8C6" stop-opacity="0.14"/>
      <stop offset="1" stop-color="#6FBFA8" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="{p}beam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#EAF6F1" stop-opacity="0.55"/>
      <stop offset="0.45" stop-color="{JADE}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{JADE}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="{p}mtn" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2A5E58"/>
      <stop offset="0.18" stop-color="#173B3A"/>
      <stop offset="0.55" stop-color="#0A1A1C"/>
      <stop offset="1" stop-color="#04080A"/>
    </linearGradient>
    <linearGradient id="{p}sea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#BFE8D8" stop-opacity="0.5"/>
      <stop offset="0.4" stop-color="#5E9186" stop-opacity="0.4"/>
      <stop offset="1" stop-color="#0E1E20" stop-opacity="0.05"/>
    </linearGradient>
    <filter id="{p}cloud6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
    <filter id="{p}cloud14" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14"/></filter>
    <filter id="{p}cloud26" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="26"/></filter>
  </defs>""")

    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}sky)"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}aurora)"/>')

    # 巨月
    s.append(f'<circle cx="1080" cy="250" r="300" fill="url(#{p}moon)"/>')
    s.append(f'<circle cx="1080" cy="250" r="132" fill="#CFEDE2" opacity="0.10"/>')
    s.append(f'<circle cx="1080" cy="250" r="132" fill="none" stroke="#CFEDE2" stroke-opacity="0.16" stroke-width="1"/>')

    s.append(stars(W, H, 190, 21, BONE, H * 0.46, 0.3, 1.4, 0.1, 0.65))

    # 极光
    for i in range(4):
        y0 = 60 + i * 38
        pts = [(x, y0 + math.sin(x / 240 + i * 1.7) * 44 + math.sin(x / 98 + i) * 15)
               for x in range(-40, W + 60, 34)]
        s.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{JADE}" '
                 f'stroke-opacity="{0.12 - i*0.024:.3f}" stroke-width="{44 - i*9}" filter="url(#{p}soft2)"/>')

    # 体积光柱（多层）
    for cx, wd, op, bl in [(800, 210, 0.30, "soft2"), (800, 96, 0.34, "soft"), (800, 34, 0.5, "soft3")]:
        s.append(f'<polygon points="{cx-wd/2},0 {cx+wd/2},0 {cx+wd*1.9},720 {cx-wd*1.9},720" '
                 f'fill="url(#{p}beam)" opacity="{op}" filter="url(#{p}{bl})"/>')

    # 远山 3 层（越远越亮越淡）
    for base, amp, freq, seed, col, op in [
        (400, 34, 1.4, 101, "#3A6E68", 0.42),
        (470, 48, 2.0, 202, "#24504C", 0.6),
        (545, 60, 2.7, 303, "#14312F", 0.78),
    ]:
        pts = ridge(W, base, amp, freq, seed, 4, 0.52, 15)
        s.append(f'<path d="{ridge_path(pts, W, H)}" fill="{col}" opacity="{op}"/>')

    # 主山脉：尖峰叠加
    peaks = [(800, 430, 118), (628, 268, 92), (972, 246, 88),
             (452, 158, 78), (1150, 176, 82), (250, 96, 70), (1390, 88, 66)]
    def mtn_y(x):
        y = 790.0
        for cx, amp, sg in peaks:
            y -= amp * math.exp(-((x - cx) ** 2) / (2 * sg ** 2))
        y += math.sin(x / 44) * 6 + math.sin(x / 16) * 2.4
        return y

    main = [(x, mtn_y(x)) for x in range(-40, W + 60, 8)]
    s.append(f'<path d="{ridge_path(main, W, H)}" fill="url(#{p}mtn)"/>')

    # 山脊受光棱线
    for off, op, sw in [(0, 0.42, 2.6), (18, 0.16, 1.6), (-22, 0.10, 1.4)]:
        lit = [(x, mtn_y(x) + off) for x in range(520, 1100, 8)]
        s.append(f'<path d="{smooth_path(lit)}" fill="none" stroke="#9FE0CC" stroke-opacity="{op}" stroke-width="{sw}" filter="url(#{p}soft3)"/>')

    # 山体纹理
    rnd = random.Random(88)
    for i in range(34):
        x0 = rnd.uniform(80, 1520)
        y0 = mtn_y(x0) + rnd.uniform(16, 240)
        ln = rnd.uniform(50, 190)
        pts = [(x0 + k * ln / 5, y0 + math.sin(k * 1.3 + i) * 8 + k * 4) for k in range(6)]
        s.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{BONE}" stroke-opacity="{rnd.uniform(0.03,0.10):.3f}" stroke-width="1"/>')

    # 云海：三层云团，覆盖山腰
    s.append(cloud_bank(800, 640, 900, 46, 501, "#CFEDE2", "#3E6E68", 0.30, 26))
    s.append(cloud_bank(800, 668, 820, 40, 502, "#E4F6EE", "#5E9186", 0.34, 14))
    s.append(cloud_bank(800, 700, 760, 34, 503, "#F2FBF7", "#7FB3A6", 0.30, 6))

    # 云海亮边
    for i in range(3):
        y0 = 622 + i * 26
        pts = [(x, y0 + math.sin(x / 160 + i * 2.1) * 18 + math.sin(x / 62 + i) * 7)
               for x in range(-40, W + 60, 26)]
        s.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="#EAF8F2" stroke-opacity="{0.22 - i*0.05:.2f}" stroke-width="{2.6 - i*0.5}" filter="url(#{p}soft3)"/>')

    # 峰顶碑
    s.append(f'<g transform="translate(800,{mtn_y(800)-6:.0f})">')
    s.append(f'<rect x="-4" y="-58" width="8" height="62" fill="#04080A"/>')
    s.append(f'<rect x="-4" y="-58" width="8" height="62" fill="none" stroke="{JADE}" stroke-opacity="0.6" stroke-width="1"/>')
    s.append(f'<circle cx="0" cy="-62" r="5" fill="#DDF3EA" opacity="0.95"/>')
    s.append(glow(0, -62, 46, JADE, 0.65, p + "soft"))
    s.append('</g>')

    # 前景山脊
    fg = ridge(W, 862, 46, 2.4, 909, 3, 0.5, 17)
    s.append(f'<path d="{ridge_path(fg, W, H)}" fill="#03070A"/>')

    # 前景薄雾
    s.append(f'<rect y="740" width="{W}" height="160" fill="url(#{p}sea)" opacity="0.28"/>')
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("scene-kunlun.svg", "".join(s))


# ============================================================
# 2. 奥瑞恩巨城
# ============================================================
def orion_city():
    p = "o"
    s = [defs_common(p)]
    s.append(f"""
  <defs>
    <linearGradient id="{p}sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#06090B"/>
      <stop offset="0.3" stop-color="#0D1114"/>
      <stop offset="0.58" stop-color="#1A1710"/>
      <stop offset="0.8" stop-color="#2A2114"/>
      <stop offset="1" stop-color="#0B0E10"/>
    </linearGradient>
    <radialGradient id="{p}halo" cx="0.5" cy="0.62" r="0.55">
      <stop offset="0" stop-color="{BRASS}" stop-opacity="0.34"/>
      <stop offset="0.5" stop-color="{BRASS_D}" stop-opacity="0.12"/>
      <stop offset="1" stop-color="{BRASS_DD}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="{p}tower" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#0A0D0F"/>
      <stop offset="0.55" stop-color="#14181A"/>
      <stop offset="1" stop-color="#0A0D0F"/>
    </linearGradient>
    <linearGradient id="{p}win" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BRASS}" stop-opacity="0.9"/>
      <stop offset="1" stop-color="{BRASS_D}" stop-opacity="0.2"/>
    </linearGradient>
  </defs>""")

    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}sky)"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}halo)"/>')
    s.append(stars(W, H, 120, 55, BRASS, H * 0.5, 0.3, 1.2, 0.08, 0.5))

    # 法阵天幕
    cx, cy = 800, 470
    s.append(f'<g opacity="0.5" filter="url(#{p}soft3)">')
    for r, op, sw in [(430, 0.30, 1.2), (360, 0.22, 0.9), (250, 0.18, 0.8)]:
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BRASS}" stroke-opacity="{op}" stroke-width="{sw}"/>')
    # 刻度
    for i in range(72):
        a = i * math.tau / 72
        r1, r2 = 430, 430 - (14 if i % 6 == 0 else 7)
        s.append(f'<line x1="{cx+math.cos(a)*r1:.1f}" y1="{cy+math.sin(a)*r1:.1f}" '
                 f'x2="{cx+math.cos(a)*r2:.1f}" y2="{cy+math.sin(a)*r2:.1f}" '
                 f'stroke="{BRASS}" stroke-opacity="0.28" stroke-width="0.9"/>')
    # 内接三角与六边
    for k in range(2):
        n = 3 if k == 0 else 6
        pts = []
        for i in range(n):
            a = i * math.tau / n - math.pi / 2 + k * 0.26
            pts.append((cx + math.cos(a) * 360, cy + math.sin(a) * 360))
        d = "M " + " L ".join("%.1f %.1f" % q for q in pts) + " Z"
        s.append(f'<path d="{d}" fill="none" stroke="{BRASS}" stroke-opacity="0.16" stroke-width="0.9"/>')
    s.append('</g>')

    # 远景城廓
    rnd = random.Random(77)
    s.append(f'<g opacity="0.55">')
    for i in range(26):
        x = rnd.uniform(-20, W)
        w = rnd.uniform(18, 46)
        h = rnd.uniform(60, 190)
        s.append(f'<rect x="{x:.0f}" y="{700-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#0C1012"/>')
    s.append('</g>')

    # 主塔群
    towers = [
        (300, 250, 46, 470), (390, 330, 34, 390), (470, 200, 54, 520),
        (600, 300, 40, 420), (700, 120, 62, 600), (800, 60, 74, 660),
        (900, 150, 58, 570), (1010, 280, 44, 440), (1100, 210, 50, 510),
        (1200, 330, 36, 390), (1290, 260, 44, 460),
    ]
    for x, top, w, h in towers:
        base = 720
        s.append(f'<rect x="{x-w/2}" y="{top}" width="{w}" height="{base-top}" fill="url(#{p}tower)"/>')
        # 尖顶
        s.append(f'<polygon points="{x-w/2},{top} {x},{top-58} {x+w/2},{top}" fill="#0A0D0F"/>')
        s.append(f'<line x1="{x}" y1="{top-58}" x2="{x}" y2="{top-96}" stroke="{BRASS}" stroke-opacity="0.45" stroke-width="1.2"/>')
        s.append(f'<circle cx="{x}" cy="{top-98}" r="2.6" fill="{BRASS}" opacity="0.85"/>')
        s.append(glow(x, top - 98, 26, BRASS, 0.4, p + "soft"))
        # 窗
        rows = int((base - top) / 34)
        for r in range(rows):
            wy = top + 26 + r * 34
            if wy > base - 20:
                break
            for c in range(2):
                wx = x - w / 4 + c * (w / 2)
                if rnd.random() < 0.55:
                    s.append(f'<rect x="{wx-2.2:.1f}" y="{wy:.1f}" width="4.4" height="9" fill="url(#{p}win)" opacity="{rnd.uniform(0.35,0.95):.2f}"/>')

    # 中央巨塔光
    s.append(glow(800, 60, 150, BRASS, 0.35, p + "soft2"))

    # 前景桥与柱
    s.append(f'<g fill="#05080A">')
    s.append(f'<rect x="0" y="760" width="{W}" height="140"/>')
    s.append(f'<path d="M 0 760 Q 400 700 800 760 T 1600 760 L 1600 800 L 0 800 Z" fill="#070B0D"/>')
    s.append('</g>')
    for x in [180, 420, 1180, 1420]:
        s.append(f'<rect x="{x-9}" y="640" width="18" height="130" fill="#080C0E"/>')
        s.append(f'<circle cx="{x}" cy="636" r="4" fill="{BRASS}" opacity="0.7"/>')
        s.append(glow(x, 636, 30, BRASS, 0.35, p + "soft"))

    s.append(f'<rect y="600" width="{W}" height="300" fill="url(#{p}halo)" opacity="0.35"/>')
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("scene-orion-city.svg", "".join(s))


# ============================================================
# 3. 界痕特写
# ============================================================
def rift_closeup():
    p = "r"
    s = [defs_common(p)]
    s.append(f"""
  <defs>
    <linearGradient id="{p}bg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#0A1A18"/>
      <stop offset="0.42" stop-color="#0B1416"/>
      <stop offset="0.5" stop-color="#1A1410"/>
      <stop offset="0.58" stop-color="#0B1416"/>
      <stop offset="1" stop-color="#141009"/>
    </linearGradient>
    <linearGradient id="{p}core" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BONE}" stop-opacity="0.95"/>
      <stop offset="0.35" stop-color="{JADE}" stop-opacity="0.75"/>
      <stop offset="0.62" stop-color="{BRASS}" stop-opacity="0.7"/>
      <stop offset="1" stop-color="{CINNABAR}" stop-opacity="0.55"/>
    </linearGradient>
    <radialGradient id="{p}lg" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{JADE}" stop-opacity="0.4"/>
      <stop offset="1" stop-color="{JADE}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="{p}rg" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="{BRASS}" stop-opacity="0.4"/>
      <stop offset="1" stop-color="{BRASS}" stop-opacity="0"/>
    </radialGradient>
  </defs>""")

    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>')
    s.append(f'<ellipse cx="420" cy="450" rx="520" ry="520" fill="url(#{p}lg)"/>')
    s.append(f'<ellipse cx="1180" cy="450" rx="520" ry="520" fill="url(#{p}rg)"/>')

    # 裂缝路径
    rnd = random.Random(9)
    crack = []
    for y in range(-20, H + 40, 26):
        x = 800 + math.sin(y / 90) * 26 + math.sin(y / 31) * 9 + rnd.uniform(-7, 7)
        crack.append((x, y))

    # 裂缝外晕
    for wd, op in [(120, 0.05), (70, 0.08), (34, 0.12)]:
        s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="{JADE}" stroke-opacity="{op}" stroke-width="{wd}" filter="url(#{p}soft2)"/>')
        s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="{BRASS}" stroke-opacity="{op*0.8:.3f}" stroke-width="{wd}" filter="url(#{p}soft2)"/>')

    # 裂缝主体
    s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="url(#{p}core)" stroke-width="7" filter="url(#{p}soft3)"/>')
    s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="{BONE}" stroke-opacity="0.85" stroke-width="1.6"/>')

    # 分支裂纹
    for i in range(14):
        idx = rnd.randrange(4, len(crack) - 4)
        bx, by = crack[idx]
        side = -1 if rnd.random() < 0.5 else 1
        ln = rnd.uniform(40, 150)
        pts = [(bx, by)]
        for k in range(1, 5):
            pts.append((bx + side * ln * k / 4 + rnd.uniform(-12, 12),
                        by + rnd.uniform(-26, 26) + k * 6))
        s.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{BONE}" stroke-opacity="{rnd.uniform(0.12,0.4):.2f}" stroke-width="{rnd.uniform(0.5,1.4):.1f}"/>')

    # 左侧：气旋与符箓
    s.append(f'<g opacity="0.55">')
    for i in range(5):
        cx, cy = 300 + i * 62, 300 + (i % 3) * 130
        for k in range(3):
            rr = 26 + k * 16
            s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rr}" ry="{rr*0.42}" fill="none" '
                     f'stroke="{JADE}" stroke-opacity="{0.3 - k*0.07:.2f}" stroke-width="0.9" '
                     f'transform="rotate({-24 + k*16} {cx} {cy})"/>')
    s.append('</g>')
    # 符箓
    for i, (fx, fy, sc) in enumerate([(210, 620, 1.0), (330, 700, 0.8), (150, 430, 0.7)]):
        s.append(f'<g transform="translate({fx},{fy}) scale({sc})" opacity="0.5">')
        s.append(f'<rect x="-16" y="-46" width="32" height="92" fill="none" stroke="{JADE}" stroke-opacity="0.55" stroke-width="1"/>')
        for k in range(5):
            yy = -34 + k * 17
            s.append(f'<line x1="-10" y1="{yy}" x2="{10 - (k%2)*6}" y2="{yy}" stroke="{JADE}" stroke-opacity="0.45" stroke-width="1.1"/>')
        s.append(f'<circle cx="0" cy="-40" r="2.4" fill="{JADE}" opacity="0.8"/>')
        s.append('</g>')

    # 右侧：几何星图
    s.append(f'<g opacity="0.5">')
    for i in range(4):
        cx, cy = 1180 + (i % 2) * 180, 240 + i * 150
        r = 60 + i * 12
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BRASS}" stroke-opacity="0.28" stroke-width="0.9"/>')
        n = 6
        pts = [(cx + math.cos(k * math.tau / n) * r, cy + math.sin(k * math.tau / n) * r) for k in range(n)]
        s.append(f'<path d="M ' + " L ".join("%.1f %.1f" % q for q in pts) + ' Z" fill="none" stroke="%s" stroke-opacity="0.2" stroke-width="0.8"/>' % BRASS)
        for q in pts:
            s.append(f'<circle cx="{q[0]:.1f}" cy="{q[1]:.1f}" r="1.8" fill="{BRASS}" opacity="0.6"/>')
    s.append('</g>')

    # 漂浮碎屑
    rnd2 = random.Random(31)
    for _ in range(90):
        x = rnd2.uniform(0, W)
        y = rnd2.uniform(0, H)
        d = abs(x - 800)
        if d < 60:
            continue
        col = JADE if x < 800 else BRASS
        s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{rnd2.uniform(1,3):.1f}" height="{rnd2.uniform(1,3):.1f}" '
                 f'fill="{col}" opacity="{rnd2.uniform(0.1,0.5):.2f}" transform="rotate({rnd2.uniform(0,90):.0f} {x:.1f} {y:.1f})"/>')

    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("scene-rift.svg", "".join(s))


# ============================================================
# 4. 首页背景：双界对峙
# ============================================================
def hero():
    p = "h"
    s = [defs_common(p)]
    s.append(f"""
  <defs>
    <linearGradient id="{p}sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#04080A"/>
      <stop offset="0.4" stop-color="#081214"/>
      <stop offset="0.72" stop-color="#0E1C1E"/>
      <stop offset="1" stop-color="#060B0D"/>
    </linearGradient>
    <radialGradient id="{p}jl" cx="0.28" cy="0.55" r="0.5">
      <stop offset="0" stop-color="{JADE}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{JADE}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="{p}bl" cx="0.72" cy="0.55" r="0.5">
      <stop offset="0" stop-color="{BRASS}" stop-opacity="0.2"/>
      <stop offset="1" stop-color="{BRASS}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="{p}rift" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{BONE}" stop-opacity="0"/>
      <stop offset="0.2" stop-color="{JADE}" stop-opacity="0.7"/>
      <stop offset="0.55" stop-color="{BONE}" stop-opacity="0.9"/>
      <stop offset="0.8" stop-color="{BRASS}" stop-opacity="0.7"/>
      <stop offset="1" stop-color="{BONE}" stop-opacity="0"/>
    </linearGradient>
  </defs>""")

    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}sky)"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}jl)"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}bl)"/>')
    s.append(stars(W, H, 200, 3, BONE, H * 0.62, 0.3, 1.4, 0.08, 0.55))

    # 左：玄洲浮岛山
    for i, (base, amp, freq, seed, col, op) in enumerate([
        (520, 40, 1.8, 11, "#0E2224", 0.7),
        (600, 56, 2.6, 22, "#0A181A", 0.85),
        (680, 70, 3.4, 33, "#071012", 0.95),
    ]):
        pts = [(x, y) for x, y in ridge(760, base, amp, freq, seed, 4, 0.5, 16)]
        s.append(f'<path d="{ridge_path(pts, 760, H)}" fill="{col}" opacity="{op}"/>')

    # 右：奥瑞恩塔群
    rnd = random.Random(44)
    s.append(f'<g opacity="0.9">')
    for i in range(16):
        x = rnd.uniform(860, W + 20)
        w = rnd.uniform(16, 40)
        h = rnd.uniform(90, 300)
        top = 700 - h
        s.append(f'<rect x="{x:.0f}" y="{top:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#080C0E"/>')
        s.append(f'<polygon points="{x:.0f},{top:.0f} {x+w/2:.0f},{top-40:.0f} {x+w:.0f},{top:.0f}" fill="#080C0E"/>')
        if rnd.random() < 0.7:
            s.append(f'<circle cx="{x+w/2:.0f}" cy="{top-42:.0f}" r="2" fill="{BRASS}" opacity="0.7"/>')
    s.append('</g>')

    # 地平线雾
    s.append(f'<rect y="640" width="{W}" height="260" fill="#060B0D" opacity="0.55" filter="url(#{p}soft2)"/>')

    # 界痕
    crack = [(800 + math.sin(y / 110) * 30 + math.sin(y / 37) * 10, y) for y in range(-20, H + 40, 22)]
    for wd, op in [(150, 0.05), (80, 0.09), (36, 0.14)]:
        s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="{JADE}" stroke-opacity="{op}" stroke-width="{wd}" filter="url(#{p}soft2)"/>')
    s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="url(#{p}rift)" stroke-width="6" filter="url(#{p}soft3)"/>')
    s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="{BONE}" stroke-opacity="0.7" stroke-width="1.2"/>')

    # 前景
    fg = ridge(W, 850, 34, 2.2, 707, 3, 0.5, 18)
    s.append(f'<path d="{ridge_path(fg, W, H)}" fill="#04080A"/>')
    s.append(grain_rect(W, H, p + "grain", 0.85))
    save("hero-rift.svg", "".join(s))


if __name__ == "__main__":
    print("生成景物概念图...")
    kunlun()
    orion_city()
    rift_closeup()
    hero()
    print("完成")