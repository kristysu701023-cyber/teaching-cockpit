# 交接檔（handoff.md）

## ⏯️ 目前做到哪
- 2026-11-24（Antigravity）：性平單元與五、六年級數學解謎室全面升級上線。
  - **性平單元**（`units/g6-gender-equality/index.html`）：第一站補上 CEDAW 英文全名（不寫「西道」）、避開敏感字眼的溫和版【葉永鋕的故事】、以及五月天 feat. 蔡依林〈玫瑰少年〉Live 影片（相信音樂官方頻道 `DdCJRnPFZEc`）；第二站第 5 題改為完全對應學習單 情2-1 第 1 題的「廣告／卡通／偶像劇」表格（`83dd27c`、`91bee7e`、`cf0f5e1`）。性平學習單 v2／v4 `.docx` 已備份進專案根目錄（不進公開 Git repo，隨 robocopy 備份到 G 槽）。
  - **數學解謎室版面統一升級**（`units/g5-math-puzzles`、`units/g6-math-puzzles`）：全面改為與情意單元一致的 **單欄滿版 `1100px`**（不分左右欄）；黃色副標題框 `.ribbon` 擺正；放大 `①先想一想`／`③文字詳解` 標題、折疊框、名偵探 X／助手 Y 角色與對話框、頁尾合照與解題提醒框；每題「解題影片／文字詳解」下方均加入**助手 Y**登場（`7401617`、`9cefbe4`、`e2dd2cb`、`c4bc693`）。
  - **五上第 4 單元整數四則運算**：從學習單 `數4-1` 製作 2 張觀念教導卡片（`d8ccaee`），並以 HyperFrames + Edge-TTS 製作 8 支精熟／資優解題動畫 MP4（`C:\2026AI_Agent\五年級數學\videos\build_u4_all.py`），**全數經本機 Claude 審查發音（二百/二千改兩百/兩千、多音字排雷）與教學步驟後重算定稿**。透過 Chrome 自動上傳 YouTube Studio 成功 5 支（`b7ZnMAGwXAI`、`39tym2DeSpY`、`RA_S_kDkAnc`、`j-iEl5Yv5JY`、`3pEpf_lrRM0`），8 題題目卡＋5 支影片已上線（`7f09a6e`）。

## 🚦 目前狀態
- 網站：https://kristysu701023-cyber.github.io/teaching-cockpit/（四個情意單元＋五、六年級數學解謎室皆已上線）。
- 五上第 4 單元剩下 **3 支 MP4 尚未上傳 YouTube**（昨碰帳號「已達每日上傳數量上限」）：
  - `u4-pair-sub`（第 3 題：雙數列對應相減巧算）
  - `u4-double-dist`（第 5 題：二次分配律巧算）
  - `u4-factor33333`（第 6 題：倍數變形＋分配律巧算）
  - 這 3 題的題目卡、互動答案、提示與文字詳解皆已在網站上線，只差補傳 YouTube ID。
- 工作區保留兩份未追蹤學習單備份檔（`情2-1至2-2_性別平等_兩頁版v2.docx`、`v4.docx`），刻意不進公開 Git repo。

## ➡️ 下一步
1. **補傳五上第 4 單元剩下 3 支 YouTube 解題影片**（今天已過 24 小時或完成手機驗證即可直接執行 `python -X utf8 upload_u4_to_youtube.py` → `python -X utf8 update_g5_cockpit.py` → push）。
2. Kristy 上課前確認資安單元〈末日2.0〉影片內容。
3. 若性平單元要再加有趣動畫，上次已篩選 3 支可嵌入官方影片（《Snack Attack》、《Redraw The Balance》、《刻版的幻影》）可隨時挑選加入。

## ⚠️ 注意事項
- **內容不能牽涉台灣政治**；**家庭題材要小心**，不強調多元成家、不追問家庭組成；教師密碼維持 `0000`；不選粵語影片。
- **數學解謎室版面**：已定案為單欄滿版 `1100px`（不分左右欄），勿再改回左右兩欄。
- **解題影片發音品管**：Edge-TTS（`zh-TW-HsiaoChenNeural`）講稿一律用「兩百／兩千」，避開多音字（得、差、長、數、倒數），算圖後用 contact sheet 檢視防壓框。
- **GitHub Pages 快取**：推送後約 1 分鐘生效，但同台電腦點書籤可能因瀏覽器 10 分鐘快取看到舊畫面，按 `Ctrl + Shift + R` 即可強制刷新。另外數學解謎室視窗寬度 < 640px 會套用手機版（人物與標題變小），反映「沒變大」時也要確認視窗夠寬。
- **頁首放大（7985e61，Claude Code）**：標題 `clamp(2.6rem, 11vw, 6.6rem)`、`.hero .ch-l/.ch-r` 150×235（左 9%、右 6%），五、六年級兩頁 CSS 同步改。本機預覽用 `.claude/launch.json` 的 `cockpit`（http.server 8123），直接開 file:// 圖片載不出來。

## 🕐 最後更新
- 時間：2026-11-25 08:12（Antigravity 08:06 收工後，Claude Code 補記頁首放大）
- 更新者：Claude Code @ LAPTOP-IUMJF2MM
- Git push：待推
