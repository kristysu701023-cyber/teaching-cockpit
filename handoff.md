# 交接檔（handoff.md）

## ⏯️ 目前做到哪
- 2026-11-25（Claude Code）：五、六年級數學解謎室頁首與題目字級微調，全部已上線。
  - 題目敘述 `.ask` 放大到 1.45rem（手機 1.15rem）（`14500b7`）。
  - 「解謎搭檔：名偵探 X 和助手 Y」放大到 1.55rem、年級貼紙 `.badge` 放大到 1.45rem、星星 `.doodle` 放大到 58px；手機版保留小星星（`e75dfa3`）。
  - X／Y 人物改成以標題中心定位（`left/right: calc(50% - 440px)`），避免女孩擋到「數」；「五年級／六年級 數學難題」貼紙移到標題右上角（`right:-24px; top:-26px`），維持兩行、rotate(-8deg)（`63b2496`）。平板 ≤960px 隱藏貼紙、人物縮成 115×180。
- 2026-11-24（Antigravity）：性平單元補 CEDAW／葉永鋕／〈玫瑰少年〉；數學解謎室單欄滿版 1100px；五上第 4 單元 8 題＋5 支 YouTube 影片上線。

## 🚦 目前狀態
- 網站：https://kristysu701023-cyber.github.io/teaching-cockpit/（四個情意單元＋五、六年級數學解謎室皆已上線）。
- 五上第 4 單元剩下 **3 支 MP4 尚未上傳 YouTube**（碰到每日上傳上限）：`u4-pair-sub`（第 3 題）、`u4-double-dist`（第 5 題）、`u4-factor33333`（第 6 題）。題目卡、答案、提示、文字詳解皆已上線，只差 YouTube ID。
- 工作區保留兩份未追蹤學習單備份檔（`情2-1至2-2_性別平等_兩頁版v2.docx`、`v4.docx`），刻意不進公開 Git repo。

## ➡️ 下一步
1. **補傳五上第 4 單元剩下 3 支 YouTube 解題影片**（`C:\2026AI_Agent\五年級數學\videos`：`python -X utf8 upload_u4_to_youtube.py` → `python -X utf8 update_g5_cockpit.py` → push）。
2. Kristy 上課前確認資安單元〈末日2.0〉影片內容。
3. 若性平單元要再加動畫，已篩選 3 支可嵌入官方影片（《Snack Attack》、《Redraw The Balance》、《刻版的幻影》）。

## ⚠️ 注意事項
- **內容不能牽涉台灣政治**；**家庭題材要小心**；教師密碼維持 `0000`；不選粵語影片。
- **數學解謎室版面**：單欄滿版 `1100px`，勿改回左右兩欄。頁首人物以標題中心 `calc(50% - 440px)` 定位，不要改回百分比（會擋到標題字）；五、六年級兩頁 CSS 要同步改。
- **多 Agent 同時改同一頁**：11-25 Antigravity 與 Claude Code 交錯改頁首（`e1e4aa4` 曾把女孩移到擋字）；動工前先 `git fetch` 看有沒有新 commit。
- **解題影片發音品管**：Edge-TTS 講稿用「兩百／兩千」，避開多音字（得、差、長、數、倒數）。
- **GitHub Pages 快取**：推送後 1～2 分鐘生效，按 `Ctrl + F5` 強制刷新；視窗 < 640px 套手機版、≤960px 套平板版。本機預覽用 `.claude/launch.json` 的 `cockpit`（http.server 8123），file:// 圖片載不出來。

## 🕐 最後更新
- 時間：2026-11-26 07:52
- 更新者：Claude Code @ LAPTOP-IUMJF2MM
- Git push：✅ 已推 (6c6ea39)
