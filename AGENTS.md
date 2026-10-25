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
| 2026-10-25 | 第一單元《資安偵探學院》11 案全套 3D 皮克斯視覺大修復、偵探證微卡片重構、《2020》網路危機全套短片收錄完工上線 |

## 🎯 目標與路線圖

- [x] 專案初始化（AGENTS.md、handoff.md、.gitignore）
- [x] RDQ 需求探索，規格卡確認
- [x] 框架初版：首頁（單元卡＋QR code）、單元頁範本、共用 CSS／JS、全站設定、Pages 部署
- [x] 國小通用版 skill：`skills/teaching-cockpit/SKILL.md`
- [x] 建立公開 repo `teaching-cockpit`，推上去，啟用 GitHub Pages
- [x] 第一個單元：國小五年級資優專題《資安偵探學院》（units/g5-cyber-safety）11 個案件全套純白底 3D 皮克斯風格投影片、資訊圖表、偵探證微卡片、全套短片全面完工定案上線
- [ ] Kristy 在 `assets/config.js` 改教師密碼（目前是 `0000`）
- [ ] 第二個單元（另開任務，用 skill 製作）

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
| 1600×900 JPG q75（簡報頁、資訊圖表、插圖） | repo：`units/<slug>/assets/` |
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

---

## 🎨 國小教學駕駛艙 4 大圖片風格庫與選型指南

在規劃任何國小教學單元、投影片與互動學習教材時，依據教學領域與學科屬性，統一挑選以下 **4 大主流風格** 之一：

| 風格類型 | 視覺特徵與表現手法 | 代表 Prompt 關鍵詞 | 最適合的教學主題 |
|---|---|---|---|
| **1. 3D 皮克斯立體繪本風**<br>*(資安單元標準風格)* | • 圓潤大眼、生動溫暖表情、立體光影柔和<br>• 道具質感飽滿（發光護盾、高科技平板）<br>• 國小中高年級吸睛度最高、代入感最強 | `3D Pixar Disney style, cute character design, warm soft studio lighting, pure clean white background, high quality 3D digital render` | 科技資訊、資安偵探、AI 探索、自然科學實驗、未來想像 |
| **2. 宮崎駿／吉卜力手繪水彩生活風**<br>*(Kristy 最愛之生活美學)* | • 溫暖手繪水彩與水粉筆觸、細膩深色手繪墨線<br>• 藍天白雲、陽光微風、校園走廊生活感<br>• 人文氣息與故事氛圍最強，最具溫度 | `Studio Ghibli aesthetic, Hayao Miyazaki anime style, hand-painted watercolor and gouache, delicate ink outlines, heartwarming atmosphere` | 國語文閱讀、情意教育、生命教育、品格故事、社會人文 |
| **3. 2.5D 扁平立體等角向量風 (Isometric)** | • 乾淨幾何線條、45 度俯視立體空間<br>• 模組清晰、層次嚴謹、理性專業<br>• 圖解複雜結構與運作流程時一目了然 | `Clean isometric 2.5D vector illustration, cute pastel color palette, geometric precision, modern educational infographic, pure white background` | 數學幾何、建築地圖、都市交通網絡、工廠產線、系統流程圖 |
| **4. 日系暖色手繪繪本插畫風 (Chibi Storybook)** | • 柔和蠟筆／色鉛筆筆觸、淡雅粉彩配色<br>• 無生硬光斑、純真童趣、低壓親切<br>• 消除學生的學習焦慮與緊張感 | `Japanese cute picture book illustration, soft crayon and colored pencil texture, gentle pastel palette, adorable chibi characters, heartwarming` | 低年級生活課程、情緒調適、同儕相處、品德繪本導讀 |

