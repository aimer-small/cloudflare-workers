# -*- coding: utf-8 -*-
"""人物概念图：奥瑞恩三人（900x1200 竖版，黄铜几何）"""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_common import *
from _gen_figures import W, H, save, bg, bg_lines, head, torso, rim, shadow

A = BRASS


def brass_bg(p, seed, n=12):
    s = bg(p, A)
    s.append(bg_lines(p, A, seed, n))
    s.append(stars(W, H, 70, seed + 7, BONE, H * 0.8, 0.3, 1.4, 0.08, 0.45))
    return s


def sigil(cx, cy, r, p, op=0.4, ticks=36):
    """法阵：同心圆 + 刻度 + 内接多边形"""
    out = [f'<g opacity="{op}" transform="translate({cx},{cy})">']
    for rr, o in [(r, 0.5), (r * 0.82, 0.3), (r * 0.56, 0.22)]:
        out.append(f'<circle cx="0" cy="0" r="{rr:.0f}" fill="none" stroke="{A}" stroke-opacity="{o}" stroke-width="1.1"/>')
    for i in range(ticks):
        a = i * math.tau / ticks
        r1 = r
        r2 = r - (14 if i % 3 == 0 else 6)
        out.append(f'<line x1="{math.cos(a)*r1:.1f}" y1="{math.sin(a)*r1:.1f}" '
                   f'x2="{math.cos(a)*r2:.1f}" y2="{math.sin(a)*r2:.1f}" stroke="{A}" stroke-opacity="0.35" stroke-width="0.9"/>')
    for k in (3, 6):
        pts = [(math.cos(i * math.tau / k - math.pi / 2) * r * 0.56,
                math.sin(i * math.tau / k - math.pi / 2) * r * 0.56) for i in range(k)]
        d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
        out.append(f'<path d="{d}" fill="none" stroke="{A}" stroke-opacity="0.28" stroke-width="0.9"/>')
    out.append('</g>')
    return "".join(out)


def collar(cx, y, w, h, p):
    """立领"""
    d = (f"M {cx-w/2} {y+h} L {cx-w/2+6} {y} L {cx+w/2-6} {y} L {cx+w/2} {y+h} "
         f"L {cx+w/2-14} {y+h} L {cx+w/2-18} {y+12} L {cx-w/2+18} {y+12} L {cx-w/2+14} {y+h} Z")
    return (f'<path d="{d}" fill="#05090B"/>'
            f'<path d="{d}" fill="none" stroke="{A}" stroke-opacity="0.55" stroke-width="1.2"/>')


def pauldron(cx, y, side, w, h, p):
    """肩甲：几何块面"""
    x = cx + side * w * 0.5
    d = (f"M {x} {y} L {x+side*w*0.62} {y+18} L {x+side*w*0.52} {y+h} "
         f"L {x-side*w*0.06} {y+h*0.86} Z")
    return (f'<path d="{d}" fill="#070D0F"/>'
            f'<path d="{d}" fill="none" stroke="{A}" stroke-opacity="0.6" stroke-width="1.3"/>'
            f'<path d="M {x+side*w*0.16} {y+16} L {x+side*w*0.44} {y+26}" stroke="{A}" stroke-opacity="0.35" stroke-width="1"/>')


