# -*- coding: utf-8 -*-
"""场景概念图：界碑（1600x900）"""
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


def scene_monument():
    p = "n"
    s = [defs_common(p)]
    s.append(f"""
  <defs>
    <linearGradient id="{p}sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#02060A"/>
      <stop offset="0.3" stop-color="#061114"/>
      <stop offset="0.55" stop-color="#0E2427"/>
      <stop offset="0.75" stop-color="#16383A"/>
      <stop offset="1" stop-color="#050B0D"/>
    </linearGradient>
    <linearGradient id="{p}left" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{JADE}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{JADE}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="{p}right" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="{BRASS}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{BRASS}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="{p}stone" x1="0.2" y1="0" x2="0.8" y2="1">
      <stop offset="0" stop-color="#1E3A3A"/>
      <stop offset="0.35" stop-color="#0C1A1C"/>
      <stop offset="1" stop-color="#04080A"/>
    </linearGradient>
    <linearGradient id="{p}ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0C1E20"/>
      <stop offset="0.4" stop-color="#060E10"/>
      <stop offset="1" stop-color="#02060A"/>
    </linearGradient>
  </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}sky)"/>')
    s.append(f'<rect width="{W/2}" height="{H}" fill="url(#{p}left)"/>')
    s.append(f'<rect x="{W/2}" width="{W/2}" height="{H}" fill="url(#{p}right)"/>')
    s.append(stars(W, H, 170, 17, BONE, H * 0.6, 0.3, 1.4, 0.08, 0.5))

    # 界痕（碑后，垂直）
    cx = W / 2
    crack = [(cx + math.sin(y / 110) * 26 + math.sin(y / 43) * 10, y) for y in range(-20, 720, 18)]
    s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="{JADE}" stroke-opacity="0.22" stroke-width="40" filter="url(#{p}soft2)"/>')
    s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="{BONE}" stroke-opacity="0.35" stroke-width="1.6"/>')

    # 两侧光柱
    for side, col in [(-1, JADE), (1, BRASS)]:
        x = cx + side * 300
        s.append(f'<polygon points="{x-40},0 {x+40},0 {x+side*90},760 {x-side*90},760" fill="{col}" opacity="0.10" filter="url(#{p}soft2)"/>')

    # 远山
    for base, amp, freq, seed, col, op in [(560, 36, 1.5, 501, "#1B3E3E", 0.55), (600, 46, 2.1, 502, "#0E2224", 0.75)]:
        pts = ridge(W, base, amp, freq, seed, 4, 0.52, 15)
        s.append(f'<path d="{ridge_path(pts, W, H)}" fill="{col}" opacity="{op}"/>')

    # 地面
    s.append(f'<path d="M 0 640 L {W} 640 L {W} {H} L 0 {H} Z" fill="url(#{p}ground)"/>')

    # 石阶
    for i in range(5):
        w = 420 - i * 46
        y = 700 + i * 34
        s.append(f'<path d="M {cx-w/2} {y} L {cx+w/2} {y} L {cx+w/2-14} {y+30} L {cx-w/2+14} {y+30} Z" fill="#050B0D" stroke="{BONE}" stroke-opacity="0.10" stroke-width="1"/>')

    # 碑体
    bw, bh = 150, 400
    by = 700
    s.append(f'<path d="M {cx-bw/2} {by} L {cx-bw/2+8} {by-bh} L {cx+bw/2-8} {by-bh} L {cx+bw/2} {by} Z" fill="url(#{p}stone)"/>')
    s.append(f'<path d="M {cx-bw/2} {by} L {cx-bw/2+8} {by-bh} L {cx+bw/2-8} {by-bh} L {cx+bw/2} {by}" fill="none" stroke="{BONE}" stroke-opacity="0.28" stroke-width="1.6"/>')
    # 碑顶
    s.append(f'<path d="M {cx-bw/2+8} {by-bh} L {cx} {by-bh-34} L {cx+bw/2-8} {by-bh} Z" fill="#050B0D" stroke="{BONE}" stroke-opacity="0.22" stroke-width="1.4"/>')

    # 碑面刻字（竖排）
    chars = ["界", "痕", "之", "碑"]
    for i, ch in enumerate(chars):
        s.append(f'<text x="{cx}" y="{by-bh+70+i*62}" text-anchor="middle" font-size="42" '
                 f'fill="{BONE}" fill-opacity="0.55" letter-spacing="0">{ch}</text>')
    # 碑面细刻线
    for i in range(6):
        y = by - bh + 46 + i * 62
        s.append(f'<line x1="{cx-52}" y1="{y}" x2="{cx+52}" y2="{y}" stroke="{BONE}" stroke-opacity="0.06" stroke-width="1"/>')

    # 碑体边缘光（左玉青 / 右黄铜）
    s.append(f'<path d="M {cx-bw/2} {by} L {cx-bw/2+8} {by-bh}" stroke="{JADE}" stroke-opacity="0.6" stroke-width="2.4" filter="url(#{p}soft3)"/>')
    s.append(f'<path d="M {cx+bw/2} {by} L {cx+bw/2-8} {by-bh}" stroke="{BRASS}" stroke-opacity="0.6" stroke-width="2.4" filter="url(#{p}soft3)"/>')

    # 碑顶光点
    s.append(f'<circle cx="{cx}" cy="{by-bh-34}" r="6" fill="{BONE}" opacity="0.9"/>')
    s.append(glow(cx, by - bh - 34, 70, JADE, 0.55, p + "soft"))

    # 碑前供台
    s.append(f'<path d="M {cx-90} 700 L {cx+90} 700 L {cx+76} 726 L {cx-76} 726 Z" fill="#04080A" stroke="{BONE}" stroke-opacity="0.14" stroke-width="1"/>')

    # 雾
    rnd = random.Random(71)
    s.append(f'<g filter="url(#{p}soft2)">')
    for _ in range(24):
        x = rnd.uniform(-100, W + 100)
        y = 660 + rnd.uniform(-40, 60)
        s.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(120,320):.0f}" ry="{rnd.uniform(18,44):.0f}" fill="#8FD4BE" opacity="{rnd.uniform(0.04,0.14):.2f}"/>')
    s.append('</g>')

    # 前景
    fg = ridge(W, 880, 44, 2.5, 909, 3, 0.5, 17)
    s.append(f'<path d="{ridge_path(fg, W, H)}" fill="#02060A"/>')

    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("scene-monument.svg", "".join(s))


if __name__ == "__main__":
    print("生成界碑...")
    scene_monument()
    print("完成")