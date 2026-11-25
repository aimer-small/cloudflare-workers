# -*- coding: utf-8 -*-
"""场景概念图：界门 / 战场（1600x900）"""
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


def fog_band(p, y, h, color, op, seed, n=26):
    rnd = random.Random(seed)
    out = [f'<g filter="url(#{p}soft2)">']
    for _ in range(n):
        x = rnd.uniform(-100, W + 100)
        yy = y + rnd.uniform(-h * 0.4, h * 0.4)
        rx = rnd.uniform(120, 340)
        ry = rnd.uniform(h * 0.18, h * 0.42)
        out.append(f'<ellipse cx="{x:.0f}" cy="{yy:.0f}" rx="{rx:.0f}" ry="{ry:.0f}" fill="{color}" opacity="{op*rnd.uniform(0.4,1.0):.2f}"/>')
    out.append('</g>')
    return "".join(out)


# ------------------------------------------------------------
# 界门
# ------------------------------------------------------------
def scene_gate():
    p = "g"
    s = [defs_common(p)]
    s.append(f"""
  <defs>
    <linearGradient id="{p}sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#02060A"/>
      <stop offset="0.34" stop-color="#061114"/>
      <stop offset="0.62" stop-color="#0C2226"/>
      <stop offset="0.82" stop-color="#123033"/>
      <stop offset="1" stop-color="#050B0D"/>
    </linearGradient>
    <radialGradient id="{p}core" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#F2FBF7" stop-opacity="0.95"/>
      <stop offset="0.22" stop-color="#BFE8D8" stop-opacity="0.7"/>
      <stop offset="0.55" stop-color="{JADE}" stop-opacity="0.28"/>
      <stop offset="1" stop-color="{JADE}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="{p}beam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#EAF8F2" stop-opacity="0.42"/>
      <stop offset="0.6" stop-color="{JADE}" stop-opacity="0.12"/>
      <stop offset="1" stop-color="{JADE}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="{p}ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0E2224"/>
      <stop offset="0.4" stop-color="#070F11"/>
      <stop offset="1" stop-color="#03070A"/>
    </linearGradient>
  </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}sky)"/>')
    s.append(stars(W, H, 200, 7, BONE, H * 0.55, 0.3, 1.4, 0.08, 0.55))

    # 裂隙（中央，上宽下窄）
    cx = W / 2
    left = [(cx - 150 - math.sin(y / 120) * 40 - math.sin(y / 47) * 14, y) for y in range(-20, 700, 20)]
    right = [(cx + 150 + math.sin(y / 130 + 1) * 44 + math.sin(y / 51) * 12, y) for y in range(-20, 700, 20)]
    d = "M " + " L ".join(f"{x:.0f} {y}" for x, y in left) + " L " + " L ".join(f"{x:.0f} {y}" for x, y in reversed(right)) + " Z"
    s.append(f'<path d="{d}" fill="url(#{p}core)" opacity="0.9"/>')
    s.append(f'<path d="{d}" fill="none" stroke="{BONE}" stroke-opacity="0.5" stroke-width="2" filter="url(#{p}soft3)"/>')

    # 门框：两侧石柱
    for side in (-1, 1):
        bx = cx + side * 210
        s.append(f'<path d="M {bx} 700 L {bx+side*10} 120 L {bx+side*70} 96 L {bx+side*84} 700 Z" fill="#04080A"/>')
        s.append(f'<path d="M {bx} 700 L {bx+side*10} 120 L {bx+side*70} 96 L {bx+side*84} 700" fill="none" stroke="{BONE}" stroke-opacity="0.16" stroke-width="1.4"/>')
        # 柱上刻纹
        for k in range(9):
            yy = 160 + k * 58
            s.append(f'<line x1="{bx+side*16}" y1="{yy}" x2="{bx+side*66}" y2="{yy-6}" stroke="{BONE}" stroke-opacity="0.10" stroke-width="1"/>')

    # 门楣
    s.append(f'<path d="M {cx-300} 118 L {cx-140} 74 L {cx+140} 74 L {cx+300} 118 L {cx+300} 150 L {cx-300} 150 Z" fill="#04080A"/>')
    s.append(f'<path d="M {cx-300} 118 L {cx-140} 74 L {cx+140} 74 L {cx+300} 118" fill="none" stroke="{BONE}" stroke-opacity="0.2" stroke-width="1.4"/>')

    # 门楣符文（左符箓 / 右几何）
    for i in range(7):
        x = cx - 120 + i * 40
        s.append(f'<rect x="{x-7}" y="96" width="14" height="34" fill="none" stroke="{JADE}" stroke-opacity="0.45" stroke-width="0.9"/>')
        s.append(f'<line x1="{x-4}" y1="104" x2="{x+4}" y2="104" stroke="{JADE}" stroke-opacity="0.4" stroke-width="1"/>')
        s.append(f'<line x1="{x-4}" y1="114" x2="{x+2}" y2="114" stroke="{JADE}" stroke-opacity="0.4" stroke-width="1"/>')
        s.append(f'<line x1="{x-4}" y1="124" x2="{x+4}" y2="124" stroke="{JADE}" stroke-opacity="0.4" stroke-width="1"/>')
    for i in range(6):
        x = cx + 150 + i * 26
        s.append(f'<path d="M {x} 100 L {x+10} 112 L {x} 124 L {x-10} 112 Z" fill="none" stroke="{BRASS}" stroke-opacity="0.4" stroke-width="0.9"/>')

    # 光柱
    s.append(f'<polygon points="{cx-120},0 {cx+120},0 {cx+300},760 {cx-300},760" fill="url(#{p}beam)" opacity="0.5" filter="url(#{p}soft2)"/>')

    # 地面
    s.append(f'<path d="M 0 700 L {W} 700 L {W} {H} L 0 {H} Z" fill="url(#{p}ground)"/>')
    # 地面反光
    s.append(f'<ellipse cx="{cx}" cy="740" rx="360" ry="70" fill="{JADE}" opacity="0.16" filter="url(#{p}soft2)"/>')

    # 碎石
    rnd = random.Random(19)
    for _ in range(70):
        x = rnd.uniform(0, W)
        y = rnd.uniform(700, H)
        w = rnd.uniform(6, 34) * (0.4 + (y - 700) / 200)
        h = w * rnd.uniform(0.3, 0.6)
        s.append(f'<path d="M {x:.0f} {y:.0f} L {x+w*0.5:.0f} {y-h:.0f} L {x+w:.0f} {y:.0f} Z" fill="#04080A" opacity="{rnd.uniform(0.5,0.95):.2f}"/>')

    # 雾
    s.append(fog_band(p, 690, 120, "#8FD4BE", 0.16, 21, 22))
    s.append(fog_band(p, 760, 150, "#BFE8D8", 0.10, 22, 18))

    # 前景剪影
    fg = ridge(W, 860, 40, 2.2, 909, 3, 0.5, 17)
    s.append(f'<path d="{ridge_path(fg, W, H)}" fill="#02060A"/>')

    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("scene-gate.svg", "".join(s))


# ------------------------------------------------------------
# 战场
# ------------------------------------------------------------
def scene_battlefield():
    p = "b"
    s = [defs_common(p)]
    s.append(f"""
  <defs>
    <linearGradient id="{p}sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#05080A"/>
      <stop offset="0.3" stop-color="#0C1416"/>
      <stop offset="0.52" stop-color="#241A16"/>
      <stop offset="0.68" stop-color="#3A211A"/>
      <stop offset="0.8" stop-color="#1A1210"/>
      <stop offset="1" stop-color="#05080A"/>
    </linearGradient>
    <radialGradient id="{p}sun" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#E8A87C" stop-opacity="0.55"/>
      <stop offset="0.4" stop-color="{CINNABAR}" stop-opacity="0.28"/>
      <stop offset="1" stop-color="{CINNABAR}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="{p}ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1A1210"/>
      <stop offset="0.35" stop-color="#0A0C0D"/>
      <stop offset="1" stop-color="#03060A"/>
    </linearGradient>
  </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}sky)"/>')

    # 落日
    s.append(f'<circle cx="1180" cy="470" r="420" fill="url(#{p}sun)"/>')
    s.append(f'<circle cx="1180" cy="470" r="86" fill="#E8A87C" opacity="0.22"/>')

    # 云层
    rnd = random.Random(31)
    for i in range(9):
        y = 200 + i * 34
        pts = [(x, y + math.sin(x / 200 + i) * 16 + math.sin(x / 70 + i * 2) * 6) for x in range(-40, W + 60, 40)]
        s.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{mix("#E8A87C", "#1A1210", i*0.12)}" stroke-opacity="{0.16 - i*0.012:.3f}" stroke-width="{34 - i*2}" filter="url(#{p}soft2)"/>')

    # 远山
    for base, amp, freq, seed, col, op in [(520, 40, 1.6, 401, "#2A1E1A", 0.7), (560, 52, 2.2, 402, "#150F0E", 0.85)]:
        pts = ridge(W, base, amp, freq, seed, 4, 0.52, 15)
        s.append(f'<path d="{ridge_path(pts, W, H)}" fill="{col}" opacity="{op}"/>')

    # 远处界痕光
    s.append(f'<path d="M 300 520 L 316 470 L 306 430 L 330 380 L 318 330" fill="none" stroke="{JADE}" stroke-opacity="0.35" stroke-width="14" filter="url(#{p}soft2)"/>')
    s.append(f'<path d="M 300 520 L 316 470 L 306 430 L 330 380 L 318 330" fill="none" stroke="{BONE}" stroke-opacity="0.4" stroke-width="1.4"/>')

    # 地面
    s.append(f'<path d="M 0 600 L {W} 600 L {W} {H} L 0 {H} Z" fill="url(#{p}ground)"/>')

    # 中景：断裂石柱群
    rnd2 = random.Random(41)
    for i in range(11):
        x = rnd2.uniform(60, W - 60)
        h = rnd2.uniform(70, 210)
        w = rnd2.uniform(14, 34)
        y0 = 600 + rnd2.uniform(-10, 40)
        tilt = rnd2.uniform(-7, 7)
        s.append(f'<g transform="translate({x:.0f},{y0:.0f}) rotate({tilt:.1f})">')
        s.append(f'<path d="M {-w/2} 0 L {-w/2+3} {-h} L {w/2-6} {-h+8} L {w/2} 0 Z" fill="#05080A"/>')
        s.append(f'<path d="M {-w/2} 0 L {-w/2+3} {-h} L {w/2-6} {-h+8} L {w/2} 0" fill="none" stroke="{BONE}" stroke-opacity="0.12" stroke-width="1"/>')
        s.append('</g>')

    # 旗杆（断裂）
    for x, h, tilt, flag in [(420, 300, -6, True), (980, 240, 5, False), (700, 180, -3, True)]:
        s.append(f'<g transform="translate({x},640) rotate({tilt})">')
        s.append(f'<rect x="-3" y="{-h}" width="6" height="{h}" fill="#04070A"/>')
        s.append(f'<rect x="-3" y="{-h}" width="6" height="{h}" fill="none" stroke="{BONE}" stroke-opacity="0.14" stroke-width="0.9"/>')
        if flag:
            s.append(f'<path d="M 3 {-h+8} C 40 {-h+26} 70 {-h+6} 96 {-h+30} L 96 {-h+96} C 70 {-h+72} 40 {-h+92} 3 {-h+74} Z" fill="#0A0C0D" opacity="0.9"/>')
            s.append(f'<path d="M 3 {-h+8} C 40 {-h+26} 70 {-h+6} 96 {-h+30}" fill="none" stroke="{CINNABAR}" stroke-opacity="0.35" stroke-width="1.2"/>')
        s.append('</g>')

    # 散落甲片 / 兵器
    rnd3 = random.Random(53)
    for _ in range(46):
        x = rnd3.uniform(0, W)
        y = rnd3.uniform(640, H)
        ln = rnd3.uniform(10, 46) * (0.5 + (y - 640) / 260)
        a = rnd3.uniform(-0.5, 0.5)
        s.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+math.cos(a)*ln:.0f}" y2="{y+math.sin(a)*ln*0.4:.0f}" stroke="{BONE}" stroke-opacity="{rnd3.uniform(0.06,0.2):.2f}" stroke-width="{rnd3.uniform(0.8,2):.1f}"/>')

    # 雾
    s.append(fog_band(p, 610, 110, "#C08A6A", 0.14, 61, 20))
    s.append(fog_band(p, 700, 140, "#8A6A5A", 0.10, 62, 16))

    # 前景
    fg = ridge(W, 880, 46, 2.6, 909, 3, 0.5, 17)
    s.append(f'<path d="{ridge_path(fg, W, H)}" fill="#02050A"/>')

    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("scene-battlefield.svg", "".join(s))


if __name__ == "__main__":
    print("生成场景概念图...")
    scene_gate()
    scene_battlefield()
    print("完成")