# ------------------------------------------------------------
# 1. 奥瑞尔 · 首席律法师
# ------------------------------------------------------------
def fig_auriel():
    p = "a"
    s = brass_bg(p, 21, 14)

    s.append(sigil(W / 2, 430, 300, p, 0.42, 48))
    s.append(sigil(W / 2, 430, 210, p, 0.3, 24))

    # 垂直光带
    s.append(f'<polygon points="{W/2-90},0 {W/2+90},0 {W/2+150},{H} {W/2-150},{H}" fill="{A}" opacity="0.05" filter="url(#{p}soft2)"/>')

    s.append(shadow(p))

    body = torso(W / 2, 436, 292, 200, 764, 500)
    s.append(f'<path d="{body}" fill="url(#{p}body)"/>')
    s.append(rim(body, A, p, 0.55, 2.4))

    # 长披风
    cape = (f"M {W/2-146} 448 C {W/2-244} 540 {W/2-262} 800 {W/2-248} 1080 "
            f"L {W/2+248} 1080 C {W/2+262} 800 {W/2+244} 540 {W/2+146} 448 Z")
    s.append(f'<path d="{cape}" fill="#05090B" opacity="0.9"/>')
    s.append(rim(cape, A, p, 0.34, 1.8))

    # 胸前法阵纹
    s.append(f'<g opacity="0.5" transform="translate({W/2},640)">')
    s.append(f'<circle cx="0" cy="0" r="52" fill="none" stroke="{A}" stroke-opacity="0.6" stroke-width="1.2"/>')
    s.append(f'<circle cx="0" cy="0" r="34" fill="none" stroke="{A}" stroke-opacity="0.35" stroke-width="0.9"/>')
    for i in range(6):
        a = i * math.tau / 6 - math.pi / 2
        s.append(f'<line x1="0" y1="0" x2="{math.cos(a)*52:.1f}" y2="{math.sin(a)*52:.1f}" stroke="{A}" stroke-opacity="0.4" stroke-width="0.9"/>')
    s.append(f'<circle cx="0" cy="0" r="7" fill="{A}" opacity="0.8"/>')
    s.append('</g>')
    s.append(glow(W / 2, 640, 90, A, 0.35, p + "soft"))

    # 肩甲
    s.append(pauldron(W / 2, 452, -1, 150, 96, p))
    s.append(pauldron(W / 2, 452, 1, 150, 96, p))

    # 腰带
    s.append(f'<rect x="{W/2-112}" y="748" width="224" height="26" fill="#05090B"/>')
    s.append(f'<rect x="{W/2-112}" y="748" width="224" height="26" fill="none" stroke="{A}" stroke-opacity="0.55" stroke-width="1.2"/>')
    s.append(f'<rect x="{W/2-16}" y="744" width="32" height="34" fill="#05090B" stroke="{A}" stroke-opacity="0.7" stroke-width="1.2"/>')

    # 衣纹
    rnd = random.Random(33)
    for i in range(10):
        x0 = W / 2 + rnd.uniform(-140, 140)
        y0 = 800 + rnd.uniform(0, 110)
        pts = [(x0 + k * rnd.uniform(-6, 6), y0 + k * 44) for k in range(5)]
        s.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{BONE}" stroke-opacity="{rnd.uniform(0.04,0.1):.3f}" stroke-width="1.1"/>')

    # 颈 + 立领
    s.append(f'<path d="M {W/2-32} 376 L {W/2-32} 448 L {W/2+32} 448 L {W/2+32} 376 Z" fill="#060B0D"/>')
    s.append(collar(W / 2, 396, 132, 62, p))

    # 头
    hd = head(W / 2, 302, 60, 78)
    s.append(f'<path d="{hd}" fill="url(#{p}body)"/>')
    s.append(rim(hd, A, p, 0.6, 2))

    # 短发 + 冠环
    s.append(f'<path d="M {W/2-60} 286 C {W/2-56} 232 {W/2+56} 232 {W/2+60} 286 C {W/2+40} 258 {W/2-40} 258 {W/2-60} 286 Z" fill="#05090B"/>')
    s.append(f'<ellipse cx="{W/2}" cy="252" rx="62" ry="16" fill="none" stroke="{A}" stroke-opacity="0.65" stroke-width="1.6"/>')
    s.append(f'<ellipse cx="{W/2}" cy="252" rx="62" ry="16" fill="none" stroke="{A}" stroke-opacity="0.25" stroke-width="6" filter="url(#{p}soft3)"/>')
    s.append(f'<circle cx="{W/2}" cy="236" r="6" fill="{A}" opacity="0.9"/>')
    s.append(glow(W / 2, 236, 44, A, 0.6, p + "soft"))

    # 面部微光
    s.append(f'<ellipse cx="{W/2}" cy="318" rx="32" ry="38" fill="{A}" opacity="0.06" filter="url(#{p}soft6)"/>')

    # 粒子
    rnd2 = random.Random(55)
    for _ in range(50):
        x = rnd2.uniform(0, W)
        y = rnd2.uniform(0, H)
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd2.uniform(0.5,2.2):.1f}" fill="{A}" opacity="{rnd2.uniform(0.1,0.55):.2f}"/>')

    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}fade)"/>')
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("fig-auriel.svg", "".join(s))


