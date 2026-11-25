---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: e9a66d4f35ebbacd2fb7fcf643613b8a_fce3d49ce8a911f1afe3525400ffa3eb
    ReservedCode1: wA6rvLGHfmhu815tTZ/R/4iZEtCyeqleiSEs46HBTCsEhjuB8HyZnR1RhuCs27JQjNeVS84uHPkkDDOAGbRpqNvJt56nXWRRcZO0i+h5OtSH39DTg0iv014lus6b8KDQrisVAoTUJ0BFR6SGc91qMRtZhA2aEqUb92/R8k6JRxYDtruTnMw5NGqaAmM=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: e9a66d4f35ebbacd2fb7fcf643613b8a_fce3d49ce8a911f1afe3525400ffa3eb
    ReservedCode2: wA6rvLGHfmhu815tTZ/R/4iZEtCyeqleiSEs46HBTCsEhjuB8HyZnR1RhuCs27JQjNeVS84uHPkkDDOAGbRpqNvJt56nXWRRcZO0i+h5OtSH39DTg0iv014lus6b8KDQrisVAoTUJ0BFR6SGc91qMRtZhA2aEqUb92/R8k6JRxYDtruTnMw5NGqaAmM=
---

# 部署说明 · 裂界纪 2.0

纯静态站点，零构建、零依赖。把整个目录上传即可。

---

## 一、体积

| 部分 | 大小 |
|---|---|
| 2.0 主站（HTML + CSS + JS + 15 张 SVG） | 约 320KB |
| `v1/` 1.0 归档（含 6.6MB 音频） | 约 7.2MB |

如不需要 1.0 归档，删除 `v1/` 即可，主站仍为 320KB。

---

## 二、Cloudflare Pages

### 方式 A：控制台直传

1. Workers & Pages → Create → Pages → Upload assets
2. 上传本目录全部内容（`index.html` 须在根）
3. 完成，绑定自定义域名（可选）

### 方式 B：Wrangler

```bash
npm i -g wrangler
wrangler pages deploy . --project-name=epoch
```

`wrangler.toml` 已配置 `pages_build_output_dir = "."`。

---

## 三、GitHub Pages

仓库 Settings → Pages → Source 选 `Deploy from a branch`，分支 `main`，目录 `/epoch`（或把本目录设为仓库根）。

`.nojekyll` 已放置，避免 Jekyll 处理下划线开头的 `_headers`。

---

## 四、本地预览

```bash
cd <本目录>
python3 -m http.server 8000
# 打开 http://127.0.0.1:8000
```

不要直接双击 `index.html`（`file://` 协议下部分浏览器会拦截 SVG 内联脚本与相对路径解析）。

---

## 五、缓存与响应头

`_headers` 提供：

- HTML：`no-cache`，保证改版即时可见
- CSS / JS / SVG：`max-age=604800`，一周强缓存
- 全站：`X-Content-Type-Options: nosniff`、`Referrer-Policy: strict-origin-when-cross-origin`、`Permissions-Policy` 关闭无关能力

---

## 六、验证清单

部署后逐项确认：

1. 首屏底色为纸白 `#F7F4EC`，不是黑
2. 页面**无横向滚动条**（2.0 修复了出血图版溢出）
3. 东线整段偏玉青，西线整段偏黄铜，两色不混在同一屏
4. 纪年表在手机上折叠为单列，年份在左、东/西标签前缀自动出现
5. 页脚「1.0 归档」能打开暗色原版
6. 系统开启「减少动态效果」后，内容直接显示、无位移动画

---

## 七、已知限制

- 中文字体全部依赖系统字体，未加载 Web Font。极少数无中文字体的环境（如部分 Linux 容器）中文会显示为方框，需系统安装 Noto CJK。
- 2.0 无背景音乐。1.0 的音景仅在 `v1/` 内，需手动点击播放。
- 所有图像为 SVG，矢量无损放大，但每张约 8—25KB，首屏建议保持连接复用（HTTP/2 或 HTTP/3）。
*（内容由AI生成，仅供参考）*
