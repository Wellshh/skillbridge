# Allegro 17.2 内部 DRC 数值模型反向探测报告

状态：**最终版**（Probe A/B/C 全部完成；Probe C run-2 bvc57j0lt exit 0，
Phase 6 与 run-1 b2gigon2b 位一致复现）。原始运行日志存于 `logs/`。
范围：unit=mm，accuracy=4，grid g=1e-4 mm；板 EL5_MIAN_FPC.brd 一次性副本；
自有无头 Allegro 进程 + 唯一端口；未修改任何生产代码。

---

## 0. 探测方法与证据等级

- 每个几何对象严格区分四个量：**requested**（发往 Allegro 的 binary64 位）、
  **committed**（创建后回读 + 独立 re-query 的位）、**externally reconstructed**
  （Python Decimal-60 / binary64 模型计算值）、**DRC result**（marker 的
  expected/actual/verdict）。
- 所有临界用例先离线精确扫描（float 预过滤 + Decimal-60 精确验证），再在
  Allegro 会话内用**本次会话学到的规则值 R** 重新计算放置（不硬编码 0.06）。
- marker `actual` 只是显示层证据；判决以 marker 有无（verdict）为准。
- drc.check(target) 为立即操作，逐对象执行； Probe C 增加 partner-figure
  归属过滤，排除同名 marker 来自其它对象对的污染。

## 1. 已证结论（仅列有直接实验证据的）

### 1.1 提交/存储语义（Probe A，位级证据）

- **Line**：端点在 commit 时量化到整数 DBU（1e-4 mm 格点）；requested==committed
  在格点上成立（Probe B L 阶梯复证）。
- **ARC center**：沿弦垂直平分线分量**位精确保存**（binary64 逐位一致，
  re-query 位一致）；垂直平分线方向的分量被投影掉（残差 ~1e-11）。
- **ARC radius**：派生/存储的 binary64，与 |S−C| 的 Decimal-60 精确值之差：
  Probe A/B 样本 ≤1.6e-14（全为正）；Probe C CC_GRID_FLAG 观测到 −5.573e-14
  → 统一观测包络 |Δr| ≤ 5.6e-14（该弧端点坐标非 binary-exact；机制不推断）。
- **is_clockwise 约定**：cw=False 提交 → None；cw=True 提交 → True；
  committed length 与 math-CW/math-CCW 预测比对校准了方向约定。
- **独立性**：19 条弧 re-query 位一致（Probe B STAGE4），存储非查询时派生。

### 1.2 DRC 测量与判决语义（Probe B，任务 b9phteksv，exit 0）

- **模型 A（全精度测量）确认**：对 committed binary64 几何做全精度测量，
  严格 `measured < rule` 判决。
- **等号判 clean**：GRID_EQ（clearance==R，格点域）clean；−1 grid → FLAGGED；
  无 epsilon 带。
- **亚格点可分辨**：FLIP_LO FLAGGED / FLIP_HI clean，两弧 committed center 差
  Δcy=3.5e-6（==requested，位精确），远小于 1 个 grid → **boxed 问题答案 YES**。
- **格点域精确性**：staircase n0–n5 clean / n6–n10 FLAGGED，翻转发生在
  clearance 跨越 R 的整格点处，无漂移；GRID_EQ 处 FULL/naive-BINARY64 在
  doubles 上有 −2.05e-11 伪差而 Allegro 判 clean → 格点域是 DBU 整数/十进制
  精确算术，或 binary64+极小 epsilon（上界见 §6）。
- **测量分辨率**：≤2.5e-6 已证实（FLIP 窗口边界 (−2.49e-6 FLAGGED,
  +0.57e-6 clean)）。
- **显示层**：marker actual 对 clearance **向零截断**到 4 位小数、去尾零、
  加 ' MM' 后缀（FLIP_LO 0.0599975 → '0.0599 MM'；BELOW display_match=True）。
  推论：`actual==expected 且 FLAGGED` 的金标用例**结构上不可能**——
  FLAGGED ⟹ clear<R ⟹ trunc4 ≤ R−1e-4 或显示截断掉差异；GOLD 用例实际
  显示 '0.0599 MM'。
- **规则学习**：会话内学到 marker 'Line to Line Spacing'，R='0.06 MM'，
  on_grid=True（不硬编码，逐会话学习）。

### 1.3 模型 A 泛化（Probe C，run-2 bvc57j0lt exit 0；Phase 6 与 run-1 b2gigon2b 位一致复现）

