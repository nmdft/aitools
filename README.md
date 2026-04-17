# AITools — AI Tools for Solopreneurs

Honest reviews of AI tools for one-person businesses. We test tools so you don't have to.

**Site:** https://aitools.nmdft.cn

## Structure

- **English:** `/en/slug/`
- **Chinese:** `/zh/slug/`
- **Categories:** AI Coding, AI Marketing, AI Content, AI Automation, AI Analytics, Infrastructure

## Writing

### New English post
Create `source/_posts/tool-name-review.md`:
```yaml
---
title: "Tool Name Review: Description"
date: 2026-04-18 10:00:00
categories: [AI Coding]
description: "SEO description here"
lang: en
---
```

### New Chinese post
Create `source/_posts/zh-tool-name-review.md`:
```yaml
---
title: "工具名评测：描述"
date: 2026-04-18 10:00:00
categories: [AI Coding]
description: "SEO 描述"
lang: zh
---
```
**Important:** Chinese filename must have `zh-` prefix. The generator strips it for the URL.

### Build & Deploy
```bash
./push.sh "post: Article Title"
```
Pushes to GitHub → EdgeOne Pages auto-deploys to aitools.nmdft.cn

## Tech Stack
- Hexo 7 + Fluid theme
- Custom i18n generator (scripts/i18n-generator.js)
- EdgeOne Pages (auto-deploy from GitHub)
- hexo-generator-sitemap (SEO)
- hexo-generator-feed (RSS)