# ------------------------------------------------------------
# 2. 卡西娅 · 星图师
# ------------------------------------------------------------
def fig_cassia():
    p = "c"
    s = brass_bg(p, 41, 10)

    # 星图圆盘
    s.append(f'<g opacity="0.4" transform="translate({W/2},450)">')
    for r, o in [(320, 0.16), (270, 0.2), (220, 0.14)]:
        s.append(f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="{A}" stroke-opacity="{o}" stroke-width="1"/>')
    rnd0 = random.Random(9)
    for _ in range(26):
        a = rnd0.uniform(0, math.tau)
        r = rnd0.uniform(60, 320)
        s.append(f'<circle cx="{math.cos(a)*r:.0f}" cy="{math.sin(a)*r:.0f}" r="{rnd0.uniform(1,2.6):.1f}" fill="{A}" opacity="{rnd0.uniform(0.2,0.7):.2f}"/>')
    for _ in range(14):
        a1 = rnd0.uniform(0, math.tau)
        r1 = rnd0.uniform(60, 320)
        a2 = a1 + rnd0.uniform(-0.5, 0.5)
        r2 = r1 + rnd0.uniform(-70, 70)
        s.append(f'<line x1="{math.cos(a1)*r1:.0f}" y1="{math.sin(a1)*r1:.0f}" x2="{math.cos(a2)*r2:.0f}" y2="{math.sin(a2)*r2:.0f}" stroke="{A}" stroke-opacity="0.18" stroke-width="0.8"/>')
    s.append('</g>')

    s.append(shadow(p))

    body = torso(W / 2, 444, 262, 182, 772, 460)
    s.append(f'<path d="{body}" fill="url(#{p}body)"/>')
    s.append(rim(body, A, p, 0.5, 2.2))

    # 高领长袍 + 侧开衩
    s.append(f'<path d="M {W/2-131} 456 C {W/2-186} 560 {W/2-196} 720 {W/2-188} 900 L {W/2+188} 900 C {W/2+196} 720 {W/2+186} 560 {W/2+131} 456 Z" fill="#05090B" opacity="0.75"/>')

    # 胸前星图纹
    s.append(f'<g opacity="0.55" transform="translate({W/2},630)">')
    s.append(f'<circle cx="0" cy="0" r="44" fill="none" stroke="{A}" stroke-opacity="0.5" stroke-width="1"/>')
    for i in range(5):
        a = i * math.tau / 5 - math.pi / 2
        s.append(f'<circle cx="{math.cos(a)*44:.1f}" cy="{math.sin(a)*44:.1f}" r="3" fill="{A}" opacity="0.8"/>')
    s.append(f'<path d="M 0 -44 L 42 14 L -42 14 Z" fill="none" stroke="{A}" stroke-opacity="0.3" stroke-width="0.9"/>')
    s.append('</g>')

    # 肩甲（小）
    s.append(pauldron(W / 2, 458, -1, 132, 74, p))
    s.append(pauldron(W / 2, 458, 1, 132, 74, p))

    # 腰带
    s.append(f'<rect x="{W/2-100}" y="756" width="200" height="22" fill="#05090B"/>')
    s.append(f'<rect x="{W/2-100}" y="756" width="200" height="22" fill="none" stroke="{A}" stroke-opacity="0.5" stroke-width="1.1"/>')

    # 衣纹
    rnd = random.Random(43)
    for i in range(9):
        x0 = W / 2 + rnd.uniform(-120, 120)
        y0 = 800 + rnd.uniform(0, 90)
        pts = [(x0 + k * rnd.uniform(-5, 5), y0 + k * 46) for k in range(5)]
        s.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{BONE}" stroke-opacity="{rnd.uniform(0.04,0.1):.3f}" stroke-width="1.1"/>')

    # 颈 + 立领
    s.append(f'<path d="M {W/2-28} 384 L {W/2-28} 456 L {W/2+28} 456 L {W/2+28} 384 Z" fill="#060B0D"/>')
    s.append(collar(W / 2, 402, 118, 56, p))

    # 头
    hd = head(W / 2, 310, 56, 74)
    s.append(f'<path d="{hd}" fill="url(#{p}body)"/>')
    s.append(rim(hd, A, p, 0.55, 1.9))

    # 长发（垂至肩）
    s.append(f'<path d="M {W/2-58} 292 C {W/2-72} 350 {W/2-70} 420 {W/2-56} 470 L {W/2-34} 470 C {W/2-44} 410 {W/2-44} 350 {W/2-40} 300 Z" fill="#05090B"/>')
    s.append(f'<path d="M {W/2+58} 292 C {W/2+72} 350 {W/2+70} 420 {W/2+56} 470 L {W/2+34} 470 C {W/2+44} 410 {W/2+44} 350 {W/2+40} 300 Z" fill="#05090B"/>')
    s.append(f'<path d="M {W/2-58} 286 C {W/2-50} 240 {W/2+50} 240 {W/2+58} 286 C {W/2+34} 262 {W/2-34} 262 {W/2-58} 286 Z" fill="#05090B"/>')

    # 额饰
    s.append(f'<path d="M {W/2-46} 268 L {W/2} 254 L {W/2+46} 268" fill="none" stroke="{A}" stroke-opacity="0.7" stroke-width="1.6"/>')
    s.append(f'<circle cx="{W/2}" cy="252" r="5" fill="{A}" opacity="0.9"/>')
    s.append(glow(W / 2, 252, 38, A, 0.55, p + "soft"))

    # 手持星盘
    s.append(f'<g transform="translate({W/2+206},690)">')
    s.append(f'<circle cx="0" cy="0" r="62" fill="#05090B" stroke="{A}" stroke-opacity="0.6" stroke-width="1.4"/>')
    s.append(f'<circle cx="0" cy="0" r="46" fill="none" stroke="{A}" stroke-opacity="0.35" stroke-width="0.9"/>')
    for i in range(12):
        a = i * math.tau / 12
        s.append(f'<line x1="{math.cos(a)*46:.1f}" y1="{math.sin(a)*46:.1f}" x2="{math.cos(a)*62:.1f}" y2="{math.sin(a)*62:.1f}" stroke="{A}" stroke-opacity="0.4" stroke-width="0.9"/>')
    s.append(f'<circle cx="0" cy="0" r="6" fill="{A}" opacity="0.85"/>')
    s.append(glow(0, 0, 80, A, 0.4, p + "soft"))
    s.append('</g>')

    rnd2 = random.Random(67)
    for _ in range(44):
        x = rnd2.uniform(0, W)
        y = rnd2.uniform(0, H)
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd2.uniform(0.5,2):.1f}" fill="{A}" opacity="{rnd2.uniform(0.1,0.5):.2f}"/>')

    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}fade)"/>')
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("fig-cassia.svg", "".join(s))