- **ARC-ARC 双非格点**：PHASE6_PAIR committed center 差 dcy1−10=3.500000048e-6
  （requested Δ=3.5e-6，位精确），LO FLAGGED / HI clean；GRID/DROUND oracle
  在 CC_FLIP_LO/CC_GOLD 误判 clean → 模型 B/C/D/DROUND 在**纯 ARC 域**再排除，
  并杀死"Line-ARC 中是 line/DBU 侧起作用"的残余解释（细节 §7.1）。
- **ARC-Via 径向**：R_via=0.065（marker 'Line to Thru Via Spacing' expected）与
  pad 半径 rp=0.1500（9 个正 actual 夹逼出的唯一格点候选）均**会话内学习**；
  27 committed via 一致性检验 mismatches=0；CV_FLIP_LO δ=−2.4993e-6 →
  FLAGGED（'0.0649 MM'，display_match=True）/ CV_FLIP_HI +5.669e-7 → clean
  （细节 §7.2）。
- **等号 clean、显示截断、re-query 位一致**在新域复现：CC_GRID_EQ clean
  （DBU-decimal 精确 ==R）、所有 FLAGGED rung display_match=True、
  REQUERY 18/18 identical（count=131）。

## 2. 被排除的模型（引用测试用例）

| 模型 | 内容 | 排除证据 |
|---|---|---|
| B 几何先量化 | center/radius 先量化到 grid 再测量 | Probe B FLIP_LO；Probe C CC_FLIP_LO（纯 ARC-ARC）、CV_FLIP_LO（ARC-Via 径向，GRID oracle clean 实际 FLAGGED） |
| C 距离先取整 | clearance 先 round 到 1e-4 再比较 | Probe B FLIP_LO/GOLD；Probe C CC_FLIP_LO、CC_GOLD（DROUND clean 实际 FLAGGED）、CV_FLIP_LO |
| D 规范重建 | 从量化端点重建圆 | 同 B：无法区分亚格点 center 差（CC_FLIP_LO PHASE6_PAIR Δ=3.5e-6 位精确） |
| DISTANCE-ROUND | round-half-even 到 4 位 | 同 C（CC_FLIP_LO/CC_GOLD/CV_FLIP_LO） |
| naive-BINARY64 | 纯 double 比较 clear<R | Probe B GRID_EQ/STAIR_n7：double 域 −2.05e-11 伪差预测 FLAGGED，实际 clean。（Probe C CC_GRID_EQ 伪差为 +3.64e-14，B64 碰巧判对，不构成反证） |
| 显示=四舍五入 | actual 用 round-half | FLIP_LO 实际 '0.0599 MM'（截断），非 '0.06 MM'；CV_FLIP_LO '0.0649 MM' 同 |

## 3. 最小一致模型（当前全部证据）

1. Line/Via：端点/位置 commit 时量化到整数 DBU（格点输入 committed==requested：
   Probe B L 阶梯；Probe C 27 via dx=dy=0，位级回读）。
2. ARC：center 沿平分线位精确 binary64 存储；radius binary64（|Δr|≤5.6e-14
   观测包络）；非格点几何**不**被量化。
3. 测量：对存储值全精度（格点量走 DBU 精确域；浮点量 binary64 级）；
   无距离量化。该模型在 **Line-ARC、ARC-ARC、ARC-Via 径向**
   （sqrt((cx−xv)²+(cy−yv)²) − r − rp − w/2，rp 为 pad 半径）三域均成立
   （Probe C CV_CONSISTENCY mismatches=0）。
4. 判决：严格 `measured < rule`；等号 clean；无 epsilon 带
   （格点域；非格点域边界被限制在 (−2.5e-6, +0.57e-6) 内翻转，三域一致）。
5. 显示：actual 向零截断 4 位小数；clearance ≤0 时显示 '0 MM'（Probe C
   pass1 j0/j1，via 与弧重叠；clamp-还是-负值截断未区分）。

## 4. 对外部 DRC 引擎（Python/CGAL）的工程含义

- **整数 DBU 全域方案不可行**：Allegro 能分辨亚格点 ARC 几何差异
  （Δ=3.5e-6 mm = 0.035 DBU），把 ARC center/radius 量化到 DBU 会丢失
  Allegro 实际使用的信息（模型 B/D 已被排除）。Probe C 将该结论推广到
  **纯 ARC-ARC 对**（双方 center/radius 均非格点）与 **ARC-Via 径向
  sqrt 距离**（CV_FLIP_LO：GRID oracle 判 clean，Allegro FLAGGED）。
