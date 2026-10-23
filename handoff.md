# 交接檔（handoff.md）

## ⏯️ 目前做到哪
- RDQ 規格卡確認（`rdq/RDQ-spec-teaching-cockpit-20261022.md`，含加選 a、b、d）。
- 框架初版完成：首頁（單元卡＋QR code）、單元頁範本 `templates/unit/`、共用 `assets/cockpit.css`／`cockpit.js`／`config.js`、QR 產生器、README。
- 國小通用版 skill：`skills/teaching-cockpit/SKILL.md`。
- GitHub Pages 自動部署已正式上線（https://kristysu701023-cyber.github.io/teaching-cockpit/）。
- **全單元視覺升級完成**：全面移除舊教材 22 張舊簡報截圖（`orig_01`～`orig_35`，已安全移入 `待刪除/`），全數升級為統一風格的可愛小偵探與高質感教學插畫卡片（開場、案件 1～11 全面煥然一新）。

## 🚦 目前狀態
- 本地 git 主分支為 main，全數 commit 並 push 直上 GitHub（commit `e9033a1`）。
- GitHub Pages 已建置完成（built），所有新圖已全數上線。
- Google 雲端硬碟（`G:\我的雲端硬碟\2026AI_Agent\教學駕駛艙`）備份完成。
- 教師密碼暫定 `0000`，在 `assets/config.js`。

## ➡️ 下一步
1. 改 `assets/config.js` 的教師密碼。
2. 用 `skills/teaching-cockpit/SKILL.md` 製作下一個新單元。

## ⚠️ 注意事項
- 在本機直接雙擊 index.html 可以看，但 QR code 會是 file:// 網址；給學生掃請用上線網址。
- 本專案採用 GitHub Pages 原生根目錄部署，每次 `git push origin main` 即自動更新。
- 舊圖已暫存於 `待刪除/`，Kristy 確認後可隨時清空。

## 🕐 最後更新
- 時間：2026-10-23 08:01
- 更新者：Antigravity @ LAPTOP-IUMJF2MM
- Git push：✅（origin/main - e9033a1）
