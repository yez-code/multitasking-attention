注意力 LLM Wiki：下載與解壓縮

使用者已於2026-11-21確認簡報內容無問題。這次只重新打包，HTML與Wiki沒有修改。

建議先下載 attention-assignment.zip，儲存至裝置後解壓縮，再使用瀏覽器開啟其中的 attention-v3/attention-v3.html。ZIP需解壓縮，不能作為簡報直接開啟。

檔案用途：
1. attention-assignment.zip：小型作業包，含已確認HTML、Wiki與來源筆記、大綱與逐頁稿、Graph／Loop、實際審查與修正報告、反思素材、開發及測試腳本、Git提交清單與全部文字檔案的歷史差異。已排除體積較大的截圖和Git二進位歷史，但保留其文字紀錄。
2. attention-screenshots.zip：附加的v3實際瀏覽器截圖，含初測、重測、樣張及人工回饋修訂；誤啟動後中止的截圖放在明示aborted的資料夾，不當成通過證據。
3. attention-git-history.zip：可完整還原本專案Git歷史的bundle。解壓後可執行 git clone /完整路徑/attention-history.bundle attention-history；不需要Git也能直接使用第一包。
4. attention-final.html：已確認的簡報獨立副本，與作業包內HTML位元組完全相同。

三個ZIP各自是標準壓縮檔，無須拼接。需要附加資料時，可將其解壓縮到和第一包相同的位置，合併attention-v3資料夾。

作業包的GIT-HISTORY.txt是提交紀錄，GIT-TEXT-HISTORY.patch是排除圖片後的歷史差異，並不冒充可clone的完整Git儲存庫。完整二進位歷史保留在第三包與原儲存庫中。

原53MB完整包的CRC與逐檔雜湊已通過。附圖是Codex檔案服務錯誤，無法僅由本機驗證確定遠端原因。較小的新包及新路徑是交付替代方式，並非宣稱已修復Codex伺服器。

HTML原有的617項瀏覽器測試仍有效，因本次未改教材或程式。管理環境禁止直接file://開檔，因此這項測試限制仍保留；人工內容核准不改寫自動測試證據。
