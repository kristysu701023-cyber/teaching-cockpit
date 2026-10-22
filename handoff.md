# 交接檔（handoff.md）

## ⏯️ 目前做到哪
- RDQ 規格卡確認（`rdq/RDQ-spec-teaching-cockpit-20261022.md`，含加選 a、b、d）。
- 框架初版完成：首頁（單元卡＋QR code）、單元頁範本 `templates/unit/`、共用 `assets/cockpit.css`／`cockpit.js`／`config.js`、QR 產生器、部署 workflow、README。
- 國小通用版 skill：`skills/teaching-cockpit/SKILL.md`。
- 已在雲端用瀏覽器實測：翻頁佔位、作答回饋、教師模式、抽籤（不重複）、計時、畫筆、QR、手機寬度無橫向捲動，無 JS 錯誤。

## 🚦 目前狀態
- 本機檔案齊全，尚未 git init、尚未推。
- GitHub repo 還沒建；這個專案的 repo 要**公開**（GitHub Pages 免費版需要）。
- 教師密碼暫定 `0000`，在 `assets/config.js`。

## ➡️ 下一步
1. Kristy 到 github.com/new 建**公開**空 repo `teaching-cockpit`（不勾 README），再由 Agent 推上去。
2. 推完後到 repo 的 Settings → Pages，Source 選「GitHub Actions」。
3. 改 `assets/config.js` 的教師密碼。
4. 用 `skills/teaching-cockpit/SKILL.md` 做第一個單元。

## ⚠️ 注意事項
- 在本機直接雙擊 index.html 可以看，但 QR code 會是 file:// 網址；要給學生掃請用上線網址。
- 建 repo 後若在雲端硬碟資料夾內 git 寫入出錯，執行 `git config windows.appendAtomically false`。
- 部署 workflow 會把整個 repo 發布（含 AGENTS.md、handoff.md），所以這些檔案也不能有機密。

## 🕐 最後更新
- 時間：2026-10-22 12:10
- 更新者：Claude @ 雲端
- Git push：—（repo 尚未建立）
