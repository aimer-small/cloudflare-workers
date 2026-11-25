# -*- coding: utf-8 -*-
"""重要节点：三次界战地图（1200x760）"""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_common import *

W, H = 1200, 760
OUT = os.path.dirname(os.path.abspath(__file__))
MX0, MY0, MX1, MY1 = 70, 118, 1130, 660


def save(name, body):
    svg = svg_open(W, H) + body + "</svg>"
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("  ->", name, len(svg), "bytes")


def frame(p):
    s = []
    s.append(f'<rect x="{MX0}" y="{MY0}" width="{MX1-MX0}" height="{MY1-MY0}" fill="none" stroke="{BONE}" stroke-opacity="0.22" stroke-width="1.2"/>')
    s.append(f'<rect x="{MX0-8}" y="{MY0-8}" width="{MX1-MX0+16}" height="{MY1-MY0+16}" fill="none" stroke="{BONE}" stroke-opacity="0.10" stroke-width="0.8"/>')
    # 角饰
    for cx, cy, sx, sy in [(MX0, MY0, 1, 1), (MX1, MY0, -1, 1), (MX0, MY1, 1, -1), (MX1, MY1, -1, -1)]:
        s.append(f'<path d="M {cx} {cy+sy*26} L {cx} {cy} L {cx+sx*26} {cy}" fill="none" stroke="{BONE}" stroke-opacity="0.4" stroke-width="1.4"/>')
    # 网格
    for x in range(MX0, MX1 + 1, 53):
        s.append(f'<line x1="{x}" y1="{MY0}" x2="{x}" y2="{MY1}" stroke="{BONE}" stroke-opacity="0.045" stroke-width="0.7"/>')
    for y in range(MY0, MY1 + 1, 54):
        s.append(f'<line x1="{MX0}" y1="{y}" x2="{MX1}" y2="{y}" stroke="{BONE}" stroke-opacity="0.045" stroke-width="0.7"/>')
    return "".join(s)


def rift_path(x0, drift, seed, amp=26):
    rnd = random.Random(seed)
    pts = []
    y = MY0 - 10
    x = x0
    while y < MY1 + 20:
        pts.append((x, y))
        y += rnd.uniform(26, 46)
        x += rnd.uniform(-amp, amp) + drift * 0.06
    return pts


def draw_rift(p, pts, color, glow_op=0.5, core_op=0.85):
    s = []
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="{glow_op*0.35:.2f}" stroke-width="26" filter="url(#{p}soft2)"/>')
    s.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="{glow_op*0.6:.2f}" stroke-width="9" filter="url(#{p}soft3)"/>')
    s.append(f'<path d="{d}" fill="none" stroke="{BONE}" stroke-opacity="{core_op}" stroke-width="1.6"/>')
    # 分叉
    rnd = random.Random(len(pts) * 7)
    for i in range(2, len(pts) - 2, 3):
        x, y = pts[i]
        for side in (-1, 1):
            if rnd.random() < 0.55:
                ln = rnd.uniform(18, 52)
                ex = x + side * ln
                ey = y + rnd.uniform(-24, 24)
                s.append(f'<path d="M {x:.1f} {y:.1f} L {ex:.1f} {ey:.1f}" stroke="{color}" stroke-opacity="0.4" stroke-width="1"/>')
    return "".join(s)


def city(x, y, kind, label, color, p, size=1.0, destroyed=False):
    s = [f'<g transform="translate({x},{y})">']
    if kind == "jade":
        s.append(f'<circle cx="0" cy="0" r="{7*size}" fill="{INK}" stroke="{color}" stroke-opacity="0.9" stroke-width="1.6"/>')
        s.append(f'<circle cx="0" cy="0" r="{13*size}" fill="none" stroke="{color}" stroke-opacity="0.4" stroke-width="0.9"/>')
        s.append(f'<circle cx="0" cy="0" r="{3*size}" fill="{color}" opacity="0.9"/>')
    else:
        pts = [(math.cos(i * math.tau / 6 - math.pi / 2) * 8 * size,
                math.sin(i * math.tau / 6 - math.pi / 2) * 8 * size) for i in range(6)]
        d = "M " + " L ".join(f"{a:.1f} {b:.1f}" for a, b in pts) + " Z"
        s.append(f'<path d="{d}" fill="{INK}" stroke="{color}" stroke-opacity="0.9" stroke-width="1.6"/>')
        s.append(f'<circle cx="0" cy="0" r="{3*size}" fill="{color}" opacity="0.9"/>')
    if destroyed:
        s.append(f'<path d="M -11 -11 L 11 11 M 11 -11 L -11 11" stroke="{CINNABAR}" stroke-opacity="0.85" stroke-width="1.8"/>')
    s.append(f'<text x="0" y="{-16*size}" text-anchor="middle" font-size="11" fill="{BONE}" fill-opacity="0.72" letter-spacing="1">{label}</text>')
    s.append('</g>')
    return "".join(s)