# ------------------------------------------------------------
# 3. 塞维鲁 · 界战统帅
# ------------------------------------------------------------
def fig_severus():
    p = "v"
    s = brass_bg(p, 61, 16)

    # 战旗光带
    s.append(f'<g opacity="0.3">')
    for i in range(5):
        x = 120 + i * 170
        s.append(f'<rect x="{x}" y="0" width="3" height="{H}" fill="{A}" opacity="0.25"/>')
    s.append('</g>')

    s.append(shadow(p))

    # 重甲躯干（更宽）
    body = torso(W / 2, 424, 340, 236, 750, 560)
    s.append(f'<path d="{body}" fill="url(#{p}body)"/>')
    s.append(rim(body, A, p, 0.6, 2.6))

    # 胸甲块面
    s.append(f'<path d="M {W/2-150} 470 L {W/2} 452 L {W/2+150} 470 L {W/2+128} 700 L {W/2} 736 L {W/2-128} 700 Z" fill="#070D0F"/>')
    s.append(f'<path d="M {W/2-150} 470 L {W/2} 452 L {W/2+150} 470 L {W/2+128} 700 L {W/2} 736 L {W/2-128} 700 Z" fill="none" stroke="{A}" stroke-opacity="0.6" stroke-width="1.4"/>')
    s.append(f'<line x1="{W/2}" y1="452" x2="{W/2}" y2="736" stroke="{A}" stroke-opacity="0.35" stroke-width="1.2"/>')
    s.append(f'<path d="M {W/2-96} 560 L {W/2} 528 L {W/2+96} 560" fill="none" stroke="{A}" stroke-opacity="0.4" stroke-width="1.2"/>')

    # 大肩甲
    s.append(pauldron(W / 2, 440, -1, 190, 130, p))
    s.append(pauldron(W / 2, 440, 1, 190, 130, p))

    # 披风
    cape = (f"M {W/2-170} 440 C {W/2-280} 560 {W/2-300} 820 {W/2-286} 1090 "
            f"L {W/2+286} 1090 C {W/2+300} 820 {W/2+280} 560 {W/2+170} 440 Z")
    s.append(f'<path d="{cape}" fill="#04080A" opacity="0.92"/>')
    s.append(rim(cape, A, p, 0.3, 1.8))

    # 腰带
    s.append(f'<rect x="{W/2-130}" y="736" width="260" height="30" fill="#05090B"/>')
    s.append(f'<rect x="{W/2-130}" y="736" width="260" height="30" fill="none" stroke="{A}" stroke-opacity="0.6" stroke-width="1.3"/>')
    s.append(f'<circle cx="{W/2}" cy="751" r="12" fill="none" stroke="{A}" stroke-opacity="0.8" stroke-width="1.6"/>')

    # 颈 + 高护颈
    s.append(f'<path d="M {W/2-38} 366 L {W/2-38} 440 L {W/2+38} 440 L {W/2+38} 366 Z" fill="#060B0D"/>')
    s.append(collar(W / 2, 384, 150, 70, p))

    # 头
    hd = head(W / 2, 292, 62, 80)
    s.append(f'<path d="{hd}" fill="url(#{p}body)"/>')
    s.append(rim(hd, A, p, 0.6, 2))

    # 头盔：覆盖上半 + 鼻梁护条
    s.append(f'<path d="M {W/2-64} 300 C {W/2-64} 226 {W/2+64} 226 {W/2+64} 300 L {W/2+58} 300 C {W/2+58} 244 {W/2-58} 244 {W/2-58} 300 Z" fill="#05090B"/>')
    s.append(f'<path d="M {W/2-64} 300 C {W/2-64} 226 {W/2+64} 226 {W/2+64} 300" fill="none" stroke="{A}" stroke-opacity="0.65" stroke-width="1.6"/>')
    s.append(f'<rect x="{W/2-5}" y="252" width="10" height="86" fill="#05090B" stroke="{A}" stroke-opacity="0.5" stroke-width="1"/>')
    s.append(f'<path d="M {W/2-64} 300 L {W/2-72} 330 L {W/2-56} 322 Z" fill="#05090B" stroke="{A}" stroke-opacity="0.45" stroke-width="1"/>')
    s.append(f'<path d="M {W/2+64} 300 L {W/2+72} 330 L {W/2+56} 322 Z" fill="#05090B" stroke="{A}" stroke-opacity="0.45" stroke-width="1"/>')
    # 盔顶羽饰
    s.append(f'<path d="M {W/2} 226 C {W/2-14} 190 {W/2-6} 160 {W/2+10} 140" fill="none" stroke="{A}" stroke-opacity="0.5" stroke-width="3" stroke-linecap="round"/>')
    s.append(f'<circle cx="{W/2}" cy="228" r="6" fill="{A}" opacity="0.9"/>')
    s.append(glow(W / 2, 228, 46, A, 0.6, p + "soft"))

    # 目缝微光
    s.append(f'<rect x="{W/2-46}" y="306" width="34" height="4" fill="{A}" opacity="0.55"/>')
    s.append(f'<rect x="{W/2+12}" y="306" width="34" height="4" fill="{A}" opacity="0.55"/>')
    s.append(f'<rect x="{W/2-46}" y="306" width="92" height="4" fill="{A}" opacity="0.2" filter="url(#{p}soft3)"/>')

    # 长枪
    s.append(f'<g transform="translate({W/2-236},700) rotate(-6)">')
    s.append(f'<rect x="-4" y="-460" width="8" height="620" fill="#05090B"/>')
    s.append(f'<rect x="-4" y="-460" width="8" height="620" fill="none" stroke="{A}" stroke-opacity="0.45" stroke-width="1"/>')
    s.append(f'<path d="M 0 -560 L 14 -470 L 0 -452 L -14 -470 Z" fill="#05090B" stroke="{A}" stroke-opacity="0.7" stroke-width="1.3"/>')
    s.append(glow(0, -500, 60, A, 0.45, p + "soft"))
    s.append('</g>')

    rnd2 = random.Random(73)
    for _ in range(48):
        x = rnd2.uniform(0, W)
        y = rnd2.uniform(0, H)
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd2.uniform(0.5,2.2):.1f}" fill="{A}" opacity="{rnd2.uniform(0.1,0.5):.2f}"/>')

    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}fade)"/>')
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("fig-severus.svg", "".join(s))


if __name__ == "__main__":
    print("生成奥瑞恩人物...")
    fig_auriel()
    fig_cassia()
    fig_severus()
    print("完成")