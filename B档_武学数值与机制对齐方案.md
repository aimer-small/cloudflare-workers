---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: e9a66d4f35ebbacd2fb7fcf643613b8a_e3ef2a71e7d611f1a03c525400638852
    ReservedCode1: uQvzZa6dpJTKFhcJchwSo/Ednn9wiQp2jMRijIsXDy9sTXUl3i/O8qMGxQBTRkXVBMhMwG9hmLpglvbDQKlF7vyw/R8/kAu1bCoarGkB3ELMDKeQOg+60ax3bCn13ZTViJg6bIGaykkBN/oMc9RaFyzvWJSY90DRpHTApCYVZN1M5r0iHHGsimtDDR0=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: e9a66d4f35ebbacd2fb7fcf643613b8a_e3ef2a71e7d611f1a03c525400638852
    ReservedCode2: uQvzZa6dpJTKFhcJchwSo/Ednn9wiQp2jMRijIsXDy9sTXUl3i/O8qMGxQBTRkXVBMhMwG9hmLpglvbDQKlF7vyw/R8/kAu1bCoarGkB3ELMDKeQOg+60ax3bCn13ZTViJg6bIGaykkBN/oMc9RaFyzvWJSY90DRpHTApCYVZN1M5r0iHHGsimtDDR0=
---

# B档：书剑3 武学/技能 → GoMud 数值公式与核心机制对齐方案

> 范围：kungfu/skill 840 个武学、kungfu/condition 186 个状态、kungfu/class 316 个门派脚本
> 目标：在保留书剑3 门派差异与招式风味的前提下，接入 GoMud 原生战斗系统，不重写引擎

---

## 一、机制对比：原生差异诊断

| 维度 | 书剑3（LPC） | GoMud 原生 | 差异性质 |
|---|---|---|---|
| 技能定义 | `.c` 文件：`action` 数组 + `query_action()` 函数 | yaml（skillid/name/maxlevel）+ JS spell | 结构可映射 |
| **技能等级作用** | 直接参与战斗：level 决定招式池、force/damage 浮动幅度 | **仅作能力开关**（解锁命令），战斗公式不读技能等级 | **根本冲突** |
| 攻击数值来源 | 武学 `query_action` 返回 force/dodge/parry/damage | 武器骰 `dCount*dSides+dBonus` + 力量差加成 | 需折算 |
| 命中判定 | force 对抗目标 dodge/parry | Speed 比例 → `ToHitMin/Max` | 需折算 |
| 闪避 | 武学 dodge 值 | Perception 比例 → `DodgeChance` | 需折算 |
| 招架 | parry 独立减伤 | **无 parry**，仅装备 `DamageReduction` | **缺失** |
| 伤害类型 | 瘀伤/刺伤/砍伤/内伤 | **无伤害类型系统** | **缺失** |
| 连招状态机 | `temp` 变量 + 多段 action 覆盖 | 无（buff 可近似） | 需近似 |
| 内功/中毒状态 | `condition` 周期 `update_condition` | buff：`statmods` + JS `onTrigger` | 可映射 |
| 招式文案 | `action` 数组，按 lvl 门槛 + 加权随机 | `GetAttackMessage(武器子类型, 伤害档位)` 硬编码 | 需注入层 |

**核心结论**：GoMud 的战斗是「属性 + 武器骰」驱动，技能只是开关；书剑3 是「武学等级 + 招式表」驱动。这是 B 档唯一真正的结构性冲突，其余均可映射。

---

## 二、三套方案对比

| 方案 | 做法 | 工作量 | 结果 | 风险 |
|---|---|---|---|---|
| **A 纯文案移植** | 只搬 action 文案，数值全走 GoMud 公式 | 1-2 天 | 风味保留，840 个武学数值差异全丢，门派强弱失衡，玩家感知「所有武学一样」 | 低，但收益也低 |
| **B 数值折算层（推荐）** | 文案池注入 + 武学等级折算为战斗修正 + condition→buff | 3-5 天 | 保留门派差异，公式可控，不动核心引擎 | 中，需改 2 处代码 |
| **C 完整状态机移植** | 实现 query_action 等价物 + temp 状态机 + 伤害类型 + parry | 2-3 周 | 1:1 复刻 | 高，等于重写战斗系统，破坏原生平衡 |

**推荐 B**，理由：
1. GoMud 的 buff `statmods` 已能承接「武学加成」，无需改核心公式；
2. 文案注入点 `items.GetAttackMessage` 已存在，只需加一层 yaml 覆盖分支；
3. 保留 GoMud 原生平衡基线，后续调参有参照。

---

## 三、方案 B 具体映射口径

### 3.1 数值折算公式

