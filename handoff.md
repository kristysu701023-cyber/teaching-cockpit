# 交接檔（handoff.md）

## ⏯️ 目前做到哪
- RDQ 規格卡確認（`rdq/RDQ-spec-teaching-cockpit-20261022.md`，含加選 a、b、d）。
- 框架初版完成：首頁（單元卡＋QR code）、單元頁範本 `templates/unit/`、共用 `assets/cockpit.css`／`cockpit.js`／`config.js`、QR 產生器、部署 workflow、README。
- 國小通用版 skill：`skills/teaching-cockpit/SKILL.md`。
- 已在雲端用瀏覽器實測：翻頁佔位、作答回饋、教師模式、抽籤（不重複）、計時、畫筆、QR、手機寬度無橫向捲動，無 JS 錯誤。

## 🚦 目前狀態
- 本地 git 已初始化，主分支為 main。
- GitHub 公開倉庫已建立：`kristysu701023-cyber/teaching-cockpit`。
- GitHub Pages 已自動啟用並完成首發部署（Source: main 分支根目錄）。
- 部署網址：https://kristysu701023-cyber.github.io/teaching-cockpit/
- 教師密碼暫定 `0000`，在 `assets/config.js`。

## ➡️ 下一步
1. 改 `assets/config.js` 的教師密碼。
2. 用 `skills/teaching-cockpit/SKILL.md` 做第一個單元。

## ⚠️ 注意事項
- 在本機直接雙擊 index.html 可以看，但 QR code 會是 file:// 網址；給學生掃請用上線網址。
- 本專案採用 GitHub Pages 原生根目錄部署，無需額外 Actions workflow，每次 `git push origin main` 即自動更新。
- 部署會發布整份靜態內容，確認無機密資訊。

## 🕐 最後更新
- 時間：2026-10-23 06:53
- 更新者：Antigravity @ LAPTOP-IUMJF2MM
- Git push：✅（origin/main）
