# 资产清单与生成方式

全部资产由 Python 脚本程序化生成，无外部素材、无版权风险、无网络请求。

---

## 一、图像资产（SVG）

### 公共工具库

`assets/img/_gen_common.py` 提供全部绘图原语：

| 函数 | 作用 |
|---|---|
| `svg_open(w,h)` | 输出 SVG 头（含 viewBox、命名空间） |
| `defs_common(p)` | 输出通用滤镜（soft / soft2 / soft3 高斯模糊） |
| `ridge(w, base, amp, freq, seed, octaves, persistence, step)` | 生成山脊控制点（多倍频叠加） |
| `ridge_path(pts, w, h)` | 把控制点转成闭合填充路径 |
| `smooth_path(pts)` | 把控制点转成平滑贝塞尔路径 |
| `stars(w, h, n, seed, color, maxY, rmin, rmax, opmin, opmax)` | 星点 |
| `glow(cx, cy, r, color, op, filterId)` | 辉光圆 |
| `grain_rect(w, h, id, op)` | 颗粒噪点覆盖层 |
| `mix(c1, c2, t)` | 颜色插值 |

### 调色板

| 名称 | 值 | 用途 |
|---|---|---|
| `INK` | `#070C0E` | 主背景墨色 |
| `BONE` | `#E6EDE9` | 骨白（文字、线条） |
| `JADE` | `#6FBFA8` | 玄洲玉青 |
| `BRASS` | `#B08D4F` | 奥瑞恩旧黄铜 |
| `CINNABAR` | `#A63D2F` | 丹砂（仅用于「至今」） |

### 资产表

| 文件 | 尺寸 | 生成脚本 | 内容 |
|---|---|---|---|
| `hero-rift.svg` | 1600×900 | `_gen_scenes.py` | 首屏：界痕横贯天际，两侧地貌对峙 |
| `scene-kunlun.svg` | 1600×900 | `_gen_scenes.py` | 昆仑：云海九峰、体积光柱、巨月 |
| `scene-orion-city.svg` | 1600×900 | `_gen_scenes.py` | 奥瑞恩巨城：黄铜几何建筑群 |
| `scene-rift.svg` | 1600×900 | `_gen_scenes.py` | 界痕：发光地裂，两侧地貌断裂 |
| `scene-gate.svg` | 1600×900 | `_gen_scenes2.py` | 界门：光柱贯穿，两侧石柱对峙 |
| `scene-battlefield.svg` | 1600×900 | `_gen_scenes2.py` | 战场：残旗、断柱、血色天光 |
| `scene-monument.svg` | 1600×900 | `_gen_scenes3.py` | 界碑：孤碑立于界痕，左玉青右黄铜 |
| `fig-yuxu.svg` | 900×1200 | `_gen_figures.py` | 玉虚子：守碑人，宽袍、持杖 |
| `fig-shenyan.svg` | 900×1200 | `_gen_figures.py` | 沈砚：测绘者，背负图卷 |
| `fig-yunxiu.svg` | 900×1200 | `_gen_figures.py` | 云岫：少年剑修，持剑 |
| `fig-auriel.svg` | 900×1200 | `_gen_figures2.py` | 奥瑞尔：律法师，高冠、法阵环 |
| `fig-cassia.svg` | 900×1200 | `_gen_figures2.py` | 卡西娅：星图师，星盘 |
| `fig-severus.svg` | 900×1200 | `_gen_figures2.py` | 塞维鲁：统帅，重甲 |
| `map-battle1.svg` | 1200×760 | `_gen_maps.py` | 第一次界战：界痕居中，初裂点 |
| `map-battle2.svg` | 1200×760 | `_gen_maps.py` | 第二次界战：界痕东移，焚城 |
| `map-battle3.svg` | 1200×760 | `_gen_maps.py` | 第三次界战：界痕最东，未决 |

### 重新生成

```bash
cd assets/img
python3 _gen_scenes.py
python3 _gen_scenes2.py
python3 _gen_scenes3.py
python3 _gen_figures.py
python3 _gen_figures2.py
python3 _gen_maps.py
```

渲染预览（可选，需 `rsvg-convert`）：

```bash
rsvg-convert -w 760 scene-gate.svg -o preview.png
```

---

## 二、音频资产（WAV）

### `bgm-epoch.wav`

| 属性 | 值 |
|---|---|
| 时长 | 150.0 秒 |
| 采样率 | 22050 Hz |
| 声道 | 单声道 |
| 位深 | 16 bit |
| 大小 | 约 6.3 MB |
| 循环 | 首尾交叉淡化，可无缝循环 |

### 四层结构

| 层 | 频段 | 音色 | 象征 |
|---|---|---|---|
| 地鸣 | 38 Hz | 正弦 + 缓慢失谐 | 界痕本身 |
| 气流 | 220 Hz | 带通噪声 | 玄洲 |
| 金属泛音 | 880 Hz | 三角波 + 长衰减 | 奥瑞恩 |
| 未解决持续音 | 233.08 Hz | 正弦（与 220 Hz 差半音） | 两界都无法命名的部分 |

### 合成方式

`assets/audio/_gen_bgm.py` 使用**纯 Python 标准库**（`wave`、`math`、`random`、`struct`），不依赖 numpy / scipy / ffmpeg。

核心手法：

1. 各层用相位累加生成正弦/三角波，叠加缓慢 LFO 调制。
2. 噪声层用一阶低通滤波塑形。
3. 混响用多抽头延迟（comb + allpass 简化版）模拟。
4. 首尾 3 秒交叉淡化，保证循环无缝。
5. 整体做软限幅（tanh）防止削波。

### 重新生成

```bash
cd assets/audio
python3 _gen_bgm.py
# 输出 bgm-epoch.wav，耗时约 2 分钟
```

### 降级方案

若 WAV 加载失败（404 / 解码错误 / 自动播放被拦截），`audio.js` 会自动切换到 Web Audio 实时合成：

- 四个振荡器（38 / 220 / 880 / 233.08 Hz）
- `ConvolverNode` 程序生成 3.2 秒脉冲响应（衰减 2.6，湿声 0.55）
- 每 2.1 秒随机触发一个五声音阶音符（C-D-E-G-A）

---

## 三、体积统计

| 类别 | 大小 |
|---|---|
| SVG 图像（16 个） | 约 560 KB |
| WAV 音频 | 约 6.3 MB |
| CSS | 约 29 KB |
| JS | 约 15 KB |
| HTML | 约 21 KB |
| **合计** | **约 6.9 MB** |

> 若需压缩体积，可将 WAV 转 96 kbps MP3（约 1.8 MB）或 64 kbps Opus（约 1.2 MB），并在 `audio.js` 中修改 `SRC` 常量。

---

## 四、版权

- 生成脚本与站点代码：MIT
- 生成的 SVG / WAV：CC BY 4.0
- 无任何第三方素材，可商用。