def battle(x, y, label, color, p, size=1.0):
    s = [f'<g transform="translate({x},{y})">']
    s.append(glow(0, 0, 46 * size, color, 0.55, p + "soft"))
    s.append(f'<circle cx="0" cy="0" r="{16*size}" fill="none" stroke="{color}" stroke-opacity="0.75" stroke-width="1.4"/>')
    s.append(f'<circle cx="0" cy="0" r="{26*size}" fill="none" stroke="{color}" stroke-opacity="0.3" stroke-width="0.9" stroke-dasharray="3 4"/>')
    for a in (45, 135):
        r = math.radians(a)
        s.append(f'<line x1="{-math.cos(r)*11*size:.1f}" y1="{-math.sin(r)*11*size:.1f}" '
                 f'x2="{math.cos(r)*11*size:.1f}" y2="{math.sin(r)*11*size:.1f}" stroke="{color}" stroke-opacity="0.9" stroke-width="1.8"/>')
    s.append(f'<text x="0" y="{34*size}" text-anchor="middle" font-size="10.5" fill="{color}" fill-opacity="0.85" letter-spacing="1">{label}</text>')
    s.append('</g>')
    return "".join(s)


def arrow(x1, y1, x2, y2, color, op=0.55, w=2.2):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx = x2 - math.cos(ang) * 12
    hy = y2 - math.sin(ang) * 12
    s = [f'<line x1="{x1}" y1="{y1}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{color}" stroke-opacity="{op}" stroke-width="{w}" stroke-dasharray="7 5"/>']
    for side in (-1, 1):
        a = ang + side * 0.42
        s.append(f'<line x1="{x2}" y1="{y2}" x2="{x2-math.cos(a)*14:.1f}" y2="{y2-math.sin(a)*14:.1f}" stroke="{color}" stroke-opacity="{op}" stroke-width="{w}"/>')
    return "".join(s)


def terrain_jade(p, seed, n=26):
    """玄洲侧：山形符号"""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(MX0 + 30, 560)
        y = rnd.uniform(MY0 + 40, MY1 - 40)
        h = rnd.uniform(10, 22)
        w = h * rnd.uniform(1.1, 1.7)
        out.append(f'<path d="M {x-w:.0f} {y:.0f} L {x:.0f} {y-h:.0f} L {x+w:.0f} {y:.0f}" fill="none" stroke="{JADE}" stroke-opacity="{rnd.uniform(0.12,0.3):.2f}" stroke-width="1"/>')
    return "".join(out)


def terrain_brass(p, seed, n=22):
    """奥瑞恩侧：几何方块群"""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(660, MX1 - 30)
        y = rnd.uniform(MY0 + 40, MY1 - 40)
        w = rnd.uniform(8, 18)
        out.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{w*0.7:.0f}" fill="none" stroke="{BRASS}" stroke-opacity="{rnd.uniform(0.12,0.3):.2f}" stroke-width="1"/>')
    return "".join(out)


