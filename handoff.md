# 交接檔（handoff.md）

## ⏯️ 目前做到哪
- 2026-11-26（Antigravity）：完成《做壓力的主人》與《資安偵探學院》內容與影片升級，並全數經 Claude Code CLI 跨 Agent 交叉審查通過、推送上線（`53239bc`、`c2fc04e`）。
  - **《做壓力的主人》**：第一站補「幫手 vs. 負擔」觀念、新增 2 題闖關（3→5 題）並嵌入 TED-Ed 數學焦慮（`7snnRaC4t5c`，播 0:00–2:27，避開呼吸法）；第二站補資優生「隱形壓力」、新增 8 題壓力雷達與多壓力源單選（2→4 題）並嵌入 TED-Ed 冒名頂替症候群（`ZQUxL4Jm1Lo`，0:00–4:04）；第五站嵌入 TED-Ed 拖延症兩段（`FWTNMzK9vG4`，0:00–2:05 與 3:14–3:48，避開六年級情緒調節段落）。
  - **《資安偵探學院》**：新增 `addCaseVideo()` 將對應特定案件的影片移入各案件播放（案件 1 張忠謀金字塔、案件 3《三資小豬》、案件 4《魔女宅急騙》、案件 5 刑事局《猜猜我是誰》）；《2020》1–9 集逐字稿敏感詞檢查完成，保留全套於頁面最後、修正 4–9 集官方片名並加註國小課堂播放提醒。
  - **用語統一與環境建置**：兩頁剩餘「爸媽／媽媽」全部統一改為「家人」；本機安裝並登入 Claude Code CLI（`C:\Users\user\.local\bin\claude.exe`，v2.1.332），日後可直接從 Antigravity 呼叫 `claude -p` 做交叉審查。

## 🚦 目前狀態
- 網站：https://kristysu701023-cyber.github.io/teaching-cockpit/（四個情意單元＋五、六年級數學解謎室皆已上線）。
- 五上第 4 單元仍剩 **3 支 MP4 尚未上傳 YouTube**（前日碰每日上限）：`u4-pair-sub`（第 3 題）、`u4-double-dist`（第 5 題）、`u4-factor33333`（第 6 題）。題目卡、答案、提示、文字詳解皆已上線，只差 YouTube ID。
- 工作區保留兩份未追蹤學習單備份檔（`情2-1至2-2_性別平等_兩頁版v2.docx`、`v4.docx`），刻意不進公開 Git repo。

## ➡️ 下一步
1. **補傳五上第 4 單元剩下 3 支 YouTube 解題影片**（`C:\2026AI_Agent\五年級數學\videos`：`python -X utf8 upload_u4_to_youtube.py` → `python -X utf8 update_g5_cockpit.py` → push）。
2. Kristy 上課前確認資安單元〈末日2.0〉影片內容。
3. 若性平單元要再加動畫，已篩選 3 支可嵌入官方影片（《Snack Attack》、《Redraw The Balance》、《刻版的幻影》）。

## ⚠️ 注意事項
- **內容不能牽涉台灣政治**；**家庭題材要小心**（統一用「家人」不寫死爸媽）；教師密碼維持 `0000`；不選粵語影片；**影片一律選 16:9 橫式，不用直式短片**。
- **跨 Agent 呼叫 Claude Code CLI**：PowerShell 管線傳中文會亂碼，呼叫 `claude.exe -p` 時一律用純英文指令請它讀 UTF-8 檔或直接執行 `git show`。
- **數學解謎室版面**：單欄滿版 `1100px`，勿改回左右兩欄。頁首人物以標題中心 `calc(50% - 440px)` 定位；五、六年級兩頁 CSS 要同步改。
- **GitHub Pages 快取**：推送後 1～2 分鐘生效，按 `Ctrl + F5` 強制刷新；本機預覽用 http.server 8123（file:// 圖片載不出來）。

## 🕐 最後更新
- 時間：2026-11-26 14:11
- 更新者：Antigravity @ LAPTOP-IUMJF2MM
- Git push：✅ 已推 (bc7e5db)
