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

> 2026-10-25 Kristy：兩個單元都太花時間（資安單元改圖最久）。開新單元固定照下面的順序：**先選製作方式 → 先定文字 → 要繪圖先選風格 → 整單元預覽一次列修改**。

### 0. 開工先給 Kristy 選製作方式
- 讀完教材、動手做之前，先提出 **2–4 種製作方式**讓她選（用選項卡），每種寫清楚：怎麼做、她要花多少時間、適合什麼單元。不自己決定，也不預設只有一種。
- 可參考的選項（依單元調整，不必每次全列）：
  - **A. 文字先行＋Claude 自畫扁平向量 SVG**：圖示、圖解、地圖多由 Claude 畫（地圖用真實地理資料、中文用程式排字，不用 AI 寫字），只有封面、終點站等情境大圖用 Gemini／NotebookLM 生；Kristy 改圖的時間最少。
  - **B. 以 Kristy 既有簡報與教材為主**：匯出成圖片放進頁面，只補缺的圖與互動題。
  - **C. 全部情境插圖風**：每站都用 Gemini／NotebookLM／ChatGPT 生情境插圖（可由 Kristy 自己生，我給逐張提示詞），畫面最豐富，但改圖最花時間。
  - **D. NotebookLM 補充**：NotebookLM 只當補充素材（資訊圖表、影片），主內容仍是手做 HTML（Kristy 說純 NotebookLM 產出效果不好）。

### 0.5 先定文字大綱（固定步驟，Kristy 確認後才做圖）
- 不論選哪種製作方式，都先交一份**文字大綱**給 Kristy：各站標題、每站重點文字、所有題目與選項、正確答案與解說、教師版答案（每一題都要有）、需要的圖片清單（每張圖要表達什麼）。
- Kristy 確認或改完文字後，才開始做圖與排版；做圖時不再改文字內容，避免圖做完又重做。

### 1. 讀教材、歸納重點
- PDF 用 PyMuPDF 取文字；Word／PowerPoint 用對應技能讀取。
- 歸納 **3–6 個教學重點**（國小一節 40 分鐘，重點不要太多），每個重點記下：名稱、學習內容代碼（有才填）、核心概念、一個例題。
- 數學單元另依 `kristy-math-materials` 的標準檢查用語與符號。

### 2. 備素材（混用）
- **Kristy 既有教材優先**：她的簡報匯出成圖片，學習單只取題目概念，不直接貼學生作答頁。
- **缺的再用 NotebookLM 補**：簡報（chalkboard、detailed_deck）、每個重點一張資訊圖表（sketch_note、landscape、detailed）、學生自學影片（explainer、whiteboard），一律 `language: "zh-TW"`。focus_prompt 寫明「國小○年級」，用語用台灣國小慣用語。
- NotebookLM 沒有連線或認證過期時，跳過並在回報中註明，只用既有教材。

### 3. 圖片處理

**先定風格、先打樣，才量產**（《資安偵探學院》先做佔位圖再重做、配色改了好幾次、裁切遮擋沒檢查，花掉 Kristy 很多時間，以下流程必走）：

1. **給 Kristy 挑風格**：只要需要繪圖，動手前一律先提出 2–4 種繪圖風格讓她選（參考 `AGENTS.md` 的「4 大圖片風格庫」，**一定包含扁平向量風 SVG**，Claude 自畫、好修改），每種附名稱、一句特色，能附範例圖就附範例圖。她選定後才往下做，不自己決定。
2. **先打樣 1–2 張**：用選定風格做 1–2 張樣張（含配色），給 Kristy 看過、點頭後才做其餘圖片。不要先做文字佔位圖再整批重做。
3. **全單元風格與配色一致**：同一單元所有圖片（投影片、資訊圖表、插圖）用同一種風格、同一組配色，做到一半不換。要換風格或配色，先問 Kristy。把定案的風格與色碼記在單元工作資料夾的 README，後續補圖照著做。
4. **放進版面後自己先檢查**：每張圖放進投影片、資訊圖表或網頁後，逐張看一遍，確認人物的手、腳、臉沒被裁切，文字沒被遮住、沒被切斷或擠到換行，圖與文字卡片不重疊。檢查過才給 Kristy 看。
5. **換圖先給她看**：已經放上去的圖要替換，先把新圖給 Kristy 看過、同意後才換，不直接覆蓋。舊圖移到 `待刪除/`。
6. **生圖工具不限**：可以用 Canva、Gemini、ChatGPT 等任何工具，也可能是 Kristy 自己生圖。由她自己生圖時，先寫一段**共用風格描述**（風格、配色色碼、光線、背景、16:9 構圖、角色外型），再為每張圖寫一段可直接貼上的提示詞（共用風格描述＋該張的場景與動作），整理成一份清單（檔名對照提示詞）給她。她把圖交回後，由我統一裁切、縮放、轉檔，並照第 4 點檢查後再放進版面。
7. **規格**：所有圖片轉成 **1600×900 JPG（quality 75）**，單張約 70–150 KB，存到 `units/<slug>/assets/`，命名 `slide_01.jpg`、`01_重點名.jpg`。簡報 PDF 每頁轉圖用 300 DPI 再縮成上述規格。
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
- 每張圖都看過：手、腳、臉沒被裁切，文字沒被遮住或切斷；全單元風格、配色一致。

### 5.5 整單元預覽，一次列修改
- 自己檢查完，給 Kristy **一個預覽連結**（或預覽截圖集）看整個單元，請她把所有要改的地方**一次列完**，我整批改好再給她看一次。
- 不要做一站給她看一站、來回逐張改；也不在她看完整體前先推上 GitHub。

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
6. 圖片：先給 Kristy 挑風格、打樣 1–2 張通過才量產；全單元風格配色一致；生圖工具不限，Kristy 自己生圖時給她共用風格描述＋逐張提示詞；放進版面後自己檢查裁切與遮擋；換圖先給她看。
7. 開新單元固定順序：先給 2–4 種製作方式選 → 先定文字大綱並確認 → 要繪圖先給風格選項（含扁平向量風）→ 整單元預覽，請 Kristy 一次列完修改。