- **推荐表示**：CGAL 精确有理数（或 Python Fraction/Decimal）承载
  requested 几何 + 显式 commit 仿真（§5），比较用严格 `<`，**不加 epsilon**。
  via pad 参与测量（径向减 rp），外部引擎必须持有 padstack 几何。
- **参数可学习性**：规则值 R（'0.06 MM'/'0.065 MM' expected 字段）与 pad 半径
  rp=0.1500（9 个正 actual 夹逼 + 格点唯一性）均可仅从 marker 文本在会话内
  标定——Probe C 全程未硬编码，证明外部引擎可用同样方法自校准。
- **安全方向**：外部精确计算 clear ≥ R ⟹ 已观测 Allegro clean
  （ABOVE/GRID_EQ/staircase n0–n5/CC_FLIP_HI/CV_FLIP_HI）。残余不确定带仅在
  (R−2.5e-6, R)：此带内 Allegro 也 FLAGGED（FLIP_LO/GOLD/BELOW/staircase n6+/
  CC_FLIP_LO/CV_FLIP_LO），即外部判"违例"是保守方向，三域均不存在
  外部 clean 而 Allegro FLAGGED 的已观测反例。
- **naive float 管线不可用**：binary64 直接比较在格点域会产生
  伪 FLAGGED（GRID_EQ），必须先归一到精确域。

## 5. 对 Commit Emulator 的影响

要在外部复现 Allegro 的"committed 几何"，需要模拟：

- Line/Via：坐标 → 最近 DBU（floor/round 语义已有格点证据；requested==committed
  于格点输入）。
- ARC center：保留 binary64；将请求 center 投影到弦垂直平分线
  （off-bisector 分量被丢弃，残差 ~1e-11）；平分线分量位精确。
- ARC radius：以 |S−C_committed| 的 binary64 最近值为中心、±5.6e-14 观测包络
  （Probe C 更新，含一个 −5.573e-14 样本；外部预测取最近 double 即可，
  DRC 分辨率 2.5e-6 比该噪声大 4.5 个数量级）。
- is_clockwise：cw=False→None，cw=True→True（存储约定）。
- 显示层：actual 字符串 = trunc4（向零）+ 去尾零 + ' MM'。

## 6. 开放问题

1. **格点域精确机制**：DBU 整数/十进制算术 vs binary64+epsilon∈[2.05e-11,
   2.49e-6)——现有证据只能夹逼，不能区分；工程结论对两者相同。
2. **非格点域比较精度上限**：翻转边界观测窗 (−2.5e-6, +0.57e-6)；
   更细的 epsilon 结构未探测。
3. **off-bisector 投影语义**：是存储时投影还是显示/导出时派生，未区分
   （DRC 观测上等价）。
4. **radius 噪声来源**：Probe C CC_GRID_FLAG 观测到 −5.573e-14（Probe A/B
   包络 ≤1.6e-14 且全为正）；该弧端点坐标非 binary-exact，推测方向是
   派生路径用了 double 端点算术，但未验证，不下结论。
5. **via 创建 extent 边界**（Probe C run-1 崩溃诊断，badl9grq2 exit 0）：
   空区域（x[288,314] y[580,800] 内 0 vias/0 pins/0 comps/0 shapes/
   0 route segments）中 y≥700 时 x=292..308 全部 `VIA_CREATE_FAILED`，
   y≤698 与 y=480..560 全部 OK → 边界 ∈ (698,700)。错误是创建失败而非 DRC；
   与板 extent/draw area 的关系未验证，不推断机制。Phase 7 因此迁移选区。
6. **非正 clearance 显示语义**：ARC-Via 重叠时 actual='0 MM'（pass1 j0/j1）；
   clamp-到-0 还是负值截断显示未区分（不影响 verdict 证据链）。
7. axlAirGap 等更底层 API 不可用（需改生产代码，超出本任务边界）。
8. **Probe C scope change（诚实说明）**：原任务 Phase 6 目的是判别模型 B vs C；
   Probe B 已将两者同时排除，判别目的失效（MOOT）。Probe C 改为验证模型 A
   的**泛化性**：Phase 6 双非格点 ARC-ARC（排除"只有 line/DBU 侧起作用"的
   残余解释），Phase 7 ARC-Via 径向距离（pad 半径 rp 在会话内从 marker
   actual 学习，因客户端 API 不暴露 padstack 几何）。两阶段均已完成，
   结果见 §7。
