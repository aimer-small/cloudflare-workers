# -*- coding: utf-8 -*-
"""人物概念图：玄洲三人（900x1200 竖版）"""
import math, random, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _gen_common import *

W, H = 900, 1200
OUT = os.path.dirname(os.path.abspath(__file__))


def save(name, body):
    svg = svg_open(W, H) + body + "</svg>"
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("  ->", name, len(svg), "bytes")


def bg(p, accent):
    s = [defs_common(p)]
    s.append(f"""
  <defs>
    <radialGradient id="{p}bg" cx="0.5" cy="0.34" r="0.72">
      <stop offset="0" stop-color="{mix(accent, INK, 0.55)}"/>
      <stop offset="0.42" stop-color="{mix(accent, INK, 0.82)}"/>
      <stop offset="1" stop-color="{INK}"/>
    </radialGradient>
    <radialGradient id="{p}halo" cx="0.5" cy="0.36" r="0.42">
      <stop offset="0" stop-color="{accent}" stop-opacity="0.34"/>
      <stop offset="0.55" stop-color="{accent}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="{p}body" x1="0.15" y1="0" x2="0.85" y2="1">
      <stop offset="0" stop-color="{mix(accent, INK, 0.72)}"/>
      <stop offset="0.42" stop-color="#0A1214"/>
      <stop offset="1" stop-color="#04080A"/>
    </linearGradient>
    <linearGradient id="{p}fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{INK}" stop-opacity="0"/>
      <stop offset="0.72" stop-color="{INK}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="1"/>
    </linearGradient>
  </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}bg)"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}halo)"/>')
    return s


def bg_lines(p, accent, seed, n=14):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x = rnd.uniform(0, W)
        w = rnd.uniform(0.6, 2.2)
        op = rnd.uniform(0.03, 0.12)
        out.append(f'<rect x="{x:.0f}" y="0" width="{w:.1f}" height="{H}" fill="{accent}" opacity="{op:.3f}"/>')
    return "".join(out)


def head(cx, cy, rx, ry):
    return (f"M {cx} {cy-ry} "
            f"C {cx+rx*0.92} {cy-ry} {cx+rx} {cy-ry*0.42} {cx+rx} {cy-ry*0.06} "
            f"C {cx+rx} {cy+ry*0.42} {cx+rx*0.62} {cy+ry*0.86} {cx} {cy+ry} "
            f"C {cx-rx*0.62} {cy+ry*0.86} {cx-rx} {cy+ry*0.42} {cx-rx} {cy-ry*0.06} "
            f"C {cx-rx} {cy-ry*0.42} {cx-rx*0.92} {cy-ry} {cx} {cy-ry} Z")


def torso(cx, y_top, sh_w, waist_w, y_waist, flare, y_bottom=H + 40):
    l_sh = cx - sh_w / 2
    r_sh = cx + sh_w / 2
    l_w = cx - waist_w / 2
    r_w = cx + waist_w / 2
    l_b = cx - flare / 2
    r_b = cx + flare / 2
    return (f"M {cx} {y_top} "
            f"C {l_sh+sh_w*0.18} {y_top} {l_sh} {y_top+34} {l_sh-6} {y_top+86} "
            f"C {l_sh-14} {y_top+150} {l_w-8} {y_waist-70} {l_w} {y_waist} "
            f"C {l_w-10} {y_waist+90} {l_b+18} {y_bottom-160} {l_b} {y_bottom} "
            f"L {r_b} {y_bottom} "
            f"C {r_b-18} {y_bottom-160} {r_w+10} {y_waist+90} {r_w} {y_waist} "
            f"C {r_w+8} {y_waist-70} {r_sh+14} {y_top+150} {r_sh+6} {y_top+86} "
            f"C {r_sh} {y_top+34} {r_sh-sh_w*0.18} {y_top} {cx} {y_top} Z")


def rim(d, accent, p, op=0.55, sw=2.2):
    return (f'<path d="{d}" fill="none" stroke="{accent}" stroke-opacity="{op}" '
            f'stroke-width="{sw}" filter="url(#{p}soft3)"/>')


def shadow(p):
    return f'<ellipse cx="{W/2}" cy="{H-40}" rx="330" ry="70" fill="#000" opacity="0.5" filter="url(#{p}soft2)"/>'


def fig_yuxu():
    p = "y"
    A = JADE
    s = bg(p, A)
    s.append(bg_lines(p, A, 12, 16))
    s.append(stars(W, H, 110, 31, BONE, H * 0.8, 0.3, 1.4, 0.08, 0.5))

    s.append('<g opacity="0.5">')
    for i in range(6):
        r = 210 + i * 46
        s.append(f'<ellipse cx="{W/2}" cy="470" rx="{r}" ry="{r*0.34}" fill="none" '
                 f'stroke="{A}" stroke-opacity="{0.16 - i*0.02:.3f}" stroke-width="1.1" '
                 f'transform="rotate({-16 + i*5} {W/2} 470)"/>')
    s.append('</g>')

    s.append('<g opacity="0.42">')
    for i in range(9):
        a = i * math.tau / 9 - math.pi / 2
        fx = W / 2 + math.cos(a) * 300
        fy = 470 + math.sin(a) * 300 * 0.62
        s.append(f'<g transform="translate({fx:.0f},{fy:.0f}) rotate({math.degrees(a)+90:.0f})">')
        s.append(f'<rect x="-11" y="-30" width="22" height="60" fill="none" stroke="{A}" stroke-opacity="0.5" stroke-width="0.9"/>')
        for k in range(4):
            s.append(f'<line x1="-6" y1="{-20+k*13}" x2="{6-(k%2)*4}" y2="{-20+k*13}" stroke="{A}" stroke-opacity="0.4" stroke-width="1"/>')
        s.append('</g>')
    s.append('</g>')

    s.append(shadow(p))

    for x0, y0, c1, c2, x1, y1 in [(300, 520, 180, 700, 120, 980), (600, 520, 720, 700, 790, 1010)]:
        s.append(f'<path d="M {x0} {y0} C {c1} {c2} {c1-40} {c2+120} {x1} {y1}" '
                 f'fill="none" stroke="{A}" stroke-opacity="0.22" stroke-width="14" filter="url(#{p}soft6)"/>')

    body = torso(W / 2, 430, 300, 210, 760, 520)
    s.append(f'<path d="{body}" fill="url(#{p}body)"/>')
    s.append(rim(body, A, p, 0.5, 2.4))

    for side in (-1, 1):
        sx = W / 2 + side * 150
        d = (f"M {sx} 470 C {sx+side*70} 500 {sx+side*96} 620 {sx+side*80} 760 "
             f"C {sx+side*70} 850 {sx+side*40} 900 {sx+side*10} 910 "
             f"C {sx-side*10} 830 {sx-side*6} 700 {sx-side*4} 600 Z")
        s.append(f'<path d="{d}" fill="url(#{p}body)"/>')
        s.append(rim(d, A, p, 0.34, 1.8))

    s.append(f'<path d="M {W/2-70} 440 L {W/2} 560 L {W/2+70} 440" fill="none" stroke="{A}" stroke-opacity="0.5" stroke-width="2"/>')
    s.append(f'<path d="M {W/2-70} 440 L {W/2} 560 L {W/2+70} 440" fill="none" stroke="{A}" stroke-opacity="0.2" stroke-width="7" filter="url(#{p}soft3)"/>')

    rnd = random.Random(5)
    for i in range(11):
        x0 = W / 2 + rnd.uniform(-150, 150)
        y0 = 600 + rnd.uniform(0, 120)
        pts = [(x0 + k * rnd.uniform(-6, 6), y0 + k * 46) for k in range(6)]
        s.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{BONE}" stroke-opacity="{rnd.uniform(0.04,0.11):.3f}" stroke-width="1.2"/>')

    s.append(f'<rect x="{W/2-118}" y="742" width="236" height="26" fill="#05090B"/>')
    s.append(f'<rect x="{W/2-118}" y="742" width="236" height="26" fill="none" stroke="{A}" stroke-opacity="0.45" stroke-width="1"/>')
    s.append(f'<circle cx="{W/2}" cy="755" r="9" fill="none" stroke="{A}" stroke-opacity="0.7" stroke-width="1.4"/>')

    s.append(f'<path d="M {W/2-34} 372 L {W/2-34} 442 L {W/2+34} 442 L {W/2+34} 372 Z" fill="#060B0D"/>')

    hd = head(W / 2, 300, 62, 80)
    s.append(f'<path d="{hd}" fill="url(#{p}body)"/>')
    s.append(rim(hd, A, p, 0.6, 2))

    s.append(f'<ellipse cx="{W/2}" cy="228" rx="46" ry="30" fill="#05090B"/>')
    s.append(f'<ellipse cx="{W/2}" cy="228" rx="46" ry="30" fill="none" stroke="{A}" stroke-opacity="0.4" stroke-width="1"/>')
    s.append(f'<rect x="{W/2-8}" y="176" width="16" height="34" fill="#05090B"/>')
    s.append(f'<rect x="{W/2-8}" y="176" width="16" height="34" fill="none" stroke="{A}" stroke-opacity="0.55" stroke-width="1"/>')
    s.append(f'<circle cx="{W/2}" cy="172" r="5" fill="{A}" opacity="0.9"/>')
    s.append(glow(W / 2, 172, 40, A, 0.6, p + "soft"))

    s.append(f'<ellipse cx="{W/2}" cy="316" rx="34" ry="40" fill="{A}" opacity="0.05" filter="url(#{p}soft6)"/>')

    rnd2 = random.Random(77)
    for _ in range(46):
        a = rnd2.uniform(0, math.tau)
        r = rnd2.uniform(180, 420)
        x = W / 2 + math.cos(a) * r
        y = 520 + math.sin(a) * r * 0.7
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd2.uniform(0.6,2.2):.1f}" fill="{A}" opacity="{rnd2.uniform(0.1,0.5):.2f}"/>')

    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}fade)"/>')
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("fig-yuxu.svg", "".join(s))


def fig_shenyan():
    p = "s"
    A = JADE
    s = bg(p, A)
    s.append(bg_lines(p, A, 44, 12))
    s.append(stars(W, H, 80, 63, BONE, H * 0.8, 0.3, 1.4, 0.08, 0.5))

    crack = [(W / 2 + math.sin(y / 90) * 22 + math.sin(y / 31) * 8, y) for y in range(-20, H + 40, 24)]
    s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="{A}" stroke-opacity="0.16" stroke-width="26" filter="url(#{p}soft2)"/>')
    s.append(f'<path d="{smooth_path(crack)}" fill="none" stroke="{BONE}" stroke-opacity="0.22" stroke-width="1.4"/>')

    s.append(f'<g opacity="0.4" transform="translate({W/2},470)">')
    for r, op in [(250, 0.22), (200, 0.16), (150, 0.12)]:
        s.append(f'<circle cx="0" cy="0" r="{r}" fill="none" stroke="{A}" stroke-opacity="{op}" stroke-width="1"/>')
    for i in range(48):
        a = i * math.tau / 48
        r1, r2 = 250, 250 - (12 if i % 4 == 0 else 6)
        s.append(f'<line x1="{math.cos(a)*r1:.1f}" y1="{math.sin(a)*r1:.1f}" x2="{math.cos(a)*r2:.1f}" y2="{math.sin(a)*r2:.1f}" stroke="{A}" stroke-opacity="0.3" stroke-width="0.9"/>')
    s.append('</g>')

    s.append(shadow(p))

    body = torso(W / 2, 440, 268, 190, 770, 470)
    s.append(f'<path d="{body}" fill="url(#{p}body)"/>')
    s.append(rim(body, A, p, 0.45, 2.2))

    cape = (f"M {W/2-134} 452 C {W/2-230} 520 {W/2-250} 760 {W/2-236} 1060 "
            f"L {W/2+236} 1060 C {W/2+250} 760 {W/2+230} 520 {W/2+134} 452 Z")
    s.append(f'<path d="{cape}" fill="#05090B" opacity="0.85"/>')
    s.append(rim(cape, A, p, 0.3, 1.6))

    s.append(f'<path d="M {W/2-62} 450 L {W/2} 566 L {W/2+62} 450" fill="none" stroke="{A}" stroke-opacity="0.55" stroke-width="2"/>')

    rnd = random.Random(15)
    for i in range(9):
        x0 = W / 2 + rnd.uniform(-120, 120)
        y0 = 610 + rnd.uniform(0, 100)
        pts = [(x0 + k * rnd.uniform(-5, 5), y0 + k * 50) for k in range(5)]
        s.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{BONE}" stroke-opacity="{rnd.uniform(0.04,0.1):.3f}" stroke-width="1.1"/>')

    s.append(f'<rect x="{W/2-104}" y="752" width="208" height="22" fill="#05090B"/>')
    s.append(f'<rect x="{W/2-104}" y="752" width="208" height="22" fill="none" stroke="{A}" stroke-opacity="0.4" stroke-width="1"/>')
    s.append(f'<g transform="translate({W/2},763)">')
    s.append(f'<circle cx="0" cy="0" r="26" fill="#05090B" stroke="{A}" stroke-opacity="0.6" stroke-width="1.2"/>')
    s.append(f'<circle cx="0" cy="0" r="17" fill="none" stroke="{A}" stroke-opacity="0.35" stroke-width="0.8"/>')
    s.append(f'<line x1="0" y1="-14" x2="0" y2="14" stroke="{A}" stroke-opacity="0.7" stroke-width="1.2"/>')
    s.append(f'<line x1="-14" y1="0" x2="14" y2="0" stroke="{A}" stroke-opacity="0.4" stroke-width="0.8"/>')
    s.append('</g>')

    s.append(f'<path d="M {W/2-30} 380 L {W/2-30} 450 L {W/2+30} 450 L {W/2+30} 380 Z" fill="#060B0D"/>')

    hd = head(W / 2, 306, 58, 76)
    s.append(f'<path d="{hd}" fill="url(#{p}body)"/>')
    s.append(rim(hd, A, p, 0.55, 1.9))

    s.append(f'<path d="M {W/2-58} 268 C {W/2-40} 232 {W/2+40} 232 {W/2+58} 268 C {W/2+30} 250 {W/2-30} 250 {W/2-58} 268 Z" fill="#05090B"/>')
    s.append(f'<rect x="{W/2-6}" y="196" width="12" height="40" fill="#05090B"/>')
    s.append(f'<rect x="{W/2-6}" y="196" width="12" height="40" fill="none" stroke="{A}" stroke-opacity="0.5" stroke-width="1"/>')

    s.append(f'<g transform="translate({W/2+196},700) rotate(8)">')
    s.append(f'<rect x="-3" y="-330" width="6" height="470" fill="#05090B"/>')
    s.append(f'<rect x="-3" y="-330" width="6" height="470" fill="none" stroke="{A}" stroke-opacity="0.4" stroke-width="0.9"/>')
    s.append(f'<circle cx="0" cy="-336" r="12" fill="none" stroke="{A}" stroke-opacity="0.75" stroke-width="1.4"/>')
    s.append(f'<circle cx="0" cy="-336" r="4" fill="{A}" opacity="0.9"/>')
    s.append(glow(0, -336, 44, A, 0.6, p + "soft"))
    s.append('</g>')

    rnd2 = random.Random(91)
    for _ in range(40):
        x = rnd2.uniform(0, W)
        y = rnd2.uniform(0, H)
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd2.uniform(0.5,2):.1f}" fill="{A}" opacity="{rnd2.uniform(0.08,0.45):.2f}"/>')

    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}fade)"/>')
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("fig-shenyan.svg", "".join(s))


def fig_yunxiu():
    p = "x"
    A = JADE
    s = bg(p, A)
    s.append(bg_lines(p, A, 71, 10))
    s.append(stars(W, H, 70, 83, BONE, H * 0.8, 0.3, 1.4, 0.08, 0.5))

    s.append('<g opacity="0.45">')
    for i in range(3):
        r = 300 + i * 40
        s.append(f'<path d="M {W/2-r} 620 A {r} {r*0.9} 0 0 1 {W/2+r} 620" fill="none" '
                 f'stroke="{A}" stroke-opacity="{0.3 - i*0.08:.2f}" stroke-width="{3 - i*0.6}" filter="url(#{p}soft3)"/>')
    s.append('</g>')

    s.append(shadow(p))

    body = torso(W / 2, 452, 250, 176, 780, 430)
    s.append(f'<path d="{body}" fill="url(#{p}body)"/>')
    s.append(rim(body, A, p, 0.5, 2.2))

    s.append(f'<path d="M {W/2-126} 462 C {W/2-176} 560 {W/2-186} 700 {W/2-176} 820 L {W/2+176} 820 C {W/2+186} 700 {W/2+176} 560 {W/2+126} 462 Z" fill="#05090B" opacity="0.8"/>')

    s.append(f'<path d="M {W/2-56} 462 L {W/2} 570 L {W/2+56} 462" fill="none" stroke="{A}" stroke-opacity="0.55" stroke-width="2"/>')

    rnd = random.Random(23)
    for i in range(8):
        x0 = W / 2 + rnd.uniform(-110, 110)
        y0 = 620 + rnd.uniform(0, 90)
        pts = [(x0 + k * rnd.uniform(-5, 5), y0 + k * 48) for k in range(5)]
        s.append(f'<path d="{smooth_path(pts)}" fill="none" stroke="{BONE}" stroke-opacity="{rnd.uniform(0.04,0.1):.3f}" stroke-width="1.1"/>')

    s.append(f'<rect x="{W/2-96}" y="762" width="192" height="20" fill="#05090B"/>')
    s.append(f'<rect x="{W/2-96}" y="762" width="192" height="20" fill="none" stroke="{A}" stroke-opacity="0.4" stroke-width="1"/>')

    s.append(f'<path d="M {W/2-28} 392 L {W/2-28} 462 L {W/2+28} 462 L {W/2+28} 392 Z" fill="#060B0D"/>')

    hd = head(W / 2, 318, 56, 74)
    s.append(f'<path d="{hd}" fill="url(#{p}body)"/>')
    s.append(rim(hd, A, p, 0.55, 1.9))

    s.append(f'<path d="M {W/2-54} 282 C {W/2-30} 244 {W/2+30} 244 {W/2+54} 282 C {W/2+26} 262 {W/2-26} 262 {W/2-54} 282 Z" fill="#05090B"/>')
    s.append(f'<path d="M {W/2+40} 268 C {W/2+96} 300 {W/2+110} 400 {W/2+86} 500" fill="none" stroke="#05090B" stroke-width="16" stroke-linecap="round"/>')
    s.append(f'<path d="M {W/2+40} 268 C {W/2+96} 300 {W/2+110} 400 {W/2+86} 500" fill="none" stroke="{A}" stroke-opacity="0.3" stroke-width="1.6"/>')

    s.append(f'<g transform="translate({W/2-150},760) rotate(-24)">')
    s.append(f'<rect x="-4" y="-420" width="8" height="520" fill="#05090B"/>')
    s.append(f'<rect x="-4" y="-420" width="8" height="520" fill="none" stroke="{A}" stroke-opacity="0.45" stroke-width="1"/>')
    s.append(f'<rect x="-16" y="96" width="32" height="10" fill="#05090B" stroke="{A}" stroke-opacity="0.5" stroke-width="1"/>')
    s.append(f'<rect x="-5" y="106" width="10" height="60" fill="#05090B" stroke="{A}" stroke-opacity="0.35" stroke-width="0.9"/>')
    s.append('</g>')

    rnd2 = random.Random(101)
    for _ in range(44):
        x = rnd2.uniform(0, W)
        y = rnd2.uniform(0, H)
        s.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd2.uniform(0.5,2.2):.1f}" fill="{A}" opacity="{rnd2.uniform(0.08,0.5):.2f}"/>')

    s.append(f'<rect width="{W}" height="{H}" fill="url(#{p}fade)"/>')
    s.append(grain_rect(W, H, p + "grain", 0.9))
    save("fig-yunxiu.svg", "".join(s))


if __name__ == "__main__":
    print("生成玄洲人物...")
    fig_yuxu()
    fig_shenyan()
    fig_yunxiu()
    print("完成")