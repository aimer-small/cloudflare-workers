# 部署指南

站点为纯静态资源（HTML + CSS + JS + SVG + WAV），无服务端逻辑，可部署到任意静态托管。

---

## 一、Cloudflare Pages（推荐）

### 方式 A：Wrangler CLI

```bash
# 安装
npm install -g wrangler

# 登录
wrangler login

# 部署（在仓库根目录执行）
wrangler pages deploy epoch --project-name=epoch-of-the-rift
```

首次部署会创建项目，之后每次执行即更新。

### 方式 B：Git 集成（自动部署）

1. 打开 Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git
2. 选择仓库 `aimer-small/cloudflare-workers`
3. 构建设置：

| 项 | 值 |
|---|---|
| Framework preset | None |
| Build command | （留空） |
| Build output directory | `epoch` |
| Root directory | （留空） |

4. 保存并部署。之后每次 push 到 `main` 自动重新部署。

### 方式 C：直接上传

Dashboard → Pages → 项目 → Create deployment → 拖入 `epoch` 文件夹。

---

## 二、Cloudflare Workers（静态资源模式）

若需以 Worker 形式托管（可叠加自定义路由、鉴权、A/B 测试）：

`wrangler.toml`：

```toml
name = "epoch-of-the-rift"
compatibility_date = "2025-01-01"
assets = { directory = "./epoch" }
```

```bash
wrangler deploy
```

> Workers 静态资源单文件上限 25 MB（免费版），`bgm-epoch.wav` 为 6.3 MB，符合要求。

---

## 三、其他平台

### Vercel

```bash
vercel --prod epoch
```

### Netlify

```bash
netlify deploy --prod --dir=epoch
```

### GitHub Pages

1. Settings → Pages → Source 选 `main` 分支
2. 若站点在子目录，需在 `index.html` 中把 `assets/...` 改为 `/cloudflare-workers/epoch/assets/...`，或改用相对路径 `./assets/...`（当前已是相对路径，可直接用）

### Nginx

```nginx
server {
    listen 80;
    server_name epoch.example.com;
    root /var/www/epoch;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # SVG 与 WAV 长缓存
    location ~* \.(svg|wav|css|js)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    gzip on;
    gzip_types text/css application/javascript image/svg+xml;
}
```

---

## 四、缓存与压缩建议

### `_headers`（Cloudflare Pages / Netlify）

放在 `epoch/_headers`：

```
/assets/img/*
  Cache-Control: public, max-age=31536000, immutable

/assets/audio/*
  Cache-Control: public, max-age=31536000, immutable

/assets/css/*
  Cache-Control: public, max-age=604800

/assets/js/*
  Cache-Control: public, max-age=604800

/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```

### 音频压缩（可选）

6.3 MB 的 WAV 对移动端偏大。转码方案：

```bash
# MP3 96kbps（约 1.8 MB）
ffmpeg -i bgm-epoch.wav -codec:a libmp3lame -b:a 96k bgm-epoch.mp3

# Opus 64kbps（约 1.2 MB，需浏览器支持）
ffmpeg -i bgm-epoch.wav -codec:a libopus -b:a 64k bgm-epoch.opus
```

转码后修改 `assets/js/audio.js`：

```js
var SRC = 'assets/audio/bgm-epoch.mp3';
```

---

## 五、部署前检查清单

- [ ] `index.html` 中所有 `assets/...` 路径为相对路径（当前已是）
- [ ] 音频文件存在且可访问（`curl -I https://域名/assets/audio/bgm-epoch.wav` 返回 200）
- [ ] SVG 在目标浏览器正常渲染（Safari 对 `filter` 支持较弱，已做降级）
- [ ] 移动端首屏高度正常（使用 `100svh`，iOS 15+ 支持）
- [ ] 音景默认静音，点击后才播放
- [ ] `prefers-reduced-motion` 下动效关闭

---

## 六、常见问题

**Q：音频不播放？**
A：浏览器要求用户交互后才能播放音频。点击右下角音景按钮即可。若仍无声，检查 WAV 是否 404，或查看控制台是否触发降级合成。

**Q：SVG 显示为空白？**
A：部分 CDN 对 `.svg` 的 MIME 类型配置错误。确保返回 `Content-Type: image/svg+xml`。

**Q：字体不对？**
A：站点使用系统字体栈（Songti SC / Noto Serif SC / STSong / SimSun）。Linux 服务器无中文字体时，客户端仍会用自己的系统字体渲染，不影响显示。

**Q：部署后样式错乱？**
A：检查 `base.css` 与 `site.css` 是否都加载成功（`site.css` 含图片适配与响应式修正，缺失会导致图片撑破布局）。