9. evalstring col-255 缓冲边界假设（旁支，未验证，与本模型无关）。

## 7. Probe C 结果

证据：run-2 `logs/probe_c.run2-full-success.bvc57j0lt.log`（exit 0，
SUMMARY 9/9 rungs 按设计、全部 in_window=True，TOTAL_MARKERS=178）；
run-1 `logs/probe_c.run1-phase6-y700fail.b2gigon2b.log`（Phase 6 与 run-2
**位一致**，Phase 7 在 (300.0,700.0) `VIA_CREATE_FAILED` 崩溃）；
崩溃诊断 `logs/diag_y700.badl9grq2.log`（§6.5）。脚本 `probe_c.py`、
`diag_y700.py`。

### 7.1 Phase 6：ARC-ARC 双非格点

每个 rung = 上弧 NET_A cw=False（S/E 格点，center 非格点）+ 下弧 NET_B
cw=True；间距 = 下弧顶 − 上弧底 − 2×(w/2)。R=0.06 会话内学习。
marker FIG 归属逐一校验（仅本 rung 两弧）。clear 用 Decimal-60 对
**committed 回读值**计算：

| rung | y0 | committed clear | 偏差 | FULL | B64 | GRID | DROUND | Allegro | actual |
|---|---|---|---|---|---|---|---|---|---|
| CC_FLIP_LO | 600 | 0.0599975028007488 | δ=−2.4972e-6 | FLAGGED | FLAGGED | clean **误** | clean **误** | **FLAGGED** | '0.0599 MM' ✓ |
| CC_FLIP_HI | 610 | 0.0600005687606963 | +5.6876e-7 | clean | clean | clean | clean | **clean** | — |
| CC_GOLD | 620 | 0.0599510038616914 | δ=−4.8996e-5 | FLAGGED | FLAGGED | FLAGGED | clean **误** | **FLAGGED** | '0.0599 MM' ✓ |
| CC_ABOVE | 630 | 0.0600005074416702 | +5.0744e-7 | clean | clean | clean | clean | **clean** | — |
| CC_BELOW | 640 | 0.0599005071712243 | δ=−9.9493e-5 | FLAGGED | FLAGGED | FLAGGED | FLAGGED | **FLAGGED** | '0.0599 MM' ✓ |
| CC_GRID_EQ | 660 | 0.0600000000000364 | +3.64e-14（DBU-decimal 精确==R） | clean | clean | clean | clean | **clean** | match=True |
| CC_GRID_FLAG | 680 | 0.0599000000000035 | −(1 grid −3.5e-15) | FLAGGED | FLAGGED | FLAGGED | FLAGGED | **FLAGGED** | '0.0599 MM' ✓ |

关键观测：

- **PHASE6_PAIR（决定性）**：LO/HI 两上弧 committed center y 差
  `dcy1(committed)−10 = 3.500000048e-6`（requested Δ=3.5e-6，位精确保持；
  下弧 dcy2−10=0E-43、dr2=0E-49，上弧 dr1=4.340e-7 为 radius 随 eps 的
  确定性变化）。两 rung 都是**双方 center+radius 均非格点的纯 ARC-ARC 对**，
  Allegro 判 LO=FLAGGED / HI=clean → 亚格点差异在两对象均无 DBU 量化
  "帮忙"时仍被分辨；"Line-ARC 中是 line 侧起作用"的残余解释被排除。
- **GRID/DROUND 在 CC_FLIP_LO 与 CC_GOLD 误判 clean**（量化/取整把
  −2.5e-6 / −4.9e-5 的亏欠抹平到 ≥R）→ 模型 B/C/D/DROUND 在纯 ARC 域
  被独立再排除，与 Probe B（Line-ARC 域）交叉印证。
- **CC_GRID_EQ**：格点对的 DBU-decimal 精确 clearance == R → clean，
  等号 clean 语义在 ARC-ARC 域复现；binary64 表示在该点引入 +3.64e-14
  伪差（此例为正，naive-B64 碰巧判对——naive-B64 的排除仍以 Probe B
  GRID_EQ/STAIR_n7 的 −2.05e-11 负伪差为准）。
- **CC_GRID_FLAG 下弧** committed r=1.2499999999999443，
  `r − |S−C|_exact = −5.573e-14`，超出 Probe A/B 的 ≤1.6e-14 包络
  → §1.1/§3/§5 包络更新为 |Δr|≤5.6e-14；仍比已证分辨率 2.5e-6 小
  4.5 个数量级，不影响任何 verdict。
