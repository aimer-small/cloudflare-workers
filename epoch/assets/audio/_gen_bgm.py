# -*- coding: utf-8 -*-
"""纯标准库合成史诗氛围音乐（无 numpy / 无 ffmpeg）
输出 22050Hz 16bit 单声道 WAV，约 150 秒可无缝循环
"""
import wave, math, random, array, os, sys

SR = 22050
DUR = 150.0
N = int(SR * DUR)
OUT = os.path.dirname(os.path.abspath(__file__))

buf = array.array('d', [0.0]) * N


def osc_add(freq, start, length, amp, detune=0.0, attack=1.2, release=2.0, shape=1.0):
    """递推正弦振荡器 + 包络，叠加到 buf"""
    f = freq + detune
    if f <= 0 or f >= SR / 2:
        return
    w = 2.0 * math.pi * f / SR
    c = 2.0 * math.cos(w)
    y1 = math.sin(-w)
    y2 = math.sin(-2 * w)
    s0 = int(start * SR)
    n = int(length * SR)
    a_n = max(1, int(attack * SR))
    r_n = max(1, int(release * SR))
    end = min(N, s0 + n)
    for i in range(s0, end):
        y = c * y1 - y2
        y2 = y1
        y1 = y
        k = i - s0
        if k < a_n:
            env = k / a_n
        elif k > n - r_n:
            env = max(0.0, (n - k) / r_n)
        else:
            env = 1.0
        buf[i] += y * amp * env


def bell(freq, start, amp=0.16, decay=3.2):
    """钟声：基频 + 泛音，指数衰减"""
    s0 = int(start * SR)
    n = int(decay * SR * 1.6)
    end = min(N, s0 + n)
    parts = [(1.0, 1.0), (2.01, 0.42), (2.98, 0.24), (4.07, 0.12)]
    oscs = []
    for mult, pa in parts:
        f = freq * mult
        if f >= SR / 2:
            continue
        w = 2.0 * math.pi * f / SR
        oscs.append((2.0 * math.cos(w), math.sin(-w), math.sin(-2 * w), pa))
    for i in range(s0, end):
        k = i - s0
        t = k / SR
        env = math.exp(-t * (3.0 / decay))
        v = 0.0
        for idx, (c, y1, y2, pa) in enumerate(oscs):
            y = c * y1 - y2
            oscs[idx] = (c, y, y1, pa)
            v += y * pa
        buf[i] += v * amp * env


def drum(start, amp=0.34, dur=1.1, f0=86.0, f1=38.0):
    """低频鼓：扫频正弦 + 快速衰减"""
    s0 = int(start * SR)
    n = int(dur * SR)
    end = min(N, s0 + n)
    phase = 0.0
    for i in range(s0, end):
        k = i - s0
        t = k / n
        f = f0 * (f1 / f0) ** t
        phase += 2.0 * math.pi * f / SR
        env = math.exp(-t * 5.2)
        buf[i] += math.sin(phase) * amp * env


def noise_swell(start, length, amp=0.05, seed=0):
    """风噪：低通随机 + 缓慢包络"""
    rnd = random.Random(seed)
    s0 = int(start * SR)
    n = int(length * SR)
    end = min(N, s0 + n)
    lp = 0.0
    for i in range(s0, end):
        k = i - s0
        t = k / n
        lp = lp * 0.985 + rnd.uniform(-1, 1) * 0.015
        env = math.sin(math.pi * t) ** 1.6
        buf[i] += lp * amp * env * 6.0


# ------------------------------------------------------------
# 1. 和声铺底（A 小调氛围，四和弦循环）
# ------------------------------------------------------------
CHORDS = [
    [110.00, 164.81, 220.00, 261.63],   # Am
    [87.31, 130.81, 174.61, 220.00],    # F
    [130.81, 196.00, 261.63, 329.63],   # C
    [98.00, 146.83, 196.00, 246.94],    # G
]
SEG = 12.0
t = 0.0
ci = 0
while t < DUR:
    chord = CHORDS[ci % len(CHORDS)]
    for f in chord:
        for det, amp in [(-0.55, 0.052), (0.0, 0.062), (0.62, 0.048)]:
            osc_add(f, t, SEG + 3.0, amp, detune=det, attack=2.6, release=3.4)
    t += SEG
    ci += 1

# ------------------------------------------------------------
# 2. 低频 drone（贯穿全曲）
# ------------------------------------------------------------
osc_add(55.0, 0, DUR, 0.085, attack=6.0, release=8.0)
osc_add(82.5, 0, DUR, 0.040, attack=8.0, release=8.0)
osc_add(36.7, 0, DUR, 0.055, attack=10.0, release=10.0)

# ------------------------------------------------------------
# 3. 高音长音（空灵层）
# ------------------------------------------------------------
for st, f in [(18, 659.26), (54, 587.33), (90, 783.99), (126, 659.26)]:
    osc_add(f, st, 26.0, 0.030, attack=5.0, release=8.0)
    osc_add(f * 1.5, st + 2, 22.0, 0.016, attack=6.0, release=8.0)

# ------------------------------------------------------------
# 4. 钟声（稀疏，叙事节点）
# ------------------------------------------------------------
rnd = random.Random(2024)
for st in [4, 22, 40, 58, 76, 94, 112, 130, 146]:
    bell(rnd.choice([440.0, 523.25, 659.26, 783.99]), st, amp=0.13, decay=3.6)

# ------------------------------------------------------------
# 5. 低频鼓（每 8 秒，渐强）
# ------------------------------------------------------------
for i, st in enumerate(range(8, int(DUR), 8)):
    prog = i / max(1, (DUR - 8) / 8)
    drum(st, amp=0.20 + 0.16 * prog)

# ------------------------------------------------------------
# 6. 风噪
# ------------------------------------------------------------
for i in range(6):
    noise_swell(i * 26.0, 30.0, amp=0.045, seed=i * 13 + 1)

# ------------------------------------------------------------
# 7. 简易混响（双抽头反馈延迟）
# ------------------------------------------------------------
d1 = int(0.113 * SR)
d2 = int(0.237 * SR)
for i in range(d1, N):
    buf[i] += buf[i - d1] * 0.26
for i in range(d2, N):
    buf[i] += buf[i - d2] * 0.19

# ------------------------------------------------------------
# 8. 归一化 + 首尾淡化（可循环）
# ------------------------------------------------------------
peak = 0.0
for v in buf:
    av = v if v >= 0 else -v
    if av > peak:
        peak = av
gain = 0.86 / peak if peak > 0 else 1.0

fade = int(2.5 * SR)
out = array.array('h', bytes(2 * N))
for i in range(N):
    v = buf[i] * gain
    if i < fade:
        v *= i / fade
    elif i > N - fade:
        v *= (N - i) / fade
    if v > 1.0:
        v = 1.0
    elif v < -1.0:
        v = -1.0
    out[i] = int(v * 32767)

path = os.path.join(OUT, "bgm-epoch.wav")
with wave.open(path, "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(out.tobytes())
print("done", path, os.path.getsize(path), "bytes", DUR, "s")