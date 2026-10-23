# 教學駕駛艙（AGENTS.md）

> 本檔是專案藍圖，所有 Agent（Claude、Codex、Antigravity、Gemini）開工時先讀本檔與 `handoff.md`。

## 📌 專案簡介

- 專案名稱：教學駕駛艙
- 一句話目標：建立不限科目的國小教學駕駛艙框架（首頁＋可重複套用的單元頁範本＋國小版生成 skill），部署到 GitHub Pages，之後每個單元只要換素材就能上線。
- 規格卡：`rdq/RDQ-spec-teaching-cockpit-20261022.md`（confirmed，revisions 1）
- 參考範本：https://github.com/mathruffian-dot/math-cockpit（國中數學版）
- 本機位置：`C:\2026AI_Agent\教學駕駛艙`
- 雲端同步：`G:\我的雲端硬碟\2026AI_Agent\教學駕駛艙`（robocopy）
- GitHub：`kristysu701023-cyber/teaching-cockpit`（**公開**，GitHub Pages 需要；這是「repo 一律私有」的例外，尚未建立）
- 網址：https://kristysu701023-cyber.github.io/teaching-cockpit/（repo 建好、啟用 Pages 後生效）

## 🗓️ 關鍵時程

| 日期 | 事項 |
|---|---|
| 2026-10-21 | 專案初始化 |
| 2026-10-22 | RDQ 規格卡確認，框架初版完成 |

## 🎯 目標與路線圖

- [x] 專案初始化（AGENTS.md、handoff.md、.gitignore）
- [x] RDQ 需求探索，規格卡確認
- [x] 框架初版：首頁（單元卡＋QR code）、單元頁範本、共用 CSS／JS、全站設定、Pages 部署
- [x] 國小通用版 skill：`skills/teaching-cockpit/SKILL.md`
- [x] 建立公開 repo `teaching-cockpit`，推上去，啟用 GitHub Pages
- [ ] Kristy 在 `assets/config.js` 改教師密碼（目前是 `0000`）
- [ ] 第一個單元（另開任務，用 skill 製作）

## 📁 資料夾結構

```
教學駕駛艙/
├── AGENTS.md / handoff.md / CLAUDE.md / GEMINI.md / README.md
├── .gitignore                排除 mp4、pdf、png、pptx、.env 等
├── index.html                首頁：單元卡片＋學生掃描 QR code
├── assets/
│   ├── cockpit.css           共用黑板風格樣式
│   ├── cockpit.js            共用程式：依 UNIT 設定長出整個單元頁＋課堂工具
│   ├── config.js             全站設定：教師密碼、抽籤座號範圍
│   └── vendor/qrcode.js      QR 產生器（本地檔，MIT）
├── templates/unit/           單元頁範本（index.html＋assets/）
├── units/                    正式單元，一個單元一個資料夾
├── skills/teaching-cockpit/  國小通用版生成 skill
└── rdq/                      需求規格卡
```

## 🧩 素材放置規則

| 素材 | 放哪裡 |
|---|---|
| 1920×1080 JPG（簡報頁、資訊圖表） | repo：`units/<slug>/assets/` |
| 原始 PNG、簡報 PDF、PPTX | 本機工作資料夾，不進 repo |
| 影片 MP4 | 上傳 YouTube（不公開），頁面只填影片 ID |

## 🔄 同步層級

| 層級 | 內容 | 狀態 |
|---|---|---|
| L1 本地 | AGENTS.md＋handoff.md，每次都讀 | ✅ |
| L2 GitHub | `kristysu701023-cyber/teaching-cockpit`（公開） | ✅ 已建立並啟用 Pages |
| L3 Obsidian | — | 未啟用 |

## 🤝 工作約定

- 一律使用繁體中文、台灣習慣用語（國小、評量、學習單、核心素養）。
- 修改前先列計畫並確認；優先保留原有資料結構；處理資料時保留原始檔，輸出到新位置。
- 改共用的 `cockpit.js`／`cockpit.css` 會影響所有單元，改之前先說明影響範圍。
- 不直接刪檔：移到 `待刪除/`，由 Kristy 確認後清空。
- 桌面只放最後定稿的成果檔。
- 教學簡報與教材不用系統 Emoji 當圖示或項目符號；條列用 `▸`、`•` 或文字標籤。
- 語音輸入的同音錯字依上下文還原，人名、日期、數字、檔名要明確標出請 Kristy 確認。

## 🔒 安全與隱私

- repo 與網站都是公開的：學生資料只用座號，不出現姓名、照片、聯絡方式。
- 教師密碼寫在 `assets/config.js`，看原始碼就看得到，只用來收起教學提示；教學提示不放機密內容。
- 評量作答結果不回傳、不儲存。
- API key、密碼、憑證（含 `.clasprc.json`）絕不寫進 repo；一律放 `.env` 並列入 `.gitignore`。

---

## 🎨 視覺與生圖風格偏好記錄（Kristy 專屬美學指南）

### 🌟 Kristy 偏好風格：宮崎駿／吉卜力手繪水彩生活美學 (Studio Ghibli Aesthetic)
- **視覺特徵**：
  - 溫暖細膩的手繪水彩質感（hand-painted watercolor and gouache texture）。
  - 乾淨細緻的深色手繪墨線線稿（clean organic ink line art / outlines）。
  - 充滿故事感與生活感的情境光影：蔚藍天空、蓬鬆棉花白雲、溫暖陽光、街道植栽花盆、生活化街景（如公車站牌、校園長廊、紅綠燈）。
  - 角色神情純真清澈、表情溫暖自然、生動親切（齊瀏海、可愛大眼或純真笑容、小學生制服/雙肩書包）。
  - 避免生硬的 3D 塑膠反光或過度寫實，保留日系經典動畫手繪的空氣感與人文溫度。

- **Prompt 提示詞標準公式**：
  ```
  Studio Ghibli aesthetic, Hayao Miyazaki anime style, hand-painted watercolor and gouache illustration with delicate ink outlines.
  [角色描述：如 A cheerful 10-year-old Taiwanese school girl with cute bangs and bright expressive eyes],
  [情境與動作：taking a selfie with smartphone on a sunny street near a bus stop],
  [背景與氛圍：vibrant blue sky with fluffy cumulus clouds, warm gentle sunlight, green potted plants along the sidewalk, heartwarming cinematic atmosphere, nostalgic aesthetic],
  clean composition, 16:9 widescreen, masterwork storybook illustration.
  ```

