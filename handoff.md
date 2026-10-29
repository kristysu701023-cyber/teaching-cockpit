# 交接檔（handoff.md）

## ⏯️ 目前做到哪
- 兩個單元都已上線（GitHub Pages）：
  - 第一單元《資安偵探學院》`units/g5-cyber-safety/`：11 案 3D 皮克斯風格定案；10/29 雲端對話在影片清單第 1 支加入張忠謀金字塔理論（中視《與卓越同行》），案件 1 教師提示註明他的頂端是「洞察力 → 創新」（942cc6b）。
  - 第二單元《世界的角落》`units/g6-world-corners/`：六年級情意，六站拖拉闖關、護照集章、真實地圖、影片分段，已上線。
- **第三單元《做壓力的主人》（五年級資優情意）已開工，只有圖片，尚未進 repo**：
  - 10/29 下午由 claude.ai 上的專案對話（雲端）指揮本機用 Gemini 生圖。畫風 Kristy 已選定：**吉卜力手繪水彩風**。
  - 圖片在 `C:\2026AI_Agent\做壓力的主人_新圖\`（PNG 原檔，每張 7–10 MB），提示詞在同資料夾 `生圖提示詞.md`。
  - 單元架構（從提示詞推得）：封面 → 第一站 壓力怎麼來（含壓力曲線）→ 第二站 壓力來源 → 第三站 身體訊號 → 第四站 古人面對壓力（韓信、曹操、伍子胥）→ 第五站 紓壓方法 → 終點站。
  - 已生 7 張：cover、s1_steps、s2_sources（另有 s2_sources_alt 備選）、s3_body、s3_signals、s4_hanxin；壓力曲線用 `sample_watercolor_v2.png`。
  - 還沒生 7 張：s4_caocao、s4_wuzixu、s5_priorities、s5_steps、s5_support、s5_healthy、end。

## 🚦 目前狀態
- 網站：https://kristysu701023-cyber.github.io/teaching-cockpit/
- 《做壓力的主人》的**文字大綱（各站標題、重點、題目、答案、教師版答案）不在本機、GitHub、雲端硬碟或 NotebookLM**，只在 claude.ai 那個專案對話裡；本機 Claude 讀不到。
- Obsidian（L3）：`G:\我的雲端硬碟\Obsidian筆記\Claude專案\教學駕駛艙\`

## ➡️ 下一步
1. 《做壓力的主人》：Kristy 把 claude.ai 專案對話裡的文字大綱貼過來（或請 Claude 依六站架構重擬一版給她確認），文字定案後再做頁面。
2. 補生剩下 7 張圖（照 `生圖提示詞.md`），全部轉成 1600×900 JPG q75 放進 `units/<slug>/assets/`，逐張檢查裁切與遮擋。
3. 整單元做好給 Kristy 預覽一次列修改，她看過才推 GitHub。
4. 其他待辦：勾選待清除檔案清單（雲端專案資料夾 `work/cleanup/待清除檔案清單_20261025.md`）；改教師密碼（`assets/config.js`，目前 `0000`）。

## ⚠️ 注意事項
- **雲端／網頁版對話改完也要說「收工」**：10/29 雲端對話推了 942cc6b 卻沒更新本檔，開工時看不出當天進度。
- repo 公開：學生只用座號；教學提示不放機密。
- 換圖前先給 Kristy 看；她看過整個單元前不推 GitHub；推之前先問她。
- 影片不下載剪進網站，只用 YouTube start/end 分段。
- 本機 git 有一個 stash（`local-copy-identical-to-origin`），內容和 942cc6b 完全相同，可以用 `git stash drop` 清掉。

## 🕐 最後更新
- 時間：2026-10-29 17:50
- 更新者：Claude @ LAPTOP-IUMJF2MM
- Git push：待推
