# 交接檔（handoff.md）

## ⏯️ 目前做到哪
- 2026-11-21 晚（Claude Code）：數學解謎室角色圖與電腦版兩欄版面完成並上線。
  - 名偵探 X／助手 Y 5 張圖：x_hello、y_hello、x_think 用 Kristy 的 Canva 原圖，duo_cheer 是 Kristy 給的合照，y_check 用 Gemini（Kristy 的 Chrome）參考 y_hello 生成。全部去背成透明 WebP（寬 400、q80、43–53KB）放 `assets/mascot/`，換進五、六年級兩頁（9afa864）。
  - 版面微調：拿掉標題右上角裝飾數字串；手機版角色縮小、對話框留在角色旁換行；頁尾合照和「解題提醒」左右並排、電腦版提醒字放大。
  - 電腦版（≥1100px）每題改左右兩欄 5:7：左＝題目＋題圖＋顯示答案＋①先想一想；右＝②解題影片＋③文字詳解。打開詳解後右欄會補滿（66d169a）。手機版排版不變。
- 四個情意單元都已上線：《資安偵探學院》、《世界的角落》、《做壓力的主人》、《不一樣又怎樣：性別平等任務》。

## 🚦 目前狀態
- 網站：https://kristysu701023-cyber.github.io/teaching-cockpit/
- 數學解謎室五年級 2 題、六年級 5 題已上線，角色圖完整。
- 工作區有 Kristy 自己未 commit 的檔案（`scripts/worksheets/build_stress_v1.py`、兩份《做壓力的主人》學習單 docx），這次沒動、也沒一起 commit。
- GitHub 上還留著已合併的 `mascot-xy` 分支，可刪可留。

## ➡️ 下一步
1. Kristy 用投影機實際看一次數學解謎室電腦版兩欄，確認字級與影片大小。
2. 確認上面三個未 commit 的壓力單元檔案要 commit 還是還原。
3. Kristy 上課前自己看一遍資安單元〈末日2.0〉。

## ⚠️ 注意事項
- **內容不能牽涉台灣政治**；**家庭題材要小心**，不強調多元成家、不追問家庭組成。
- 網路照片要先查授權：新聞網站圖多半是 Shutterstock／版權所有不能用；改找 Wikimedia Commons CC 圖並標作者＋授權。Wikimedia 直接 curl 會 429，請 Kristy 用瀏覽器下載。
- 影片有死亡、悲觀結尾等段落用 start/end 切掉；先讀字幕（或燒進畫面的字幕）再出題。
- 學習單標題用華康字型，別台電腦沒裝會變普通字；要印先轉 PDF。
- 推 GitHub 時，桌面版權限檢查可能擋 push；Kristy 說「推」之後重試即可。
- 教師密碼維持 `0000`；不選粵語影片。
- 用 Gemini 生圖：內建瀏覽器沒登入 Google，要用 Kristy 的 Chrome（Claude in Chrome）。Gemini 頁面沒有現成的檔案輸入框，參考圖是用 JS 臨時插入 `<input type=file>` 再以 paste 事件送進對話框；下載原尺寸圖時 Chrome 可能停在 `.tmp` 檔，內容是完整的。
- 角色圖去背沒有 rembg：用 PIL 從外框灌水去白底（腳本在當次暫存區，沒進 repo），白襪、鏡片因被描邊包住不會被去掉。

## 🕐 最後更新
- 時間：2026-11-21 22:10
- 更新者：Claude Code @ LAPTOP-IUMJF2MM
- Git push：✅ 已推 (6650b7f)
