---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: e9a66d4f35ebbacd2fb7fcf643613b8a_fd615e5be8a911f1aa8b525400dc9a98
    ReservedCode1: qgI2kRGfGVdQKsGfvRMgZMWYJOxoKM1vEFcuknE8mjBdADZAqblCxhpOltIkqDA6uE/I/W/9Tdpl5IdwgrTDzyyq1l9UsOaCen+BIPCYwXtfpgLycS8m/EJcv4XlyISe0+7RLGn5wsWVRC3OD8YwU2PgZP08+qNESgZu4KsJCc+kWIUoxXhL+C+rCXA=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: e9a66d4f35ebbacd2fb7fcf643613b8a_fd615e5be8a911f1aa8b525400dc9a98
    ReservedCode2: qgI2kRGfGVdQKsGfvRMgZMWYJOxoKM1vEFcuknE8mjBdADZAqblCxhpOltIkqDA6uE/I/W/9Tdpl5IdwgrTDzyyq1l9UsOaCen+BIPCYwXtfpgLycS8m/EJcv4XlyISe0+7RLGn5wsWVRC3OD8YwU2PgZP08+qNESgZu4KsJCc+kWIUoxXhL+C+rCXA=
---

# 裂界纪 · 双轨纪（EPOCH II）

一个纯静态的世界观概念展示站。仙侠与西幻不是对立，是同一件事的两种叙述。

**2.0「双轨纪」** 为明亮主题版本：纸白底、墨色字、玉青归东、黄铜归西。
1.0 暗色版本完整保留在 `v1/`。

---

## 结构

```
index.html              主页面（单页，六段：首屏 / 序章 / 东线 / 西线 / 交汇 / 纪年表）
assets/css/site.css     全站样式（CSS 变量 token，含响应式与 reduced-motion）
assets/js/site.js       滚动揭示、顶栏行为、导航高亮（原生 JS，2.5KB）
assets/img/*.svg        15 张程序化生成的矢量概念图
docs/WORLDBUILDING-2.0.md   2.0 世界观设定（东西双线、人物、纪年、视觉语言）
docs/ASSETS.md          资产清单与重新生成方式
docs/DEPLOY.md          部署说明
docs/CHANGELOG.md       更新日志（2.0 对 1.0 的完整差异）
v1/                     1.0 暗色版归档（含 150s 音景）
```

零构建、零依赖、零外部素材。直接静态托管即可。

---

## 本地预览

```bash
python3 -m http.server 8000
# http://127.0.0.1:8000
```

---

## 世界线一览

| | 东线 · 青鸾执月 | 西线 · 铜律锁星 |
|---|---|---|
| 地 | 玄洲 | 奥瑞恩 |
| 事 | 青鸾衔月升天，月不可即 | 界痕闭合，名字回流 |
| 法 | 记录。四千三百二十一笔《月行图》 | 编号。锁星阵把夜空划成网格 |
| 命题 | 命名产生了「不是」 | 编号产生了「例外」 |
| 人 | 云岫 / 阿鸾 / 无名 | 卡西娅 / 塞维鲁 / 第七十二 |

1529 年，两条线并置：那颗星在东被叫「执月」，在西被编为 `ORI-0001`。
而它继续移动。

---

## 许可

见 `LICENSE`。图像与文本均为程序化生成本次原创，可自由引用，注明出处即可。
*（内容由AI生成，仅供参考）*