def base(p, title, sub, accent, seed):
    s = [defs_common(p)]
    s.append(f"""
  <defs>
    <radialGradient id="{p}bg" cx="0.5" cy="0.45" r="0.78">
      <stop offset="0" stop-color="#0A1416"/>
      <stop offset="1" stop-color="{INK}"/>
    </radialGradient>
    <linearGradient id="{p}left" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{JADE}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{JADE}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="{p}right" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="{BRASS}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{BRASS}" stop-opacity="0"/>
    </linearGradient>
  </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>')
    s.append(f'<rect x="{MX0}" y="{MY0}" width="{(MX1-MX0)/2}" height="{MY1-MY0}" fill="url(#{p}left)"/>')
    s.append(f'<rect x="{MX0+(MX1-MX0)/2}" y="{MY0}" width="{(MX1-MX0)/2}" height="{MY1-MY0}" fill="url(#{p}right)"/>')
    s.append(frame(p))
    # 标题
    s.append(f'<text x="{MX0}" y="62" font-size="13" fill="{accent}" fill-opacity="0.85" letter-spacing="6">{sub}</text>')
    s.append(f'<text x="{MX0}" y="98" font-size="30" fill="{BONE}" fill-opacity="0.94" letter-spacing="4">{title}</text>')
    s.append(f'<line x1="{MX0}" y1="108" x2="{MX0+300}" y2="108" stroke="{accent}" stroke-opacity="0.5" stroke-width="1.2"/>')
    # 两侧标注
    s.append(f'<text x="{MX0+16}" y="{MY0+26}" font-size="11" fill="{JADE}" fill-opacity="0.7" letter-spacing="4">玄 洲</text>')
    s.append(f'<text x="{MX1-16}" y="{MY0+26}" text-anchor="end" font-size="11" fill="{BRASS}" fill-opacity="0.7" letter-spacing="4">奥 瑞 恩</text>')
    # 指北针
    s.append(f'<g transform="translate({MX1-40},{MY1-46})" opacity="0.5">')
    s.append(f'<circle cx="0" cy="0" r="18" fill="none" stroke="{BONE}" stroke-opacity="0.3" stroke-width="0.9"/>')
    s.append(f'<path d="M 0 -14 L 5 4 L 0 0 L -5 4 Z" fill="{BONE}" fill-opacity="0.6"/>')
    s.append(f'<text x="0" y="-20" text-anchor="middle" font-size="9" fill="{BONE}" fill-opacity="0.6">N</text>')
    s.append('</g>')
    return s


def legend(p, items, accent):
    s = [f'<g transform="translate({MX0},{MY1+22})">']
    x = 0
    for kind, label in items:
        if kind == "jade":
            s.append(f'<circle cx="{x+6}" cy="0" r="5" fill="none" stroke="{JADE}" stroke-opacity="0.9" stroke-width="1.4"/>')
        elif kind == "brass":
            s.append(f'<rect x="{x+1}" y="-5" width="10" height="10" fill="none" stroke="{BRASS}" stroke-opacity="0.9" stroke-width="1.4"/>')
        elif kind == "battle":
            s.append(f'<circle cx="{x+6}" cy="0" r="6" fill="none" stroke="{accent}" stroke-opacity="0.9" stroke-width="1.3"/>')
            s.append(f'<line x1="{x+2}" y1="-4" x2="{x+10}" y2="4" stroke="{accent}" stroke-opacity="0.9" stroke-width="1.3"/>')
        elif kind == "rift":
            s.append(f'<line x1="{x}" y1="0" x2="{x+12}" y2="0" stroke="{BONE}" stroke-opacity="0.85" stroke-width="1.6"/>')
        s.append(f'<text x="{x+18}" y="4" font-size="10.5" fill="{BONE}" fill-opacity="0.6" letter-spacing="1">{label}</text>')
        x += 18 + len(label) * 12 + 26
    s.append('</g>')
    return "".join(s)


# ------------------------------------------------------------
# 第一次界战
# ------------------------------------------------------------
def map1():
    p = "m1"
    A = JADE
    s = base(p, "第一次界战 · 界痕初现", "纪年 一 · 裂痕之年", A, 1)
    s.append(terrain_jade(p, 11))
    s.append(terrain_brass(p, 12))
    pts = rift_path(600, 0, 101, 22)
    s.append(draw_rift(p, pts, JADE, 0.55, 0.9))

    s.append(city(300, 300, "jade", "昆仑", JADE, p, 1.2))
    s.append(city(430, 500, "jade", "玉京", JADE, p, 1.0))
    s.append(city(200, 520, "jade", "云梦泽", JADE, p, 0.9))
    s.append(city(880, 280, "brass", "奥瑞恩", BRASS, p, 1.2))
    s.append(city(1000, 470, "brass", "铁砧城", BRASS, p, 1.0))
    s.append(city(760, 560, "brass", "白塔", BRASS, p, 0.9))

    s.append(battle(600, 380, "初裂点", A, p, 1.3))
    s.append(arrow(430, 500, 560, 400, JADE, 0.5))
    s.append(arrow(880, 280, 650, 360, BRASS, 0.5))

    s.append(legend(p, [("jade", "玄洲城"), ("brass", "奥瑞恩城"), ("battle", "战场"), ("rift", "界痕")], A))
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("map-battle1.svg", "".join(s))


# ------------------------------------------------------------
# 第二次界战
# ------------------------------------------------------------
def map2():
    p = "m2"
    A = BRASS
    s = base(p, "第二次界战 · 界痕东移", "纪年 二 · 焚城之年", A, 2)
    s.append(terrain_jade(p, 21))
    s.append(terrain_brass(p, 22))
    pts = rift_path(690, 90, 202, 30)
    s.append(draw_rift(p, pts, BRASS, 0.6, 0.9))

    s.append(city(300, 300, "jade", "昆仑", JADE, p, 1.2))
    s.append(city(470, 480, "jade", "玉京", JADE, p, 1.0, destroyed=True))
    s.append(city(200, 520, "jade", "云梦泽", JADE, p, 0.9))
    s.append(city(920, 280, "brass", "奥瑞恩", BRASS, p, 1.2))
    s.append(city(1010, 470, "brass", "铁砧城", BRASS, p, 1.0))
    s.append(city(800, 560, "brass", "白塔", BRASS, p, 0.9, destroyed=True))

    s.append(battle(660, 300, "焚城之战", A, p, 1.2))
    s.append(battle(700, 520, "白塔陷落", A, p, 1.1))
    s.append(arrow(470, 480, 620, 340, JADE, 0.5))
    s.append(arrow(920, 280, 730, 330, BRASS, 0.55))
    s.append(arrow(800, 560, 720, 540, BRASS, 0.45))

    s.append(legend(p, [("jade", "玄洲城"), ("brass", "奥瑞恩城"), ("battle", "战场"), ("rift", "界痕")], A))
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("map-battle2.svg", "".join(s))


# ------------------------------------------------------------
# 第三次界战（至今）
# ------------------------------------------------------------
def map3():
    p = "m3"
    A = CINNABAR
    s = base(p, "第三次界战 · 至今", "纪年 三 · 未终之年", A, 3)
    s.append(terrain_jade(p, 31))
    s.append(terrain_brass(p, 32))
    pts = rift_path(770, 60, 303, 34)
    s.append(draw_rift(p, pts, CINNABAR, 0.62, 0.92))

    s.append(city(300, 300, "jade", "昆仑", JADE, p, 1.2))
    s.append(city(500, 470, "jade", "玉京", JADE, p, 1.0, destroyed=True))
    s.append(city(210, 540, "jade", "云梦泽", JADE, p, 0.9))
    s.append(city(960, 280, "brass", "奥瑞恩", BRASS, p, 1.2))
    s.append(city(1040, 480, "brass", "铁砧城", BRASS, p, 1.0))
    s.append(city(830, 570, "brass", "白塔", BRASS, p, 0.9, destroyed=True))

    s.append(battle(760, 250, "第三次界战", A, p, 1.4))
    s.append(battle(720, 430, "未决", A, p, 1.1))
    s.append(battle(790, 590, "碑前", A, p, 1.0))
    s.append(arrow(500, 470, 700, 300, JADE, 0.5))
    s.append(arrow(960, 280, 800, 300, BRASS, 0.55))

    # 界痕移动方向
    s.append(f'<g opacity="0.6">')
    s.append(f'<path d="M 640 700 L 800 700" stroke="{CINNABAR}" stroke-opacity="0.5" stroke-width="1.4" stroke-dasharray="6 5"/>')
    s.append(f'<path d="M 800 700 L 788 694 M 800 700 L 788 706" stroke="{CINNABAR}" stroke-opacity="0.7" stroke-width="1.4"/>')
    s.append(f'<text x="720" y="692" text-anchor="middle" font-size="10" fill="{CINNABAR}" fill-opacity="0.8" letter-spacing="2">每年东移七里</text>')
    s.append('</g>')

    s.append(legend(p, [("jade", "玄洲城"), ("brass", "奥瑞恩城"), ("battle", "战场"), ("rift", "界痕")], A))
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("map-battle3.svg", "".join(s))


if __name__ == "__main__":
    print("生成界战地图...")
    map1()
    map2()
    map3()
    print("完成")