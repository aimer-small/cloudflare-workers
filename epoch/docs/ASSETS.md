---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: e9a66d4f35ebbacd2fb7fcf643613b8a_fbe3b8f4e8a911f1aa8b525400dc9a98
    ReservedCode1: OeaEeXohwcQorxS7gpkjB9I9veYSN8O23KwR7wYwnu0K/AHpLvWHR1kqz4XnSoxpeJ3ln/ZP/koemiH6xQMBswlZCsV1v93zTCPltEYYU0gKKSGTH39nkvg//3k5KishQ0zmxJGbJdfdJbt5N4ipapnU7WvxJFWCdneBgtAGQpvvf+pso7nRnavwyE4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: e9a66d4f35ebbacd2fb7fcf643613b8a_fbe3b8f4e8a911f1aa8b525400dc9a98
    ReservedCode2: OeaEeXohwcQorxS7gpkjB9I9veYSN8O23KwR7wYwnu0K/AHpLvWHR1kqz4XnSoxpeJ3ln/ZP/koemiH6xQMBswlZCsV1v93zTCPltEYYU0gKKSGTH39nkvg//3k5KishQ0zmxJGbJdfdJbt5N4ipapnU7WvxJFWCdneBgtAGQpvvf+pso7nRnavwyE4=
---

# 资产清单 · 裂界纪 2.0「双轨纪」

全部图像为**手工程序化 SVG**（Python 脚本生成，无外部素材、无位图、无版权依赖）。
配色 token 统一出自 `assets/css/site.css` 的 `:root`。

---

## 一、图像资产（15 个 SVG）

### 首屏

| 文件 | 尺寸 | 内容 | 用途 |
|---|---|---|---|
| `hero-dual.svg` | 1600×900 | 中央竖线分界，左侧玉青山脊与云，右侧黄铜几何星图与塔影，两半同一地平线 | 首屏主视觉，象征双轨并置 |

### 东线 · 青鸾执月（玉青 `#2E7D6E` / `#8FC4B4` / `#D6E8E1`）

| 文件 | 尺寸 | 内容 |
|---|---|---|
| `east-qingluan.svg` | 1600×900 | 青羽长尾的鸟自左飞向圆月，喙衔一点光，身后虚线轨迹 |
| `east-moon.svg` | 1600×900 | 巨大月轮占画面，外圈二十四道刻度，前景山脊四个仰望剪影 |
| `east-chaser.svg` | 1600×900 | 层叠山峦间折线山道，十余持卷剪影沿道而行，远山一轮小月 |

### 西线 · 铜律锁星（黄铜 `#9A7B3F` / `#C9AE7A` / `#EDE2C9`）

| 文件 | 尺寸 | 内容 |
|---|---|---|
| `west-return.svg` | 1600×900 | 旧城几何轮廓上方，大量名字与编号自地面浮起 |
| `west-lockstar.svg` | 1600×900 | 黄铜同心圆法阵覆盖夜空网格，阵心星标注 `ORI-0001` |
| `west-tower.svg` | 1600×900 | 多层白塔线稿，塔身布满细小 ORI 编号刻痕 |

### 交汇

| 文件 | 尺寸 | 内容 |
|---|---|---|
| `converge.svg` | 1600×900 | 中央圆体：左半玉青描边带月相刻度，右半黄铜描边带网格坐标，中缝一道细线 |

### 人物（900×1200 竖版）

| 文件 | 归属 | 形象 |
|---|---|---|
| `fig-yunxiu.svg` | 东 | 云岫 · 深墨长袍，手持展开卷轴，腰挂锈剑 |
| `fig-alun.svg` | 东 | 阿鸾 · 深墨长裙立于月轮前，手托小月，青羽飘落 |
| `fig-wuming.svg` | 东 | 无名 · 背对观者立于碑前，第四字为虚线空框，笔落于地 |
| `fig-cassia.svg` | 西 | 卡西娅 · 手持黄铜星盘，背后巨大星图圆盘与网格 |
| `fig-severus.svg` | 西 | 塞维鲁 · 深墨披风侧身在砖墙上书写，墙面密布黄铜名字 |
| `fig-72.svg` | 西 | 第七十二 · 半透明人形，头顶 `0072` 方框，胸口被划掉的名字 |

### 备用

| 文件 | 说明 |
|---|---|
| `timeline.svg` | 左右双列 SVG 版纪年表。当前页面改用 HTML/CSS 实现（响应式更好、可被屏幕阅读器读取），此文件保留备用 |

---

## 二、样式与脚本

| 文件 | 体积 | 说明 |
|---|---|---|
| `assets/css/site.css` | 约 17KB | 全站唯一样式表。CSS 自定义属性建 token：纸/墨/玉青/黄铜/丹砂；含双线主题、图版、人物卡、交汇对照、纪年表、页脚、响应式（760px 断点）、`prefers-reduced-motion`、打印样式 |
| `assets/js/site.js` | 约 2.5KB | 原生 JS，零依赖。滚动揭示（IntersectionObserver）、顶栏下滚隐藏/上滚出现、导航当前章节高亮、图片加载失败兜底 |

---

## 三、字体策略

不加载任何 Web Font，避免 FOUT 与体积开销，直接使用系统字体栈：

```
--serif: "Noto Serif CJK SC", "Source Han Serif SC", "Songti SC", "SimSun", Georgia, serif
--sans : "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", system-ui, sans-serif
--mono : "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace
```

中文正文走衬线（纸感、纪年感），编号与图注走等宽（档案感）。

---

## 四、色彩语义

| Token | 值 | 语义 |
|---|---|---|
| `--paper` | `#F7F4EC` | 纸底，全站主背景 |
| `--paper-2` | `#EFEAE0` | 次级纸面，图版底 |
| `--ink` | `#1C2624` | 正文墨色 |
| `--jade` | `#2E7D6E` | **东线专属**：青鸾、月、追月者 |
| `--brass` | `#9A7B3F` | **西线专属**：编号、锁星阵、白塔 |
| `--cinnabar` | `#B04A38` | **仅用于「至今」**，全站出现不超过 3 处 |

对比度：`--ink` 于 `--paper` 上约 13.8:1，`--ink-3` 于 `--paper` 上约 5.6:1，均满足 WCAG AA。

---

## 五、重新生成

生成脚本未随站点部署，保存在会话中间产物目录 `temp/gen-scripts/`：

```
_gen_light.py      # 调色板、山脊、云、月轮、印章、网格等公共绘图函数
_gen_scenes.py     # 8 张横版场景
_gen_figures.py    # 6 张竖版人物
_gen_timeline.py   # SVG 版纪年表
```

运行方式：`python3 _gen_scenes.py`，输出到 `assets/img/`。
*（内容由AI生成，仅供参考）*
