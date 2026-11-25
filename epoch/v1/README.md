# 裂界纪 · Epoch of the Rift

> 一道界痕，两种本体论。三次界战，至今未终。

一个关于「什么才算存在」的世界观概念展示站。全部图像为**程序化生成 SVG**，音景为**程序合成 WAV**，零外部素材依赖，可直接部署到 Cloudflare Pages / Workers。

---

## 这是什么

环宇大陆纪元一一二七年，大衍之变。一道宽三里、每年东移七里的界痕，把世界劈成两半：

| | 玄洲（东） | 奥瑞恩（西） |
|---|---|---|
| 核心命题 | 以身为炉 | 以名为咒 |
| 存在定义 | 存在即燃烧，名字是外物 | 被命名才存在，未命名可被抹去 |
| 术法形态 | 符箓 = 气的走向图 | 法阵 = 圆 + 七十二刻度 |
| 视觉语言 | 玉青 `#6FBFA8` · 宋体 · 竖排 | 旧黄铜 `#B08D4F` · 衬线大写 · 几何 |
| 代表人物 | 玉虚子 / 沈砚 / 云岫 | 奥瑞尔 / 卡西娅 / 塞维鲁 |

冲突不来自正邪，来自两种各自完备、无法调和的本体论。

---

## 站点结构

```
epoch/
├── index.html                  # 单页站点（序 + 六章 + 页脚）
├── assets/
│   ├── css/
│   │   ├── base.css            # 设计 token、排版、组件基础样式
│   │   └── site.css            # 图片适配、导航、响应式、动效补充
│   ├── js/
│   │   ├── field.js            # Canvas 粒子场 + 界痕扰动
│   │   ├── audio.js            # 音景播放器（WAV + 合成降级）
│   │   └── ui.js               # 导航 / 滚动揭示 / 逐字 / 视差
│   ├── img/                    # 13 张程序化生成 SVG
│   │   ├── hero-rift.svg       # 首屏：界痕横贯天际
│   │   ├── scene-kunlun.svg    # 景物：昆仑
│   │   ├── scene-orion-city.svg# 景物：奥瑞恩巨城
│   │   ├── scene-rift.svg      # 景物：界痕
│   │   ├── scene-gate.svg      # 场景：界门开启
│   │   ├── scene-battlefield.svg # 场景：战场第七年
│   │   ├── scene-monument.svg  # 场景：界碑
│   │   ├── fig-yuxu.svg        # 人物：玉虚子
│   │   ├── fig-shenyan.svg     # 人物：沈砚
│   │   ├── fig-yunxiu.svg      # 人物：云岫
│   │   ├── fig-auriel.svg      # 人物：奥瑞尔
│   │   ├── fig-cassia.svg      # 人物：卡西娅
│   │   ├── fig-severus.svg     # 人物：塞维鲁
│   │   ├── map-battle1.svg     # 节点：第一次界战
│   │   ├── map-battle2.svg     # 节点：第二次界战
│   │   ├── map-battle3.svg     # 节点：第三次界战
│   │   └── _gen_*.py           # 生成脚本（可重新生成全部图像）
│   └── audio/
│       ├── bgm-epoch.wav       # 150s 无缝循环音景（6.3 MB）
│       └── _gen_bgm.py         # 合成脚本（纯标准库）
└── docs/
    ├── WORLDBUILDING.md        # 世界观设定全稿
    ├── ASSETS.md               # 资产清单与生成方式
    ├── DEPLOY.md               # 部署指南
    └── CHANGELOG.md            # 版本记录
```

---

## 章节

| 章节 | 内容 | 视觉 |
|---|---|---|
| 序 · 裂界 | 大衍之变，界痕出现 | 界痕 / 界门 |
| 一 · 两界 | 玄洲与奥瑞恩的本体论分歧 | 昆仑 / 奥瑞恩巨城 |
| 二 · 人物 | 六位角色，各带一句台词 | 六张竖版立绘 |
| 三 · 景物 | 三处两界都承认存在的地方 | 三张横版场景 |
| 四 · 场景 | 门开、旗倒、碑立 | 界门 / 战场 / 界碑 |
| 五 · 节点 | 三次界战，战场每年东移七里 | 三张节点地图 |
| 六 · 音景 | 四层结构，永不解决 | 播放器 + 结构图 |

---

## 技术要点

- **零外部依赖**：无 CDN、无字体文件、无位图、无第三方库。全部 SVG 内联生成，音频本地合成。
- **程序化资产**：所有图像由 `assets/img/_gen_*.py` 生成，改参数即可重出全套。
- **音景**：`bgm-epoch.wav` 为纯 Python 标准库合成（无 numpy / ffmpeg 依赖），150 秒无缝循环；WAV 不可用时自动降级为 Web Audio 实时合成。
- **动效克制**：只做三件事——揭示、扰动、响应。无卡片阴影、无圆角（最大 2px）、无渐变铺底。
- **可访问性**：`prefers-reduced-motion` 全量降级；音景默认静音，需用户主动点击；导航键盘可达。
- **移动端**：`100svh` 首屏、单列退化、导航折叠、音景按钮精简。

---

## 本地预览

```bash
cd epoch
python3 -m http.server 8080
# 打开 http://localhost:8080
```

> 必须用 HTTP 服务打开，直接双击 `index.html` 会导致音频与部分相对路径失效。

---

## 重新生成资产

```bash
cd epoch/assets/img
python3 _gen_scenes.py      # 昆仑 / 奥瑞恩巨城 / 界痕 / 首屏
python3 _gen_scenes2.py     # 界门 / 战场
python3 _gen_scenes3.py     # 界碑
python3 _gen_figures.py     # 玄洲三人
python3 _gen_figures2.py    # 奥瑞恩三人
python3 _gen_maps.py        # 三次界战地图

cd ../audio
python3 _gen_bgm.py         # 重新合成 150s 音景（约 2 分钟）
```

依赖：Python 3.8+。渲染预览图需 `rsvg-convert`（可选）。

---

## 部署

见 [docs/DEPLOY.md](docs/DEPLOY.md)。最短路径：

```bash
# Cloudflare Pages
npx wrangler pages deploy epoch --project-name=epoch-of-the-rift
```

---

## 设计约束（不可违反）

1. 丹砂 `#A63D2F` 全站只用于「至今」——第三次界战与未解决音。
2. 圆角最大 2px，禁止 `box-shadow` 光晕，发光一律由 Canvas / SVG 滤镜实现。
3. 不使用等大圆角卡片网格、全大写标签堆叠、`01/02/03` 序号装饰、渐变铺底。
4. 玄洲侧用宋体与竖排，奥瑞恩侧用衬线大写与几何——两侧排版语言不得混用。
5. 音景默认静音，永不自动播放。

---

## 许可

世界观文本与代码：MIT。
程序化生成的 SVG 与 WAV：CC BY 4.0。