- **REQUERY**：18/18 本 run 创建弧独立重查位一致（全板 count=131）。

### 7.2 Phase 7：ARC-Via 径向距离（rp 会话内学习）

- 校准弧 CV_CAL_ARC（y0=500，自然 center (301.00005, 500.124975)）：
  committed 与 STAGE1 弧位一致（r=1.0078287320398243，
  bits=3ff0201105414878）——同几何跨 110mm 平移位复现。
- **Pass 1**（13 via 0.1 阶梯，x=301.0）：27 个 via 全部 committed==requested
  （dx=dy=0，on_grid，位级回读）。发现 marker
  `'Line to Thru Via Spacing' expected='0.065 MM'` → **R_via=0.065 会话内
  学习**（FIG 归属校验：via NET_B ↔ 校准弧 NET_A）。flagged={j0,j1}
  （via 与弧铜皮重叠，clearance≤0），actual 均 `'0 MM'`——非正 clearance
  的显示下限观测（§6.6）；verdict 证据不受影响。
- **Pass 2**（bracket 内 0.007 步长 14 via）：via marker 累计 11 个，其中
  9 个正 actual 给出
  rp ∈ (0.14994626897241…, 0.15004626892854…]，区间内唯一格点候选 →
  **rp=0.1500**（VIA_ALL_0103 的 pad 半径，即 0.3mm pad）。全程仅用
  marker expected/actual 文本，未依赖 padstack 几何 API。
- **CV_CONSISTENCY**：27 committed via（11 flagged）逐一用模型 A
  （committed 值全精度 + 学习 rp/R_via + 严格 `<`）预测 verdict，
  **mismatches=0** —— 模型 A 在 ARC-Via 径向域零误预测。
- **临界对**（via y 由 committed 弧 p1 + 学习 rp 反解，落格点后创建，
  committed==requested）：

| rung | y0 | committed cy1 | via y | committed clear | 偏差 | FULL | B64 | GRID | DROUND | Allegro | actual |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CV_FLIP_LO | 540 | 540.1249193299999 | 538.8271 | 0.0649975007234218 | δ=−2.4993e-6 | FLAGGED | FLAGGED | clean **误** | clean **误** | **FLAGGED** | '0.0649 MM' ✓ |
| CV_FLIP_HI | 550 | 550.12492283（=LO+10+3.5e-6） | 548.8271 | 0.0650005668931151 | +5.6689e-7 | clean | clean | clean | clean | **clean** | — |

  → sqrt 径向距离测量同样分辨亚格点几何（0.025 DBU 亏欠 → FLAGGED）；
  GRID/DROUND 再次在 LO 误判 clean。CV_PAIR：LO=FLAGGED HI=clean，
  与设计一致。

### 7.3 boxed 问题的完整证据链

**问题**：Allegro DRC 能否区分两个 committed ARC 几何、其差异仅存在于
设计坐标格点（1e-4 mm）之下？ **答案：YES。** 四条独立环节、三种测量
类型（Line-ARC / ARC-ARC / ARC-Via），且 Phase 6 跨 run 位一致复现：

1. **持久化**：requested 的亚格点 center 差 Δcy=3.5e-6 mm（0.035 DBU）
   位精确 commit（Probe B PHASE4；Probe C PHASE6_PAIR
   dcy1−10=3.500000048e-6），re-query 位一致（19/19 + 18/18）——
   差异不是瞬态，进入数据库。
2. **Line-ARC 分辨**（Probe B b9phteksv）：FLIP_LO δ=−2.49e-6 → FLAGGED，
   FLIP_HI +0.57e-6 → clean；两弧 committed center 差恰为 3.5e-6。
3. **ARC-ARC 泛化**（Probe C Phase 6）：双方均非格点浮点对象、同一
   3.5e-6 committed 差 → LO FLAGGED / HI clean；排除"量化侧代劳"解释。
4. **ARC-Via 泛化**（Probe C Phase 7）：径向 sqrt 距离，rp/R_via 在线
   学习，δ=−2.4993e-6 → FLAGGED（'0.0649 MM'）/ +0.5669e-7 → clean；
   27 对象一致性检验零误预测。

已证测量分辨率 ≤2.5e-6 mm = 0.025 DBU = 坐标格点的 1/40；判决边界
（−2.5e-6, +0.57e-6) 在三域一致。任何把 committed 几何量化到 DBU 的
外部模型（B/C/D/DROUND）都已被三类测量各自独立证伪。
