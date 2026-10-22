---
name: teaching-cockpit
description: 國小教學駕駛艙單元生成技能（不限科目）。把備課教材（課本 PDF、Kristy 既有學習單與簡報、NotebookLM 生成素材）做成黑板粉筆風格的互動單元頁，放進 teaching-cockpit 框架並部署到 GitHub Pages。說「做教學駕駛艙」、「把這個單元做成駕駛艙」、「新增駕駛艙單元」時使用。
---

# 教學駕駛艙單元生成（國小通用版）

改寫自 [math-cockpit](https://github.com/mathruffian-dot/math-cockpit) 的 teaching-cockpit skill（MIT）。差別：對象改為國小、不限科目；不再每次手寫整份 HTML，而是把內容填進框架的 `UNIT` 設定；遵守 Kristy 的工作約定。

## 框架結構（repo：kristysu701023-cyber/teaching-cockpit）

```
index.html                  首頁：單元卡片＋學生掃描 QR code
assets/cockpit.css          共用黑板風格樣式
assets/cockpit.js           共用程式：依 UNIT 長出頁面、翻頁器、評量、抽籤器、計時器、畫筆、教師模式、QR
assets/config.js            全站設定：教師密碼、抽籤座號範圍
assets/vendor/qrcode.js     QR 產生器（本地檔，不連外部服務）
templates/unit/index.html   單元頁範本（所有欄位都有註解）
units/<slug>/               每個單元一個資料夾：index.html＋assets/*.jpg
```

## 輸入（開始前確認，已知的不重問）

- 教材來源（必要）：課本 PDF、既有學習單或簡報、或 NotebookLM 筆記本
- 單元名稱、年級、科目（必要）
- 單元資料夾英文名 `<slug>`（選填，預設依單元名擬一個，例 `g5-triangles`）
- YouTube 影片 ID（選填，之後再補）

## 流程

### 1. 讀教材、歸納重點
- PDF 用 PyMuPDF 取文字；Word／PowerPoint 用對應技能讀取。
- 歸納 **3–6 個教學重點**（國小一節 40 分鐘，重點不要太多），每個重點記下：名稱、學習內容代碼（有才填）、核心概念、一個例題。
- 數學單元另依 `kristy-math-materials` 的標準檢查用語與符號。

### 2. 備素材（混用）
- **Kristy 既有教材優先**：她的簡報匯出成圖片，學習單只取題目概念，不直接貼學生作答頁。
- **缺的再用 NotebookLM 補**：簡報（chalkboard、detailed_deck）、每個重點一張資訊圖表（sketch_note、landscape、detailed）、學生自學影片（explainer、whiteboard），一律 `language: "zh-TW"`。focus_prompt 寫明「國小○年級」，用語用台灣國小慣用語。
- NotebookLM 沒有連線或認證過期時，跳過並在回報中註明，只用既有教材。

### 3. 圖片處理
- 簡報 PDF 每頁轉圖（300 DPI），所有 PNG 轉 **1920×1080 JPG（quality 85）**，存到 `units/<slug>/assets/`，命名 `slide_01.jpg`、`01_重點名.jpg`。
- 原始 PNG、PDF、MP4 留在本機工作資料夾，不進 repo（`.gitignore` 已排除）。

### 4. 建單元頁
1. 複製 `templates/unit/` 為 `units/<slug>/`。
2. 改 `index.html` 裡的 `Cockpit.renderUnit({...})`：title、grade、subject、objectives、intro.slides、sections、summary、video.youtube、teacher.mistakes、teacher.links（NotebookLM 連結放這裡）。
3. 每個重點：
   - `slides`：該重點的簡報圖片
   - `interactive`：依概念客製一個 `function (canvas, out) {...}`（畫布 640×360，用 pointer 事件以支援平板觸控）；想不到合適互動就省略，不硬做
   - `quizzes`：2–3 題，4 選 1，以 Bloom「記憶／理解」為主，數值不和教材例題重複，`feedback` 寫一句解題說明
   - `infographic`：資訊圖表 JPG
   - `teacherTips`：教學提示（只在教師模式出現，**不放機密內容**）
4. 在首頁 `index.html` 的 `units` 陣列加一張卡：title、summary、`href: 'units/<slug>/index.html'`、badges（年級、科目、單元代碼）。

### 5. 檢查（推之前）
- 本機開 `python -m http.server` 實際點過：翻頁、作答回饋、教師模式、抽籤、計時、畫筆、QR。
- 手機寬度（390px）不出現橫向捲動。
- `find units/<slug> -size +50M` 無結果；整站 `du -sh` 遠低於 1 GB。
- 搜尋單元檔，確認**沒有學生姓名、照片、聯絡方式**；抽籤只用座號。
- 沒有用系統 Emoji 當圖示或項目符號。

### 6. 推上 GitHub
- 擬繁體中文 commit 訊息（例：「新增 五上03 三角形與多邊形 駕駛艙」，正文列 3–5 條變動），給 Kristy 過目，點頭才推。
- 只 add 本單元資料夾與首頁 `index.html`，不用 `git add .`。
- push 到 main 後 GitHub Actions 自動部署，網址：`https://kristysu701023-cyber.github.io/teaching-cockpit/units/<slug>/`

### 7. 回報
- 單元網址、首頁網址
- 用了哪些既有教材、哪些是 NotebookLM 生成、哪些區塊還是佔位
- 本機保留的完整素材位置

## 鐵則

1. repo 是公開的：不放學生資料、金鑰、密碼檔；教師密碼在 `assets/config.js`，看原始碼就看得到，只用來收起教學提示。
2. 不用系統 Emoji 當圖示；條列用 `▸`、`•` 或文字標籤。
3. 圖片一律 `.jpg`；影片放 YouTube（不公開），頁面只填影片 ID。
4. 改共用的 `cockpit.js`／`cockpit.css` 會影響所有單元，改之前先說明影響範圍並確認。
5. 刪檔不直接刪，移到 `待刪除/`。
