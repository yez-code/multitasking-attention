# 如何開啟與驗收 v3

2026-11-21補記：使用者已確認內容無問題，最終人工內容驗收通過。原53MB下載包遭遇Codex服務錯誤，本機CRC與全部manifest雜湊正常。現在優先使用delivery/內的attention-assignment.zip；截圖與可還原Git歷史分包提供，詳delivery/README.txt。下文「等待最終驗收」及大型包內檔案說明保留為歷史。管理環境未能直接驗證本機file開檔這項技術限制仍如實保留。

最新為結果解讀人工退修版：正文9與12、遊戲回饋已補研究發現、原理、預期方向及不符時的可能因素。兩道新獨立審查與617項瀏覽器檢查通過；本機直接開檔仍待補驗。請優先讀 `records/runs/attention-v3-001/feedback01-handoff.md` 與 `feedback01-checklist.md`，較早的587項報告保留為歷史。

先開啟 `attention-v3.html`。它是單一檔案，不需要安裝程式或啟動伺服器。共14頁正文，另有封面與來源頁。較長頁面在中央區域上下捲動；左右鍵、底部按鈕及右上跳頁選單都可導覽。遊戲作答時請使用畫面提示的按鍵；離開遊戲頁會中止尚未完成的作答，避免把中斷時間算入結果。

兩個遊戲分別在正文8（任務切換）與11（Stroop），都可先練習、跳過及重來，結果在後一頁。未完成或資料不足時不提供比較結論。結果只在當次開啟中保留，沒有上傳或跨次儲存。

這是**等待最終驗收**的交付版本。請斷網後直接開啟，確認導覽、長頁捲動、兩遊戲及引用返回。管理環境禁止`file://`，因此我們只驗證了相同HTML位元組在離線瀏覽器中的執行，不能把直接雙擊開檔列為已通過。外部原始文獻連結需要網路，但不影響簡報內容或遊戲。

閱讀檢查與作業說明：

- `records/runs/attention-v3-001/final-handoff.md`：實際檢查與限制。
- `records/runs/attention-v3-001/final-checklist.md`：自我檢查表。
- `records/runs/attention-v3-001/gaps-status.md`：Wiki缺口處理。
- `workflow/v3-graph.md`：Graph、人工關卡與Loop停止規則。
- `records/runs/attention-v3-001/observations.md`：真實反思素材。
- `records/runs/attention-v3-001/versions.md`：各輪Git對照。

交付壓縮檔另含 `GIT-HISTORY.txt` 與 `attention-history.bundle`。若要完整還原歷史，可在解壓縮目錄外執行 `git clone /完整路徑/attention-history.bundle attention-history`。bundle含本專案歷史；交付目錄的檔案便於直接閱讀。舊版在歷史中保留，不作為本次學術知識來源。

開發來源在 `presentation/v3/`，學術內容來源僅`wiki/`，來源筆記可追溯於`sources/`。獨立審查的兩版凍結輸入在`review-packets/`，初審失敗與重審均保留。瀏覽器測試中遊戲作答為合成資料，不代表真人實驗。