书剑3 单次攻击典型值（以黯然销魂掌为例）：
- `force`：250 + random(350) → 250-600
- `damage`：50 + random(50) → 50-100
- `dodge`：random(30) → 0-30
- `parry`：random(20)+10 → 10-30

GoMud 单次攻击：
```
伤害 = RollDice(dCount, dSides) + dBonus
     × (1 + 力量差加成)
     - GetDefense()
```

**折算原则：武学只做修正，不推翻原生公式。**

| 书剑3 字段 | 折算目标 | 公式 |
|---|---|---|
| force | 攻击系数 | `atkCoef = force / 600`（0.42-1.0） |
| damage | 伤害系数 | `dmgCoef = damage / 100`（0.5-1.0） |
| 综合 | 最终伤害 | `GoMud基础骰 × (0.6 + 0.4×atkCoef) × (0.7 + 0.3×dmgCoef)` |
| dodge | 闪避加成 | `DodgeChance += dodge/30 × 15`（最多 +15%） |
| parry | 减伤加成 | `GetDefense += parry × 0.5`（+5~15） |
| damage_type | 文案标签 | 暂不建抗性系统，仅作描述 |

即武学对最终伤害的影响幅度控制在 **±40%** 以内，避免单门派碾压。

### 3.2 技能等级 → 加成曲线

- 书剑3 level 范围 1-500+，GoMud maxlevel 建议设 100
- 映射：`GoMud level = 书剑3 level / 5`
- 加成生效比例：`effect = 0.3 + 0.7 × (level / 100)`
  - 1 级：30% 效果
  - 50 级：65% 效果
  - 100 级：100% 效果

### 3.3 招式文案注入

**数据结构**（新增 yaml，挂 `_datafiles/world/default/skills/`）：
```yaml
skillid: anran-zhang
name: 黯然销魂掌
maxlevel: 100
actions:
  - lvl: 0
    text: "$N挥袖卷出，拍出一掌，只听得噗的一声，这一掌正好击向$n肩头"
    damage_type: 瘀伤
  - lvl: 60
    text: "$N使出一式「心惊肉跳」，掌风忽左忽右，$n难以捉摸"
    damage_type: 瘀伤
```

**运行时取文案**：
1. 按角色当前技能等级过滤 `lvl <= level` 的招式
2. 按本次伤害档位（Miss/Weak/Normal/Heavy/Critical）匹配
3. 同档位内随机取一条

**代码改动**：`internal/items/attack_messages.go` 的 `GetAttackMessage` 增加「技能文案优先」分支（约 50 行），无技能时回落原生表。

### 3.4 连招状态机近似

书剑3 的 `temp("anran")` 多段连招 → GoMud buff：
- `triggercount: 2`，`onTrigger` 时切换文案池
- 只做 **Top 20 知名绝学**（黯然销魂掌、独孤九剑、降龙十八掌等），其余不做

### 3.5 condition → buff

| 书剑3 | GoMud buff |
|---|---|
| `update_condition` 周期伤害 | `onTrigger` 里扣血 + 提示 |
| `query_type` 返回 poison | buff 分类标签 |
| duration 递减 | `triggercount` |

需先验证 GoMud buff JS 的 `ActorObject` 是否暴露扣血方法，否则用 `statmods` 近似（如中毒降 vitality）。

---

## 四、落地路线

| 阶段 | 内容 | 工期 | 验收标准 |
|---|---|---|---|
| **P0 抽样验证** | 选 5 个代表武学（掌/剑/刀/内功/毒）手工转 yaml + 改一处代码 | 0.5 天 | 跑通「技能等级影响伤害」闭环，游戏内可见招式文案 |
| **P1 批量转录** | 840 skill → yaml，脚本解析 action 数组 + query_action 常量 | 1.5 天 | 生成 840 个 yaml，悬空引用 0 |
| **P2 代码层** | GetAttackMessage 注入 + 武学加成计算 + buff 桥接 | 1.5 天 | 编译通过，telnet 验证 3 组对战 |
| **P3 平衡校准** | 抽样 20 组对战，对比书剑3 原始数值曲线 | 1 天 | 同等级对战 TTK 偏差 < 30% |

---

## 五、需拍板的决策点

1. **数值保真度**：±40% 修正（推荐）还是 1:1 复刻（需改核心公式，风险高）
2. **技能等级上限**：GoMud 100 级（推荐）vs 书剑3 500 级原样
3. **伤害类型**：是否新增瘀伤/刺伤/砍伤抗性系统（建议先不做，仅作文案）
4. **状态机范围**：Top 20 绝学（推荐）vs 全量 840
5. **class 目录定位**：316 个文件实为门派任务/杂项 NPC 脚本，非门派武学，建议归入 C 档（任务样板），不占 B 档工作量
*（内容由AI生成，仅供参考）*