### 🔒 圖片風格一致性四大金律
1. **全單元固定單一風格**：同一個單元絕不混搭（嚴禁混雜扁平向量與 3D 貼圖）。
2. **全套統一純白底 16:9**：所有插圖與簡報一律為純白底（`#FFFFFF`），徹底避免灰邊、不對稱色塊或切斷感。
3. **文字卡片留白餘裕**：任何卡片與右側插圖間，一律預留至少 **70px~100px** 呼吸邊界，卡片內文字亦需留出充足邊距，絕不貼邊、不重疊。
4. **教學清晰大字體規範（Kristy 準則：以後字也都大一點）**：
   - 專為國小課堂電子白板與後排學生閱讀量身訂做，字體飽滿有力、層次分明：
   - **大主標題**：`52px`~`55px`（900 粗體）
   - **引導副標題**：`24px`~`25px`（700 粗體）
   - **彩色卡片標題**：`24px`~`26px`（700 粗體，醒目易記）
   - **卡片內文說明**：`19px`~`20px`（500/700 權重，行距 1.45~1.5，字級大且舒適）
   - **序號圈圈徽章**：`50px`~`54px`，數字 `24px`~`26px`
   - **底部想一想／金律提示框**：`20px`~`22px`（搭配柔和底色框，視覺焦點明確）
5. **中文字型渲染金律（杜絕忽粗忽細與細明體 fallback）**：
   - 投影片與圖解一律使用 Windows 本地完整思源黑體：`file:///C:/Windows/Fonts/NotoSansTC-VF.ttf`，嚴禁使用遠端 Google Fonts `@import`（防止網路動態分卷延遲導致部分字元 fallback 回新細明體）。
   - 字重一律規範為標準 `font-weight: 700;`，禁止使用 `900` 以防瀏覽器 synthetic bold 破壞複雜繁體字筆畫結構。
   - Chrome headless 截圖必須帶有 `--allow-file-access-from-files`。

### 🧭 新單元開工流程（必走）

> 起因（2026-10-25）：《資安偵探學院》與《世界的角落》都太花時間，資安單元改圖最久。Kristy 要求以後開新單元照以下順序。

1. **先給製作方式選**：動手前提出 2–4 種製作方式（怎麼做、她要花多少時間、適合什麼單元），由 Kristy 選。例如：A. 文字先行＋Claude 自畫扁平向量 SVG（地圖用真實資料、中文用程式排），只有封面／終點站用 Gemini／NotebookLM；B. 以她既有簡報與教材為主；C. 全部情境插圖風（可由她自己生圖）；D. NotebookLM 只當補充。這些只是選項，不預設其中一種。
2. **先定文字（固定步驟）**：先交文字大綱（各站標題、重點文字、題目選項、答案解說、教師版每題答案、圖片清單），Kristy 確認後才做圖。
3. **要繪圖先給風格選**：照下方「單元圖片製作流程」第 1 點，給 2–4 種繪圖風格（一定含扁平向量風 SVG）。
4. **整單元預覽一次列修改**：自己檢查完，給一個預覽連結看整個單元，請 Kristy 一次列完要改的地方，整批改好再給她看；她看過整體前不推 GitHub。

### 🖼️ 單元圖片製作流程（必走）

> 起因：《資安偵探學院》先做佔位圖再整批重做、配色改了好幾次、裁切與遮擋沒先檢查，花掉 Kristy 很多時間。

1. **先給 Kristy 挑風格**：做任何單元圖片前，從上方風格庫提出 2–4 種風格（**一定包含扁平向量風 SVG**；附名稱、特色，能附範例圖就附），由 Kristy 選定，不自己決定。
2. **先打樣 1–2 張**：用選定的風格與配色做 1–2 張樣張，Kristy 同意後才做其餘圖片；不先做文字佔位圖再重做。
3. **風格與配色全單元一致**：定案後不中途更換；要換先問 Kristy。定案的風格名稱與色碼寫進單元工作資料夾的 README。
4. **放進版面後自己先檢查**：每張圖放進投影片、資訊圖表或網頁後逐張檢查：手、腳、臉沒被裁切，文字沒被遮住、切斷或擠到換行，圖與文字卡片不重疊。檢查過才給 Kristy 看。
5. **換圖先給她看**：已上線或已放進版面的圖，替換前先給 Kristy 看新圖、同意才換；舊圖移到 `待刪除/`，不直接覆蓋。
6. **生圖工具不限**：Canva、Gemini、ChatGPT 或 Kristy 自己生圖都可以。她自己生圖時，先給她一段共用風格描述（風格、色碼、光線、背景、16:9、角色外型），再為每張圖寫可直接貼上的提示詞（共用描述＋該張場景），附檔名對照；圖交回後統一裁切、縮放、轉檔並照第 4 點檢查。
7. **圖片規格**：1600×900 JPG、quality 75（單張約 70–150 KB），檔案不要太大。
